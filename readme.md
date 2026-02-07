## ENV Variables
export JWT_SECRET='sXlEdRsYxjJt1p6t9LCiB4/rfPiWVAYL7ckS0ckkDPo=' <-- Exchange with your own secret
export DEFAULT_ADMIN_PASSWORD='your-admin-password'

**for making them persistent add them to ~/.bashrc**

### Script to generate a JWT secret:
$bytes = New-Object byte[] 32; [System.Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($bytes); [Convert]::ToBase64String($bytes)

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
