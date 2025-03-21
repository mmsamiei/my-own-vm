class CPU:
    def __init__(self, memory):
        self.memory = memory
        
        # Registers
        self.register_a = 0  # Accumulator
        self.register_b = 0  # Secondary register
        
        # Program counter
        self.pc = 0
        
        # Flags
        self.zero_flag = False
        self.carry_flag = False
        
        # State
        self.running = False
        
        # Define the instruction set
        self.instructions = {
            # Load operations
            "LDA": self._lda,        # Load immediate value into A
            "LDB": self._ldb,        # Load immediate value into B
            "LDA_MEM": self._lda_mem,  # Load from memory into A
            "LDB_MEM": self._ldb_mem,  # Load from memory into B
            
            # Store operations
            "STA": self._sta,        # Store A to memory
            "STB": self._stb,        # Store B to memory
            
            # Arithmetic operations
            "ADD": self._add,        # A = A + B
            "SUB": self._sub,        # A = A - B
            
            # Comparison operation
            "CMP": self._cmp,        # Compare A and B, set flags
            
            # Jump operations
            "JMP": self._jmp,        # Unconditional jump
            "JZ": self._jz,          # Jump if zero flag is set
            "JNZ": self._jnz,        # Jump if zero flag is not set
            
            # Control operations
            "HALT": self._halt,      # Stop execution
        }
        
    def execute(self, instruction, operand):
        """Execute a single instruction with its operand."""
        if instruction in self.instructions:
            self.instructions[instruction](operand)
        else:
            raise ValueError(f"Unknown instruction: {instruction}")
    
    def _lda(self, value):
        """Load immediate value into register A."""
        self.register_a = value
        self.pc += 1
    
    def _ldb(self, value):
        """Load immediate value into register B."""
        self.register_b = value
        self.pc += 1
    
    def _lda_mem(self, address):
        """Load value from memory into register A."""
        self.register_a = self.memory.read(address)
        self.pc += 1
    
    def _ldb_mem(self, address):
        """Load value from memory into register B."""
        self.register_b = self.memory.read(address)
        self.pc += 1
    
    def _sta(self, address):
        """Store register A to memory."""
        self.memory.write(address, self.register_a)
        self.pc += 1
    
    def _stb(self, address):
        """Store register B to memory."""
        self.memory.write(address, self.register_b)
        self.pc += 1
    
    def _add(self, _):
        """A = A + B"""
        self.register_a += self.register_b
        self.pc += 1
    
    def _sub(self, _):
        """A = A - B"""
        self.register_a -= self.register_b
        self.pc += 1
    
    def _cmp(self, _):
        """Compare A and B, set flags."""
        if self.register_a == self.register_b:
            self.zero_flag = True
            self.carry_flag = False
        elif self.register_a < self.register_b:
            self.zero_flag = False
            self.carry_flag = True
        else:
            self.zero_flag = False
            self.carry_flag = False
        self.pc += 1
    
    def _jmp(self, address):
        """Unconditional jump."""
        self.pc = address
    
    def _jz(self, address):
        """Jump if zero flag is set."""
        if self.zero_flag:
            self.pc = address
        else:
            self.pc += 1
    
    def _jnz(self, address):
        """Jump if zero flag is not set."""
        if not self.zero_flag:
            self.pc = address
        else:
            self.pc += 1
    
    def _halt(self, _):
        """Stop execution."""
        self.running = False
        self.pc += 1