# PowerShell script to run the Simple Rogue-like Game
# This script ensures proper execution without PowerShell syntax errors
# Encoding: UTF-8 without BOM

param(
    [switch]$Debug,
    [switch]$Verbose,
    [switch]$Help
)

# Display help information
if ($Help) {
    Write-Host "Simple Rogue-like Game Launcher" -ForegroundColor Cyan
    Write-Host "================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage: .\run_game.ps1 [options]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Options:" -ForegroundColor Green
    Write-Host "  -Debug    : Run with debug output" -ForegroundColor White
    Write-Host "  -Verbose  : Show detailed execution information" -ForegroundColor White
    Write-Host "  -Help     : Show this help message" -ForegroundColor White
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Green
    Write-Host "  .\run_game.ps1           # Run the game normally" -ForegroundColor White
    Write-Host "  .\run_game.ps1 -Debug    # Run with debug output" -ForegroundColor White
    Write-Host "  .\run_game.ps1 -Verbose  # Run with verbose output" -ForegroundColor White
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
        # Try alternative python commands
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

# Function to check if required dependencies are installed
function Test-Dependencies {
    if ($Verbose) {
        Write-Host "Checking dependencies..." -ForegroundColor Yellow
    }

    try {
        $result = python -c "import pygame; print('Pygame version:', pygame.version.ver)" 2>$null
        if ($LASTEXITCODE -eq 0) {
            if ($Verbose) {
                Write-Host "✅ Pygame is installed: $result" -ForegroundColor Green
            }
            return $true
        }
        else {
            Write-Host "❌ Pygame is not installed" -ForegroundColor Red
            Write-Host "Please install pygame: pip install pygame" -ForegroundColor Yellow
            return $false
        }
    }
    catch {
        Write-Host "❌ Error checking dependencies" -ForegroundColor Red
        return $false
    }
}

# Main execution
Write-Host "Simple Rogue-like Game Launcher" -ForegroundColor Cyan
Write-Host "===============================" -ForegroundColor Cyan

# Check if we're in the correct directory
if (-not (Test-Path "main.py")) {
    Write-Host "❌ Error: main.py not found in current directory" -ForegroundColor Red
    Write-Host "Please run this script from the game's root directory" -ForegroundColor Yellow
    exit 1
}

# Check Python availability
if (-not (Test-PythonAvailable)) {
    Write-Host "❌ Error: Python is not available" -ForegroundColor Red
    Write-Host "Please ensure Python is installed and added to your PATH" -ForegroundColor Yellow
    Write-Host "You can download Python from: https://python.org" -ForegroundColor Cyan
    exit 1
}

if ($Verbose) {
    $pythonVersion = python --version
    Write-Host "✅ Python is available: $pythonVersion" -ForegroundColor Green
}

# Check dependencies
if (-not (Test-Dependencies)) {
    Write-Host "❌ Dependencies check failed" -ForegroundColor Red
    exit 1
}

# Set up environment
if ($Debug) {
    $env:PYTHONPATH = $PWD.Path
    Write-Host "🐛 Debug mode enabled" -ForegroundColor Magenta
    Write-Host "PYTHONPATH set to: $($env:PYTHONPATH)" -ForegroundColor Gray
}

if ($Verbose) {
    Write-Host "📁 Current directory: $($PWD.Path)" -ForegroundColor Gray
    Write-Host "🎮 Starting the game..." -ForegroundColor Yellow
}

# Launch the game
try {
    if ($Debug) {
        Write-Host "🚀 Executing: python main.py" -ForegroundColor Gray
    }

    # Use proper PowerShell syntax to run Python
    & python main.py

    if ($LASTEXITCODE -eq 0) {
        if ($Verbose) {
            Write-Host "✅ Game exited successfully" -ForegroundColor Green
        }
    }
    else {
        Write-Host "⚠️  Game exited with code: $LASTEXITCODE" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "❌ Error running the game: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

if ($Verbose) {
    Write-Host "Game launcher finished" -ForegroundColor Cyan
}
