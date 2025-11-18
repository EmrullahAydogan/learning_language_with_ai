'use client';

import { useState } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { apiClient } from '@/lib/api/client';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { LoadingSpinner } from '@/components/ui/Loading';
import { useLanguageStore } from '@/stores/languageStore';
import { CheckCircle, XCircle, Clock, Trophy } from 'lucide-react';

export default function ExercisesPage() {
  const { currentLanguage } = useLanguageStore();
  const [selectedExercise, setSelectedExercise] = useState<any>(null);

  const { data: exercises, isLoading } = useQuery({
    queryKey: ['exercises', currentLanguage?.id],
    queryFn: () => apiClient.getExercises(currentLanguage?.id || 1),
    enabled: !!currentLanguage,
  });

  if (!currentLanguage) {
    return (
      <DashboardLayout>
        <Card>
          <CardContent className="py-8 text-center">
            <p className="text-gray-600">Please select a language to start exercises</p>
          </CardContent>
        </Card>
      </DashboardLayout>
    );
  }

  if (selectedExercise) {
    return (
      <DashboardLayout>
        <ExerciseViewer
          exercise={selectedExercise}
          onBack={() => setSelectedExercise(null)}
        />
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold">Exercises</h1>
          <p className="text-gray-600 mt-1">Practice and improve your skills</p>
        </div>

        {isLoading ? (
          <Card>
            <CardContent className="py-12 text-center">
              <LoadingSpinner size="lg" />
              <p className="mt-4 text-gray-600">Loading exercises...</p>
            </CardContent>
          </Card>
        ) : exercises && exercises.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {exercises.map((exercise: any) => (
              <Card
                key={exercise.id}
                hover
                className="cursor-pointer"
                onClick={() => setSelectedExercise(exercise)}
              >
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <CardTitle className="text-lg">{exercise.title}</CardTitle>
                      <CardDescription className="mt-2">
                        {exercise.description}
                      </CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Badge variant={
                        exercise.difficulty === 'easy' ? 'success' :
                        exercise.difficulty === 'medium' ? 'warning' : 'danger'
                      }>
                        {exercise.difficulty || 'medium'}
                      </Badge>
                      {exercise.estimated_time_minutes && (
                        <div className="flex items-center gap-1 text-sm text-gray-500">
                          <Clock className="h-4 w-4" />
                          {exercise.estimated_time_minutes} min
                        </div>
                      )}
                    </div>
                    <div className="flex items-center gap-1 text-sm text-blue-600">
                      <Trophy className="h-4 w-4" />
                      {exercise.xp_reward} XP
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        ) : (
          <Card>
            <CardContent className="py-12 text-center">
              <p className="text-gray-600">No exercises available yet</p>
              <p className="text-sm text-gray-500 mt-2">
                Check back later for new content!
              </p>
            </CardContent>
          </Card>
        )}
      </div>
    </DashboardLayout>
  );
}

function ExerciseViewer({ exercise, onBack }: { exercise: any; onBack: () => void }) {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState<{ [key: number]: any }>({});
  const [showResults, setShowResults] = useState(false);
  const [results, setResults] = useState<any>(null);
  const [startTime] = useState(Date.now());

  const submitMutation = useMutation({
    mutationFn: (data: { answers: any; time_taken_seconds: number }) =>
      apiClient.submitExercise(exercise.id, data.answers, data.time_taken_seconds),
    onSuccess: (data) => {
      setResults(data);
      setShowResults(true);
    },
  });

  const currentQuestion = exercise.questions?.[currentQuestionIndex];

  const handleAnswer = (answer: any) => {
    setAnswers({
      ...answers,
      [currentQuestion.id]: answer,
    });
  };

  const handleNext = () => {
    if (currentQuestionIndex < exercise.questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    }
  };

  const handlePrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
    }
  };

  const handleSubmit = () => {
    const timeTaken = Math.floor((Date.now() - startTime) / 1000);
    submitMutation.mutate({
      answers,
      time_taken_seconds: timeTaken,
    });
  };

  if (showResults && results) {
    return (
      <div className="space-y-6">
        <Button variant="ghost" onClick={onBack}>
          ← Back to Exercises
        </Button>

        <Card>
          <CardHeader className="text-center">
            <CardTitle className="text-3xl">Exercise Complete!</CardTitle>
            <CardDescription>Here are your results</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="max-w-2xl mx-auto space-y-6">
              <div className="grid grid-cols-3 gap-4">
                <div className="text-center p-4 bg-blue-50 rounded-lg">
                  <p className="text-3xl font-bold text-blue-600">{Math.round(results.score)}%</p>
                  <p className="text-sm text-gray-600 mt-1">Score</p>
                </div>
                <div className="text-center p-4 bg-green-50 rounded-lg">
                  <p className="text-3xl font-bold text-green-600">
                    {results.correct_answers}/{results.total_questions}
                  </p>
                  <p className="text-sm text-gray-600 mt-1">Correct</p>
                </div>
                <div className="text-center p-4 bg-purple-50 rounded-lg">
                  <p className="text-3xl font-bold text-purple-600">+{results.xp_earned}</p>
                  <p className="text-sm text-gray-600 mt-1">XP Earned</p>
                </div>
              </div>

              <div className="flex gap-3">
                <Button onClick={onBack} className="flex-1">
                  Back to Exercises
                </Button>
                <Button
                  variant="outline"
                  onClick={() => {
                    setShowResults(false);
                    setCurrentQuestionIndex(0);
                    setAnswers({});
                    setResults(null);
                  }}
                  className="flex-1"
                >
                  Try Again
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (!currentQuestion) {
    return (
      <Card>
        <CardContent className="py-12 text-center">
          <p className="text-gray-600">No questions available</p>
          <Button onClick={onBack} className="mt-4">
            Back to Exercises
          </Button>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <Button variant="ghost" onClick={onBack}>
          ← Back to Exercises
        </Button>
        <div className="flex items-center gap-4">
          <Badge variant="info">
            Question {currentQuestionIndex + 1} of {exercise.questions.length}
          </Badge>
          <Badge>
            {Object.keys(answers).length} answered
          </Badge>
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>{exercise.title}</CardTitle>
          {exercise.instructions && (
            <CardDescription>{exercise.instructions}</CardDescription>
          )}
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-medium mb-4">{currentQuestion.question_text}</h3>

              {/* Multiple Choice */}
              {currentQuestion.answer_data.options && (
                <div className="space-y-3">
                  {currentQuestion.answer_data.options.map((option: string, index: number) => (
                    <button
                      key={index}
                      onClick={() => handleAnswer(index)}
                      className={`w-full p-4 text-left rounded-lg border-2 transition ${
                        answers[currentQuestion.id] === index
                          ? 'border-blue-500 bg-blue-50'
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                    >
                      {option}
                    </button>
                  ))}
                </div>
              )}

              {/* Fill in the Blank */}
              {!currentQuestion.answer_data.options && (
                <input
                  type="text"
                  value={answers[currentQuestion.id] || ''}
                  onChange={(e) => handleAnswer(e.target.value)}
                  className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:outline-none"
                  placeholder="Type your answer here..."
                />
              )}
            </div>

            {currentQuestion.explanation && answers[currentQuestion.id] !== undefined && (
              <div className="p-4 bg-gray-50 rounded-lg">
                <p className="text-sm text-gray-600">{currentQuestion.explanation}</p>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      <div className="flex gap-3">
        <Button
          variant="outline"
          onClick={handlePrevious}
          disabled={currentQuestionIndex === 0}
        >
          Previous
        </Button>
        <div className="flex-1" />
        {currentQuestionIndex < exercise.questions.length - 1 ? (
          <Button onClick={handleNext}>
            Next
          </Button>
        ) : (
          <Button
            onClick={handleSubmit}
            disabled={Object.keys(answers).length === 0 || submitMutation.isPending}
            isLoading={submitMutation.isPending}
          >
            Submit Exercise
          </Button>
        )}
      </div>
    </div>
  );
}
