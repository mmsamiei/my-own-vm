#!/usr/bin/env python3
"""
SimpleScript Functions Example Runner

This script runs the functions.ss example to demonstrate function capabilities.
"""

import sys
import os
from src.compiler import SimpleCompiler
from src.computer import Computer

def main():
    # Get the path to the functions example
    example_path = os.path.join('examples', 'functions.ss')
    
    if not os.path.exists(example_path):
        print(f"Error: Could not find example file: {example_path}")
        return
    
    print(f"Running SimpleScript functions example: {example_path}")
    print("=" * 50)
    
    # Read the source code
    with open(example_path, 'r') as f:
        source_code = f.read()
    
    # Print the source code for reference
    print("Source code:")
    print("-" * 50)
    for i, line in enumerate(source_code.split('\n'), 1):
        print(f"{i:3d} | {line}")
    print("-" * 50)
    
    # Compile the source code
    compiler = SimpleCompiler()
    
    try:
        program = compiler.compile(source_code)
        
        # Create and initialize the computer
        computer = Computer()
        computer.load_program(program)
        
        # Run the program
        print("\nProgram output:")
        print("-" * 50)
        computer.run()
        computer.print_output()
        print("-" * 50)
        
        # Print variable information
        print("\nVariables:")
        print("-" * 50)
        for name, addr in sorted(compiler.variables.items()):
            value = computer.memory.read(addr)
            print(f"{name}: {value} (address: {addr})")
            
        # Print function information
        print("\nFunctions:")
        print("-" * 50)
        for name, info in sorted(compiler.functions.items()):
            params = ", ".join(info['params'])
            print(f"{name}({params})")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        
    print("=" * 50)

if __name__ == "__main__":
    main() 