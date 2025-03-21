class SimpleCompiler:
    def __init__(self):
        self.variables = {}  # Symbol table for variables
        self.next_var_addr = 16  # Start variables at address 16
        self.instructions = []
        self.current_line = 0
        self.label_counter = 0  # For generating unique labels
        
    def allocate_variable(self, var_name):
        """Allocate memory for a variable"""
        if var_name not in self.variables:
            self.variables[var_name] = self.next_var_addr
            self.next_var_addr += 1
        return self.variables[var_name]
    
    def generate_label(self):
        """Generate a unique label for jumps"""
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label
        
    def compile(self, source_code):
        """Compile source code to computer instructions"""
        self.instructions = []
        self.labels = {}  # Map from label to instruction index
        self.fixups = []  # List of (instruction_index, label) pairs to fix later
        self.current_line = 0  # Reset line counter
        
        # Preprocess to remove comments and store clean lines
        clean_lines = []
        for line in source_code.strip().split('\n'):
            # Skip empty lines
            if not line.strip():
                continue
                
            # Skip comment lines
            if line.strip().startswith('#'):
                continue
                
            # Remove trailing comments from content lines
            if '#' in line:
                line = line.split('#', 1)[0].rstrip()
            
            clean_lines.append(line)
        
        # First pass: parse the code and generate instructions
        self.parse_block(clean_lines, 0, 0)
        
        # Second pass: resolve labels and fix jumps
        for instr_idx, label in self.fixups:
            if label not in self.labels:
                raise ValueError(f"Undefined label: {label}")
            self.instructions[instr_idx] = (self.instructions[instr_idx][0], self.labels[label])
        
        # Always end the program with HALT
        self.instructions.append(("HALT", None))
        return self.instructions

    def parse_block(self, lines, start_idx, indent_level):
        """Parse a block of code starting at the given index and indent level"""
        i = start_idx
        while i < len(lines):
            line = lines[i]
            line_indent = self.get_indent(line)
            
            # If we encounter a line with less indent than our current level, 
            # we've exited the current block
            if line_indent < indent_level:
                break
                
            # Only process lines at the current indent level
            if line_indent == indent_level:
                self.current_line += 1
                line_content = line.strip()
                
                if '=' in line_content and not line_content.startswith('if') and not line_content.startswith('while'):
                    # Variable assignment
                    self.compile_assignment(line_content)
                    i += 1
                elif line_content.startswith('print '):
                    # Print statement
                    self.compile_print(line_content)
                    i += 1
                elif line_content.startswith('if '):
                    # IF statement - find the matching block
                    condition = line_content[3:]  # Remove 'if '
                    else_idx = self.find_matching_else(lines, i, line_indent)
                    
                    # Compile the if condition
                    end_label = self.generate_label()
                    if else_idx != -1:
                        else_label = self.generate_label()
                        self.compile_condition(condition, else_label)
                        
                        # Compile the if block
                        i = self.parse_block(lines, i + 1, line_indent + 2)
                        
                        # Jump to end (skip else)
                        jump_idx = len(self.instructions)
                        self.instructions.append(("JMP", None))
                        self.fixups.append((jump_idx, end_label))
                        
                        # Mark the else label position
                        self.labels[else_label] = len(self.instructions)
                        
                        # Compile the else block
                        # Skip the 'else' line
                        i = self.parse_block(lines, else_idx + 1, line_indent + 2)
                    else:
                        # No else block
                        skip_label = self.generate_label()
                        self.compile_condition_inverse(condition, skip_label)
                        
                        # Compile the if block
                        i = self.parse_block(lines, i + 1, line_indent + 2)
                        
                        # Mark the skip label position
                        self.labels[skip_label] = len(self.instructions)
                    
                    # Mark the end label position
                    self.labels[end_label] = len(self.instructions)
                elif line_content.startswith('while '):
                    # WHILE loop - find the matching block
                    condition = line_content[6:]  # Remove 'while '
                    
                    # Create labels for the loop
                    start_label = self.generate_label()
                    end_label = self.generate_label()
                    
                    # Mark the start of the loop
                    self.labels[start_label] = len(self.instructions)
                    
                    # Compile the condition
                    self.compile_condition_inverse(condition, end_label)
                    
                    # Remember the current position for block start
                    block_start = i + 1
                    
                    # Compile the loop body
                    i = self.parse_block(lines, block_start, line_indent + 2)
                    
                    # Jump back to the start of the loop
                    self.instructions.append(("JMP", None))
                    self.fixups.append((len(self.instructions) - 1, start_label))
                    
                    # Mark the end of the loop
                    self.labels[end_label] = len(self.instructions)
                elif line_content == 'else':
                    # Just skip the else line, it will be handled in the if block
                    i += 1
                else:
                    raise SyntaxError(f"Unknown statement at line {self.current_line}: {line_content}")
            else:
                # Skip lines with different indentation
                i += 1
        
        return i

    def find_matching_else(self, lines, if_idx, if_indent):
        """Find the matching else statement for an if"""
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
        """Get the indentation level of a line"""
        return len(line) - len(line.lstrip())
    
    def compile_condition(self, condition, jump_label):
        """Compile a condition with jump to label if condition is false"""
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
        """Compile a condition with jump to label if condition is true (inverse logic)"""
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
        
    def compile_assignment(self, line):
        """Compile a variable assignment like 'x = 5' or 'y = x + 3'"""
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
        else:
            # Simple assignment
            self.load_operand(right, 'A')
            
        # Store the result in the variable
        self.instructions.append(("STA", var_addr))
        
    def compile_print(self, line):
        """Compile a print statement like 'print x'"""
        # Remove 'print ' prefix and strip whitespace
        var_name = line[6:].strip()
        
        # Output uses memory-mapped I/O at address 241 (0xF1)
        OUTPUT_ADDR = 0xF1
        
        if var_name in self.variables:
            # Load the variable value into A
            self.instructions.append(("LDA_MEM", self.variables[var_name]))
            # Store A to output buffer
            self.instructions.append(("STA", OUTPUT_ADDR))
        elif var_name.isdigit():
            # Load immediate value
            self.instructions.append(("LDA", int(var_name)))
            # Store A to output buffer
            self.instructions.append(("STA", OUTPUT_ADDR))
        else:
            raise NameError(f"Unknown variable '{var_name}' at line {self.current_line}")
     
    def load_operand(self, operand, register):
        """Load an operand into a register (A or B)"""
        operand = operand.strip()
        
        if operand.isdigit():
            # Immediate value
            if register == 'A':
                self.instructions.append(("LDA", int(operand)))
            else:
                self.instructions.append(("LDB", int(operand)))
        elif operand in self.variables:
            # Variable
            if register == 'A':
                self.instructions.append(("LDA_MEM", self.variables[operand]))
            else:
                self.instructions.append(("LDB_MEM", self.variables[operand]))
        else:
            raise NameError(f"Unknown operand '{operand}' at line {self.current_line}")


# Example usage
def main():
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