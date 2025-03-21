class CPU:
    def __init__(self, memory):
        self.memory = memory
        
        # Registers
        self.register_a = 0  # Accumulator
        self.register_b = 0  # General purpose
        
        # Program counter
        self.pc = 0
        
        # Flags
        self.zero_flag = False
        self.carry_flag = False
        
        # Stack pointer
        self.sp = memory.size - 1
        
        self.running = False
        
    def execute(self, instruction, operand=None):
        # Execute the instruction based on the string mnemonic
        if instruction == "NOP":
            pass  # No operation
            
        elif instruction == "LDA":
            self.register_a = operand
            self.zero_flag = (self.register_a == 0)
            
        elif instruction == "LDB":
            self.register_b = operand
            
        elif instruction == "LDA_MEM":
            self.register_a = self.memory.read(operand)
            self.zero_flag = (self.register_a == 0)
            
        elif instruction == "LDB_MEM":
            self.register_b = self.memory.read(operand)
            
        elif instruction == "STA":
            self.memory.write(operand, self.register_a)
            
        elif instruction == "ADD":
            self.register_a = (self.register_a + self.register_b) & 0xFF
            self.zero_flag = (self.register_a == 0)
            
        elif instruction == "SUB":
            self.register_a = (self.register_a - self.register_b) & 0xFF
            self.zero_flag = (self.register_a == 0)
            
        elif instruction == "AND":
            self.register_a = (self.register_a & self.register_b) & 0xFF
            self.zero_flag = (self.register_a == 0)
            
        elif instruction == "OR":
            self.register_a = (self.register_a | self.register_b) & 0xFF
            self.zero_flag = (self.register_a == 0)
            
        elif instruction == "XOR":
            self.register_a = (self.register_a ^ self.register_b) & 0xFF
            self.zero_flag = (self.register_a == 0)
                        
        elif instruction == "CMP":
            result = (self.register_a - self.register_b) & 0xFF
            self.zero_flag = (result == 0)
            self.carry_flag = (self.register_a < self.register_b)
            
        elif instruction == "JMP":
            self.pc = operand
            return  # Skip the automatic increment of pc
            
        elif instruction == "JZ":
            if self.zero_flag:
                self.pc = operand
                return  # Skip the automatic increment of pc
                
        elif instruction == "JNZ":
            if not self.zero_flag:
                self.pc = operand
                return  # Skip the automatic increment of pc
                
        elif instruction == "PUSH":
            self.memory.write(self.sp, self.register_a)
            self.sp = (self.sp - 1) & 0xFF
            
        elif instruction == "POP":
            self.sp = (self.sp + 1) & 0xFF
            self.register_a = self.memory.read(self.sp)
            self.zero_flag = (self.register_a == 0)
            
        elif instruction == "CALL":
            # Push return address onto stack
            return_address = self.pc + 1  # Next instruction after call
            self.memory.write(self.sp, return_address & 0xFF)
            self.sp = (self.sp - 1) & 0xFF
            # Jump to subroutine
            self.pc = operand
            return  # Skip the automatic increment of pc
            
        elif instruction == "RET":
            # Pop return address from stack
            self.sp = (self.sp + 1) & 0xFF
            self.pc = self.memory.read(self.sp)
            return  # Skip the automatic increment of pc
            
        elif instruction == "HALT":
            self.running = False
            
        else:
            raise Exception(f"Unknown instruction: {instruction}")
            
        # Increment program counter for next instruction
        self.pc += 1