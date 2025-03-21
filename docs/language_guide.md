# SimpleScript Language Guide

## Introduction

SimpleScript is a minimalist programming language designed for educational purposes. It demonstrates the basics of language design, compilation, and execution on a simple virtual machine.

## Language Overview

SimpleScript is:
- **Minimalist**: Includes only essential programming constructs
- **Imperative**: Programs consist of sequences of commands
- **Indentation-based**: Uses indentation (2 spaces) to denote code blocks
- **Integer-focused**: Only works with integer values
- **Line-oriented**: Each statement occupies its own line

## Syntax Elements

### Comments

Comments start with `#` and continue to the end of the line:

```
# This is a comment
x = 5  # This is an inline comment
```

### Variables

Variable names can contain letters, numbers, and underscores, and must start with a letter:

```
count = 1
result = 42
```

Variables are automatically allocated memory addresses during compilation.

### Arithmetic Operations

SimpleScript supports addition and subtraction:

```
x = 5 + 3  # Addition
y = 10 - 2  # Subtraction
z = x + y  # Using variables
```

### Output

The `print` statement outputs a value:

```
print x
print 42
```

### Control Structures

#### If-Else Statements

Conditional execution with `if` and optional `else`:

```
if x == 5
  print 100
else
  print 200
```

Conditions can use equality (`==`) or inequality (`!=`):

```
if count != 0
  print count
```

#### Nested If-Else Statements

If-else statements can be nested:

```
if x > 0
  if y > 0
    print 1  # x > 0 and y > 0
  else
    print 2  # x > 0 and y <= 0
else
  print 3    # x <= 0
```

#### While Loops

Repetitive execution with `while`:

```
counter = 1
while counter != 6
  print counter
  counter = counter + 1
```

#### Nested While Loops

While loops can be nested:

```
i = 1
while i != 4
  j = 1
  while j != 4
    print i + j
    j = j + 1
  i = i + 1
```

## Memory Model

SimpleScript uses a simple memory model:
- Memory addresses 0-15 are reserved for system use
- Variables are allocated memory addresses starting from 16
- Output uses memory-mapped I/O at address 241 (0xF1)

## Example Programs

### Hello World (Simplified)

```
# Since there's no string support, we use a number
print 42
```

### Counting Loop

```
# Print numbers 1 through 5
counter = 1
while counter != 6
  print counter
  counter = counter + 1
```

### Conditional Logic

```
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

### Fibonacci Sequence

```
# Generate the first 8 Fibonacci numbers
a = 0
b = 1
print a  # 0
print b  # 1

count = 2
while count != 10
  next = a + b
  print next
  a = b
  b = next
  count = count + 1
```

## Best Practices

1. **Use Meaningful Variable Names**: Makes code more readable
2. **Add Comments**: Explain complex logic
3. **Consistent Indentation**: Always use 2 spaces
4. **Avoid Large Numbers**: Keep values below 200 to prevent overflow
5. **Structure Code Logically**: Organize related operations together

## Limitations

- No arrays or complex data structures
- No functions or procedures
- Only integer values (with limited range)
- Limited to addition and subtraction
- No input methods
- No string support

## Compiler and VM Architecture

SimpleScript is implemented with:
1. **Compiler**: Translates source code to bytecode instructions
2. **Virtual Machine**: Executes the bytecode instructions
3. **Memory**: Stores program state
4. **CPU**: Processes instructions with registers A and B

## Debugging

Run programs with `--debug` flag to see detailed execution information:

```bash
python3 run_simplescript.py examples/your_program.txt --debug
```

This shows:
- Instruction execution sequence
- Register values at each step
- Memory operations
- Flag states 