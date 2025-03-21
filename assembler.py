class Assembler:
    def __init__(self):
        # Define opcodes
        self.opcodes = {
            'NOP': 0x00, 'LDA': 0x01, 'LDB': 0x02, 'ADD': 0x03,
            'SUB': 0x04, 'STA': 0x05, 'JMP': 0x06, 'JZ': 0x07,
            'AND': 0x08, 'OR': 0x09, 'XOR': 0x0A, 'SHL': 0x0B,
            'SHR': 0x0C, 'CMP': 0x0D, 'JNZ': 0x0E, 'LDA_MEM': 0x0F,
            'LDB_MEM': 0x10, 'PUSH': 0x20, 'POP': 0x21, 'CALL': 0x22,
            'RET': 0x23, 'HALT': 0xFF
        }
        self.labels = {}
        
    def assemble(self, assembly_code):
        # First pass: collect labels
        lines = [line.strip() for line in assembly_code.split('\n')]
        lines = [line for line in lines if line and not line.startswith(';')]
        
        address = 0
        for line in lines:
            if ':' in line:
                label, instruction = line.split(':', 1)
                self.labels[label.strip()] = address
                line = instruction.strip()
            
            # Count bytes for this instruction
            parts = line.split()
            mnemonic = parts[0].upper()
            
            if mnemonic in self.opcodes:
                address += 1  # Opcode byte
                # Add bytes for operands
                if mnemonic in ['LDA', 'LDB', 'STA', 'JMP', 'JZ', 'JNZ', 'LDA_MEM', 'LDB_MEM', 'CALL']:
                    address += 1  # One operand byte
        
        # Second pass: generate machine code
        program = []
        address = 0
        
        for line in lines:
            if ':' in line:
                _, instruction = line.split(':', 1)
                line = instruction.strip()
            
            parts = line.split()
            if not parts:
                continue
                
            mnemonic = parts[0].upper()
            if mnemonic in self.opcodes:
                opcode = self.opcodes[mnemonic]
                program.append(opcode)
                
                # Handle operands
                if len(parts) > 1 and mnemonic in ['LDA', 'LDB', 'STA', 'JMP', 'JZ', 'JNZ', 'LDA_MEM', 'LDB_MEM', 'CALL']:
                    operand = parts[1]
                    
                    # Convert label to address if needed
                    if operand in self.labels:
                        program.append(self.labels[operand])
                    else:
                        # Convert immediate value
                        try:
                            value = int(operand)
                            program.append(value & 0xFF)
                        except ValueError:
                            raise Exception(f"Unknown label or invalid value: {operand}")
        
        return program