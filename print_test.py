#!/usr/bin/env python3
"""
Test script for print statement compilation.
"""

import sys
import os

# Add the src directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.compiler import SimpleCompiler


def main():
    """Test the compilation of a print statement."""
    print("SimpleScript Print Test")
    print("======================")
    
    # Test with indentation
    source1 = """
        x = 42
        print x
        """
    print(f"\nTest Program 1 (with indentation):\n{source1}")
    
    # Create compiler and compile the program
    print("\nCompiling program 1...")
    compiler1 = SimpleCompiler()
    instructions1 = compiler1.compile(source1)
    
    # Display the instructions
    print("\nGenerated Instructions:")
    for i, (op, arg) in enumerate(instructions1):
        if arg is not None:
            print(f"{i}: {op} {arg}")
        else:
            print(f"{i}: {op}")
    
    # Debug output - variable mapping
    print("\nVariable Mapping:")
    for var_name, address in compiler1.variables.items():
        print(f"  {var_name}: Memory location {address}")
    
    print("\n" + "="*50 + "\n")
    
    # Test without indentation
    source2 = """
x = 42
print x
"""
    print(f"\nTest Program 2 (without indentation):\n{source2}")
    
    # Create compiler and compile the program
    print("\nCompiling program 2...")
    compiler2 = SimpleCompiler()
    instructions2 = compiler2.compile(source2)
    
    # Display the instructions
    print("\nGenerated Instructions:")
    for i, (op, arg) in enumerate(instructions2):
        if arg is not None:
            print(f"{i}: {op} {arg}")
        else:
            print(f"{i}: {op}")
    
    # Debug output - variable mapping
    print("\nVariable Mapping:")
    for var_name, address in compiler2.variables.items():
        print(f"  {var_name}: Memory location {address}")
    

if __name__ == "__main__":
    main() 