# Script to start both backend and frontend for development
Write-Host "Starting Document Expiry Reminder services..." -ForegroundColor Green

# Start Backend
Write-Host "Starting Backend on port 8000..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; .\venv\Scripts\activate; uvicorn app.main:app --reload --port 8000"

# Start Frontend
Write-Host "Starting Frontend on port 5173..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

Write-Host "Both services started in new windows!" -ForegroundColor Green
Write-Host "Backend API docs: http://localhost:8000/docs"
Write-Host "Frontend App: http://localhost:5173"
