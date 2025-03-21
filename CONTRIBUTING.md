# Contributing to SimpleScript

Thank you for your interest in contributing to SimpleScript! This document provides guidelines and instructions for contributing to this project.

## Project Structure

```
SimpleScript/
├── src/              # Source code for the compiler and VM
│   ├── compiler.py   # SimpleScript compiler
│   ├── computer.py   # Virtual machine implementation
│   ├── cpu.py        # CPU emulator
│   └── memory.py     # Memory manager
├── examples/         # Example SimpleScript programs
├── docs/             # Documentation
├── run_simplescript.py # Main script to run programs
├── Makefile          # Build and run tasks
├── README.md         # Project overview
└── CONTRIBUTING.md   # This file
```

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in the Issues section.
2. If not, create a new issue with a clear title and description.
3. Include steps to reproduce the bug.
4. Include any error messages or unexpected output.
5. Specify your operating system and Python version.

### Suggesting Enhancements

1. Open a new issue describing your enhancement suggestion.
2. Explain why this enhancement would be useful.
3. Provide examples of how it would be used.

### Code Contributions

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes.
4. Add tests for your changes if applicable.
5. Ensure all tests pass.
6. Submit a pull request.

## Development Guidelines

### Code Style

- Follow PEP 8 for Python code.
- Use 4 spaces for indentation in Python files.
- Use descriptive variable names.
- Add docstrings for functions and classes.
- Comment code where necessary.

### SimpleScript Language Guidelines

When extending the SimpleScript language, maintain consistency with existing syntax:
- Keep the language simple and beginner-friendly.
- Maintain the use of indentation for block structure.
- Follow the existing pattern for keywords and operators.
- Document new features thoroughly.

### Documentation

- Update documentation when adding or changing features.
- Use Markdown for documentation files.
- Keep the README.md file up to date.

### Testing

- Write test programs in SimpleScript to verify your changes.
- Use the debug mode to check execution behavior.
- Ensure existing example programs still work with your changes.

## Future Enhancements

Here are some areas where contributions would be valuable:

1. **Language Features**:
   - Function/procedure support
   - More arithmetic operations (multiplication, division, modulo)
   - Support for larger numeric values
   - Basic array support
   - Input functionality

2. **Tooling**:
   - Improved error messages and debugging
   - Syntax highlighting for code editors
   - Testing framework
   - Visual representation of program execution

3. **Documentation**:
   - More example programs
   - Detailed language specification
   - Tutorials for beginners

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project. 