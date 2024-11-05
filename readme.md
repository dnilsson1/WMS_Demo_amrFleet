## Backend

### Activate .venv

##### Windows

cmd: .venv\Scripts\activate
PowerShell: .venv\Scripts\Activate.ps1

##### Linux

source .venv/bin/activate

##### Run the app

uvicorn main:app --reload --port 8000
