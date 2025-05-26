# PowerShell script to run all tests for the Simple Rogue-like Game
# This script ensures proper execution without PowerShell syntax errors

param(
    [switch]$Verbose,
    [switch]$Individual,
    [switch]$Coverage,
    [switch]$Help,
    [string]$TestFile = ""
)

# Display help information
if ($Help) {
    Write-Host "Simple Rogue-like Game Test Runner" -ForegroundColor Cyan
    Write-Host "==================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage: .\run_tests.ps1 [options]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Options:" -ForegroundColor Green
    Write-Host "  -Verbose     : Show detailed test execution information" -ForegroundColor White
    Write-Host "  -Individual  : Run each test file separately" -ForegroundColor White
    Write-Host "  -Coverage    : Run tests with coverage report (requires coverage.py)" -ForegroundColor White
    Write-Host "  -TestFile    : Run a specific test file (e.g., 'test_progression')" -ForegroundColor White
    Write-Host "  -Help        : Show this help message" -ForegroundColor White
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Green
    Write-Host "  .\run_tests.ps1                           # Run all tests" -ForegroundColor White
    Write-Host "  .\run_tests.ps1 -Verbose                  # Run with verbose output" -ForegroundColor White
    Write-Host "  .\run_tests.ps1 -Individual               # Run each test file separately" -ForegroundColor White
    Write-Host "  .\run_tests.ps1 -TestFile test_progression # Run specific test file" -ForegroundColor White
    Write-Host "  .\run_tests.ps1 -Coverage                 # Run with coverage report" -ForegroundColor White
    exit 0
}

# Function to check if Python is available
function Test-PythonAvailable {
    try {
        $pythonVersion = python --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            return $true
        }
    }
    catch {
        try {
            $pythonVersion = py --version 2>$null
            if ($LASTEXITCODE -eq 0) {
                return $true
            }
        }
        catch {
            return $false
        }
    }
    return $false
}

# Function to run a single test file
function Invoke-SingleTest {
    param([string]$TestPath, [string]$TestName)
    
    Write-Host "🧪 Running $TestName..." -ForegroundColor Yellow
    
    try {
        & python $TestPath
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ $TestName passed" -ForegroundColor Green
            return $true
        }
        else {
            Write-Host "❌ $TestName failed (exit code: $LASTEXITCODE)" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "❌ Error running $TestName : $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Function to run all tests using the test runner
function Invoke-AllTests {
    Write-Host "🧪 Running all tests using test runner..." -ForegroundColor Yellow
    
    try {
        & python run_tests.py
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ All tests completed successfully" -ForegroundColor Green
            return $true
        }
        else {
            Write-Host "❌ Some tests failed (exit code: $LASTEXITCODE)" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "❌ Error running tests: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Function to run tests with coverage
function Invoke-TestsWithCoverage {
    Write-Host "📊 Running tests with coverage..." -ForegroundColor Yellow
    
    # Check if coverage is installed
    try {
        & python -c "import coverage" 2>$null
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Coverage.py is not installed" -ForegroundColor Red
            Write-Host "Install with: pip install coverage" -ForegroundColor Yellow
            return $false
        }
    }
    catch {
        Write-Host "❌ Error checking coverage installation" -ForegroundColor Red
        return $false
    }
    
    try {
        # Run tests with coverage
        & python -m coverage run --source=. run_tests.py
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "📈 Generating coverage report..." -ForegroundColor Cyan
            & python -m coverage report
            & python -m coverage html
            Write-Host "✅ Coverage report generated in htmlcov/" -ForegroundColor Green
            return $true
        }
        else {
            Write-Host "❌ Coverage tests failed" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "❌ Error running coverage: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Main execution
Write-Host "Simple Rogue-like Game Test Runner" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan

# Check if we're in the correct directory
if (-not (Test-Path "tests")) {
    Write-Host "❌ Error: tests directory not found" -ForegroundColor Red
    Write-Host "Please run this script from the game's root directory" -ForegroundColor Yellow
    exit 1
}

# Check Python availability
if (-not (Test-PythonAvailable)) {
    Write-Host "❌ Error: Python is not available" -ForegroundColor Red
    Write-Host "Please ensure Python is installed and added to your PATH" -ForegroundColor Yellow
    exit 1
}

if ($Verbose) {
    $pythonVersion = python --version
    Write-Host "✅ Python is available: $pythonVersion" -ForegroundColor Green
    Write-Host "📁 Current directory: $($PWD.Path)" -ForegroundColor Gray
}

# Set up environment
$env:PYTHONPATH = $PWD.Path

# Define test files
$testFiles = @(
    @{Path = "tests/test_progression.py"; Name = "Progression System Tests"},
    @{Path = "tests/test_skill_tree.py"; Name = "Skill Tree Tests"},
    @{Path = "tests/test_equipment.py"; Name = "Equipment System Tests"},
    @{Path = "tests/test_player.py"; Name = "Player Tests"}
)

$allPassed = $true

# Handle specific test file
if ($TestFile) {
    $targetTest = $testFiles | Where-Object { $_.Path -like "*$TestFile*" }
    if ($targetTest) {
        $result = Invoke-SingleTest -TestPath $targetTest.Path -TestName $targetTest.Name
        if (-not $result) { $allPassed = $false }
    }
    else {
        Write-Host "❌ Test file '$TestFile' not found" -ForegroundColor Red
        Write-Host "Available tests:" -ForegroundColor Yellow
        foreach ($test in $testFiles) {
            Write-Host "  - $($test.Name) ($($test.Path))" -ForegroundColor White
        }
        exit 1
    }
}
# Handle coverage tests
elseif ($Coverage) {
    $result = Invoke-TestsWithCoverage
    if (-not $result) { $allPassed = $false }
}
# Handle individual test execution
elseif ($Individual) {
    Write-Host "🔄 Running tests individually..." -ForegroundColor Cyan
    
    foreach ($test in $testFiles) {
        if (Test-Path $test.Path) {
            $result = Invoke-SingleTest -TestPath $test.Path -TestName $test.Name
            if (-not $result) { $allPassed = $false }
            Write-Host "" # Add spacing between tests
        }
        else {
            Write-Host "⚠️  Test file not found: $($test.Path)" -ForegroundColor Yellow
        }
    }
}
# Handle all tests using test runner
else {
    $result = Invoke-AllTests
    if (-not $result) { $allPassed = $false }
}

# Final summary
Write-Host ""
Write-Host "=" * 50 -ForegroundColor Gray
if ($allPassed) {
    Write-Host "🎉 All tests completed successfully!" -ForegroundColor Green
    exit 0
}
else {
    Write-Host "💥 Some tests failed!" -ForegroundColor Red
    exit 1
}
