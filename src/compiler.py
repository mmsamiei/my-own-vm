"""
SimpleScript Compiler

This module implements the compiler for the SimpleScript language.
It translates SimpleScript source code into bytecode that can be executed
by the SimpleScript virtual machine (computer.py).

The SimpleCompiler class handles parsing, code generation, and optimization
for the SimpleScript language features including:
- Variable assignments
- Arithmetic operations (addition, subtraction)
- Conditional statements (if/else)
- Loops (while)
- Print statements
- Function definitions and calls
"""

class SimpleCompiler:
    """
    The SimpleScript compiler that translates SimpleScript source code to bytecode.
    
    This compiler implements a simple two-pass compilation process:
    1. First pass: Parse the code and generate instructions with placeholders for jumps
    2. Second pass: Resolve labels and fix jump instructions
    """
    
    def __init__(self):
        """Initialize the compiler with empty variable table and instruction list."""
        self.variables = {}  # Symbol table for variables
        self.functions = {}  # Symbol table for functions
        self.next_var_addr = 16  # Start variables at address 16
        self.instructions = []
        self.current_line = 0
        self.label_counter = 0  # For generating unique labels
        
    def allocate_variable(self, var_name):
        """
        Allocate memory for a variable.
        
        Args:
            var_name: The name of the variable to allocate
            
        Returns:
            The memory address assigned to the variable
        """
        if var_name not in self.variables:
            self.variables[var_name] = self.next_var_addr
            self.next_var_addr += 1
        return self.variables[var_name]
    
    def generate_label(self):
        """
        Generate a unique label for jumps.
        
        Returns:
            A unique label string for branching instructions
        """
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label
        
    def compile(self, source_code):
        """
        Compile source code to computer instructions.
        
        Args:
            source_code: The SimpleScript source code as a string
            
        Returns:
            A list of tuples (instruction, operand) representing the compiled program
            
        Raises:
            SyntaxError: If the source code contains syntax errors
            NameError: If an undefined variable is referenced
            ValueError: If an invalid operation is attempted
        """
        self.instructions = []
        self.labels = {}  # Map from label to instruction index
        self.fixups = []  # List of (instruction_index, label) pairs to fix later
        self.current_line = 0  # Reset line counter
        
        # Preprocess to remove comments and store clean lines
        clean_lines = []
        for line in source_code.strip().split('\n'):
            line = line.split('#', 1)[0].rstrip()  # Remove comments
            if line.strip():  # Skip empty lines
                clean_lines.append(line)
                
        # First pass: Process the main program and register function definitions
        i = 0
        while i < len(clean_lines):
            line = clean_lines[i]
            stripped = line.strip()
            
            # Check for function definitions
            if stripped.startswith('def '):
                # Extract function name
                func_parts = stripped[4:].split('(')
                if len(func_parts) != 2 or not func_parts[1].rstrip().endswith(')'):
                    raise SyntaxError(f"Invalid function definition: {line}")
                
                func_name = func_parts[0].strip()
                params_str = func_parts[1].rstrip(')')
                params = [p.strip() for p in params_str.split(',')] if params_str.strip() else []
                
                # Find the end of the function
                start_idx = i
                indent_level = self.get_indent(line)
                end_idx, _ = self.parse_block(clean_lines, start_idx, indent_level)
                
                # Register the function
                self.functions[func_name] = {
                    'params': params,
                    'start_line': start_idx,
                    'end_line': end_idx,
                    'indent': indent_level
                }
                
                # Skip the function body
                i = end_idx + 1
            else:
                i += 1
                
        # Generate a jump to skip over function definitions
        main_start_label = self.generate_label()
        self.instructions.append(("JMP", main_start_label))
        self.fixups.append((len(self.instructions) - 1, main_start_label))
        
        # Second pass: Process function definitions
        for func_name, func_info in self.functions.items():
            # Add function entry point label
            func_label = f"func_{func_name}"
            self.labels[func_label] = len(self.instructions)
            
            # Process function body
            func_lines = clean_lines[func_info['start_line']+1:func_info['end_line']+1]
            func_indent = func_info['indent'] + 2  # Function body is indented
            
            # Generate code for function body
            for line in func_lines:
                # Skip lines that don't have enough indentation (must be at least func_indent)
                if self.get_indent(line) < func_indent:
                    continue
                    
                # Remove the indentation up to func_indent level
                adjusted_line = line[func_indent:]
                self.process_line(adjusted_line)
                
            # Add return instruction at the end of function
            self.instructions.append(("RET", None))
            
        # Add main program start label - this is the position after all functions
        self.labels[main_start_label] = len(self.instructions)
        
        # Third pass: Process the main program
        i = 0
        while i < len(clean_lines):
            stripped = clean_lines[i].strip()
            # Skip function definitions
            if stripped.startswith('def '):
                indent_level = self.get_indent(clean_lines[i])
                _, end_idx = self.parse_block(clean_lines, i, indent_level)
                i = end_idx + 1
            # Process non-function lines
            elif not stripped.startswith('def '):
                self.current_line = i
                self.process_line(clean_lines[i])
                i += 1
            else:
                i += 1  # Handle any other case
        
        # Add halt instruction at the end of the program
        self.instructions.append(("HALT", None))
        
        # Fix up jumps using labels
        for idx, label in self.fixups:
            if label in self.labels:
                self.instructions[idx] = (self.instructions[idx][0], self.labels[label])
            else:
                raise ValueError(f"Undefined label: {label}")
                
        return self.instructions
        
    def process_line(self, line):
        """Process a single line of code and generate appropriate instructions."""
        stripped = line.strip()
        
        # Skip empty lines
        if not stripped:
            return
            
        # Handle function calls
        if "(" in stripped and ")" in stripped and not stripped.startswith(('if ', 'while ', 'print ')):
            self.compile_function_call(stripped)
            return
            
        # Handle return statements
        if stripped.startswith('return'):
            self.compile_return(stripped)
            return
        
        # Handle if statements
        if stripped.startswith('if '):
            self.compile_if_statement(stripped, line)
            return
            
        # Handle while loops
        if stripped.startswith('while '):
            self.compile_while_loop(stripped, line)
            return
            
        # Handle print statements
        if stripped.startswith('print '):
            self.compile_print(stripped)
            return
            
        # Handle variable assignments
        if '=' in stripped and not stripped.startswith('if') and not '==' in stripped and not '!=' in stripped:
            self.compile_assignment(stripped)
            return
            
        # If we get here, the syntax is not recognized
        raise SyntaxError(f"Syntax error at line: {line}")
        
    def compile_function_call(self, line):
        """Compile a function call."""
        # Extract function name and arguments
        parts = line.split('(', 1)
        func_name = parts[0].strip()
        
        # Check if the function exists
        if func_name not in self.functions:
            raise NameError(f"Undefined function: {func_name}")
            
        # Extract arguments
        args_str = parts[1].split(')', 1)[0].strip()
        args = [arg.strip() for arg in args_str.split(',')] if args_str else []
        
        # Validate argument count
        if len(args) != len(self.functions[func_name]['params']):
            raise ValueError(f"Function {func_name} expects {len(self.functions[func_name]['params'])} arguments, but {len(args)} were provided")
            
        # Push arguments onto the stack (in reverse order)
        for arg in reversed(args):
            # Load the argument into register A
            self.load_operand(arg, 'A')
            # Push it onto the stack
            self.instructions.append(("PUSH", None))
            
        # Call the function
        func_label = f"func_{func_name}"
        self.instructions.append(("CALL", func_label))
        self.fixups.append((len(self.instructions) - 1, func_label))
        
    def compile_return(self, line):
        """Compile a return statement."""
        parts = line.split('return', 1)
        if len(parts) > 1 and parts[1].strip():
            # Return a value
            return_value = parts[1].strip()
            self.load_operand(return_value, 'A')
        
        # Add return instruction
        self.instructions.append(("RET", None))
        
    def compile_if_statement(self, stripped_line, full_line):
        """
        Compile an if statement.
        
        Args:
            stripped_line: The if statement without indentation
            full_line: The original line with indentation
        """
        # Extract condition
        condition = stripped_line[3:].strip()  # Remove 'if '
        
        # Generate labels for branching
        else_label = self.generate_label()
        end_label = self.generate_label()
        
        # Compile condition and conditional jump
        self.compile_condition(condition, else_label)
        
        # Remember current position for if block
        if_block_start = len(self.instructions)
        
        # Compile if block (this would be done by parse_block in the full compiler)
        # For now, we'll just add a placeholder
        
        # Add unconditional jump to end (to skip else block)
        jump_idx = len(self.instructions)
        self.instructions.append(("JMP", end_label))
        self.fixups.append((jump_idx, end_label))
        
        # Mark else label position
        self.labels[else_label] = len(self.instructions)
        
        # Compile else block (would be parsed in full compiler)
        # Placeholder for else block
        
        # Mark end label position
        self.labels[end_label] = len(self.instructions)
        
    def compile_while_loop(self, stripped_line, full_line):
        """
        Compile a while loop.
        
        Args:
            stripped_line: The while statement without indentation
            full_line: The original line with indentation
        """
        # Extract condition
        condition = stripped_line[6:].strip()  # Remove 'while '
        
        # Generate labels for branching
        start_label = self.generate_label()
        end_label = self.generate_label()
        
        # Mark start of loop
        self.labels[start_label] = len(self.instructions)
        
        # Compile condition - if not true, jump to end
        self.compile_condition_inverse(condition, end_label)
        
        # Remember current position for loop body
        loop_body_start = len(self.instructions)
        
        # Compile loop body (would be parsed in full compiler)
        # Placeholder for loop body
        
        # Jump back to start of loop
        self.instructions.append(("JMP", start_label))
        self.fixups.append((len(self.instructions) - 1, start_label))
        
        # Mark end of loop
        self.labels[end_label] = len(self.instructions)
        
    def compile_print(self, line):
        """
        Compile a print statement.
        
        Args:
            line: A string containing the print statement
            
        Example:
            'print x' -> Load value of x into A, then store A to output buffer
        """
        # Extract what to print
        parts = line.split('print', 1)
        if len(parts) < 2:
            raise SyntaxError(f"Invalid print statement: {line}")
            
        expr = parts[1].strip()
        
        # Load the value to print into register A
        self.load_operand(expr, 'A')
        
        # Store register A to the output buffer (memory address 241 / 0xF1)
        self.instructions.append(("STA", 0xF1))
        
    def compile_assignment(self, line):
        """
        Compile a variable assignment like 'x = 5' or 'y = x + 3'.
        
        Args:
            line: The assignment statement
        """
        # Split at first equals sign
        parts = line.split('=', 1)
        if len(parts) != 2:
            raise SyntaxError(f"Invalid assignment at line {self.current_line}: {line}")
            
        left = parts[0].strip()
        right = parts[1].strip()
        
        # Allocate memory for the variable
        var_addr = self.allocate_variable(left)
        
        # Handle different right-hand expressions
        if '+' in right:
            # Addition
            operands = [s.strip() for s in right.split('+')]
            self.load_operand(operands[0], 'A')
            self.load_operand(operands[1], 'B')
            self.instructions.append(("ADD", None))
        elif '-' in right:
            # Subtraction
            operands = [s.strip() for s in right.split('-')]
            self.load_operand(operands[0], 'A')
            self.load_operand(operands[1], 'B')
            self.instructions.append(("SUB", None))
        elif '*' in right:
            # Multiplication
            operands = [s.strip() for s in right.split('*')]
            self.load_operand(operands[0], 'A')
            self.load_operand(operands[1], 'B')
            self.instructions.append(("MUL", None))
        elif '/' in right:
            # Division
            operands = [s.strip() for s in right.split('/')]
            self.load_operand(operands[0], 'A')
            self.load_operand(operands[1], 'B')
            self.instructions.append(("DIV", None))
        else:
            # Simple assignment
            self.load_operand(right, 'A')
            
        # Store the result in the variable
        self.instructions.append(("STA", var_addr))
        
    def compile_condition(self, condition, jump_label):
        """
        Compile a condition with jump to label if condition is false.
        
        Args:
            condition: The condition string (e.g., "x == 5")
            jump_label: The label to jump to if the condition is false
        """
        if '==' in condition:
            left, right = [s.strip() for s in condition.split('==')]
            
            # Load left operand into A
            self.load_operand(left, 'A')
            
            # Load right operand into B
            self.load_operand(right, 'B')
            
            # Compare A and B
            self.instructions.append(("CMP", None))
            
            # Jump if not equal
            jump_idx = len(self.instructions)
            self.instructions.append(("JNZ", None))
            self.fixups.append((jump_idx, jump_label))
            
        elif '!=' in condition:
            left, right = [s.strip() for s in condition.split('!=')]
            
            # Load left operand into A
            self.load_operand(left, 'A')
            
            # Load right operand into B
            self.load_operand(right, 'B')
            
            # Compare A and B
            self.instructions.append(("CMP", None))
            
            # Jump if equal
            jump_idx = len(self.instructions)
            self.instructions.append(("JZ", None))
            self.fixups.append((jump_idx, jump_label))
            
        else:
            raise SyntaxError(f"Unsupported condition at line {self.current_line}: {condition}")
    
    def compile_condition_inverse(self, condition, jump_label):
        """
        Compile a condition with jump to label if condition is true (inverse logic).
        
        Args:
            condition: The condition string (e.g., "x == 5")
            jump_label: The label to jump to if the condition is true
        """
        if '==' in condition:
            left, right = [s.strip() for s in condition.split('==')]
            
            # Load left operand into A
            self.load_operand(left, 'A')
            
            # Load right operand into B
            self.load_operand(right, 'B')
            
            # Compare A and B
            self.instructions.append(("CMP", None))
            
            # Jump if not equal (condition is false)
            jump_idx = len(self.instructions)
            self.instructions.append(("JNZ", None))
            self.fixups.append((jump_idx, jump_label))
            
        elif '!=' in condition:
            left, right = [s.strip() for s in condition.split('!=')]
            
            # Load left operand into A
            self.load_operand(left, 'A')
            
            # Load right operand into B
            self.load_operand(right, 'B')
            
            # Compare A and B
            self.instructions.append(("CMP", None))
            
            # Jump if equal (condition is false)
            jump_idx = len(self.instructions)
            self.instructions.append(("JZ", None))
            self.fixups.append((jump_idx, jump_label))
            
        else:
            raise SyntaxError(f"Unsupported condition at line {self.current_line}: {condition}")
        
    def find_matching_else(self, lines, if_idx, if_indent):
        """
        Find the matching else statement for an if.
        
        Args:
            lines: List of code lines
            if_idx: Index of the if statement
            if_indent: Indentation level of the if statement
            
        Returns:
            The index of the matching else statement, or -1 if not found
        """
        i = if_idx + 1
        # Skip the if block
        while i < len(lines):
            line = lines[i].strip()
            line_indent = self.get_indent(lines[i])
            
            # If we find an else at the same level as the if, it's our match
            if line == 'else' and line_indent == if_indent:
                return i
                
            # If we find a line with less indent than the if, we've exited without finding else
            if line and line_indent < if_indent:
                return -1
                
            i += 1
        
        # Reached end of file without finding else
        return -1
    
    def get_indent(self, line):
        """
        Get the indentation level of a line.
        
        Args:
            line: A line of code
            
        Returns:
            The number of spaces at the beginning of the line
        """
        return len(line) - len(line.lstrip())
    
    def load_operand(self, operand, register):
        """
        Load an operand into a register.
        
        Args:
            operand: A string representation of the operand (variable name or numeric value)
            register: The register to load into ('A' or 'B')
            
        Raises:
            NameError: If the operand is a variable that doesn't exist
            ValueError: If the register is invalid
        """
        # Check for valid register
        if register not in ('A', 'B'):
            raise ValueError(f"Invalid register: {register}")
            
        instruction = f"LD{register}"
        mem_instruction = f"LD{register}_MEM"
        
        # Check if operand is a numeric value or a variable
        operand = operand.strip()
        try:
            # Try to convert to a number
            value = int(operand)
            self.instructions.append((instruction, value))
        except ValueError:
            # If not a number, must be a variable
            if operand not in self.variables:
                # If the variable doesn't exist, allocate it (set to 0)
                self.allocate_variable(operand)
                
            # Load from variable's memory address
            var_addr = self.variables[operand]
            self.instructions.append((mem_instruction, var_addr))

    def parse_block(self, lines, start_idx, indent_level):
        """
        Parse a block of code starting at the given index and indent level.
        
        Args:
            lines: List of code lines
            start_idx: Starting index in the lines list
            indent_level: Indentation level of this block
            
        Returns:
            Tuple of (end_idx, has_else) where:
                end_idx: The index of the next line after this block
                has_else: Boolean indicating if an else block was found
        """
        i = start_idx
        has_else = False
        
        while i < len(lines):
            line = lines[i]
            if not isinstance(line, str):
                i += 1
                continue
                
            line_indent = self.get_indent(line)
            
            # If we encounter a line with less indent than our current level, 
            # we've exited the current block
            if line_indent < indent_level:
                break
                
            # Only process lines at the current indent level
            if line_indent == indent_level:
                line_content = line.strip()
                
                if line_content.startswith('else'):
                    has_else = True
                    i += 1
                else:
                    i += 1
            else:
                # Skip lines with different indentation
                i += 1
                
        return i, has_else


# Example usage (only runs when this file is executed directly)
def main():
    """Simple demonstration of the compiler."""
    # Sample program in our simple language
    source_code = """
    # This is a simple program with an if statement
    x = 5
    y = 10
    
    if x == 5
      z = x + y
      print z
    else
      z = x - y
      print z
    
    # Try a loop too
    counter = 1
    
    while counter != 5
      print counter
      counter = counter + 1
    
    print 100  # Final output to show we're done
    """
    
    compiler = SimpleCompiler()
    program = compiler.compile(source_code)
    
    print("Compiled Program:")
    for i, (instr, operand) in enumerate(program):
        if operand is not None:
            print(f"{i}: {instr} {operand}")
        else:
            print(f"{i}: {instr}")
            
    print("\nVariable Addresses:")
    for var, addr in compiler.variables.items():
        print(f"{var}: {addr}")
    
    # Run on the computer
    from computer import Computer
    computer = Computer()
    computer.load_program(program)
    computer.run()  # Changed to run without debug for the example
    print("\nOutputs:")
    computer.print_output()


if __name__ == "__main__":
    main() 