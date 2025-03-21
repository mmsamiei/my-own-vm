# SimpleScript Makefile

.PHONY: help run-simple run-if run-while run-fibonacci run-calculator run-nested run-example

# Default target: show help
help:
	@echo "SimpleScript Makefile"
	@echo "--------------------"
	@echo "Available targets:"
	@echo "  help         - Show this help message"
	@echo "  run-simple   - Run the simple test example"
	@echo "  run-if       - Run the if statement example"
	@echo "  run-while    - Run the while loop example"
	@echo "  run-fibonacci - Run the Fibonacci sequence example"
	@echo "  run-calculator - Run the calculator example"
	@echo "  run-nested   - Run the nested structures example"
	@echo "  run-example  - Run the comprehensive example program"
	@echo "  debug-EXAMPLE - Run any example in debug mode (e.g., debug-fibonacci)"
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
	python3 run_simplescript.py examples/example_program.txt

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