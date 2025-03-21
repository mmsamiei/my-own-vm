# SimpleScript Language

SimpleScript is a minimalist programming language designed to run on a simple virtual machine.

## Language Features

SimpleScript supports:

1. **Variable assignments**: `x = 5`
2. **Arithmetic operations**: addition (`+`) and subtraction (`-`)
3. **Output**: `print` statements
4. **Comments**: Lines starting with `#`
5. **Conditionals**: `if`/`else` statements with equality/inequality checks
6. **Loops**: `while` loops for repeated execution
7. **Nested constructs**: Support for nested if/else statements and while loops

## Syntax Rules

- Indentation matters: Use 2 spaces to indent code blocks
- Each statement must be on its own line
- Variable names are case-sensitive
- Comments start with `#` and continue to the end of the line

## Examples

### Basic Arithmetic
```
# This calculates 5 + 10 and prints the result
x = 5
y = 10
z = x + y
print z
```

### If-Else Statements
```
# Conditional execution
x = 5
if x == 5
  print 100  # This will execute
else
  print 200
```

### Nested If-Else Statements
```
# Nested conditional execution
x = 5
y = 10
if x == 5
  if y == 10
    print 100  # This will execute
  else
    print 200
else
  print 300
```

### While Loops
```
# Loop execution
counter = 1
while counter != 6
  print counter  # Will print 1, 2, 3, 4, 5
  counter = counter + 1
```

### Fibonacci Sequence Example
```
# Generate Fibonacci sequence
a = 0
b = 1
print a
print b
count = 2
while count != 10
  next = a + b
  print next
  a = b
  b = next
  count = count + 1
```

## How It Works

The SimpleScript compiler translates the code into a sequence of instructions for our simple virtual machine:

1. **Lexical Analysis**: Reads the source code and identifies language elements
2. **Parsing**: Interprets the structure of the code
3. **Code Generation**: Converts parsed code into machine instructions
4. **Execution**: The virtual machine runs the generated instructions

## Memory Layout

- Memory addresses 0-15: Reserved for system use
- Memory addresses 16+: Used for storing variables
- Memory address 241 (0xF1): Output buffer

## Limitations

This is a simple language with the following limitations:

- No arrays or complex data structures
- No functions or procedures
- Only integers are supported
- Limited to addition and subtraction
- No input methods (values must be hardcoded)

## Running Programs

To run a SimpleScript program:

```bash
python3 run_simplescript.py your_program.txt
```

Add the `--debug` flag to see detailed execution information:

```bash
python3 run_simplescript.py your_program.txt --debug
```

## Example Programs

Several example programs are included to demonstrate SimpleScript's capabilities:

- `simple_test.txt`: Basic variable and arithmetic operations
- `if_test.txt`: Demonstrates if/else statements
- `while_test.txt`: Demonstrates while loops
- `fibonacci.txt`: Generates the Fibonacci sequence
- `calculator.txt`: A simple calculator with nested conditionals
- `example_program.txt`: A comprehensive example showing various features 