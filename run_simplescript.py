#!/usr/bin/env python3
"""
SimpleScript Launcher

This script runs SimpleScript programs from text files.
Usage: python3 run_simplescript.py <program_file>
"""

import sys
import traceback
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from compiler import SimpleCompiler
from computer import Computer

def main():
    # Check if program file was provided
    if len(sys.argv) < 2:
        print("Error: No program file specified")
        print("Usage: python3 run_simplescript.py <program_file>")
        print("       Add --debug to enable debug mode")
        return
    
    # Read program from file
    program_file = sys.argv[1]
    try:
        with open(program_file, 'r') as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"Error: Program file '{program_file}' not found")
        return
    
    # Determine if debug mode is enabled
    debug_mode = "--debug" in sys.argv
    
    print(f"Running SimpleScript program '{program_file}'")
    print("="*50)
    
    # Create the compiler
    compiler = SimpleCompiler()
    
    try:
        # Compile the program
        program = compiler.compile(source_code)
        
        # Print program information
        if debug_mode:
            print("Compiled Program:")
            for i, (instr, operand) in enumerate(program):
                if operand is not None:
                    print(f"{i}: {instr} {operand}")
                else:
                    print(f"{i}: {instr}")
                
            print("\nVariable Addresses:")
            for var, addr in compiler.variables.items():
                print(f"{var}: {addr}")
            
            print("\nExecution Trace:")
        
        # Create the computer and run the program
        computer = Computer()
        computer.load_program(program)
        
        if debug_mode:
            # Run in debug mode showing each step
            computer.debug_mode()
        else:
            # Run normally
            computer.run()
        
        # Display output using the computer's output handling
        computer.print_output()
            
    except SyntaxError as e:
        print(f"Error: {str(e)}")
    except NameError as e:
        print(f"Error: {str(e)}")
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        if debug_mode:
            traceback.print_exc()
        return

if __name__ == "__main__":
    main() 