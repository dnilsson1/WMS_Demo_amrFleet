## Backend

### Activate .venv

##### Windows

cmd: .venv\Scripts\activate
PowerShell: .venv\Scripts\Activate.ps1

##### Linux

source .venv/bin/activate

##### Run the app

cd wms-demo/backend

uvicorn main:app --reload --port 8000

Alternatively: python3 -m uvicorn main:app --reload --port 8000
