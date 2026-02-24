.PHONY: run-scorecard

run-scorecard:
	@echo "Running Agent Scorecard Report..."
	@python3 scripts/generate_scorecard.py
