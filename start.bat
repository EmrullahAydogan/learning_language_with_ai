@echo off
REM ============================================================================
REM AI Language Learning Platform - Windows Startup Script
REM ============================================================================
REM This script checks prerequisites and starts the application
REM Usage: start.bat or double-click start.bat
REM ============================================================================

setlocal enabledelayedexpansion

REM Print banner
echo.
echo =========================================================
echo.
echo    AI Language Learning Platform
echo.
echo    Starting your language learning journey...
echo.
echo =========================================================
echo.

REM Check if Docker is installed
echo [INFO] Checking Docker installation...
where docker >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not installed!
    echo [INFO] Please install Docker Desktop from: https://docs.docker.com/desktop/install/windows-install/
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('docker --version') do set DOCKER_VERSION=%%i
echo [SUCCESS] Docker is installed ^(!DOCKER_VERSION!^)

REM Check if Docker Compose is available
echo [INFO] Checking Docker Compose installation...
docker compose version >nul 2>nul
if %errorlevel% neq 0 (
    docker-compose --version >nul 2>nul
    if %errorlevel% neq 0 (
        echo [ERROR] Docker Compose is not installed!
        echo [INFO] Please install Docker Compose or use Docker Desktop which includes it
        pause
        exit /b 1
    )
    set DOCKER_COMPOSE_CMD=docker-compose
    for /f "tokens=*" %%i in ('docker-compose --version') do set COMPOSE_VERSION=%%i
) else (
    set DOCKER_COMPOSE_CMD=docker compose
    for /f "tokens=*" %%i in ('docker compose version') do set COMPOSE_VERSION=%%i
)
echo [SUCCESS] Docker Compose is installed ^(!COMPOSE_VERSION!^)

REM Check if Docker Desktop is running
echo [INFO] Checking if Docker is running...
docker info >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not running!
    echo [INFO] Please start Docker Desktop and try again
    pause
    exit /b 1
)
echo [SUCCESS] Docker is running

REM Check if .env file exists
echo [INFO] Checking environment configuration...
if not exist ".env" (
    echo [WARNING] .env file not found. Creating from .env.example...
    if exist ".env.example" (
        copy .env.example .env >nul
        echo [SUCCESS] .env file created!
        echo [WARNING] Please edit .env file and add your OPENAI_API_KEY for AI features
        echo [INFO] You can continue without it, but AI features will be disabled
        echo.
        set /p EDIT_ENV="Do you want to edit .env file now? (y/N): "
        if /i "!EDIT_ENV!"=="y" (
            notepad .env
        )
    ) else (
        echo [ERROR] .env.example file not found!
        pause
        exit /b 1
    )
) else (
    echo [SUCCESS] .env file found
)

REM Check if ports are available
echo [INFO] Checking if required ports are available...
set PORTS_IN_USE=

REM Check port 3000 (Frontend)
netstat -an | find ":3000" | find "LISTENING" >nul 2>nul
if %errorlevel% equ 0 (
    set PORTS_IN_USE=!PORTS_IN_USE! 3000
)

REM Check port 8000 (Backend)
netstat -an | find ":8000" | find "LISTENING" >nul 2>nul
if %errorlevel% equ 0 (
    set PORTS_IN_USE=!PORTS_IN_USE! 8000
)

REM Check port 5432 (PostgreSQL)
netstat -an | find ":5432" | find "LISTENING" >nul 2>nul
if %errorlevel% equ 0 (
    set PORTS_IN_USE=!PORTS_IN_USE! 5432
)

REM Check port 6379 (Redis)
netstat -an | find ":6379" | find "LISTENING" >nul 2>nul
if %errorlevel% equ 0 (
    set PORTS_IN_USE=!PORTS_IN_USE! 6379
)

if not "!PORTS_IN_USE!"=="" (
    echo [WARNING] The following ports are already in use:!PORTS_IN_USE!
    echo [INFO] Please stop the services using these ports or change the ports in docker-compose.yml
    echo.
    set /p CONTINUE="Do you want to continue anyway? (y/N): "
    if /i not "!CONTINUE!"=="y" (
        echo [INFO] Startup cancelled
        pause
        exit /b 0
    )
) else (
    echo [SUCCESS] All required ports are available
)

REM Start the application
echo.
echo [INFO] Starting the application...
echo.
echo This will:
echo   - Build Docker images ^(first time may take 5-10 minutes^)
echo   - Start PostgreSQL database
echo   - Start Redis cache
echo   - Start FastAPI backend
echo   - Start Next.js frontend
echo   - Run database migrations
echo   - Seed database with 400+ words
echo.
set /p START="Continue? (Y/n): "
if /i "!START!"=="n" (
    echo [INFO] Startup cancelled
    pause
    exit /b 0
)

echo.
echo [INFO] Starting services with Docker Compose...
echo.

REM Build and start
%DOCKER_COMPOSE_CMD% up --build -d

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to start services!
    echo [INFO] Check the error messages above for details
    pause
    exit /b 1
)

echo.
echo [SUCCESS] All services started successfully!

REM Wait for services to be ready
echo.
echo [INFO] Waiting for services to be ready...
echo.

REM Wait for backend (max 120 seconds)
echo [INFO] Waiting for backend API...
set BACKEND_READY=0
for /l %%i in (1,1,60) do (
    curl -s http://localhost:8000/health >nul 2>nul
    if !errorlevel! equ 0 (
        set BACKEND_READY=1
        goto :backend_ready
    )
    curl -s http://localhost:8000/ >nul 2>nul
    if !errorlevel! equ 0 (
        set BACKEND_READY=1
        goto :backend_ready
    )
    echo | set /p=.
    timeout /t 2 /nobreak >nul
)
:backend_ready

if !BACKEND_READY! equ 1 (
    echo.
    echo [SUCCESS] Backend is ready!
) else (
    echo.
    echo [WARNING] Backend didn't start in time, but it might still be starting
    echo [INFO] Check logs with: %DOCKER_COMPOSE_CMD% logs backend
)

REM Wait for frontend (max 120 seconds)
echo.
echo [INFO] Waiting for frontend...
set FRONTEND_READY=0
for /l %%i in (1,1,60) do (
    curl -s http://localhost:3000 >nul 2>nul
    if !errorlevel! equ 0 (
        set FRONTEND_READY=1
        goto :frontend_ready
    )
    echo | set /p=.
    timeout /t 2 /nobreak >nul
)
:frontend_ready

if !FRONTEND_READY! equ 1 (
    echo.
    echo [SUCCESS] Frontend is ready!
) else (
    echo.
    echo [WARNING] Frontend didn't start in time, but it might still be starting
    echo [INFO] Check logs with: %DOCKER_COMPOSE_CMD% logs frontend-web
)

REM Show access information
echo.
echo =========================================================
echo.
echo    Application is ready!
echo.
echo =========================================================
echo.
echo Access the application:
echo.
echo   Frontend ^(Web App^):     http://localhost:3000
echo   Backend API:            http://localhost:8000
echo   API Documentation:      http://localhost:8000/docs
echo   Alternative Docs:       http://localhost:8000/redoc
echo.
echo Monitor services:
echo.
echo   View logs:     %DOCKER_COMPOSE_CMD% logs -f
echo   View backend:  %DOCKER_COMPOSE_CMD% logs -f backend
echo   View frontend: %DOCKER_COMPOSE_CMD% logs -f frontend-web
echo.
echo Stop services:
echo.
echo   %DOCKER_COMPOSE_CMD% down
echo.
echo Next steps:
echo.
echo   1. Open http://localhost:3000 in your browser
echo   2. Create an account
echo   3. Take the level assessment quiz
echo   4. Start learning!
echo.
echo [WARNING] Note: If you haven't added OPENAI_API_KEY to .env,
echo           AI features ^(chat, writing evaluation^) will be disabled
echo.
echo [SUCCESS] Happy learning!
echo.
pause
