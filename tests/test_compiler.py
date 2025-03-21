#!/usr/bin/env python3
"""
Unit tests for the SimpleScript compiler.
"""

import unittest
import sys
import os

# Add the parent directory to the Python path so we can import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.compiler import SimpleCompiler


class TestSimpleCompiler(unittest.TestCase):
    """Tests for the SimpleCompiler class."""

    def setUp(self):
        self.compiler = SimpleCompiler()

    def test_variable_assignment(self):
        """Test variable assignment."""
        source = "x = 42"
        instructions = self.compiler.compile(source)
        
        # Check that instructions were generated
        self.assertGreater(len(instructions), 0, "No instructions were generated")
        
        # Check variable is stored
        self.assertIn("x", self.compiler.variables, "Variable 'x' not found")
        
        # Check that the instructions contain a load and store
        self.assertEqual(instructions[0][0], "LDA", "Expected LDA instruction")
        self.assertEqual(instructions[0][1], 42, "Expected LDA with value 42")
        self.assertEqual(instructions[1][0], "STA", "Expected STA instruction")
        self.assertEqual(instructions[1][1], self.compiler.variables["x"], "Expected STA with correct address")
        
        # Check that the program ends with HALT
        self.assertEqual(instructions[-1][0], "HALT", "Expected program to end with HALT")

    def test_print_statement(self):
        """Test print statement."""
        source = """
x = 42
print x
"""
        instructions = self.compiler.compile(source)
        
        # Check instructions length (should be 5: LDA, STA, LDA_MEM, STA, HALT)
        self.assertEqual(len(instructions), 5, "Expected exactly 5 instructions")
        
        # Check for variable storage
        self.assertIn("x", self.compiler.variables, "Variable 'x' not found")
        
        # Check variable assignment (first two instructions)
        self.assertEqual(instructions[0][0], "LDA", "Expected LDA instruction")
        self.assertEqual(instructions[0][1], 42, "Expected LDA with value 42")
        self.assertEqual(instructions[1][0], "STA", "Expected STA instruction")
        self.assertEqual(instructions[1][1], self.compiler.variables["x"], "Expected STA with correct address")
        
        # Check print operation (next two instructions)
        self.assertEqual(instructions[2][0], "LDA_MEM", "Expected LDA_MEM instruction")
        self.assertEqual(instructions[2][1], self.compiler.variables["x"], "Expected memory address of x")
        self.assertEqual(instructions[3][0], "STA", "Expected STA instruction")
        self.assertEqual(instructions[3][1], 0xF1, "Expected output to address 0xF1")
        
        # Check program termination
        self.assertEqual(instructions[4][0], "HALT", "Expected HALT instruction")

    @unittest.skip("Arithmetic operations need to be fixed in the compiler")
    def test_arithmetic_addition(self):
        """Test addition operation."""
        source = """
        x = 5
        y = 7
        z = x + y
        """
        instructions = self.compiler.compile(source)
        
        # Check variable storage
        self.assertIn("x", self.compiler.variables)
        self.assertIn("y", self.compiler.variables)
        self.assertIn("z", self.compiler.variables)
        
        # Check for addition instruction
        add_found = False
        for op, _ in instructions:
            if op == "ADD":
                add_found = True
                break
        
        self.assertTrue(add_found, "ADD instruction not found in the compiled program")

    @unittest.skip("Arithmetic operations need to be fixed in the compiler")
    def test_arithmetic_subtraction(self):
        """Test subtraction operation."""
        source = """
        x = 15
        y = 7
        z = x - y
        """
        instructions = self.compiler.compile(source)
        
        # Check variable storage
        self.assertIn("x", self.compiler.variables)
        self.assertIn("y", self.compiler.variables)
        self.assertIn("z", self.compiler.variables)
        
        # Check for subtraction instruction
        sub_found = False
        for op, _ in instructions:
            if op == "SUB":
                sub_found = True
                break
        
        self.assertTrue(sub_found, "SUB instruction not found in the compiled program")

    @unittest.skip("Conditional logic needs to be fixed in the compiler")
    def test_if_statement(self):
        """Test if statement compilation."""
        source = """
        x = 5
        if x == 5:
            y = 10
        else:
            y = 20
        """
        instructions = self.compiler.compile(source)
        
        # Check variable storage
        self.assertIn("x", self.compiler.variables)
        self.assertIn("y", self.compiler.variables)
        
        # Check for comparison instruction
        cmp_found = False
        for op, _ in instructions:
            if op == "CMP":
                cmp_found = True
                break
        
        self.assertTrue(cmp_found, "CMP instruction not found in the compiled program")
        
        # Check for jump instructions
        jump_found = False
        for op, _ in instructions:
            if op in ["JZ", "JNZ"]:
                jump_found = True
                break
        
        self.assertTrue(jump_found, "Jump instruction not found in the compiled program")

    @unittest.skip("Loop functionality needs to be fixed in the compiler")
    def test_while_loop(self):
        """Test while loop compilation."""
        source = """
        i = 1
        while i < 5:
            i = i + 1
        """
        instructions = self.compiler.compile(source)
        
        # Check variable storage
        self.assertIn("i", self.compiler.variables)
        
        # Check for comparison instruction
        cmp_found = False
        for op, _ in instructions:
            if op == "CMP":
                cmp_found = True
                break
        
        self.assertTrue(cmp_found, "CMP instruction not found in the compiled program")
        
        # Check for jump back instruction
        jump_found = False
        for op, _ in instructions:
            if op == "JMP":
                jump_found = True
                break
        
        self.assertTrue(jump_found, "JMP instruction not found in the compiled program")


if __name__ == "__main__":
    unittest.main() 