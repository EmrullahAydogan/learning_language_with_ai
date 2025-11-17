'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/stores/authStore';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api/client';
import Link from 'next/link';

export default function DashboardPage() {
  const router = useRouter();
  const { user, isAuthenticated, logout } = useAuthStore();

  const { data: xp } = useQuery({
    queryKey: ['userXP'],
    queryFn: () => apiClient.getUserXP(),
    enabled: isAuthenticated,
  });

  const { data: level } = useQuery({
    queryKey: ['userLevel'],
    queryFn: () => apiClient.getUserLevel(),
    enabled: isAuthenticated,
  });

  const { data: streak } = useQuery({
    queryKey: ['streak'],
    queryFn: () => apiClient.getStreak(),
    enabled: isAuthenticated,
  });

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, router]);

  if (!isAuthenticated || !user) {
    return <div>Loading...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">
            AI Language Learning Platform
          </h1>
          <div className="flex items-center gap-4">
            <span className="text-sm text-gray-600">Welcome, {user.email}</span>
            <button
              onClick={logout}
              className="px-4 py-2 text-sm bg-gray-200 hover:bg-gray-300 rounded-md"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-sm font-medium text-gray-600 mb-2">Level</h3>
            <p className="text-3xl font-bold text-blue-600">
              {level?.current_level || 1}
            </p>
            <p className="text-xs text-gray-500 mt-1">
              {level?.current_level_xp || 0} / {level?.xp_to_next_level || 100} XP
            </p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-sm font-medium text-gray-600 mb-2">Total XP</h3>
            <p className="text-3xl font-bold text-green-600">
              {xp?.total_xp?.toLocaleString() || 0}
            </p>
            <p className="text-xs text-gray-500 mt-1">
              {xp?.today_xp || 0} earned today
            </p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-sm font-medium text-gray-600 mb-2">Streak</h3>
            <p className="text-3xl font-bold text-orange-600">
              {streak?.current_streak || 0} days
            </p>
            <p className="text-xs text-gray-500 mt-1">
              Best: {streak?.longest_streak || 0} days
            </p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-sm font-medium text-gray-600 mb-2">This Week</h3>
            <p className="text-3xl font-bold text-purple-600">
              {xp?.week_xp?.toLocaleString() || 0}
            </p>
            <p className="text-xs text-gray-500 mt-1">XP earned</p>
          </div>
        </div>

        {/* Quick Actions */}
        <h2 className="text-xl font-bold mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Link
            href="/vocabulary"
            className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition"
          >
            <div className="text-4xl mb-4">📚</div>
            <h3 className="text-lg font-semibold mb-2">Vocabulary</h3>
            <p className="text-sm text-gray-600">
              Review flashcards and learn new words
            </p>
          </Link>

          <Link
            href="/exercises"
            className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition"
          >
            <div className="text-4xl mb-4">✍️</div>
            <h3 className="text-lg font-semibold mb-2">Exercises</h3>
            <p className="text-sm text-gray-600">
              Practice with interactive exercises
            </p>
          </Link>

          <Link
            href="/chat"
            className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition"
          >
            <div className="text-4xl mb-4">💬</div>
            <h3 className="text-lg font-semibold mb-2">AI Chat</h3>
            <p className="text-sm text-gray-600">
              Practice conversation with AI partner
            </p>
          </Link>

          <Link
            href="/speaking"
            className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition"
          >
            <div className="text-4xl mb-4">🎤</div>
            <h3 className="text-lg font-semibold mb-2">Speaking</h3>
            <p className="text-sm text-gray-600">
              Improve pronunciation with speech recognition
            </p>
          </Link>

          <Link
            href="/reading"
            className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition"
          >
            <div className="text-4xl mb-4">📖</div>
            <h3 className="text-lg font-semibold mb-2">Reading</h3>
            <p className="text-sm text-gray-600">
              Read articles and stories
            </p>
          </Link>

          <Link
            href="/writing"
            className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition"
          >
            <div className="text-4xl mb-4">✏️</div>
            <h3 className="text-lg font-semibold mb-2">Writing</h3>
            <p className="text-sm text-gray-600">
              Write essays and get AI feedback
            </p>
          </Link>
        </div>

        {/* Recent Activity */}
        <h2 className="text-xl font-bold mb-4">Recent Activity</h2>
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-gray-600">No recent activity yet. Start learning!</p>
        </div>
      </main>
    </div>
  );
}
