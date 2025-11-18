'use client';

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api/client';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { LoadingSpinner } from '@/components/ui/Loading';
import { ProgressBar } from '@/components/ui/ProgressBar';
import { useLanguageStore } from '@/stores/languageStore';
import { Mic, MicOff, Play, Square } from 'lucide-react';

export default function SpeakingPage() {
  const { currentLanguage } = useLanguageStore();
  const [view, setView] = useState<'overview' | 'practice'>('overview');

  const { data: sessions, isLoading } = useQuery({
    queryKey: ['speakingSessions', currentLanguage?.id],
    queryFn: () => apiClient.getSpeakingSessions(currentLanguage?.id),
    enabled: !!currentLanguage,
  });

  if (!currentLanguage) {
    return (
      <DashboardLayout>
        <Card>
          <CardContent className="py-8 text-center">
            <p className="text-gray-600">Please select a language to practice speaking</p>
          </CardContent>
        </Card>
      </DashboardLayout>
    );
  }

  if (view === 'practice') {
    return (
      <DashboardLayout>
        <SpeakingPractice
          languageId={currentLanguage.id}
          onBack={() => setView('overview')}
        />
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold">Speaking Practice</h1>
            <p className="text-gray-600 mt-1">Improve your pronunciation with AI feedback</p>
          </div>
          <Button onClick={() => setView('practice')}>
            <Mic className="h-4 w-4 mr-2" />
            Start Practice
          </Button>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card>
            <CardHeader className="pb-3">
              <CardDescription>Total Sessions</CardDescription>
              <CardTitle className="text-3xl text-blue-600">
                {sessions?.length || 0}
              </CardTitle>
            </CardHeader>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardDescription>Avg. Pronunciation</CardDescription>
              <CardTitle className="text-3xl text-green-600">
                {sessions && sessions.length > 0
                  ? Math.round(
                      sessions.reduce((acc: number, s: any) => acc + (s.pronunciation_score || 0), 0) /
                        sessions.length
                    )
                  : 0}
                %
              </CardTitle>
            </CardHeader>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardDescription>Avg. Fluency</CardDescription>
              <CardTitle className="text-3xl text-purple-600">
                {sessions && sessions.length > 0
                  ? Math.round(
                      sessions.reduce((acc: number, s: any) => acc + (s.fluency_score || 0), 0) /
                        sessions.length
                    )
                  : 0}
                %
              </CardTitle>
            </CardHeader>
          </Card>
        </div>

        {/* Recent Sessions */}
        <div>
          <h2 className="text-xl font-bold mb-4">Recent Sessions</h2>
          {isLoading ? (
            <Card>
              <CardContent className="py-12 text-center">
                <LoadingSpinner size="lg" />
              </CardContent>
            </Card>
          ) : sessions && sessions.length > 0 ? (
            <div className="space-y-4">
              {sessions.slice(0, 5).map((session: any) => (
                <Card key={session.id}>
                  <CardContent className="py-4">
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-3">
                          <h3 className="font-medium">
                            {session.scenario_name || session.session_type}
                          </h3>
                          <Badge variant={session.is_completed ? 'success' : 'warning'}>
                            {session.is_completed ? 'Completed' : 'In Progress'}
                          </Badge>
                        </div>
                        <p className="text-sm text-gray-600 mt-1">
                          {new Date(session.started_at).toLocaleDateString()}
                        </p>
                      </div>
                      <div className="flex items-center gap-4">
                        {session.pronunciation_score && (
                          <div className="text-center">
                            <p className="text-2xl font-bold text-green-600">
                              {Math.round(session.pronunciation_score)}%
                            </p>
                            <p className="text-xs text-gray-500">Pronunciation</p>
                          </div>
                        )}
                        {session.fluency_score && (
                          <div className="text-center">
                            <p className="text-2xl font-bold text-blue-600">
                              {Math.round(session.fluency_score)}%
                            </p>
                            <p className="text-xs text-gray-500">Fluency</p>
                          </div>
                        )}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <Card>
              <CardContent className="py-12 text-center">
                <Mic className="mx-auto h-12 w-12 text-gray-400" />
                <p className="mt-4 text-gray-600">No speaking sessions yet</p>
                <Button onClick={() => setView('practice')} className="mt-4">
                  Start Your First Session
                </Button>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </DashboardLayout>
  );
}

function SpeakingPractice({
  languageId,
  onBack,
}: {
  languageId: number;
  onBack: () => void;
}) {
  const [isRecording, setIsRecording] = useState(false);
  const [recordedAudio, setRecordedAudio] = useState<Blob | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleStartRecording = () => {
    // TODO: Implement actual recording
    setIsRecording(true);
    setTimeout(() => {
      setIsRecording(false);
      // Simulate recorded audio
      setRecordedAudio(new Blob());
    }, 3000);
  };

  const handleStopRecording = () => {
    setIsRecording(false);
  };

  const handleAnalyze = () => {
    setIsAnalyzing(true);
    // TODO: Implement actual analysis
    setTimeout(() => {
      setIsAnalyzing(false);
    }, 2000);
  };

  return (
    <div className="space-y-6 max-w-3xl mx-auto">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Speaking Practice</h2>
        <Button variant="ghost" onClick={onBack}>
          ← Back
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Pronunciation Practice</CardTitle>
          <CardDescription>
            Read the following sentence aloud and get instant feedback
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="p-6 bg-blue-50 rounded-lg text-center">
            <p className="text-2xl font-medium">
              "Hello, how are you today?"
            </p>
            <p className="text-gray-600 mt-2">/ həˈləʊ, haʊ ɑː juː təˈdeɪ /</p>
          </div>

          <div className="flex flex-col items-center gap-4">
            {!isRecording && !recordedAudio && (
              <Button
                size="lg"
                onClick={handleStartRecording}
                className="w-full max-w-xs"
              >
                <Mic className="h-5 w-5 mr-2" />
                Start Recording
              </Button>
            )}

            {isRecording && (
              <div className="text-center">
                <div className="animate-pulse">
                  <div className="w-24 h-24 bg-red-500 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Mic className="h-12 w-12 text-white" />
                  </div>
                </div>
                <p className="text-lg font-medium">Recording...</p>
                <Button
                  variant="danger"
                  onClick={handleStopRecording}
                  className="mt-4"
                >
                  <Square className="h-4 w-4 mr-2" />
                  Stop Recording
                </Button>
              </div>
            )}

            {recordedAudio && !isAnalyzing && (
              <div className="w-full space-y-4">
                <div className="flex items-center gap-3 p-4 bg-gray-50 rounded-lg">
                  <Play className="h-5 w-5 text-gray-600" />
                  <div className="flex-1 h-2 bg-gray-300 rounded-full">
                    <div className="h-2 bg-blue-600 rounded-full w-1/2"></div>
                  </div>
                  <span className="text-sm text-gray-600">0:03</span>
                </div>

                <div className="flex gap-3">
                  <Button
                    variant="outline"
                    onClick={() => setRecordedAudio(null)}
                    className="flex-1"
                  >
                    Record Again
                  </Button>
                  <Button onClick={handleAnalyze} className="flex-1">
                    Analyze Pronunciation
                  </Button>
                </div>
              </div>
            )}

            {isAnalyzing && (
              <Card className="w-full">
                <CardContent className="py-12 text-center">
                  <LoadingSpinner size="lg" />
                  <p className="mt-4 text-gray-600">Analyzing your pronunciation...</p>
                </CardContent>
              </Card>
            )}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Tips for Better Pronunciation</CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="space-y-2 text-gray-600">
            <li className="flex items-start gap-2">
              <span className="text-blue-600">•</span>
              <span>Speak clearly and at a natural pace</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-blue-600">•</span>
              <span>Pay attention to stress and intonation</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-blue-600">•</span>
              <span>Practice in a quiet environment</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-blue-600">•</span>
              <span>Listen to the pronunciation guide before speaking</span>
            </li>
          </ul>
        </CardContent>
      </Card>
    </div>
  );
}
