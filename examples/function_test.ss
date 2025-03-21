# SimpleScript function example
# Demonstrates function definition and calling

# Define a function to calculate square of a number
def square(n)
  result = n * n
  return result

# Define a function to calculate sum of two numbers
def add(a, b)
  sum = a + b
  return sum

# Define a function with no parameters
def greeting()
  print 42
  print 43

# Main program
x = 5
y = 10

# Call square function
sq_x = square(x)
print sq_x

# Call add function
sum_xy = add(x, y)
print sum_xy

# Call function with no return value
greeting()

# Nested function calls
nested_result = add(square(3), 4)
print nested_result 