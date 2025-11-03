@echo off
setlocal

REM Change to the script directory
cd /d "%~dp0"

REM Set up python executable path
set "PY_EXEC=.venv\Scripts\python.exe"
if not exist "%PY_EXEC%" (
    set "PY_EXEC=..\..\.venv\Scripts\python.exe"
)
if not exist "%PY_EXEC%" (
    set "PY_EXEC=python"
)

REM Start the server in the background
echo "Starting server..."
start "SecureChatServer" /B "%PY_EXEC%" server.py --auto

REM Wait for the server to start
echo "Waiting for server to initialize..."
timeout /t 3 /nobreak >nul

REM Run the client
echo "Starting client..."
"%PY_EXEC%" client.py --auto

endlocal