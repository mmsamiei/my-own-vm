# SimpleScript Makefile

.PHONY: all help clean test test-compiler test-computer test-integration run-example

# Default target: show help
help:
	@echo "SimpleScript Makefile"
	@echo "--------------------"
	@echo "Available targets:"
	@echo "  all            - Build the SimpleScript system"
	@echo "  clean          - Remove build artifacts"
	@echo "  test           - Run all tests"
	@echo "  test-compiler  - Run compiler tests only"
	@echo "  test-computer  - Run computer tests only"
	@echo "  test-integration - Run integration tests only"
	@echo "  run-example    - Run a SimpleScript example program (use file=examples/filename.ss)"
	@echo "  help           - Display this help message"
	@echo ""
	@echo "Usage: make [target]"

# Run example programs
run-simple:
	python3 run_simplescript.py examples/simple_test.txt

run-if:
	python3 run_simplescript.py examples/if_test.txt

run-while:
	python3 run_simplescript.py examples/while_test.txt

run-fibonacci:
	python3 run_simplescript.py examples/fibonacci.txt

run-calculator:
	python3 run_simplescript.py examples/calculator.txt

run-nested:
	python3 run_simplescript.py examples/nested_test.txt

run-example:
	@echo "Running SimpleScript example..."
	@if [ -z "$(file)" ]; then \
		echo "Error: Please specify the example file to run with 'file=examples/filename.ss'"; \
		echo "Example: make run-example file=examples/calculator.ss"; \
		exit 1; \
	fi
	@./simplescript $(file)

# Debug mode examples
debug-simple:
	python3 run_simplescript.py examples/simple_test.txt --debug

debug-if:
	python3 run_simplescript.py examples/if_test.txt --debug

debug-while:
	python3 run_simplescript.py examples/while_test.txt --debug

debug-fibonacci:
	python3 run_simplescript.py examples/fibonacci.txt --debug

debug-calculator:
	python3 run_simplescript.py examples/calculator.txt --debug

debug-nested:
	python3 run_simplescript.py examples/nested_test.txt --debug

debug-example:
	python3 run_simplescript.py examples/example_program.txt --debug

# Test targets
test:
	@echo "Running all SimpleScript tests..."
	@python3 tests/run_tests.py

test-compiler:
	@echo "Running compiler tests..."
	@python3 -m unittest tests.test_compiler

test-computer:
	@echo "Running computer (VM) tests..."
	@python3 -m unittest tests.test_computer

test-integration:
	@echo "Running integration tests..."
	@python3 -m unittest tests/test_integration.py

# Display help information about the available commands
help:
	@echo "Available targets:"
	@echo "  all            - Build the SimpleScript system"
	@echo "  clean          - Remove build artifacts"
	@echo "  test           - Run all tests"
	@echo "  test-compiler  - Run compiler tests only"
	@echo "  test-computer  - Run computer tests only"
	@echo "  test-integration - Run integration tests only"
	@echo "  run-example    - Run a SimpleScript example program (use file=examples/filename.ss)"
	@echo "  help           - Display this help message"
	@echo ""
	@echo "Usage: make [target]" 