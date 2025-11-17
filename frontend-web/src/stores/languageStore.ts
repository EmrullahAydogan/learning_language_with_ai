import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { Language } from '@/types';

interface LanguageState {
  currentLanguage: Language | null;
  setCurrentLanguage: (language: Language) => void;
}

export const useLanguageStore = create<LanguageState>()(
  persist(
    (set) => ({
      currentLanguage: null,
      setCurrentLanguage: (language) => set({ currentLanguage: language }),
    }),
    {
      name: 'language-storage',
    }
  )
);
