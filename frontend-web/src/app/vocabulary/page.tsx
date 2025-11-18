'use client';

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api/client';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { LoadingSpinner } from '@/components/ui/Loading';
import { useLanguageStore } from '@/stores/languageStore';
import { BookOpen, Plus, BarChart } from 'lucide-react';

export default function VocabularyPage() {
  const { currentLanguage } = useLanguageStore();
  const [view, setView] = useState<'overview' | 'review' | 'learn'>('overview');

  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['vocabularyStats', currentLanguage?.id],
    queryFn: () => apiClient.getVocabularyStats(currentLanguage?.id || 1),
    enabled: !!currentLanguage,
  });

  const { data: dueCards, isLoading: dueLoading } = useQuery({
    queryKey: ['dueFlashcards', currentLanguage?.id],
    queryFn: () => apiClient.getDueFlashcards(currentLanguage?.id || 1),
    enabled: !!currentLanguage && view === 'review',
  });

  const { data: newWords, isLoading: newLoading } = useQuery({
    queryKey: ['newVocabulary', currentLanguage?.id],
    queryFn: () => apiClient.getNewVocabulary(currentLanguage?.id || 1, undefined, undefined, 10),
    enabled: !!currentLanguage && view === 'learn',
  });

  if (!currentLanguage) {
    return (
      <DashboardLayout>
        <Card>
          <CardContent className="py-8 text-center">
            <p className="text-gray-600">Please select a language to start learning vocabulary</p>
          </CardContent>
        </Card>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold">Vocabulary</h1>
            <p className="text-gray-600 mt-1">Learn and review words with spaced repetition</p>
          </div>
        </div>

        {/* Statistics Overview */}
        {view === 'overview' && (
          <>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <Card>
                <CardHeader className="pb-3">
                  <CardDescription>Total Words</CardDescription>
                  <CardTitle className="text-3xl text-blue-600">
                    {statsLoading ? '...' : stats?.total_words || 0}
                  </CardTitle>
                </CardHeader>
              </Card>

              <Card>
                <CardHeader className="pb-3">
                  <CardDescription>Mastered</CardDescription>
                  <CardTitle className="text-3xl text-green-600">
                    {statsLoading ? '...' : stats?.mastered || 0}
                  </CardTitle>
                </CardHeader>
              </Card>

              <Card>
                <CardHeader className="pb-3">
                  <CardDescription>Learning</CardDescription>
                  <CardTitle className="text-3xl text-orange-600">
                    {statsLoading ? '...' : stats?.learning || 0}
                  </CardTitle>
                </CardHeader>
              </Card>

              <Card>
                <CardHeader className="pb-3">
                  <CardDescription>Due for Review</CardDescription>
                  <CardTitle className="text-3xl text-red-600">
                    {statsLoading ? '...' : stats?.due_for_review || 0}
                  </CardTitle>
                </CardHeader>
              </Card>
            </div>

            {/* Action Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Card
                hover
                className="cursor-pointer"
                onClick={() => setView('review')}
              >
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-blue-100">
                        <BookOpen className="h-6 w-6 text-blue-600" />
                      </div>
                      <div>
                        <CardTitle>Review Flashcards</CardTitle>
                        <CardDescription>
                          {stats?.due_for_review || 0} cards due today
                        </CardDescription>
                      </div>
                    </div>
                    <Badge variant="info">{stats?.due_for_review || 0}</Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-600">
                    Review words using spaced repetition to improve retention
                  </p>
                </CardContent>
              </Card>

              <Card
                hover
                className="cursor-pointer"
                onClick={() => setView('learn')}
              >
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-green-100">
                        <Plus className="h-6 w-6 text-green-600" />
                      </div>
                      <div>
                        <CardTitle>Learn New Words</CardTitle>
                        <CardDescription>
                          Expand your vocabulary
                        </CardDescription>
                      </div>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-600">
                    Add new words to your learning collection
                  </p>
                </CardContent>
              </Card>
            </div>
          </>
        )}

        {/* Review Mode */}
        {view === 'review' && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <Button variant="ghost" onClick={() => setView('overview')}>
                ← Back to Overview
              </Button>
            </div>

            {dueLoading ? (
              <Card>
                <CardContent className="py-12 text-center">
                  <LoadingSpinner size="lg" />
                  <p className="mt-4 text-gray-600">Loading flashcards...</p>
                </CardContent>
              </Card>
            ) : dueCards && dueCards.length > 0 ? (
              <FlashcardReview cards={dueCards} />
            ) : (
              <Card>
                <CardContent className="py-12 text-center">
                  <BookOpen className="mx-auto h-12 w-12 text-gray-400" />
                  <p className="mt-4 text-gray-600">No cards due for review!</p>
                  <p className="text-sm text-gray-500">Great job! Come back later for more practice.</p>
                  <Button onClick={() => setView('overview')} className="mt-4">
                    Back to Overview
                  </Button>
                </CardContent>
              </Card>
            )}
          </div>
        )}

        {/* Learn New Words Mode */}
        {view === 'learn' && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <Button variant="ghost" onClick={() => setView('overview')}>
                ← Back to Overview
              </Button>
            </div>

            {newLoading ? (
              <Card>
                <CardContent className="py-12 text-center">
                  <LoadingSpinner size="lg" />
                  <p className="mt-4 text-gray-600">Loading new words...</p>
                </CardContent>
              </Card>
            ) : newWords && newWords.length > 0 ? (
              <NewWordsLearning words={newWords} />
            ) : (
              <Card>
                <CardContent className="py-12 text-center">
                  <Plus className="mx-auto h-12 w-12 text-gray-400" />
                  <p className="mt-4 text-gray-600">No new words available</p>
                  <p className="text-sm text-gray-500">All available words have been learned!</p>
                  <Button onClick={() => setView('overview')} className="mt-4">
                    Back to Overview
                  </Button>
                </CardContent>
              </Card>
            )}
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}

// Flashcard Review Component
function FlashcardReview({ cards }: { cards: any[] }) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [showAnswer, setShowAnswer] = useState(false);
  const [startTime, setStartTime] = useState(Date.now());

  const currentCard = cards[currentIndex];

  const handleRating = async (quality: number) => {
    const timeTaken = Math.floor((Date.now() - startTime) / 1000);

    try {
      await apiClient.reviewFlashcard(
        currentCard.vocabulary_id,
        quality,
        timeTaken
      );

      // Move to next card
      if (currentIndex < cards.length - 1) {
        setCurrentIndex(currentIndex + 1);
        setShowAnswer(false);
        setStartTime(Date.now());
      } else {
        // Review complete
        window.location.reload();
      }
    } catch (error) {
      console.error('Error reviewing flashcard:', error);
    }
  };

  if (!currentCard) return null;

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <p className="text-sm text-gray-600">
          Card {currentIndex + 1} of {cards.length}
        </p>
        <Badge variant="info">{currentCard.status}</Badge>
      </div>

      <Card className="min-h-[400px]">
        <CardContent className="flex flex-col items-center justify-center py-12">
          <div className="text-center space-y-6">
            <div>
              <p className="text-sm text-gray-500 mb-2">Word</p>
              <h2 className="text-5xl font-bold">{currentCard.vocabulary.word}</h2>
              {currentCard.vocabulary.pronunciation && (
                <p className="text-lg text-gray-500 mt-2">{currentCard.vocabulary.pronunciation}</p>
              )}
            </div>

            {showAnswer ? (
              <div className="space-y-4 pt-6 border-t">
                <div>
                  <p className="text-sm text-gray-500 mb-1">Translation</p>
                  <p className="text-2xl font-semibold text-blue-600">
                    {currentCard.vocabulary.translation}
                  </p>
                </div>

                {currentCard.vocabulary.example_sentence && (
                  <div>
                    <p className="text-sm text-gray-500 mb-1">Example</p>
                    <p className="text-lg italic">{currentCard.vocabulary.example_sentence}</p>
                  </div>
                )}

                {currentCard.vocabulary.definition && (
                  <div>
                    <p className="text-sm text-gray-500 mb-1">Definition</p>
                    <p className="text-base">{currentCard.vocabulary.definition}</p>
                  </div>
                )}
              </div>
            ) : (
              <Button onClick={() => setShowAnswer(true)} size="lg">
                Show Answer
              </Button>
            )}
          </div>
        </CardContent>
      </Card>

      {showAnswer && (
        <Card>
          <CardHeader>
            <CardTitle>How well did you know this word?</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
              <Button variant="danger" onClick={() => handleRating(0)}>
                Not at all
              </Button>
              <Button variant="outline" onClick={() => handleRating(2)}>
                Barely
              </Button>
              <Button variant="outline" onClick={() => handleRating(3)}>
                Okay
              </Button>
              <Button variant="secondary" onClick={() => handleRating(4)}>
                Good
              </Button>
              <Button variant="primary" onClick={() => handleRating(5)}>
                Perfect!
              </Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

// New Words Learning Component
function NewWordsLearning({ words }: { words: any[] }) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const currentWord = words[currentIndex];

  const handleNext = () => {
    if (currentIndex < words.length - 1) {
      setCurrentIndex(currentIndex + 1);
    } else {
      window.location.reload();
    }
  };

  const handleAddToReview = async () => {
    try {
      // Add the word to review by rating it
      await apiClient.reviewFlashcard(currentWord.id, 3, 0);
      handleNext();
    } catch (error) {
      console.error('Error adding word:', error);
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <p className="text-sm text-gray-600">
          Word {currentIndex + 1} of {words.length}
        </p>
      </div>

      <Card>
        <CardContent className="py-12">
          <div className="max-w-2xl mx-auto space-y-6">
            <div className="text-center">
              <h2 className="text-5xl font-bold mb-2">{currentWord.word}</h2>
              {currentWord.pronunciation && (
                <p className="text-xl text-gray-500">{currentWord.pronunciation}</p>
              )}
            </div>

            <div className="space-y-4 pt-6 border-t">
              <div>
                <p className="text-sm font-medium text-gray-500 mb-1">Translation</p>
                <p className="text-2xl text-blue-600">{currentWord.translation}</p>
              </div>

              {currentWord.part_of_speech && (
                <div>
                  <p className="text-sm font-medium text-gray-500 mb-1">Part of Speech</p>
                  <Badge>{currentWord.part_of_speech}</Badge>
                </div>
              )}

              {currentWord.definition && (
                <div>
                  <p className="text-sm font-medium text-gray-500 mb-1">Definition</p>
                  <p className="text-lg">{currentWord.definition}</p>
                </div>
              )}

              {currentWord.example_sentence && (
                <div>
                  <p className="text-sm font-medium text-gray-500 mb-1">Example</p>
                  <p className="text-lg italic">&ldquo;{currentWord.example_sentence}&rdquo;</p>
                  {currentWord.example_translation && (
                    <p className="text-base text-gray-600 mt-1">{currentWord.example_translation}</p>
                  )}
                </div>
              )}
            </div>

            <div className="flex gap-3 pt-6">
              <Button variant="outline" onClick={handleNext} className="flex-1">
                Skip
              </Button>
              <Button onClick={handleAddToReview} className="flex-1">
                Add to Review
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
