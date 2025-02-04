.PHONY: tests

tests:
	@echo "Running tests..."
	export PYTHONPATH=.
	pytest tests/test_minesweeper.py -v
