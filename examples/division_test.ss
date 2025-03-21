# Division operator test
# This program demonstrates the new division operator

# Basic division
x = 10
y = 2
result = x / y
print result  # Should output 5

# Division with variables
a = 20
b = 4
c = a / b
print c  # Should output 5

# Division in expressions
d = 100
e = 25
f = d / e
print f  # Should output 4

# Division with constants
g = 30 / 6
print g  # Should output 5

# Test division by zero handling
# This should output a warning and set the result to 0
safe = 42
unsafe = 0
result_zero = safe / unsafe
print result_zero  # Should output 0 