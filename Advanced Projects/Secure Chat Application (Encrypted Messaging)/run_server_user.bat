@echo off
REM Wrapper to run the secure chat server in the user's session at logon.
REM Place this file in the same directory as server.py and the .venv folder.

REM Change to the script directory (handles spaces in path)
cd /d "%~dp0"

REM Resolve absolute paths to avoid quoting/parsing issues in Scheduled Task
set "SCRIPT_DIR=%~dp0"
REM Candidate venv locations (script dir, parent, repo root)
set "VENV_CAND_1=%SCRIPT_DIR%\.venv\Scripts\python.exe"
set "VENV_CAND_2=%SCRIPT_DIR%..\..\.venv\Scripts\python.exe"
set "VENV_CAND_3=%SCRIPT_DIR%..\.venv\Scripts\python.exe"

set "SERVER_PY=%SCRIPT_DIR%server.py"
set "LOG_FILE=%SCRIPT_DIR%server_user.log"
+
REM Pick the first existing venv python, otherwise fall back to system python on PATH
if exist "%VENV_CAND_1%" (
	set "PY_EXEC=%VENV_CAND_1%"
) else if exist "%VENV_CAND_2%" (
	set "PY_EXEC=%VENV_CAND_2%"
) else if exist "%VENV_CAND_3%" (
	set "PY_EXEC=%VENV_CAND_3%"
) else (
	set "PY_EXEC=python"
)

REM Start the server and append stdout/stderr to log. Use start /B so the task can exit while leaving the server running.
start "SecureChatServerUser" /B "%PY_EXEC%" "%SERVER_PY%" --auto >> "%LOG_FILE%" 2>&1

exit
