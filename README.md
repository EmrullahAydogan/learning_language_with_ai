# AI Language Learning Platform

A comprehensive, full-stack language learning platform powered by AI, featuring personalized learning paths, speech recognition, real-time feedback, and gamification.

## 🌟 Features

### Core Learning Modules
- **📚 Vocabulary Learning**: Spaced repetition flashcards using SM-2 algorithm
- **✍️ Interactive Exercises**: Multiple question types (MCQ, fill-in-blank, matching, etc.)
- **💬 AI Chat Partner**: Conversation practice with GPT-4 powered AI tutor
- **🎤 Speaking Practice**: Speech recognition with pronunciation evaluation
- **📖 Reading Comprehension**: Leveled reading materials with comprehension quizzes
- **✏️ Writing Module**: AI-powered writing evaluation and feedback

### Progress Tracking & Gamification
- **📊 Detailed Analytics**: Track progress across all learning activities
- **🏆 Achievement System**: Badges, levels, and rewards
- **🔥 Streak Tracking**: Daily learning streaks and motivation
- **⚡ XP System**: Earn experience points for all activities
- **🎯 Daily Goals**: Customizable learning targets

### Advanced Features
- **🌍 Multi-language Support**: English, Spanish, French, German, Italian, Turkish
- **🎯 Adaptive Learning**: AI-powered personalized content recommendations
- **📈 Progress Visualization**: Beautiful charts and statistics
- **🔔 Smart Notifications**: Reminder system for optimal learning
- **👥 Social Features**: Leaderboards and challenges (planned)

## 🏗️ Tech Stack

### Backend
- **FastAPI** - Modern, fast Python web framework
- **SQLAlchemy** - ORM for database management
- **PostgreSQL** - Primary database
- **Redis** - Caching and background tasks
- **Alembic** - Database migrations
- **OpenAI GPT-4** - AI chat and content evaluation
- **Whisper** - Speech-to-text
- **Celery** - Background task processing

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first CSS framework
- **Zustand** - State management
- **React Query** - Data fetching and caching
- **Recharts** - Data visualization

### DevOps
- **Docker & Docker Compose** - Containerization
- **Nginx** - Reverse proxy (production)

## 📁 Project Structure

```
learning_language_with_ai/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/      # API routes
│   │   ├── core/                  # Config, security, dependencies
│   │   ├── models/                # Database models
│   │   ├── schemas/               # Pydantic schemas
│   │   ├── services/              # Business logic
│   │   │   ├── ai/               # AI services (OpenAI, Whisper)
│   │   │   ├── flashcard/        # Spaced repetition algorithm
│   │   │   └── gamification/     # Achievement logic
│   │   └── db/                   # Database configuration
│   ├── alembic/                  # Database migrations
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend-web/
│   ├── src/
│   │   ├── app/                  # Next.js app router pages
│   │   ├── components/           # React components
│   │   ├── lib/                  # Utilities and API client
│   │   ├── stores/               # Zustand stores
│   │   └── types/                # TypeScript types
│   ├── package.json
│   └── Dockerfile
│
├── frontend-mobile/             # React Native (planned)
├── docker-compose.yml
└── README.md
```

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)
- OpenAI API Key

### Quick Start with Docker

1. **Clone the repository**
```bash
git clone <repository-url>
cd learning_language_with_ai
```

2. **Set up environment variables**
```bash
# Backend
cp backend/.env.example backend/.env
# Edit backend/.env and add your OpenAI API key
```

3. **Start with Docker Compose**
```bash
docker-compose up -d
```

4. **Run database migrations**
```bash
docker-compose exec backend alembic upgrade head
```

5. **Initialize database with default data**
```bash
docker-compose exec backend python -c "
from app.db.session import SessionLocal
from app.db.init_db import init_db
db = SessionLocal()
init_db(db)
db.close()
"
```

6. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/v1/docs

### Local Development Setup

#### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up PostgreSQL and Redis locally
# Update .env with your database URL

# Run migrations
alembic upgrade head

# Initialize database
python -c "from app.db.session import SessionLocal; from app.db.init_db import init_db; db = SessionLocal(); init_db(db); db.close()"

# Start development server
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend-web

# Install dependencies
npm install

# Start development server
npm run dev
```

## 📚 API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

## 🗄️ Database Schema

The platform uses a comprehensive database schema with the following main entities:

- **Users & Authentication**: User accounts, profiles, preferences
- **Languages & Levels**: Supported languages and proficiency levels
- **Vocabulary**: Words, translations, and user progress
- **Exercises**: Questions, answers, and user history
- **Chat**: Conversations and messages with AI
- **Speaking**: Session recordings and evaluations
- **Reading**: Materials and user reading history
- **Writing**: Submissions and AI evaluations
- **Progress**: Daily activities, streaks, XP, levels
- **Gamification**: Achievements, badges, challenges

## 🎓 Usage Guide

### First Time Setup

1. **Register an account** at http://localhost:3000/register
2. **Select your native language and target language**
3. **Take the placement test** to determine your proficiency level
4. **Set your daily goals** and preferences
5. **Start learning!**

### Daily Workflow

1. **Check your daily goals** on the dashboard
2. **Review flashcards** (spaced repetition)
3. **Complete exercises** appropriate for your level
4. **Practice conversation** with AI chat partner
5. **Work on speaking** with pronunciation feedback
6. **Read articles** and complete comprehension quizzes
7. **Write essays** and receive AI feedback

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Redis
REDIS_URL=redis://localhost:6379/0

# OpenAI
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL=gpt-4

# Security
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend-web
npm test
```

## 📦 Deployment

### Production Deployment

1. **Update environment variables** for production
2. **Build Docker images**
```bash
docker-compose -f docker-compose.prod.yml build
```

3. **Deploy with Docker Compose**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

4. **Set up reverse proxy** (Nginx recommended)
5. **Configure SSL certificates** (Let's Encrypt)
6. **Set up monitoring** and logging

## 🛣️ Roadmap

### Phase 1 (Current)
- ✅ Core platform infrastructure
- ✅ Authentication system
- ✅ Vocabulary module with spaced repetition
- ✅ Exercise module
- ✅ AI chat integration
- ✅ Basic progress tracking

### Phase 2
- [ ] Speaking module with full speech recognition
- [ ] Reading comprehension with interactive features
- [ ] Writing module with detailed AI feedback
- [ ] Advanced gamification

### Phase 3
- [ ] Mobile app (React Native)
- [ ] Offline mode
- [ ] Social features (friends, groups)
- [ ] Native speaker matching

### Phase 4
- [ ] Live video lessons
- [ ] Certification exams
- [ ] Teacher dashboard
- [ ] Advanced analytics

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- OpenAI for GPT-4 and Whisper API
- SuperMemo for the SM-2 spaced repetition algorithm
- The FastAPI and Next.js communities

## 📞 Support

For questions or issues, please open an issue on GitHub.

---

**Happy Learning! 🚀**