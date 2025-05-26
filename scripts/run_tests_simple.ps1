# Simple PowerShell script to run tests for the Rogue-like Game
# This script avoids Unicode characters and complex syntax

param(
    [switch]$Help,
    [switch]$Verbose,
    [switch]$Individual,
    [string]$TestFile = ""
)

if ($Help) {
    Write-Host "Simple Rogue-like Game Test Runner" -ForegroundColor Cyan
    Write-Host "Usage: .\run_tests_simple.ps1 [options]"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Verbose     : Show detailed output"
    Write-Host "  -Individual  : Run each test file separately"
    Write-Host "  -TestFile    : Run specific test (e.g., 'test_progression')"
    Write-Host "  -Help        : Show this help"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\run_tests_simple.ps1                    # Run all tests"
    Write-Host "  .\run_tests_simple.ps1 -Verbose           # Detailed output"
    Write-Host "  .\run_tests_simple.ps1 -Individual        # Run separately"
    Write-Host "  .\run_tests_simple.ps1 -TestFile progression # Specific test"
    exit 0
}

Write-Host "Simple Rogue-like Game Test Runner" -ForegroundColor Cyan
Write-Host "=================================="

# Check if tests directory exists
if (-not (Test-Path "tests")) {
    Write-Host "[ERROR] tests directory not found" -ForegroundColor Red
    Write-Host "Please run this script from the game's root directory" -ForegroundColor Yellow
    exit 1
}

# Check Python
try {
    $null = python --version 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Python is not available" -ForegroundColor Red
        exit 1
    }
    
    if ($Verbose) {
        $pythonVer = python --version
        Write-Host "[OK] Python available: $pythonVer" -ForegroundColor Green
    }
}
catch {
    Write-Host "[ERROR] Cannot check Python: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Set environment
$env:PYTHONPATH = $PWD.Path

# Define test files
$testFiles = @(
    "tests/test_progression.py",
    "tests/test_skill_tree.py", 
    "tests/test_equipment.py",
    "tests/test_player.py"
)

$allPassed = $true

# Function to run a single test
function Run-SingleTest {
    param([string]$TestPath, [string]$TestName)
    
    Write-Host "[TEST] Running $TestName..." -ForegroundColor Yellow
    
    try {
        & python $TestPath
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[PASS] $TestName" -ForegroundColor Green
            return $true
        } else {
            Write-Host "[FAIL] $TestName (exit code: $LASTEXITCODE)" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "[ERROR] $TestName : $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Handle specific test file
if ($TestFile) {
    $found = $false
    foreach ($testPath in $testFiles) {
        if ($testPath -like "*$TestFile*") {
            $testName = Split-Path $testPath -Leaf
            $result = Run-SingleTest -TestPath $testPath -TestName $testName
            if (-not $result) { $allPassed = $false }
            $found = $true
            break
        }
    }
    
    if (-not $found) {
        Write-Host "[ERROR] Test file '$TestFile' not found" -ForegroundColor Red
        Write-Host "Available tests:" -ForegroundColor Yellow
        foreach ($test in $testFiles) {
            $name = Split-Path $test -Leaf
            Write-Host "  - $name" -ForegroundColor White
        }
        exit 1
    }
}
# Handle individual test execution
elseif ($Individual) {
    Write-Host "[INFO] Running tests individually..." -ForegroundColor Cyan
    
    foreach ($testPath in $testFiles) {
        if (Test-Path $testPath) {
            $testName = Split-Path $testPath -Leaf
            $result = Run-SingleTest -TestPath $testPath -TestName $testName
            if (-not $result) { $allPassed = $false }
            Write-Host "" # Add spacing
        } else {
            Write-Host "[WARNING] Test file not found: $testPath" -ForegroundColor Yellow
        }
    }
}
# Handle all tests using test runner
else {
    Write-Host "[INFO] Running all tests using test runner..." -ForegroundColor Yellow
    
    try {
        & python run_tests.py
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[PASS] All tests completed successfully" -ForegroundColor Green
        } else {
            Write-Host "[FAIL] Some tests failed (exit code: $LASTEXITCODE)" -ForegroundColor Red
            $allPassed = $false
        }
    }
    catch {
        Write-Host "[ERROR] Failed to run tests: $($_.Exception.Message)" -ForegroundColor Red
        $allPassed = $false
    }
}

# Final summary
Write-Host ""
Write-Host "=================================================="
if ($allPassed) {
    Write-Host "[SUCCESS] All tests completed successfully!" -ForegroundColor Green
    exit 0
} else {
    Write-Host "[FAILURE] Some tests failed!" -ForegroundColor Red
    exit 1
}
