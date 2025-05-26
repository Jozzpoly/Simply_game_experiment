# Simple PowerShell script to run the Rogue-like Game
# This script avoids Unicode characters and complex syntax

param(
    [switch]$Help,
    [switch]$Verbose
)

if ($Help) {
    Write-Host "Simple Rogue-like Game Launcher" -ForegroundColor Cyan
    Write-Host "Usage: .\run_game_simple.ps1 [-Verbose] [-Help]"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Verbose  : Show detailed output"
    Write-Host "  -Help     : Show this help"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\run_game_simple.ps1           # Run the game"
    Write-Host "  .\run_game_simple.ps1 -Verbose  # Run with details"
    exit 0
}

Write-Host "Simple Rogue-like Game Launcher" -ForegroundColor Cyan
Write-Host "==============================="

# Check if main.py exists
if (-not (Test-Path "main.py")) {
    Write-Host "[ERROR] main.py not found in current directory" -ForegroundColor Red
    Write-Host "Please run this script from the game's root directory" -ForegroundColor Yellow
    exit 1
}

# Check Python
try {
    $null = python --version 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Python is not available" -ForegroundColor Red
        Write-Host "Please ensure Python is installed and in your PATH" -ForegroundColor Yellow
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

# Check Pygame
try {
    $null = python -c "import pygame" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Pygame is not installed" -ForegroundColor Red
        Write-Host "Install with: pip install pygame" -ForegroundColor Yellow
        exit 1
    }
    
    if ($Verbose) {
        Write-Host "[OK] Pygame is available" -ForegroundColor Green
    }
}
catch {
    Write-Host "[ERROR] Cannot check Pygame: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Run the game
if ($Verbose) {
    Write-Host "[INFO] Starting the game..." -ForegroundColor Yellow
}

try {
    & python main.py
    
    if ($Verbose) {
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] Game exited successfully" -ForegroundColor Green
        } else {
            Write-Host "[WARNING] Game exited with code: $LASTEXITCODE" -ForegroundColor Yellow
        }
    }
}
catch {
    Write-Host "[ERROR] Failed to run game: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

if ($Verbose) {
    Write-Host "[INFO] Game launcher finished" -ForegroundColor Cyan
}
