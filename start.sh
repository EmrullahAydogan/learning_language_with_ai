#!/bin/bash

# ============================================================================
# AI Language Learning Platform - Startup Script
# ============================================================================
# This script checks prerequisites and starts the application
# Usage: ./start.sh or bash start.sh
# ============================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print banner
echo -e "${BLUE}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   🌍 AI Language Learning Platform                       ║
║                                                           ║
║   Starting your language learning journey...             ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Function to print colored messages
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if Docker is installed
check_docker() {
    print_info "Checking Docker installation..."
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed!"
        print_info "Please install Docker from: https://docs.docker.com/get-docker/"
        exit 1
    fi
    print_success "Docker is installed ($(docker --version))"
}

# Check if Docker Compose is installed
check_docker_compose() {
    print_info "Checking Docker Compose installation..."
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        print_error "Docker Compose is not installed!"
        print_info "Please install Docker Compose from: https://docs.docker.com/compose/install/"
        exit 1
    fi

    # Determine which command to use
    if command -v docker-compose &> /dev/null; then
        DOCKER_COMPOSE_CMD="docker-compose"
        print_success "Docker Compose is installed ($(docker-compose --version))"
    else
        DOCKER_COMPOSE_CMD="docker compose"
        print_success "Docker Compose is installed ($(docker compose version))"
    fi
}

# Check if .env file exists
check_env_file() {
    print_info "Checking environment configuration..."
    if [ ! -f ".env" ]; then
        print_warning ".env file not found. Creating from .env.example..."
        if [ -f ".env.example" ]; then
            cp .env.example .env
            print_success ".env file created!"
            print_warning "Please edit .env file and add your OPENAI_API_KEY for AI features"
            print_info "You can continue without it, but AI features will be disabled"
            echo ""
            read -p "Do you want to edit .env file now? (y/N) " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                ${EDITOR:-nano} .env
            fi
        else
            print_error ".env.example file not found!"
            exit 1
        fi
    else
        print_success ".env file found"
    fi
}

# Check if ports are available
check_ports() {
    print_info "Checking if required ports are available..."

    PORTS=(3000 8000 5432 6379)
    PORTS_IN_USE=()

    for port in "${PORTS[@]}"; do
        if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1 || netstat -an | grep -q ":$port.*LISTEN" 2>/dev/null; then
            PORTS_IN_USE+=($port)
        fi
    done

    if [ ${#PORTS_IN_USE[@]} -gt 0 ]; then
        print_warning "The following ports are already in use: ${PORTS_IN_USE[*]}"
        print_info "Please stop the services using these ports or change the ports in docker-compose.yml"
        echo ""
        read -p "Do you want to continue anyway? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "Startup cancelled"
            exit 0
        fi
    else
        print_success "All required ports are available"
    fi
}

# Start the application
start_app() {
    print_info "Starting the application..."
    echo ""

    print_info "This will:"
    echo "  📦 Build Docker images (first time may take 5-10 minutes)"
    echo "  🗄️  Start PostgreSQL database"
    echo "  💾 Start Redis cache"
    echo "  🐍 Start FastAPI backend"
    echo "  ⚛️  Start Next.js frontend"
    echo "  📊 Run database migrations"
    echo "  🌱 Seed database with 400+ words"
    echo ""

    read -p "Continue? (Y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Nn]$ ]]; then
        print_info "Startup cancelled"
        exit 0
    fi

    echo ""
    print_info "Starting services with Docker Compose..."
    echo ""

    # Build and start
    $DOCKER_COMPOSE_CMD up --build -d

    echo ""
    print_success "All services started successfully!"
}

# Show access information
show_access_info() {
    echo ""
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                                           ║${NC}"
    echo -e "${GREEN}║   🎉 Application is ready!                                ║${NC}"
    echo -e "${GREEN}║                                                           ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BLUE}📱 Access the application:${NC}"
    echo ""
    echo -e "  ${GREEN}Frontend (Web App):${NC}     http://localhost:3000"
    echo -e "  ${GREEN}Backend API:${NC}            http://localhost:8000"
    echo -e "  ${GREEN}API Documentation:${NC}     http://localhost:8000/docs"
    echo -e "  ${GREEN}Alternative Docs:${NC}      http://localhost:8000/redoc"
    echo ""
    echo -e "${BLUE}📊 Monitor services:${NC}"
    echo ""
    echo -e "  View logs:     ${YELLOW}$DOCKER_COMPOSE_CMD logs -f${NC}"
    echo -e "  View backend:  ${YELLOW}$DOCKER_COMPOSE_CMD logs -f backend${NC}"
    echo -e "  View frontend: ${YELLOW}$DOCKER_COMPOSE_CMD logs -f frontend-web${NC}"
    echo ""
    echo -e "${BLUE}🛑 Stop services:${NC}"
    echo ""
    echo -e "  ${YELLOW}$DOCKER_COMPOSE_CMD down${NC}"
    echo ""
    echo -e "${BLUE}📝 Next steps:${NC}"
    echo ""
    echo "  1. Open http://localhost:3000 in your browser"
    echo "  2. Create an account"
    echo "  3. Take the level assessment quiz"
    echo "  4. Start learning!"
    echo ""
    echo -e "${YELLOW}⚠️  Note: If you haven't added OPENAI_API_KEY to .env,${NC}"
    echo -e "${YELLOW}   AI features (chat, writing evaluation) will be disabled${NC}"
    echo ""
    print_success "Happy learning! 🚀"
    echo ""
}

# Wait for services to be ready
wait_for_services() {
    print_info "Waiting for services to be ready..."
    echo ""

    # Wait for backend
    print_info "Waiting for backend API..."
    max_attempts=60
    attempt=0
    while [ $attempt -lt $max_attempts ]; do
        if curl -s http://localhost:8000/health > /dev/null 2>&1 || curl -s http://localhost:8000/ > /dev/null 2>&1; then
            print_success "Backend is ready!"
            break
        fi
        attempt=$((attempt + 1))
        echo -n "."
        sleep 2
    done

    if [ $attempt -eq $max_attempts ]; then
        print_warning "Backend didn't start in time, but it might still be starting"
        print_info "Check logs with: $DOCKER_COMPOSE_CMD logs backend"
    fi

    echo ""

    # Wait for frontend
    print_info "Waiting for frontend..."
    attempt=0
    while [ $attempt -lt $max_attempts ]; do
        if curl -s http://localhost:3000 > /dev/null 2>&1; then
            print_success "Frontend is ready!"
            break
        fi
        attempt=$((attempt + 1))
        echo -n "."
        sleep 2
    done

    if [ $attempt -eq $max_attempts ]; then
        print_warning "Frontend didn't start in time, but it might still be starting"
        print_info "Check logs with: $DOCKER_COMPOSE_CMD logs frontend-web"
    fi

    echo ""
}

# Main execution
main() {
    check_docker
    check_docker_compose
    check_env_file
    check_ports
    start_app
    wait_for_services
    show_access_info
}

# Run main function
main
