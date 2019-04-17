
@echo off

@echo Starting strends program...

@echo.



cd /d "%~dp0"

python main.py "%*"



@echo.

@echo Press any key to close...

@echo off

pause > nul

exit /b