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
            0xFF: self.halt     # Halt execution
        }
        
        self.running = False
        
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
        
    def run(self):
        self.running = True
        while self.running:
            opcode = self.fetch()
            self.execute(opcode)