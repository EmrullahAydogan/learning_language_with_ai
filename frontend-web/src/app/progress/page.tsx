'use client';

import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api/client';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';
import { LoadingSpinner } from '@/components/ui/Loading';
import { ProgressBar } from '@/components/ui/ProgressBar';
import { Badge } from '@/components/ui/Badge';
import { useLanguageStore } from '@/stores/languageStore';
import { BarChart3, TrendingUp, Award, Calendar } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from 'recharts';

export default function ProgressPage() {
  const { currentLanguage } = useLanguageStore();

  const { data: overview, isLoading: overviewLoading } = useQuery({
    queryKey: ['progressOverview', currentLanguage?.id],
    queryFn: () => apiClient.getProgressOverview(currentLanguage?.id || 1),
    enabled: !!currentLanguage,
  });

  const { data: dailyActivity } = useQuery({
    queryKey: ['dailyActivity', currentLanguage?.id],
    queryFn: () => apiClient.getDailyActivity(30, currentLanguage?.id),
    enabled: !!currentLanguage,
  });

  const { data: xp } = useQuery({
    queryKey: ['userXP'],
    queryFn: () => apiClient.getUserXP(),
  });

  const { data: level } = useQuery({
    queryKey: ['userLevel'],
    queryFn: () => apiClient.getUserLevel(),
  });

  if (!currentLanguage) {
    return (
      <DashboardLayout>
        <Card>
          <CardContent className="py-8 text-center">
            <p className="text-gray-600">Please select a language to view progress</p>
          </CardContent>
        </Card>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold">Progress & Analytics</h1>
          <p className="text-gray-600 mt-1">Track your learning journey</p>
        </div>

        {/* Level & XP */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5 text-blue-600" />
                Your Level
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="text-center">
                  <p className="text-5xl font-bold text-blue-600">{level?.current_level || 1}</p>
                  <p className="text-gray-600 mt-2">Current Level</p>
                </div>
                <ProgressBar
                  value={level?.current_level_xp || 0}
                  max={level?.xp_to_next_level || 100}
                  color="blue"
                />
                <div className="flex justify-between text-sm text-gray-600">
                  <span>Level {level?.current_level || 1}</span>
                  <span>Level {(level?.current_level || 1) + 1}</span>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Award className="h-5 w-5 text-purple-600" />
                Experience Points
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="grid grid-cols-3 gap-4 text-center">
                  <div>
                    <p className="text-2xl font-bold text-purple-600">
                      {xp?.total_xp?.toLocaleString() || 0}
                    </p>
                    <p className="text-xs text-gray-600">Total</p>
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-green-600">{xp?.today_xp || 0}</p>
                    <p className="text-xs text-gray-600">Today</p>
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-blue-600">
                      {xp?.week_xp?.toLocaleString() || 0}
                    </p>
                    <p className="text-xs text-gray-600">This Week</p>
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-2 text-sm">
                  <Badge variant="info">Vocabulary: {xp?.vocabulary_xp || 0}</Badge>
                  <Badge variant="success">Exercises: {xp?.exercise_xp || 0}</Badge>
                  <Badge variant="warning">Speaking: {xp?.speaking_xp || 0}</Badge>
                  <Badge variant="default">Reading: {xp?.reading_xp || 0}</Badge>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Overall Progress */}
        {overviewLoading ? (
          <Card>
            <CardContent className="py-12 text-center">
              <LoadingSpinner size="lg" />
            </CardContent>
          </Card>
        ) : overview ? (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card>
              <CardHeader className="pb-3">
                <CardDescription>Words Learned</CardDescription>
                <CardTitle className="text-3xl text-blue-600">
                  {overview.total_words_learned || 0}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-sm text-gray-600">
                  {overview.words_mastered || 0} mastered
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-3">
                <CardDescription>Exercises Completed</CardDescription>
                <CardTitle className="text-3xl text-green-600">
                  {overview.total_exercises_completed || 0}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-sm text-gray-600">
                  Avg. Score: {Math.round(overview.average_exercise_score || 0)}%
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-3">
                <CardDescription>Study Time</CardDescription>
                <CardTitle className="text-3xl text-purple-600">
                  {Math.round((overview.total_study_time_minutes || 0) / 60)}h
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-sm text-gray-600">
                  {overview.total_study_time_minutes || 0} minutes total
                </div>
              </CardContent>
            </Card>
          </div>
        ) : null}

        {/* Activity Chart */}
        {dailyActivity && dailyActivity.length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Calendar className="h-5 w-5" />
                Daily Activity (Last 30 Days)
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={dailyActivity.reverse()}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis
                    dataKey="date"
                    tickFormatter={(value) => new Date(value).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                  />
                  <YAxis />
                  <Tooltip
                    labelFormatter={(value) => new Date(value).toLocaleDateString()}
                  />
                  <Bar dataKey="xp_earned" fill="#3b82f6" name="XP Earned" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        )}

        {/* Activity Breakdown */}
        {dailyActivity && dailyActivity.length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BarChart3 className="h-5 w-5" />
                Activity Breakdown
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={dailyActivity}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis
                    dataKey="date"
                    tickFormatter={(value) => new Date(value).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                  />
                  <YAxis />
                  <Tooltip
                    labelFormatter={(value) => new Date(value).toLocaleDateString()}
                  />
                  <Line type="monotone" dataKey="words_reviewed" stroke="#3b82f6" name="Words Reviewed" />
                  <Line type="monotone" dataKey="exercises_completed" stroke="#10b981" name="Exercises" />
                  <Line type="monotone" dataKey="study_time_minutes" stroke="#8b5cf6" name="Study Time (min)" />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        )}
      </div>
    </DashboardLayout>
  );
}
