# PowerShell Guide for Simple Rogue-like Game

This guide provides comprehensive instructions for running and developing the Simple Rogue-like Game using PowerShell on Windows systems, with proper syntax to avoid common PowerShell errors.

## 🚀 Quick Start

### Running the Game
```powershell
# Navigate to the game directory
cd "C:\path\to\simple_rouge_like"

# Run the game with the provided script
.\run_game.ps1
```

### Running Tests
```powershell
# Run all tests
.\run_tests.ps1

# Run with verbose output
.\run_tests.ps1 -Verbose

# Run individual test files
.\run_tests.ps1 -Individual
```

## 🛠️ PowerShell Scripts Overview

### 1. `run_game.ps1` - Game Launcher
**Purpose**: Safely launch the game with proper error handling and dependency checking.

**Usage:**
```powershell
.\run_game.ps1 [options]
```

**Options:**
- `-Debug`: Run with debug output
- `-Verbose`: Show detailed execution information
- `-Help`: Display help information

**Examples:**
```powershell
.\run_game.ps1                # Normal execution
.\run_game.ps1 -Verbose       # Detailed output
.\run_game.ps1 -Debug         # Debug mode
.\run_game.ps1 -Help          # Show help
```

### 2. `run_tests.ps1` - Test Runner
**Purpose**: Execute all test suites with comprehensive reporting.

**Usage:**
```powershell
.\run_tests.ps1 [options]
```

**Options:**
- `-Verbose`: Show detailed test execution
- `-Individual`: Run each test file separately
- `-Coverage`: Run with coverage report (requires coverage.py)
- `-TestFile <name>`: Run specific test file
- `-Help`: Display help information

**Examples:**
```powershell
.\run_tests.ps1                           # Run all tests
.\run_tests.ps1 -Verbose                  # Detailed output
.\run_tests.ps1 -Individual               # Run tests separately
.\run_tests.ps1 -TestFile test_progression # Run specific test
.\run_tests.ps1 -Coverage                 # With coverage report
```

### 3. `dev_utils.ps1` - Development Utilities
**Purpose**: Provide common development tasks and environment management.

**Usage:**
```powershell
.\dev_utils.ps1 <command> [options]
```

**Commands:**
- `setup`: Set up development environment
- `clean`: Clean cache files and temporary data
- `install`: Install required dependencies
- `check`: Check system requirements
- `format`: Format Python code (requires black)
- `lint`: Run code linting (requires flake8)
- `assets`: Generate missing game assets
- `help`: Show help information

**Examples:**
```powershell
.\dev_utils.ps1 setup           # Setup development environment
.\dev_utils.ps1 check -Verbose  # Check requirements with details
.\dev_utils.ps1 clean -Force    # Clean without confirmation
.\dev_utils.ps1 install         # Install dependencies
```

## ⚠️ Common PowerShell Issues and Solutions

### 1. Ampersand (&) Syntax Errors
**Problem**: Error like "The ampersand (&) character is not allowed"

**Cause**: Incorrect PowerShell command syntax or malformed commands

**Solutions:**
```powershell
# ❌ WRONG - This causes ampersand errors
a& python main.py

# ✅ CORRECT - Use provided scripts
.\run_game.ps1

# ✅ CORRECT - Proper PowerShell syntax for direct execution
& python main.py

# ✅ CORRECT - Navigate first, then run
cd "C:\path\to\game"
python main.py
```

### 2. Execution Policy Errors
**Problem**: "Execution of scripts is disabled on this system"

**Solution:**
```powershell
# Check current policy
Get-ExecutionPolicy

# Set policy for current user (recommended)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Alternative: Set for current process only
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```

### 3. Path Issues
**Problem**: "Python is not recognized" or path-related errors

**Solutions:**
```powershell
# Check if Python is in PATH
python --version

# Add Python to current session PATH (temporary)
$env:PATH += ";C:\Users\YourName\AppData\Local\Programs\Python\Python313"

# Use full path (if needed)
& "C:\Users\YourName\AppData\Local\Programs\Python\Python313\python.exe" main.py

# Use Python launcher (Windows)
py main.py
```

### 4. Permission Errors
**Problem**: Access denied or permission-related errors

**Solutions:**
```powershell
# Run PowerShell as Administrator
# Right-click PowerShell -> "Run as Administrator"

# Or adjust file permissions
icacls ".\run_game.ps1" /grant:r "$env:USERNAME:(RX)"
```

## 🔧 Development Workflow

### Initial Setup
```powershell
# 1. Navigate to project directory
cd "C:\path\to\simple_rouge_like"

# 2. Check system requirements
.\dev_utils.ps1 check

# 3. Set up development environment
.\dev_utils.ps1 setup

# 4. Verify installation
.\run_game.ps1 -Help
.\run_tests.ps1 -Help
```

### Daily Development
```powershell
# Run the game for testing
.\run_game.ps1

# Run tests after making changes
.\run_tests.ps1

# Run specific tests for features you're working on
.\run_tests.ps1 -TestFile test_progression

# Clean up cache files periodically
.\dev_utils.ps1 clean
```

### Code Quality
```powershell
# Format code (requires black)
.\dev_utils.ps1 format

# Run linting (requires flake8)
.\dev_utils.ps1 lint

# Run tests with coverage
.\run_tests.ps1 -Coverage
```

## 📋 Alternative Execution Methods

### Method 1: Direct Python Execution
```powershell
# Navigate to project directory first
cd "C:\path\to\simple_rouge_like"

# Run directly
python main.py
python tests/test_progression.py
```

### Method 2: Using Python Launcher
```powershell
# Use py command (Windows Python Launcher)
py main.py
py tests/test_progression.py
py -m pytest tests/
```

### Method 3: Using Start-Process
```powershell
Start-Process -FilePath "python" -ArgumentList "main.py" -WorkingDirectory "C:\path\to\simple_rouge_like"
```

### Method 4: Batch File Alternative
Create `run_game.bat`:
```batch
@echo off
cd /d "%~dp0"
python main.py
pause
```

## 🎯 Best Practices

### 1. Always Use Provided Scripts
- Use `.\run_game.ps1` instead of manual python commands
- Use `.\run_tests.ps1` for testing
- Use `.\dev_utils.ps1` for development tasks

### 2. Proper Path Handling
```powershell
# ✅ GOOD - Use quotes for paths with spaces
cd "C:\My Games\simple_rouge_like"

# ✅ GOOD - Use relative paths when possible
.\run_game.ps1

# ❌ AVOID - Unquoted paths with spaces
cd C:\My Games\simple_rouge_like
```

### 3. Error Handling
```powershell
# Check if script exists before running
if (Test-Path ".\run_game.ps1") {
    .\run_game.ps1
} else {
    Write-Host "Script not found!"
}
```

### 4. Environment Management
```powershell
# Set working directory at start of session
Set-Location "C:\path\to\simple_rouge_like"

# Verify you're in the right place
Get-Location
```

## 🆘 Troubleshooting Checklist

When encountering issues, check these items in order:

1. **✅ Correct Directory**: Are you in the game's root directory?
   ```powershell
   Get-Location
   Test-Path "main.py"
   ```

2. **✅ Python Available**: Is Python installed and accessible?
   ```powershell
   python --version
   ```

3. **✅ Dependencies Installed**: Are required packages available?
   ```powershell
   .\dev_utils.ps1 check
   ```

4. **✅ Execution Policy**: Can PowerShell run scripts?
   ```powershell
   Get-ExecutionPolicy
   ```

5. **✅ File Permissions**: Can you access the script files?
   ```powershell
   Test-Path ".\run_game.ps1"
   ```

6. **✅ Script Syntax**: Are you using correct PowerShell syntax?
   ```powershell
   # Use .\ prefix for local scripts
   .\run_game.ps1
   ```

## 📚 Additional Resources

- **Game Documentation**: See `README.md` for general game information
- **Progression Features**: See `PROGRESSION_FEATURES.md` for detailed progression system documentation
- **Implementation Details**: See `IMPLEMENTATION_SUMMARY.md` for technical implementation information
- **PowerShell Documentation**: [Microsoft PowerShell Docs](https://docs.microsoft.com/en-us/powershell/)

## 🎮 Game-Specific PowerShell Commands

### Quick Game Testing
```powershell
# Test game launch
.\run_game.ps1 -Verbose

# Test progression system
.\run_tests.ps1 -TestFile test_progression

# Test skill tree
.\run_tests.ps1 -TestFile test_skill_tree

# Test equipment system
.\run_tests.ps1 -TestFile test_equipment
```

### Development Tasks
```powershell
# Full development cycle
.\dev_utils.ps1 clean
.\dev_utils.ps1 check
.\run_tests.ps1
.\run_game.ps1

# Code quality check
.\dev_utils.ps1 format
.\dev_utils.ps1 lint
.\run_tests.ps1 -Coverage
```

This guide ensures you can run and develop the Simple Rogue-like Game on Windows using PowerShell without encountering syntax errors or execution issues.
