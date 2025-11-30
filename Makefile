# =============================================================================
# VIKI-Heat Docker Management Makefile
# =============================================================================

.PHONY: help dev test prod build up down logs clean restart shell db-shell

# Default target
.DEFAULT_GOAL := help

# Colors
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
NC := \033[0m # No Color

# -----------------------------------------------------------------------------
# Help
# -----------------------------------------------------------------------------
help: ## Zeige diese Hilfe
	@echo "$(BLUE)VIKI-Heat Docker Management$(NC)"
	@echo ""
	@echo "$(GREEN)Verfügbare Befehle:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""

# -----------------------------------------------------------------------------
# Development
# -----------------------------------------------------------------------------
dev: ## Starte Development-Umgebung
	@echo "$(GREEN)Starte Development-Umgebung...$(NC)"
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml --env-file .env.dev up -d
	@echo "$(GREEN)✓ Development-Umgebung gestartet$(NC)"
	@echo "Backend:         http://localhost:5000"
	@echo "Adminer:         http://localhost:8080"
	@echo "Redis Commander: http://localhost:8081"

dev-build: ## Baue und starte Development-Umgebung
	@echo "$(GREEN)Baue Development-Umgebung...$(NC)"
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml --env-file .env.dev up -d --build

dev-logs: ## Zeige Development Logs
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml logs -f

dev-down: ## Stoppe Development-Umgebung
	@echo "$(YELLOW)Stoppe Development-Umgebung...$(NC)"
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml down

# -----------------------------------------------------------------------------
# Testing
# -----------------------------------------------------------------------------
test: ## Führe Tests aus
	@echo "$(GREEN)Führe Tests aus...$(NC)"
	docker-compose -f docker-compose.yml -f docker-compose.test.yml --env-file .env.test up --abort-on-container-exit
	@echo "$(GREEN)✓ Tests abgeschlossen$(NC)"

test-build: ## Baue Test-Umgebung und führe Tests aus
	@echo "$(GREEN)Baue Test-Umgebung und führe Tests aus...$(NC)"
	docker-compose -f docker-compose.yml -f docker-compose.test.yml --env-file .env.test up --build --abort-on-container-exit

test-clean: ## Bereinige Test-Umgebung
	@echo "$(YELLOW)Bereinige Test-Umgebung...$(NC)"
	docker-compose -f docker-compose.yml -f docker-compose.test.yml down -v
	rm -rf test-results coverage htmlcov

# -----------------------------------------------------------------------------
# Production
# -----------------------------------------------------------------------------
prod: ## Starte Production-Umgebung
	@echo "$(GREEN)Starte Production-Umgebung...$(NC)"
	@if [ ! -f .env.prod ]; then \
		echo "$(RED)✗ .env.prod nicht gefunden! Erstelle diese zuerst aus .env.prod.template$(NC)"; \
		exit 1; \
	fi
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env.prod up -d
	@echo "$(GREEN)✓ Production-Umgebung gestartet$(NC)"

prod-build: ## Baue und starte Production-Umgebung
	@echo "$(GREEN)Baue Production-Umgebung...$(NC)"
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env.prod up -d --build

prod-logs: ## Zeige Production Logs
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml logs -f

prod-down: ## Stoppe Production-Umgebung
	@echo "$(YELLOW)Stoppe Production-Umgebung...$(NC)"
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml down

prod-restart: ## Starte Production-Services neu
	@echo "$(YELLOW)Starte Production-Services neu...$(NC)"
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml restart

# -----------------------------------------------------------------------------
# Database Management
# -----------------------------------------------------------------------------
db-shell: ## Öffne PostgreSQL Shell
	@echo "$(BLUE)Öffne Datenbank Shell...$(NC)"
	docker exec -it viki-db psql -U viki -d viki

db-backup: ## Erstelle Datenbank-Backup
	@echo "$(GREEN)Erstelle Datenbank-Backup...$(NC)"
	mkdir -p backups
	docker exec viki-db pg_dump -U viki viki > backups/backup_$$(date +%Y%m%d_%H%M%S).sql
	@echo "$(GREEN)✓ Backup erstellt in backups/$(NC)"

db-restore: ## Stelle Datenbank aus Backup wieder her (BACKUP=pfad/zum/backup.sql)
	@if [ -z "$(BACKUP)" ]; then \
		echo "$(RED)✗ Bitte BACKUP-Datei angeben: make db-restore BACKUP=backups/backup.sql$(NC)"; \
		exit 1; \
	fi
	@echo "$(YELLOW)Stelle Datenbank wieder her aus $(BACKUP)...$(NC)"
	docker exec -i viki-db psql -U viki viki < $(BACKUP)
	@echo "$(GREEN)✓ Datenbank wiederhergestellt$(NC)"

db-reset: ## Setze Datenbank zurück (WARNUNG: Löscht alle Daten!)
	@echo "$(RED)WARNUNG: Dieser Befehl löscht ALLE Daten!$(NC)"
	@read -p "Fortfahren? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker-compose down -v; \
		docker-compose up -d db; \
		sleep 5; \
		echo "$(GREEN)✓ Datenbank zurückgesetzt$(NC)"; \
	fi

# -----------------------------------------------------------------------------
# Container Management
# -----------------------------------------------------------------------------
logs: ## Zeige Logs aller Services
	docker-compose logs -f

logs-backend: ## Zeige Backend Logs
	docker logs -f viki-backend

logs-db: ## Zeige Database Logs
	docker logs -f viki-db

shell: ## Öffne Backend Shell
	docker exec -it viki-backend /bin/bash

shell-db: ## Öffne Database Shell
	docker exec -it viki-db /bin/bash

ps: ## Zeige laufende Container
	docker-compose ps

# -----------------------------------------------------------------------------
# Cleanup
# -----------------------------------------------------------------------------
clean: ## Stoppe und entferne alle Container
	@echo "$(YELLOW)Stoppe und entferne Container...$(NC)"
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml down
	docker-compose -f docker-compose.yml -f docker-compose.test.yml down
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml down

clean-all: ## Stoppe Container und lösche Volumes (WARNUNG: Löscht Daten!)
	@echo "$(RED)WARNUNG: Dieser Befehl löscht ALLE Docker-Volumes und Daten!$(NC)"
	@read -p "Fortfahren? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker-compose -f docker-compose.yml -f docker-compose.dev.yml down -v; \
		docker-compose -f docker-compose.yml -f docker-compose.test.yml down -v; \
		docker-compose -f docker-compose.yml -f docker-compose.prod.yml down -v; \
		docker system prune -f; \
		echo "$(GREEN)✓ Cleanup abgeschlossen$(NC)"; \
	fi

# -----------------------------------------------------------------------------
# Setup
# -----------------------------------------------------------------------------
setup: ## Erstelle .env aus Template
	@if [ ! -f .env.dev ]; then \
		cp .env.example .env.dev; \
		echo "$(GREEN)✓ .env.dev erstellt$(NC)"; \
	else \
		echo "$(YELLOW)! .env.dev existiert bereits$(NC)"; \
	fi
	@if [ ! -f .env.test ]; then \
		cp .env.example .env.test; \
		echo "$(GREEN)✓ .env.test erstellt$(NC)"; \
	else \
		echo "$(YELLOW)! .env.test existiert bereits$(NC)"; \
	fi

init: setup ## Initialisiere Projekt (erstelle .env und starte dev)
	@echo "$(GREEN)Initialisiere Projekt...$(NC)"
	make dev

# -----------------------------------------------------------------------------
# Utility
# -----------------------------------------------------------------------------
prune: ## Bereinige ungenutzte Docker-Ressourcen
	@echo "$(YELLOW)Bereinige Docker-Ressourcen...$(NC)"
	docker system prune -f
	docker volume prune -f
	@echo "$(GREEN)✓ Cleanup abgeschlossen$(NC)"

update: ## Update Dependencies und rebuilde Container
	@echo "$(GREEN)Update Dependencies...$(NC)"
	docker-compose build --no-cache

health: ## Zeige Health Status aller Services
	@echo "$(BLUE)Service Health Status:$(NC)"
	@docker ps --format "table {{.Names}}\t{{.Status}}" | grep viki
