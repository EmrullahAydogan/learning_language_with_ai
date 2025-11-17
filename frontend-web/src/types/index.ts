export interface User {
  id: number;
  email: string;
  username?: string;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
}

export interface Language {
  id: number;
  code: string;
  name: string;
  native_name: string;
  flag: string;
  is_active: boolean;
}

export interface ProficiencyLevel {
  id: number;
  code: string;
  name: string;
  description: string;
}

export interface Vocabulary {
  id: number;
  word: string;
  translation?: string;
  pronunciation?: string;
  part_of_speech?: string;
  definition?: string;
  example_sentence?: string;
  image_url?: string;
  audio_url?: string;
}

export interface UserVocabulary {
  id: number;
  vocabulary_id: number;
  status: 'new' | 'learning' | 'review' | 'mastered';
  ease_factor: number;
  interval: number;
  next_review_date?: string;
  times_reviewed: number;
  times_correct: number;
  times_incorrect: number;
  vocabulary: Vocabulary;
}

export interface Exercise {
  id: number;
  title: string;
  description?: string;
  difficulty?: string;
  xp_reward: number;
  estimated_time_minutes?: number;
  questions: ExerciseQuestion[];
}

export interface ExerciseQuestion {
  id: number;
  question_text: string;
  answer_data: any;
  explanation?: string;
  order: number;
}

export interface ChatConversation {
  id: number;
  language_id: number;
  conversation_type: string;
  scenario_name?: string;
  is_active: boolean;
  started_at: string;
  messages: ChatMessage[];
}

export interface ChatMessage {
  id: number;
  role: 'user' | 'assistant' | 'system';
  content: string;
  has_errors: boolean;
  corrections?: any;
  feedback?: string;
  created_at: string;
}

export interface UserProgress {
  total_words_learned: number;
  words_mastered: number;
  total_exercises_completed: number;
  average_exercise_score: number;
  total_speaking_sessions: number;
  total_study_time_minutes: number;
}

export interface DailyActivity {
  date: string;
  words_reviewed: number;
  exercises_completed: number;
  study_time_minutes: number;
  xp_earned: number;
  daily_goal_met: boolean;
}

export interface Streak {
  current_streak: number;
  longest_streak: number;
  last_activity_date?: string;
}

export interface UserXP {
  total_xp: number;
  vocabulary_xp: number;
  exercise_xp: number;
  speaking_xp: number;
  reading_xp: number;
  writing_xp: number;
  today_xp: number;
  week_xp: number;
}

export interface UserLevel {
  current_level: number;
  current_level_xp: number;
  xp_to_next_level: number;
  total_levels_gained: number;
}

export interface Achievement {
  id: number;
  achievement_type: string;
  target_value: number;
  xp_reward: number;
  badge: Badge;
}

export interface Badge {
  id: number;
  name: string;
  description: string;
  icon: string;
  category: string;
  rarity: string;
}

export interface UserAchievement {
  id: number;
  achievement_id: number;
  current_progress: number;
  is_completed: boolean;
  completed_at?: string;
  achievement: Achievement;
}
