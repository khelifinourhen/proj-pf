# ============================================================
# Build script for ESP32 Wokwi project (Arduino CLI)
# Run this from PowerShell inside the wokwi-vscode folder
# ============================================================

$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

$SKETCH = "$PSScriptRoot\sketch.ino"
$BUILD_DIR = "$PSScriptRoot\build"
$FQBN = "esp32:esp32:esp32"

Write-Host "=== Wokwi ESP32 Build Script ===" -ForegroundColor Cyan

# Step 1: Install required libraries
Write-Host "`n[1/3] Installing libraries..." -ForegroundColor Yellow
$libs = @(
    "DHT sensor library",
    "Adafruit Unified Sensor",
    "Adafruit BMP085 Library",
    "Adafruit MPU6050",
    "Adafruit BusIO",
    "LiquidCrystal I2C",
    "PubSubClient",
    "ArduinoJson"
)
foreach ($lib in $libs) {
    Write-Host "  Installing: $lib"
    arduino-cli lib install "$lib" 2>&1 | Select-Object -Last 2
}

# Step 2: Create build directory
New-Item -ItemType Directory -Force -Path $BUILD_DIR | Out-Null

# Step 3: Compile
Write-Host "`n[2/3] Compiling sketch..." -ForegroundColor Yellow
arduino-cli compile `
    --fqbn $FQBN `
    --build-path $BUILD_DIR `
    --warnings default `
    $SKETCH 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n[3/3] Build SUCCESSFUL!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Firmware files:" -ForegroundColor Cyan
    Get-ChildItem $BUILD_DIR -Filter "*.bin" | ForEach-Object { Write-Host "  BIN: $($_.FullName)" }
    Get-ChildItem $BUILD_DIR -Filter "*.elf" | ForEach-Object { Write-Host "  ELF: $($_.FullName)" }
    Write-Host ""
    Write-Host "Next: Open VS Code in this folder and press F1 -> 'Wokwi: Start Simulator'" -ForegroundColor Green
} else {
    Write-Host "`n[3/3] Build FAILED. See errors above." -ForegroundColor Red
    exit 1
}
