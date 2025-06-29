# Diretório-raíz
ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

# Cores
GREEN   := $(shell tput -Txterm setaf 2)
WHITE   := $(shell tput -Txterm setaf 7)
YELLOW  := $(shell tput -Txterm setaf 3)
RED     := $(shell tput -Txterm setaf 1)
RESET   := $(shell tput -Txterm sgr0)

# Comandos
UV_RUN	:= uv run

# Constrói a documentação de cada script, visualizável via 'make' ou 'make help'
# A documentação dee cada script é feita através de uma string começando por '\#\#'
# Uma categoria de comandos pode ser adicionada em uma string iniciando a mesma com @category
HELP_FUN = \
    %help; \
    while(<>) { \
		push @{$$help{$$2 // 'Comandos'}}, [$$1, $$3] if /^([a-zA-Z\-]+)\s*:.*\#\#(?:@([a-zA-Z\-]+))?\s(.*)$$/ \
	}; \
	print "Utilização: make [comando]\n\n"; \
	for (sort keys %help) { \
		print "${WHITE}$$_:${RESET}\n"; \
		for (@{$$help{$$_}}) { \
				$$sep = " " x (32 - length $$_->[0]); \
				print "  ${YELLOW}$$_->[0]${RESET}$$sep${GREEN}$$_->[1]${RESET}\n"; \
		}; \
		print "\n"; \
	}

.PHONY: help \
		header \
		format \
		lint \
		test

.DEFAULT_GOAL := help

info: header

define HEADER
+---------------------------------------------------------------------------------------------+
  _  _ _    ___          ___            _  _          _   __  __               _   ___ ___ 
 | \| | |  |   \   ___  |_ _|_ __  __ _| || |___ __ _| |_|  \/  |__ _ _ __    /_\ | _ \_ _|
 | .` | |__| |) | |___|  | || '  \/ _` | __ / -_) _` |  _| |\/| / _` | '_ \  / _ \|  _/| | 
 |_|\_|____|___/        |___|_|_|_\__, |_||_\___\__,_|\__|_|  |_\__,_| .__/ /_/ \_\_| |___|
                                  |___/                              |_|
+---------------------------------------------------------------------------------------------+
endef
export HEADER

header: ##@Outros Mostra o header deste help, formado com caracteres ASCII.
	clear
	@echo "$$HEADER"

help: ##@Outros Mostra esta documentação.
	clear
	@echo "$$HEADER"
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)

format: ## Realiza a formatação do código-fonte em Python.
	@$(UV_RUN) ./scripts/format.sh

lint: ## Realiza o linting do código-fonte em Python.
	@$(UV_RUN) ./scripts/lint.sh

test: ## Executa os testes automatizados via pytest, gerando relatório de cobertura.
	@$(UV_RUN) ./scripts/test.sh
