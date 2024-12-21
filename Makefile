# Makefile for SMASH Game (Windows and Linux)

# Paths
CONSOLE_GAME := smash_game.py
WEB_GAME := app.py

# Python command (adjust for your system)
ifeq ($(OS),Windows_NT)
    PYTHON := python
    DEL := del /Q
else
    PYTHON := python3
    DEL := rm -rf
endif

# Rules
.PHONY: run_console run_web clean help

run_console:
	@echo "Running console version of SMASH..."
	$(PYTHON) "$(CONSOLE_GAME)"

run_web:
	@echo "Running web version of SMASH..."
	$(PYTHON) "$(GAME_PATH)/$(WEB_GAME)"

clean:
	@echo "Cleaning up temporary files..."
	$(DEL) "$(GAME_PATH)/__pycache__"

help:
	@echo "Available commands:"
	@echo "  make run_console  - Run the console version of SMASH"
	@echo "  make run_web      - Run the web version of SMASH"
	@echo "  make clean        - Clean up temporary files"
	@echo "  make help        
