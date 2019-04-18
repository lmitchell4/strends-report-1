
@echo off

@echo Starting strends program...

@echo.


cd /d "%~dp0"

call conda activate strends

python main.py "%*"

call conda deactivate

@echo.

@echo Press any key to close...

@echo off

pause > nul

exit /b