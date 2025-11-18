# 🌍 AI Language Learning Platform / Yapay Zeka Destekli Dil Öğrenme Platformu

[English](#english) | [Türkçe](#turkish)

---

<a name="english"></a>
## 🇬🇧 English

A comprehensive, full-stack language learning platform powered by AI, featuring personalized learning paths, speech recognition, real-time feedback, and gamification.

### ✨ One-Command Installation

**Works on all operating systems!** Just run:

**Linux/Mac:**
```bash
./start.sh
```

**Windows:**
```cmd
start.bat
```

That's it! The script will:
- ✅ Check all prerequisites (Docker, Docker Compose)
- ✅ Create environment configuration
- ✅ Start all services
- ✅ Run database migrations
- ✅ Seed database with 400+ vocabulary words
- ✅ Open your browser to http://localhost:3000

### 🌟 Features

#### Core Learning Modules
- **📚 Vocabulary Learning**: 400+ words with spaced repetition flashcards using SM-2 algorithm
- **✍️ Interactive Exercises**: Multiple question types (MCQ, fill-in-blank, matching, etc.)
- **💬 AI Chat Partner**: Conversation practice with GPT-4 powered AI tutor
- **🎤 Speaking Practice**: Speech recognition with pronunciation evaluation
- **📖 Reading Comprehension**: Leveled reading materials with comprehension quizzes
- **✏️ Writing Module**: AI-powered writing evaluation and feedback
- **🎯 Level Assessment**: 20-question quiz with automatic proficiency level determination (A1-C1)

#### Progress Tracking & Gamification
- **📊 Detailed Analytics**: Track progress across all learning activities
- **🏆 Achievement System**: 10+ badges, levels, and rewards
- **🔥 Streak Tracking**: Daily learning streaks and motivation
- **⚡ XP System**: Earn experience points for all activities
- **🎯 Daily Goals**: Customizable learning targets
- **📈 Progress Visualization**: Beautiful charts and statistics

#### Advanced Features
- **🌍 Multi-language Support**: English, Spanish, French, German, Italian, Turkish
- **🎯 Adaptive Learning**: AI-powered personalized content recommendations
- **🔔 Smart Notifications**: Reminder system for optimal learning
- **📱 Responsive Design**: Works on desktop, tablet, and mobile
- **🐳 Docker Ready**: One-command setup on any OS

### 🏗️ Tech Stack

#### Backend
- **FastAPI** - Modern, fast Python web framework
- **SQLAlchemy** - ORM for database management
- **PostgreSQL** - Primary database
- **Redis** - Caching and background tasks
- **Alembic** - Database migrations
- **OpenAI GPT-4** - AI chat and content evaluation
- **Whisper** - Speech-to-text
- **Celery** - Background task processing

#### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first CSS framework
- **Zustand** - State management
- **React Query** - Data fetching and caching
- **Recharts** - Data visualization

#### DevOps
- **Docker & Docker Compose** - Containerization
- **Cross-platform scripts** - Works on Linux, Mac, Windows

### 📁 Project Structure

```
learning_language_with_ai/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/      # 50+ API routes
│   │   │   ├── assessment.py      # Level assessment
│   │   │   ├── auth.py            # Authentication
│   │   │   ├── chat.py            # AI chat
│   │   │   ├── exercises.py       # Interactive exercises
│   │   │   ├── gamification.py    # Achievements & XP
│   │   │   ├── languages.py       # Language management
│   │   │   ├── progress.py        # Progress tracking
│   │   │   ├── reading.py         # Reading materials
│   │   │   ├── speaking.py        # Speaking practice
│   │   │   ├── users.py           # User management
│   │   │   ├── vocabulary.py      # Vocabulary & flashcards
│   │   │   └── writing.py         # Writing evaluation
│   │   ├── core/                  # Config, security, dependencies
│   │   ├── models/                # 25+ Database models
│   │   ├── services/              # Business logic
│   │   │   ├── ai/               # AI services (OpenAI, Whisper)
│   │   │   ├── flashcard/        # SM-2 spaced repetition
│   │   │   └── gamification/     # Achievement logic
│   │   └── database.py           # Database configuration
│   ├── scripts/
│   │   ├── seed_data.py          # Database seeding
│   │   └── vocabulary_data.py    # 400+ vocabulary words
│   ├── alembic/                  # Database migrations
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend-web/
│   ├── src/
│   │   ├── app/                  # 9 main pages
│   │   │   ├── dashboard/       # User dashboard
│   │   │   ├── vocabulary/      # Flashcard learning
│   │   │   ├── exercises/       # Interactive exercises
│   │   │   ├── chat/           # AI conversation
│   │   │   ├── speaking/       # Pronunciation practice
│   │   │   ├── reading/        # Reading materials
│   │   │   ├── writing/        # Essay writing
│   │   │   ├── progress/       # Analytics & stats
│   │   │   └── settings/       # User settings
│   │   ├── components/          # 30+ React components
│   │   ├── lib/                 # Utilities and API client
│   │   ├── stores/              # Zustand stores
│   │   └── types/               # TypeScript types
│   ├── package.json
│   └── Dockerfile
│
├── docker-compose.yml           # Full stack orchestration
├── .env.example                 # Environment template
├── start.sh                     # Linux/Mac startup script
├── start.bat                    # Windows startup script
└── README.md
```

### 🚀 Quick Start

#### Prerequisites
- **Docker Desktop** (includes Docker & Docker Compose)
  - [Download for Windows](https://docs.docker.com/desktop/install/windows-install/)
  - [Download for Mac](https://docs.docker.com/desktop/install/mac-install/)
  - [Download for Linux](https://docs.docker.com/desktop/install/linux-install/)
- **OpenAI API Key** (optional, for AI features)
  - [Get your API key](https://platform.openai.com/api-keys)

#### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd learning_language_with_ai
```

2. **Run the startup script**

**On Linux/Mac:**
```bash
./start.sh
```

**On Windows:**
```cmd
start.bat
```

The script will automatically:
- Check Docker installation
- Check port availability (3000, 8000, 5432, 6379)
- Create `.env` file from `.env.example`
- Build Docker images (first time: 5-10 minutes)
- Start all services (PostgreSQL, Redis, Backend, Frontend)
- Run database migrations
- Seed database with:
  - 6 languages (English, Spanish, French, German, Italian, Turkish)
  - 5 proficiency levels (A1, A2, B1, B2, C1)
  - 400+ vocabulary words across all levels
  - 10 vocabulary categories
  - 6 interactive exercises
  - 8 reading materials (A1-A2)
  - 20 assessment questions
  - 10 achievements and badges
- Wait for services to be ready
- Show access URLs

3. **Access the application**
- **Frontend (Web App)**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

4. **Configure OpenAI (Optional)**

To enable AI features (chat, writing evaluation):
```bash
# Edit .env file and add your OpenAI API key
nano .env  # or use any text editor
# Set: OPENAI_API_KEY=sk-your-key-here
```

Then restart:
```bash
docker-compose restart backend
```

### 🎓 Usage Guide

#### First Time Setup

1. **Open** http://localhost:3000 in your browser
2. **Register** a new account
3. **Select** your native language and target language
4. **Take the level assessment quiz** (20 questions)
   - Automatic level determination based on score:
   - 90%+ = C1 (Advanced)
   - 75-90% = B2 (Upper Intermediate)
   - 60-75% = B1 (Intermediate)
   - 40-60% = A2 (Elementary)
   - <40% = A1 (Beginner)
5. **Set your daily goals** and preferences
6. **Start learning!**

#### Daily Workflow

1. **Check Dashboard** - View daily goals, streaks, and XP
2. **Review Flashcards** - Study vocabulary with spaced repetition
3. **Complete Exercises** - Practice grammar and vocabulary
4. **AI Chat Practice** - Converse with GPT-4 powered tutor
5. **Speaking Practice** - Improve pronunciation with speech recognition
6. **Read Articles** - Comprehension practice with leveled content
7. **Write Essays** - Get AI feedback on your writing
8. **Track Progress** - View detailed analytics and achievements

### 🛠️ Manual Commands

If you need to manage services manually:

```bash
# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend-web

# Restart services
docker-compose restart

# Rebuild and restart
docker-compose up --build -d

# Run database migrations manually
docker-compose exec backend alembic upgrade head

# Seed database manually
docker-compose exec backend python scripts/seed_data.py

# Access backend shell
docker-compose exec backend bash

# Access database
docker-compose exec postgres psql -U postgres -d language_learning_db
```

### 📚 API Documentation

Once the backend is running, comprehensive API documentation is available at:
- **Swagger UI**: http://localhost:8000/docs (Interactive)
- **ReDoc**: http://localhost:8000/redoc (Documentation)

**API Endpoints Include:**
- `/api/v1/auth/*` - Authentication (login, register, tokens)
- `/api/v1/users/*` - User management and profiles
- `/api/v1/languages/*` - Language and level management
- `/api/v1/vocabulary/*` - Vocabulary and flashcards
- `/api/v1/exercises/*` - Interactive exercises
- `/api/v1/assessment/*` - Level assessment quiz
- `/api/v1/chat/*` - AI chat conversations
- `/api/v1/speaking/*` - Speaking practice sessions
- `/api/v1/reading/*` - Reading materials
- `/api/v1/writing/*` - Writing submissions and evaluation
- `/api/v1/progress/*` - Progress tracking and analytics
- `/api/v1/gamification/*` - Achievements, XP, badges

### 🗄️ Database

The platform uses PostgreSQL with 25+ tables including:
- Users, authentication, and profiles
- Languages and proficiency levels
- Vocabulary with translations
- Flashcards and spaced repetition data
- Exercises and user attempts
- Level assessments and answers
- Chat conversations and messages
- Speaking sessions and evaluations
- Reading materials and history
- Writing submissions and evaluations
- Progress tracking (daily activities, streaks)
- Gamification (achievements, badges, XP)

### 🧪 Testing

```bash
# Backend tests
docker-compose exec backend pytest

# Frontend tests
docker-compose exec frontend-web npm test

# E2E tests
docker-compose exec frontend-web npm run test:e2e
```

### 🔧 Development

For local development without Docker:

#### Backend Development

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with local database URL

# Run migrations
alembic upgrade head

# Seed database
python scripts/seed_data.py

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Development

```bash
cd frontend-web

# Install dependencies
npm install

# Set up environment
cp .env.example .env.local
# Edit .env.local if needed

# Start development server
npm run dev
```

### 🌐 Supported Languages

The platform currently supports:
- 🇬🇧 English
- 🇪🇸 Spanish (Español)
- 🇫🇷 French (Français)
- 🇩🇪 German (Deutsch)
- 🇮🇹 Italian (Italiano)
- 🇹🇷 Turkish (Türkçe)

Each language includes:
- 400+ vocabulary words
- Grammar exercises
- Reading materials
- Assessment questions

### 📊 What's Included

Out of the box, the platform includes:
- ✅ **6 Languages**: English, Spanish, French, German, Italian, Turkish
- ✅ **5 Proficiency Levels**: A1, A2, B1, B2, C1 (CEFR standard)
- ✅ **400+ Vocabulary Words**: Organized by level and category
- ✅ **10 Categories**: Numbers, Colors, Family, Animals, Food, etc.
- ✅ **6 Interactive Exercises**: Grammar, verbs, articles, and more
- ✅ **8 Reading Materials**: Leveled texts with comprehension
- ✅ **20 Assessment Questions**: For automatic level placement
- ✅ **10 Achievements**: Various learning milestones
- ✅ **Gamification System**: XP, levels, streaks, badges
- ✅ **AI Integration**: GPT-4 for chat and writing feedback
- ✅ **Spaced Repetition**: SM-2 algorithm for flashcards

### 🛣️ Roadmap

#### ✅ Phase 1 - Core Platform (COMPLETED)
- ✅ Full-stack infrastructure
- ✅ Authentication & user management
- ✅ Database models (25+ tables)
- ✅ API endpoints (50+)
- ✅ Frontend UI (9 main pages, 30+ components)
- ✅ Docker setup with one-command installation
- ✅ Vocabulary module with spaced repetition
- ✅ Exercise system
- ✅ AI chat integration
- ✅ Level assessment quiz
- ✅ Progress tracking & analytics
- ✅ Gamification (XP, achievements, streaks)
- ✅ 400+ vocabulary words seeded
- ✅ Cross-platform support (Linux, Mac, Windows)

#### 🚧 Phase 2 - Enhanced Features (IN PROGRESS)
- [ ] Complete speaking module with full speech recognition
- [ ] Enhanced reading comprehension with interactive features
- [ ] Advanced writing module with detailed AI feedback
- [ ] Email notifications (verification, reminders)
- [ ] Admin panel for content management
- [ ] Real-time WebSocket for live chat
- [ ] Text-to-speech (TTS) for vocabulary
- [ ] Audio pronunciation examples

#### 📋 Phase 3 - Advanced Features (PLANNED)
- [ ] Mobile app (React Native)
- [ ] Offline mode
- [ ] Social features (friends, groups, challenges)
- [ ] Native speaker matching
- [ ] Community content creation
- [ ] Advanced analytics dashboard

#### 🚀 Phase 4 - Professional Features (FUTURE)
- [ ] Live video lessons
- [ ] Certification exams
- [ ] Teacher dashboard
- [ ] School/Organization accounts
- [ ] Custom curriculum builder
- [ ] White-label solution

### 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

### 🙏 Acknowledgments

- **OpenAI** for GPT-4 and Whisper API
- **SuperMemo** for the SM-2 spaced repetition algorithm
- **FastAPI** and **Next.js** communities for excellent frameworks
- **Docker** for containerization technology

### 📞 Support

For questions, issues, or feature requests:
- Open an issue on GitHub
- Check the API documentation at http://localhost:8000/docs

---

<a name="turkish"></a>
## 🇹🇷 Türkçe

Yapay zeka destekli, kişiselleştirilmiş öğrenme yolları, konuşma tanıma, gerçek zamanlı geri bildirim ve oyunlaştırma özellikleri içeren kapsamlı, tam yığın dil öğrenme platformu.

### ✨ Tek Komutla Kurulum

**Tüm işletim sistemlerinde çalışır!** Sadece şunu çalıştırın:

**Linux/Mac:**
```bash
./start.sh
```

**Windows:**
```cmd
start.bat
```

Bu kadar! Script otomatik olarak:
- ✅ Tüm gereksinimleri kontrol eder (Docker, Docker Compose)
- ✅ Ortam yapılandırmasını oluşturur
- ✅ Tüm servisleri başlatır
- ✅ Veritabanı migrasyonlarını çalıştırır
- ✅ Veritabanına 400+ kelime ekler
- ✅ Tarayıcınızı http://localhost:3000 adresinde açar

### 🌟 Özellikler

#### Temel Öğrenme Modülleri
- **📚 Kelime Öğrenimi**: SM-2 algoritması ile aralıklı tekrar flashcard'ları ve 400+ kelime
- **✍️ İnteraktif Alıştırmalar**: Çoktan seçmeli, boşluk doldurma, eşleştirme gibi çoklu soru türleri
- **💬 Yapay Zeka Sohbet Partneri**: GPT-4 destekli yapay zeka öğretmeni ile konuşma pratiği
- **🎤 Konuşma Pratiği**: Telaffuz değerlendirmeli konuşma tanıma
- **📖 Okuma Anlama**: Seviyeye göre okuma materyalleri ve anlama testleri
- **✏️ Yazma Modülü**: Yapay zeka destekli yazma değerlendirmesi ve geri bildirim
- **🎯 Seviye Belirleme**: 20 soruluk otomatik seviye belirleme testi (A1-C1)

#### İlerleme Takibi & Oyunlaştırma
- **📊 Detaylı Analitik**: Tüm öğrenme aktivitelerinde ilerleme takibi
- **🏆 Başarı Sistemi**: 10+ rozet, seviye ve ödül
- **🔥 Seri Takibi**: Günlük öğrenme serileri ve motivasyon
- **⚡ XP Sistemi**: Tüm aktiviteler için deneyim puanı kazanın
- **🎯 Günlük Hedefler**: Özelleştirilebilir öğrenme hedefleri
- **📈 İlerleme Görselleştirme**: Güzel grafikler ve istatistikler

#### Gelişmiş Özellikler
- **🌍 Çoklu Dil Desteği**: İngilizce, İspanyolca, Fransızca, Almanca, İtalyanca, Türkçe
- **🎯 Uyarlanabilir Öğrenme**: Yapay zeka destekli kişiselleştirilmiş içerik önerileri
- **🔔 Akıllı Bildirimler**: Optimal öğrenme için hatırlatma sistemi
- **📱 Duyarlı Tasarım**: Masaüstü, tablet ve mobilde çalışır
- **🐳 Docker Hazır**: Herhangi bir işletim sisteminde tek komutla kurulum

### 🚀 Hızlı Başlangıç

#### Gereksinimler
- **Docker Desktop** (Docker & Docker Compose içerir)
  - [Windows için İndir](https://docs.docker.com/desktop/install/windows-install/)
  - [Mac için İndir](https://docs.docker.com/desktop/install/mac-install/)
  - [Linux için İndir](https://docs.docker.com/desktop/install/linux-install/)
- **OpenAI API Anahtarı** (isteğe bağlı, yapay zeka özellikleri için)
  - [API anahtarınızı alın](https://platform.openai.com/api-keys)

#### Kurulum

1. **Depoyu klonlayın**
```bash
git clone <repository-url>
cd learning_language_with_ai
```

2. **Başlatma scriptini çalıştırın**

**Linux/Mac'te:**
```bash
./start.sh
```

**Windows'ta:**
```cmd
start.bat
```

Script otomatik olarak:
- Docker kurulumunu kontrol eder
- Port müsaitliğini kontrol eder (3000, 8000, 5432, 6379)
- `.env.example`'dan `.env` dosyası oluşturur
- Docker image'larını build eder (ilk seferinde: 5-10 dakika)
- Tüm servisleri başlatır (PostgreSQL, Redis, Backend, Frontend)
- Veritabanı migrasyonlarını çalıştırır
- Veritabanını doldurur:
  - 6 dil (İngilizce, İspanyolca, Fransızca, Almanca, İtalyanca, Türkçe)
  - 5 yeterlilik seviyesi (A1, A2, B1, B2, C1)
  - 400+ kelime (tüm seviyeler)
  - 10 kelime kategorisi
  - 6 interaktif alıştırma
  - 8 okuma materyali (A1-A2)
  - 20 seviye belirleme sorusu
  - 10 başarı ve rozet
- Servislerin hazır olmasını bekler
- Erişim URL'lerini gösterir

3. **Uygulamaya erişin**
- **Frontend (Web Uygulaması)**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Dokümantasyonu**: http://localhost:8000/docs
- **Alternatif Doküman**: http://localhost:8000/redoc

4. **OpenAI'yi Yapılandırın (İsteğe Bağlı)**

Yapay zeka özelliklerini (sohbet, yazı değerlendirme) etkinleştirmek için:
```bash
# .env dosyasını düzenleyin ve OpenAI API anahtarınızı ekleyin
nano .env  # veya herhangi bir metin editörü kullanın
# Ayarlayın: OPENAI_API_KEY=sk-anahtarınız-buraya
```

Sonra yeniden başlatın:
```bash
docker-compose restart backend
```

### 🎓 Kullanım Kılavuzu

#### İlk Kurulum

1. **Açın** http://localhost:3000 adresini tarayıcınızda
2. **Kayıt olun** yeni bir hesap oluşturun
3. **Seçin** ana dilinizi ve hedef dilinizi
4. **Seviye belirleme testini alın** (20 soru)
   - Puana göre otomatik seviye belirleme:
   - %90+ = C1 (İleri)
   - %75-90 = B2 (Üst Orta)
   - %60-75 = B1 (Orta)
   - %40-60 = A2 (Başlangıç)
   - <%40 = A1 (Temel)
5. **Günlük hedeflerinizi** ve tercihlerinizi ayarlayın
6. **Öğrenmeye başlayın!**

#### Günlük İş Akışı

1. **Kontrol Paneli** - Günlük hedefleri, serileri ve XP'yi görüntüleyin
2. **Flashcard İnceleme** - Aralıklı tekrar ile kelime çalışın
3. **Alıştırmaları Tamamlayın** - Gramer ve kelime pratiği yapın
4. **Yapay Zeka Sohbeti** - GPT-4 destekli öğretmenle konuşun
5. **Konuşma Pratiği** - Konuşma tanıma ile telaffuzunuzu geliştirin
6. **Makale Okuyun** - Seviyeye uygun içerikle anlama pratiği
7. **Deneme Yazın** - Yazınız hakkında yapay zeka geri bildirimi alın
8. **İlerleme Takibi** - Detaylı analitik ve başarıları görüntüleyin

### 🛠️ Manuel Komutlar

Servisleri manuel olarak yönetmeniz gerekirse:

```bash
# Tüm servisleri durdur
docker-compose down

# Logları görüntüle
docker-compose logs -f

# Belirli servis loglarını görüntüle
docker-compose logs -f backend
docker-compose logs -f frontend-web

# Servisleri yeniden başlat
docker-compose restart

# Yeniden build et ve başlat
docker-compose up --build -d

# Veritabanı migrasyonlarını manuel çalıştır
docker-compose exec backend alembic upgrade head

# Veritabanını manuel doldur
docker-compose exec backend python scripts/seed_data.py
```

### 📊 Neler Dahil

Platform kutudan çıktığı gibi şunları içerir:
- ✅ **6 Dil**: İngilizce, İspanyolca, Fransızca, Almanca, İtalyanca, Türkçe
- ✅ **5 Yeterlilik Seviyesi**: A1, A2, B1, B2, C1 (CEFR standardı)
- ✅ **400+ Kelime**: Seviye ve kategoriye göre düzenlenmiş
- ✅ **10 Kategori**: Sayılar, Renkler, Aile, Hayvanlar, Yemek, vb.
- ✅ **6 İnteraktif Alıştırma**: Gramer, fiiller, artikeller ve daha fazlası
- ✅ **8 Okuma Materyali**: Anlamayla birlikte seviyeli metinler
- ✅ **20 Değerlendirme Sorusu**: Otomatik seviye belirleme için
- ✅ **10 Başarı**: Çeşitli öğrenme kilometre taşları
- ✅ **Oyunlaştırma Sistemi**: XP, seviyeler, seriler, rozetler
- ✅ **Yapay Zeka Entegrasyonu**: Sohbet ve yazı geri bildirimi için GPT-4
- ✅ **Aralıklı Tekrar**: Flashcard'lar için SM-2 algoritması

### 🛣️ Yol Haritası

#### ✅ Faz 1 - Temel Platform (TAMAMLANDI)
- ✅ Tam yığın altyapı
- ✅ Kimlik doğrulama ve kullanıcı yönetimi
- ✅ Veritabanı modelleri (25+ tablo)
- ✅ API endpoint'leri (50+)
- ✅ Frontend arayüzü (9 ana sayfa, 30+ bileşen)
- ✅ Tek komutla kurulum ile Docker yapılandırması
- ✅ Aralıklı tekrar ile kelime modülü
- ✅ Alıştırma sistemi
- ✅ Yapay zeka sohbet entegrasyonu
- ✅ Seviye belirleme testi
- ✅ İlerleme takibi ve analitik
- ✅ Oyunlaştırma (XP, başarılar, seriler)
- ✅ 400+ kelime eklendi
- ✅ Çapraz platform desteği (Linux, Mac, Windows)

#### 🚧 Faz 2 - Gelişmiş Özellikler (DEVAM EDİYOR)
- [ ] Tam konuşma tanıma ile konuşma modülünü tamamla
- [ ] İnteraktif özelliklerle gelişmiş okuma anlama
- [ ] Detaylı yapay zeka geri bildirimi ile gelişmiş yazma modülü
- [ ] E-posta bildirimleri (doğrulama, hatırlatmalar)
- [ ] İçerik yönetimi için admin paneli
- [ ] Canlı sohbet için gerçek zamanlı WebSocket
- [ ] Kelimeler için metinden konuşmaya (TTS)
- [ ] Sesli telaffuz örnekleri

#### 📋 Faz 3 - İleri Özellikler (PLANLI)
- [ ] Mobil uygulama (React Native)
- [ ] Çevrimdışı mod
- [ ] Sosyal özellikler (arkadaşlar, gruplar, meydan okumalar)
- [ ] Anadili konuşan kişi eşleştirme
- [ ] Topluluk içerik oluşturma
- [ ] Gelişmiş analitik panosu

#### 🚀 Faz 4 - Profesyonel Özellikler (GELECEK)
- [ ] Canlı video dersler
- [ ] Sertifika sınavları
- [ ] Öğretmen panosu
- [ ] Okul/Organizasyon hesapları
- [ ] Özel müfredat oluşturucu
- [ ] White-label çözümü

### 🤝 Katkıda Bulunma

Katkılar memnuniyetle karşılanır! Lütfen Pull Request göndermekten çekinmeyin.

### 📄 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır.

### 📞 Destek

Sorular, sorunlar veya özellik istekleri için:
- GitHub'da bir issue açın
- API dokümantasyonuna http://localhost:8000/docs adresinden bakın

---

**İyi Öğrenmeler! 🚀 / Happy Learning! 🚀**
