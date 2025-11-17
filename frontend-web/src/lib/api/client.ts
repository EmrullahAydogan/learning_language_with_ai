import axios, { AxiosInstance, AxiosError } from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

class APIClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor to add auth token
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor to handle errors
    this.client.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        if (error.response?.status === 401) {
          // Try to refresh token
          const refreshToken = localStorage.getItem('refresh_token');
          if (refreshToken) {
            try {
              const response = await axios.post(`${API_URL}/auth/refresh`, {
                refresh_token: refreshToken,
              });

              const { access_token, refresh_token: newRefreshToken } = response.data;
              localStorage.setItem('access_token', access_token);
              localStorage.setItem('refresh_token', newRefreshToken);

              // Retry original request
              if (error.config) {
                error.config.headers.Authorization = `Bearer ${access_token}`;
                return this.client.request(error.config);
              }
            } catch (refreshError) {
              // Refresh failed, logout user
              localStorage.removeItem('access_token');
              localStorage.removeItem('refresh_token');
              window.location.href = '/login';
            }
          }
        }
        return Promise.reject(error);
      }
    );
  }

  // Auth
  async register(email: string, password: string, username?: string) {
    const response = await this.client.post('/auth/register', {
      email,
      password,
      username,
    });
    return response.data;
  }

  async login(email: string, password: string) {
    const response = await this.client.post('/auth/login', {
      email,
      password,
    });
    const { access_token, refresh_token } = response.data;
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);
    return response.data;
  }

  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.href = '/login';
  }

  // User
  async getCurrentUser() {
    const response = await this.client.get('/users/me');
    return response.data;
  }

  async updateProfile(data: any) {
    const response = await this.client.put('/users/me/profile', data);
    return response.data;
  }

  async getPreferences() {
    const response = await this.client.get('/users/me/preferences');
    return response.data;
  }

  async updatePreferences(data: any) {
    const response = await this.client.put('/users/me/preferences', data);
    return response.data;
  }

  // Languages
  async getLanguages() {
    const response = await this.client.get('/languages');
    return response.data;
  }

  async getProficiencyLevels() {
    const response = await this.client.get('/languages/levels');
    return response.data;
  }

  // Vocabulary
  async getDueFlashcards(languageId: number, limit = 20) {
    const response = await this.client.get('/vocabulary/due', {
      params: { language_id: languageId, limit },
    });
    return response.data;
  }

  async getNewVocabulary(languageId: number, limit = 10) {
    const response = await this.client.get('/vocabulary/new', {
      params: { language_id: languageId, limit },
    });
    return response.data;
  }

  async reviewFlashcard(vocabularyId: number, quality: number, timeTaken: number) {
    const response = await this.client.post('/vocabulary/review', {
      vocabulary_id: vocabularyId,
      quality,
      time_taken_seconds: timeTaken,
    });
    return response.data;
  }

  async getVocabularyStats(languageId: number) {
    const response = await this.client.get('/vocabulary/stats', {
      params: { language_id: languageId },
    });
    return response.data;
  }

  // Exercises
  async getExercises(languageId: number, levelId?: number) {
    const response = await this.client.get('/exercises', {
      params: { language_id: languageId, level_id: levelId },
    });
    return response.data;
  }

  async getExercise(exerciseId: number) {
    const response = await this.client.get(`/exercises/${exerciseId}`);
    return response.data;
  }

  async submitExercise(exerciseId: number, answers: any, timeTaken: number) {
    const response = await this.client.post(`/exercises/${exerciseId}/submit`, {
      answers,
      time_taken_seconds: timeTaken,
    });
    return response.data;
  }

  // Chat
  async createConversation(data: any) {
    const response = await this.client.post('/chat/conversations', data);
    return response.data;
  }

  async getConversations(languageId?: number) {
    const response = await this.client.get('/chat/conversations', {
      params: { language_id: languageId },
    });
    return response.data;
  }

  async getConversation(conversationId: number) {
    const response = await this.client.get(`/chat/conversations/${conversationId}`);
    return response.data;
  }

  async sendMessage(conversationId: number, content: string) {
    const response = await this.client.post(
      `/chat/conversations/${conversationId}/messages`,
      { content }
    );
    return response.data;
  }

  // Speaking
  async startSpeakingSession(data: any) {
    const response = await this.client.post('/speaking/sessions', data);
    return response.data;
  }

  async uploadRecording(sessionId: number, audioFile: File, expectedText?: string) {
    const formData = new FormData();
    formData.append('audio', audioFile);
    if (expectedText) {
      formData.append('expected_text', expectedText);
    }

    const response = await this.client.post(
      `/speaking/sessions/${sessionId}/record`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    return response.data;
  }

  // Reading
  async getReadingMaterials(languageId: number, levelId?: number) {
    const response = await this.client.get('/reading/materials', {
      params: { language_id: languageId, level_id: levelId },
    });
    return response.data;
  }

  async startReading(materialId: number) {
    const response = await this.client.post('/reading/start', {
      reading_material_id: materialId,
    });
    return response.data;
  }

  async completeReading(historyId: number, data: any) {
    const response = await this.client.post(`/reading/complete/${historyId}`, data);
    return response.data;
  }

  // Writing
  async submitWriting(data: any) {
    const response = await this.client.post('/writing/submit', data);
    return response.data;
  }

  async getWritingSubmissions(languageId?: number) {
    const response = await this.client.get('/writing/submissions', {
      params: { language_id: languageId },
    });
    return response.data;
  }

  async getWritingEvaluation(submissionId: number) {
    const response = await this.client.get(`/writing/submissions/${submissionId}/evaluation`);
    return response.data;
  }

  // Progress
  async getProgressOverview(languageId: number) {
    const response = await this.client.get('/progress/overview', {
      params: { language_id: languageId },
    });
    return response.data;
  }

  async getDailyActivity(days = 7, languageId?: number) {
    const response = await this.client.get('/progress/daily-activity', {
      params: { days, language_id: languageId },
    });
    return response.data;
  }

  async getStreak() {
    const response = await this.client.get('/progress/streak');
    return response.data;
  }

  async getUserXP() {
    const response = await this.client.get('/progress/xp');
    return response.data;
  }

  async getUserLevel() {
    const response = await this.client.get('/progress/level');
    return response.data;
  }

  // Gamification
  async getAchievements() {
    const response = await this.client.get('/gamification/achievements');
    return response.data;
  }

  async getUserAchievements() {
    const response = await this.client.get('/gamification/achievements/user');
    return response.data;
  }

  async getActiveChallenges() {
    const response = await this.client.get('/gamification/challenges/active');
    return response.data;
  }
}

export const apiClient = new APIClient();
