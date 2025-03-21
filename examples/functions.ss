# SimpleScript Example with Functions
# This demonstrates the function support in SimpleScript

# Define a function to calculate the square of a number
def square(n)
  result = n * n
  return result

# Define a function to calculate factorial
def factorial(n)
  if n == 0
    return 1
  else
    if n == 1
      return 1
    else
      temp = n - 1
      sub_fact = factorial(temp)  # Recursive call
      result = n * sub_fact
      return result

# Define a function to check if a number is even
def is_even(n)
  result = n
  while result > 1
    result = result - 2
  
  if result == 0
    return 1  # True, it's even
  else
    return 0  # False, it's odd

# Define a function to calculate Fibonacci
def fibonacci(n)
  if n == 0
    return 0
  else
    if n == 1
      return 1
    else
      a = n - 1
      b = n - 2
      result1 = fibonacci(a)
      result2 = fibonacci(b)
      return result1 + result2

# Main program
print 42  # Starting marker

# Test the square function
x = 5
sq_x = square(x)
print sq_x  # Should print 25

# Test factorial (non-recursive case)
fact_3 = factorial(3)
print fact_3  # Should print 6

# Test is_even
y = 10
is_y_even = is_even(y)
print is_y_even  # Should print 1 (true)

z = 7
is_z_even = is_even(z)
print is_z_even  # Should print 0 (false)

# Calculate Fibonacci number
fib_result = fibonacci(5)
print fib_result  # Should print 5

# End of program
print 99  # End marker 