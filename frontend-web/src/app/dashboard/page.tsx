'use client';

import { useAuthStore } from '@/stores/authStore';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api/client';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { ProgressBar } from '@/components/ui/ProgressBar';
import Link from 'next/link';

export default function DashboardPage() {
  const { user, isAuthenticated } = useAuthStore();

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

  return (
    <DashboardLayout>
      <div>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardHeader className="pb-3">
              <CardDescription>Level</CardDescription>
              <CardTitle className="text-3xl text-blue-600">
                {level?.current_level || 1}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ProgressBar
                value={level?.current_level_xp || 0}
                max={level?.xp_to_next_level || 100}
                color="blue"
                showLabel={false}
              />
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardDescription>Total XP</CardDescription>
              <CardTitle className="text-3xl text-green-600">
                {xp?.total_xp?.toLocaleString() || 0}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-500">
                {xp?.today_xp || 0} earned today
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardDescription>Streak</CardDescription>
              <CardTitle className="text-3xl text-orange-600">
                {streak?.current_streak || 0} 🔥
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-500">
                Best: {streak?.longest_streak || 0} days
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardDescription>This Week</CardDescription>
              <CardTitle className="text-3xl text-purple-600">
                {xp?.week_xp?.toLocaleString() || 0}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-500">XP earned</p>
            </CardContent>
          </Card>
        </div>

        <h2 className="text-2xl font-bold mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Link href="/vocabulary">
            <Card hover className="cursor-pointer h-full">
              <CardHeader>
                <div className="text-4xl mb-2">📚</div>
                <CardTitle>Vocabulary</CardTitle>
                <CardDescription>
                  Review flashcards and learn new words
                </CardDescription>
              </CardHeader>
            </Card>
          </Link>

          <Link href="/exercises">
            <Card hover className="cursor-pointer h-full">
              <CardHeader>
                <div className="text-4xl mb-2">✍️</div>
                <CardTitle>Exercises</CardTitle>
                <CardDescription>
                  Practice with interactive exercises
                </CardDescription>
              </CardHeader>
            </Card>
          </Link>

          <Link href="/chat">
            <Card hover className="cursor-pointer h-full">
              <CardHeader>
                <div className="text-4xl mb-2">💬</div>
                <CardTitle>AI Chat</CardTitle>
                <CardDescription>
                  Practice conversation with AI partner
                </CardDescription>
              </CardHeader>
            </Card>
          </Link>

          <Link href="/speaking">
            <Card hover className="cursor-pointer h-full">
              <CardHeader>
                <div className="text-4xl mb-2">🎤</div>
                <CardTitle>Speaking</CardTitle>
                <CardDescription>
                  Improve pronunciation with speech recognition
                </CardDescription>
              </CardHeader>
            </Card>
          </Link>

          <Link href="/reading">
            <Card hover className="cursor-pointer h-full">
              <CardHeader>
                <div className="text-4xl mb-2">📖</div>
                <CardTitle>Reading</CardTitle>
                <CardDescription>
                  Read articles and stories
                </CardDescription>
              </CardHeader>
            </Card>
          </Link>

          <Link href="/writing">
            <Card hover className="cursor-pointer h-full">
              <CardHeader>
                <div className="text-4xl mb-2">✏️</div>
                <CardTitle>Writing</CardTitle>
                <CardDescription>
                  Write essays and get AI feedback
                </CardDescription>
              </CardHeader>
            </Card>
          </Link>
        </div>

        <h2 className="text-2xl font-bold mb-4">Recent Activity</h2>
        <Card>
          <CardContent className="py-8 text-center">
            <p className="text-gray-600">No recent activity yet. Start learning!</p>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}
