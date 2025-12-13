.PHONY: install-dependencies run help

help:
	@echo Available targets:
	@echo make install-dependencies  Install Python dependencies
	@echo make run                   Run the RufusAI application

install-dependencies:
	pip install -r requirements.txt

run:
	python rufusai.py
