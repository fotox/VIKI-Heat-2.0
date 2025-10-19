export type EnergyDataPoint = {
  heating: number;
  consumer: number;
  regular: number;
  production: number;
};

export type EnergyResponse = {
  [hour: string]: EnergyDataPoint;
};

export type EnergyPriceEntry = {
  startsAt: string;
  total: number;
};
