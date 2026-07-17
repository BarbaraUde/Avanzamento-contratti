@echo off
cd /d "%~dp0"
echo Avvio Avanzamento Contratti...

if not exist venv (
    echo Creazione ambiente virtuale...
    py -m venv venv
)

call venv\Scripts\activate.bat
py -m pip install -r requirements.txt -q

echo.
echo App disponibile su http://localhost:5000
echo Premi CTRL+C per fermare il server.
echo.
py app.py
pause
