# Development utilities for the Simple Rogue-like Game
# This script provides common development tasks with proper PowerShell syntax

param(
    [Parameter(Position=0)]
    [ValidateSet("setup", "clean", "install", "check", "format", "lint", "assets", "help")]
    [string]$Command = "help",
    
    [switch]$Verbose,
    [switch]$Force
)

# Display help information
function Show-Help {
    Write-Host "Simple Rogue-like Game Development Utilities" -ForegroundColor Cyan
    Write-Host "============================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage: .\dev_utils.ps1 <command> [options]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Commands:" -ForegroundColor Green
    Write-Host "  setup    : Set up development environment" -ForegroundColor White
    Write-Host "  clean    : Clean up cache files and temporary data" -ForegroundColor White
    Write-Host "  install  : Install required dependencies" -ForegroundColor White
    Write-Host "  check    : Check system requirements and dependencies" -ForegroundColor White
    Write-Host "  format   : Format Python code (requires black)" -ForegroundColor White
    Write-Host "  lint     : Run code linting (requires flake8)" -ForegroundColor White
    Write-Host "  assets   : Generate missing game assets" -ForegroundColor White
    Write-Host "  help     : Show this help message" -ForegroundColor White
    Write-Host ""
    Write-Host "Options:" -ForegroundColor Green
    Write-Host "  -Verbose : Show detailed output" -ForegroundColor White
    Write-Host "  -Force   : Force operations (skip confirmations)" -ForegroundColor White
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Green
    Write-Host "  .\dev_utils.ps1 setup           # Set up development environment" -ForegroundColor White
    Write-Host "  .\dev_utils.ps1 clean -Force    # Clean without confirmation" -ForegroundColor White
    Write-Host "  .\dev_utils.ps1 check -Verbose  # Check with detailed output" -ForegroundColor White
}

# Function to check if Python is available
function Test-PythonAvailable {
    try {
        $null = python --version 2>$null
        return ($LASTEXITCODE -eq 0)
    }
    catch {
        return $false
    }
}

# Setup development environment
function Invoke-Setup {
    Write-Host "🔧 Setting up development environment..." -ForegroundColor Cyan
    
    if (-not (Test-PythonAvailable)) {
        Write-Host "❌ Python is not available" -ForegroundColor Red
        return $false
    }
    
    # Install dependencies
    Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
    & python -m pip install --upgrade pip
    & python -m pip install pygame
    
    # Install optional development tools
    if ($Verbose) {
        Write-Host "🛠️  Installing development tools..." -ForegroundColor Yellow
        & python -m pip install black flake8 coverage pytest
    }
    
    Write-Host "✅ Development environment setup complete!" -ForegroundColor Green
    return $true
}

# Clean up cache and temporary files
function Invoke-Clean {
    Write-Host "🧹 Cleaning up cache and temporary files..." -ForegroundColor Cyan
    
    $itemsToClean = @(
        "__pycache__",
        "*.pyc",
        "*.pyo",
        "*.pyd",
        ".coverage",
        "htmlcov",
        "*.egg-info",
        "build",
        "dist"
    )
    
    if (-not $Force) {
        $response = Read-Host "This will delete cache files and temporary data. Continue? (y/N)"
        if ($response -ne "y" -and $response -ne "Y") {
            Write-Host "❌ Operation cancelled" -ForegroundColor Yellow
            return $false
        }
    }
    
    foreach ($pattern in $itemsToClean) {
        $items = Get-ChildItem -Path . -Name $pattern -Recurse -Force -ErrorAction SilentlyContinue
        foreach ($item in $items) {
            if ($Verbose) {
                Write-Host "🗑️  Removing: $item" -ForegroundColor Gray
            }
            Remove-Item -Path $item -Recurse -Force -ErrorAction SilentlyContinue
        }
    }
    
    Write-Host "✅ Cleanup complete!" -ForegroundColor Green
    return $true
}

# Install dependencies
function Invoke-Install {
    Write-Host "📦 Installing dependencies..." -ForegroundColor Cyan
    
    if (-not (Test-PythonAvailable)) {
        Write-Host "❌ Python is not available" -ForegroundColor Red
        return $false
    }
    
    if (Test-Path "requirements.txt") {
        & python -m pip install -r requirements.txt
    }
    else {
        & python -m pip install pygame
    }
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Dependencies installed successfully!" -ForegroundColor Green
        return $true
    }
    else {
        Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
        return $false
    }
}

# Check system requirements
function Invoke-Check {
    Write-Host "🔍 Checking system requirements..." -ForegroundColor Cyan
    
    $allGood = $true
    
    # Check Python
    if (Test-PythonAvailable) {
        $pythonVersion = python --version
        Write-Host "✅ Python: $pythonVersion" -ForegroundColor Green
    }
    else {
        Write-Host "❌ Python: Not available" -ForegroundColor Red
        $allGood = $false
    }
    
    # Check Pygame
    try {
        $pygameVersion = python -c "import pygame; print(f'Pygame {pygame.version.ver}')" 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ $pygameVersion" -ForegroundColor Green
        }
        else {
            Write-Host "❌ Pygame: Not installed" -ForegroundColor Red
            $allGood = $false
        }
    }
    catch {
        Write-Host "❌ Pygame: Error checking" -ForegroundColor Red
        $allGood = $false
    }
    
    # Check game files
    $requiredFiles = @("main.py", "game.py", "entities", "level", "ui", "utils", "progression")
    foreach ($file in $requiredFiles) {
        if (Test-Path $file) {
            if ($Verbose) {
                Write-Host "✅ Found: $file" -ForegroundColor Green
            }
        }
        else {
            Write-Host "❌ Missing: $file" -ForegroundColor Red
            $allGood = $false
        }
    }
    
    if ($allGood) {
        Write-Host "🎉 All checks passed!" -ForegroundColor Green
    }
    else {
        Write-Host "⚠️  Some checks failed" -ForegroundColor Yellow
    }
    
    return $allGood
}

# Format code
function Invoke-Format {
    Write-Host "🎨 Formatting Python code..." -ForegroundColor Cyan
    
    try {
        & python -c "import black" 2>$null
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Black is not installed" -ForegroundColor Red
            Write-Host "Install with: pip install black" -ForegroundColor Yellow
            return $false
        }
    }
    catch {
        Write-Host "❌ Error checking black installation" -ForegroundColor Red
        return $false
    }
    
    & python -m black . --line-length 100
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Code formatting complete!" -ForegroundColor Green
        return $true
    }
    else {
        Write-Host "❌ Code formatting failed" -ForegroundColor Red
        return $false
    }
}

# Run linting
function Invoke-Lint {
    Write-Host "🔍 Running code linting..." -ForegroundColor Cyan
    
    try {
        & python -c "import flake8" 2>$null
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Flake8 is not installed" -ForegroundColor Red
            Write-Host "Install with: pip install flake8" -ForegroundColor Yellow
            return $false
        }
    }
    catch {
        Write-Host "❌ Error checking flake8 installation" -ForegroundColor Red
        return $false
    }
    
    & python -m flake8 . --max-line-length=100 --ignore=E203,W503
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Linting complete - no issues found!" -ForegroundColor Green
        return $true
    }
    else {
        Write-Host "⚠️  Linting found issues (see output above)" -ForegroundColor Yellow
        return $false
    }
}

# Generate assets
function Invoke-Assets {
    Write-Host "🎨 Generating game assets..." -ForegroundColor Cyan
    
    if (Test-Path "generate_assets.py") {
        & python generate_assets.py
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Assets generated successfully!" -ForegroundColor Green
            return $true
        }
        else {
            Write-Host "❌ Asset generation failed" -ForegroundColor Red
            return $false
        }
    }
    else {
        Write-Host "❌ generate_assets.py not found" -ForegroundColor Red
        return $false
    }
}

# Main execution
switch ($Command.ToLower()) {
    "setup" { Invoke-Setup }
    "clean" { Invoke-Clean }
    "install" { Invoke-Install }
    "check" { Invoke-Check }
    "format" { Invoke-Format }
    "lint" { Invoke-Lint }
    "assets" { Invoke-Assets }
    "help" { Show-Help }
    default { 
        Write-Host "❌ Unknown command: $Command" -ForegroundColor Red
        Show-Help
        exit 1
    }
}
