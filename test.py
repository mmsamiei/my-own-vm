from computer import Computer

# Example program: Add 5 and 10, store result at memory address 15
program = [
    ("LDA", 5),      # Load 5 into register A
    ("LDB", 10),     # Load 10 into register B
    ("ADD", None),   # Add B to A (result in A)
    ("STA", 15),     # Store result at address 15
    ("HALT", None)   # Stop execution
]

# Create and run the computer
computer = Computer()
computer.load_program(program)
computer.debug_mode()
# computer.run()

# Check the result
print(f"Result at memory address 15: {computer.memory.read(15)}")  # Should be 15