class CPU:
    def __init__(self, memory):
        self.memory = memory
        
        # Registers
        self.register_a = 0  # Accumulator
        self.register_b = 0  # General purpose
        
        # Program counter (instruction pointer)
        self.pc = 0
        
        # Flags
        self.zero_flag = False
        
        # Stack pointer (starts from the end of memory and grows downward)
        self.sp = memory.size - 1

        # Define instruction set
        self.instructions = {
            0x00: self.nop,     # No operation
            0x01: self.lda,     # Load value to register A
            0x02: self.ldb,     # Load value to register B
            0x03: self.add,     # Add B to A
            0x04: self.sub,     # Subtract B from A
            0x05: self.sta,     # Store A to memory
            0x06: self.jmp,     # Jump to address
            0x07: self.jz,      # Jump if zero flag is set
            0xFF: self.halt,     # Halt execution
            0x08: self.and_op,  # Logical AND with A
            0x09: self.or_op,   # Logical OR with A
            0x0A: self.xor_op,  # Logical XOR with A
            0x0B: self.shl,     # Shift A left
            0x0C: self.shr,     # Shift A right
            0x0D: self.cmp,     # Compare A with B, set flags
            0x0E: self.jnz,     # Jump if not zero
            0x0F: self.lda_mem, # Load A from memory address
            0x10: self.ldb_mem, # Load B from memory address
            0x20: self.push,    # Push A onto stack
            0x21: self.pop,     # Pop stack to A
            0x22: self.call,    # Call subroutine
            0x23: self.ret,     # Return from subroutine
        }
        
        self.running = False
        
        self.carry_flag = False
        
    def fetch(self):
        value = self.memory.read(self.pc)
        self.pc += 1
        return value
    
    def execute(self, opcode):
        if opcode in self.instructions:
            self.instructions[opcode]()
        else:
            raise Exception(f"Unknown opcode: {opcode}")
    
    # Instruction implementations
    def nop(self):
        pass  # No operation
        
    def lda(self):
        self.register_a = self.fetch()
        self.zero_flag = (self.register_a == 0)
        
    def ldb(self):
        self.register_b = self.fetch()
        
    def add(self):
        self.register_a = (self.register_a + self.register_b) & 0xFF
        self.zero_flag = (self.register_a == 0)
        
    def sub(self):
        self.register_a = (self.register_a - self.register_b) & 0xFF
        self.zero_flag = (self.register_a == 0)
        
    def sta(self):
        address = self.fetch()
        self.memory.write(address, self.register_a)
        
    def jmp(self):
        self.pc = self.fetch()
        
    def jz(self):
        address = self.fetch()
        if self.zero_flag:
            self.pc = address
            
    def halt(self):
        self.running = False
    
    def and_op(self):
        self.register_a = (self.register_a & self.register_b) & 0xFF
        self.zero_flag = (self.register_a == 0)

    def or_op(self):
        self.register_a = (self.register_a | self.register_b) & 0xFF
        self.zero_flag = (self.register_a == 0)
        
    def xor_op(self):
        self.register_a = (self.register_a ^ self.register_b) & 0xFF
        self.zero_flag = (self.register_a == 0)
        
    def shl(self):
        self.carry_flag = (self.register_a & 0x80) != 0
        self.register_a = (self.register_a << 1) & 0xFF
        self.zero_flag = (self.register_a == 0)
    
    def shr(self):
        self.carry_flag = (self.register_a & 0x01) != 0
        self.register_a = (self.register_a >> 1) & 0xFF
        self.zero_flag = (self.register_a == 0)

    def cmp(self):
        result = (self.register_a - self.register_b) & 0xFF
        self.zero_flag = (result == 0)
        self.carry_flag = (self.register_a < self.register_b)
        
    def jnz(self):
        address = self.fetch()
        if not self.zero_flag:
            self.pc = address
            
    def lda_mem(self):
        address = self.fetch()
        self.register_a = self.memory.read(address)
        self.zero_flag = (self.register_a == 0)
        
    def ldb_mem(self):
        address = self.fetch()
        self.register_b = self.memory.read(address)
    
    def push(self):
        self.memory.write(self.sp, self.register_a)
        self.sp = (self.sp - 1) & 0xFF
        
    def pop(self):
        self.sp = (self.sp + 1) & 0xFF
        self.register_a = self.memory.read(self.sp)
        self.zero_flag = (self.register_a == 0)
        
    def call(self):
        address = self.fetch()
        # Push return address onto stack
        self.memory.write(self.sp, self.pc & 0xFF)
        self.sp = (self.sp - 1) & 0xFF
        # Jump to subroutine
        self.pc = address
        
    def ret(self):
        # Pop return address from stack
        self.sp = (self.sp + 1) & 0xFF
        self.pc = self.memory.read(self.sp)

    def run(self):
        self.running = True
        while self.running:
            opcode = self.fetch()
            self.execute(opcode)