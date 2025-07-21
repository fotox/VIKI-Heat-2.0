import os
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List

import pytz
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Integer,
    String,
    UniqueConstraint,
    create_engine,
    func,
    select,
    text,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, declarative_base

Base = declarative_base()


class RawMeasurement(Base):
    __tablename__ = "measurements_raw"

    id = Column(Integer, primary_key=True)
    ts = Column(DateTime(timezone=True), nullable=False, index=True)
    metric = Column(String(32), nullable=False)
    inverter_id = Column(Integer, nullable=False)
    value = Column(Float, nullable=False)

    __table_args__ = (
        UniqueConstraint("ts", "metric", "inverter_id", name="uix_raw"),
    )


class HourlyMeasurement(Base):
    __tablename__ = "measurements_hourly"

    id = Column(Integer, primary_key=True)
    hour = Column(DateTime(timezone=True), nullable=False, index=True)
    metric = Column(String(32), nullable=False)
    inverter_id = Column(Integer, nullable=False)
    value_wh = Column(Float, nullable=False)

    __table_args__ = (
        UniqueConstraint("hour", "metric", "inverter_id", name="uix_hourly"),
    )


class FroniusClient:
    def __init__(self, host: str, timeout: float = 5.0):
        self.base = f"http://{host}/solar_api/v1"
        self.timeout = timeout
        self.inverters = self._discover_inverters()

    def fetch_powerflow(self) -> Dict[str, float]:
        data = self._get_json("/GetPowerFlowRealtimeData.fcgi")
        site = data["Body"]["Data"]["Site"]
        return {
            "production_w": site.get("P_PV", 0.0),
            "consumption_w": site.get("P_Load", 0.0),
            "feedin_w": site.get("P_Grid", 0.0),
        }

    def _get_json(self, path: str, params: Dict[str, Any] | None = None):
        r = requests.get(f"{self.base}{path}", params=params, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def _discover_inverters(self) -> List[int]:
        info = self._get_json("/GetInverterInfo.cgi")
        return [int(k) for k in info["Body"]["Data"].keys()]


class DataCollector:
    def __init__(
        self,
        db_uri: str,
        host: str,
        tz: str = "Europe/Berlin",
        use_timescale: bool = False,
    ):
        self.engine = create_engine(db_uri, future=True)
        Base.metadata.create_all(self.engine)
        self.tz = pytz.timezone(tz)
        self.client = FroniusClient(host)

        if use_timescale:
            self._init_timescale()

        self.use_timescale = use_timescale

    def _init_timescale(self):
        """Create extension, hypertable, continuous aggregate & policies."""
        sql_cmds = [
            # 1) Enable extension
            "CREATE EXTENSION IF NOT EXISTS timescaledb",
            # 2) Convert raw table
            "SELECT create_hypertable('measurements_raw', 'ts', if_not_exists => TRUE, migrate_data => TRUE)",
            # 3) Continuous aggregate (hourly)
            """
            CREATE MATERIALIZED VIEW IF NOT EXISTS measurements_hourly_ca
            WITH (timescaledb.continuous) AS
            SELECT time_bucket('1 hour', ts)  AS hour,
                   metric,
                   inverter_id,
                   avg(value)               AS avg_w
            FROM   measurements_raw
            GROUP  BY hour, metric, inverter_id
            """,
            # 4) Policy: refresh last 2 days every 15 minutes
            """
            SELECT add_continuous_aggregate_policy('measurements_hourly_ca',
              start_offset      => INTERVAL '2 days',
              end_offset        => INTERVAL '1 hour',
              schedule_interval => INTERVAL '15 minutes')
            """,
            # 5) Retention for raw table (2 days)
            "SELECT add_retention_policy('measurements_raw', INTERVAL '2 days')",
            # 6) Compression of CA after 30 days
            "ALTER MATERIALIZED VIEW measurements_hourly_ca SET (timescaledb.compress)",
            "SELECT add_compression_policy('measurements_hourly_ca', INTERVAL '30 days')",
        ]
        with self.engine.begin() as conn:
            for cmd in sql_cmds:
                conn.execute(text(cmd))

    def store_minute(self):
        ts = datetime.now(self.tz).replace(second=0, microsecond=0)
        pf = self.client.fetch_powerflow()
        rows = [
            RawMeasurement(ts=ts, metric="production_w", inverter_id=0, value=pf["production_w"]),
            RawMeasurement(ts=ts, metric="consumption_w", inverter_id=0, value=pf["consumption_w"]),
            RawMeasurement(ts=ts, metric="feedin_w", inverter_id=0, value=pf["feedin_w"]),
        ]
        with Session(self.engine) as s:
            for r in rows:
                try:
                    s.add(r)
                    s.commit()
                except IntegrityError:
                    s.rollback()

    def aggregate_yesterday(self):
        today = datetime.now(self.tz).date()
        start = self.tz.localize(datetime.combine(today - timedelta(days=1), datetime.min.time()))
        end = start + timedelta(days=1)
        with Session(self.engine) as s:
            subq = (
                select(
                    func.date_trunc("hour", RawMeasurement.ts).label("hour"),
                    RawMeasurement.metric,
                    func.avg(RawMeasurement.value).label("avg_w"),
                )
                .where(RawMeasurement.ts >= start, RawMeasurement.ts < end)
                .group_by("hour", RawMeasurement.metric)
            )
            for hour, metric, avg_w in s.execute(subq):
                obj = HourlyMeasurement(hour=hour, metric=metric, inverter_id=0, value_wh=avg_w)
                s.merge(obj)
            s.commit()
            s.execute(
                text("DELETE FROM measurements_raw WHERE ts >= :start AND ts < :end"),
                {"start": start, "end": end},
            )
            s.commit()


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Collect Fronius power data → PostgreSQL/TimescaleDB")
    parser.add_argument("--host", required=True, help="Fronius inverter IP/hostname")
    parser.add_argument(
        "--db-uri",
        default=os.getenv("DB_URI", "postgresql+psycopg2://ha:secret@localhost/energy"),
        help="SQLAlchemy DB URI",
    )
    parser.add_argument("--tz", default="Europe/Berlin", help="Timezone")
    parser.add_argument("--timescale", action="store_true", help="Initialise Timescale features & disable Python aggregation job")
    args = parser.parse_args()

    collector = DataCollector(args.db_uri, args.host, tz=args.tz, use_timescale=args.timescale)

    sched = BackgroundScheduler(timezone=args.tz)
    sched.add_job(collector.store_minute, "interval", minutes=1, id="minute_job")
    if not args.timescale:
        sched.add_job(collector.aggregate_yesterday, "cron", hour=0, minute=5, id="agg_job")
    sched.start()

    print("📡 Collector running – Ctrl+C to exit")
    try:
        while True:
            time.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        sched.shutdown()


if __name__ == "__main__":
    main()
