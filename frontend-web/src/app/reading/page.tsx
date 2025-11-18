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
import { BookOpen, Clock, CheckCircle } from 'lucide-react';

export default function ReadingPage() {
  const { currentLanguage } = useLanguageStore();
  const [selectedMaterial, setSelectedMaterial] = useState<any>(null);

  const { data: materials, isLoading } = useQuery({
    queryKey: ['readingMaterials', currentLanguage?.id],
    queryFn: () => apiClient.getReadingMaterials(currentLanguage?.id || 1),
    enabled: !!currentLanguage,
  });

  if (!currentLanguage) {
    return (
      <DashboardLayout>
        <Card>
          <CardContent className="py-8 text-center">
            <p className="text-gray-600">Please select a language to start reading</p>
          </CardContent>
        </Card>
      </DashboardLayout>
    );
  }

  if (selectedMaterial) {
    return (
      <DashboardLayout>
        <ReadingViewer
          material={selectedMaterial}
          onBack={() => setSelectedMaterial(null)}
        />
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold">Reading</h1>
          <p className="text-gray-600 mt-1">Improve your reading comprehension</p>
        </div>

        {isLoading ? (
          <Card>
            <CardContent className="py-12 text-center">
              <LoadingSpinner size="lg" />
            </CardContent>
          </Card>
        ) : materials && materials.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {materials.map((material: any) => (
              <Card
                key={material.id}
                hover
                className="cursor-pointer"
                onClick={() => setSelectedMaterial(material)}
              >
                {material.image_url && (
                  <div className="aspect-video bg-gray-200 rounded-t-lg overflow-hidden">
                    <img
                      src={material.image_url}
                      alt={material.title}
                      className="w-full h-full object-cover"
                    />
                  </div>
                )}
                <CardHeader>
                  <CardTitle className="text-lg line-clamp-2">{material.title}</CardTitle>
                  {material.subtitle && (
                    <CardDescription className="line-clamp-2">{material.subtitle}</CardDescription>
                  )}
                </CardHeader>
                <CardContent>
                  <div className="flex items-center justify-between text-sm">
                    <div className="flex items-center gap-2">
                      <Badge variant={
                        material.difficulty === 'easy' ? 'success' :
                        material.difficulty === 'medium' ? 'warning' : 'danger'
                      }>
                        {material.difficulty || 'medium'}
                      </Badge>
                      <div className="flex items-center gap-1 text-gray-500">
                        <Clock className="h-4 w-4" />
                        {material.estimated_reading_time_minutes || '5'} min
                      </div>
                    </div>
                    <span className="text-gray-500">{material.word_count} words</span>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        ) : (
          <Card>
            <CardContent className="py-12 text-center">
              <BookOpen className="mx-auto h-12 w-12 text-gray-400" />
              <p className="mt-4 text-gray-600">No reading materials available yet</p>
            </CardContent>
          </Card>
        )}
      </div>
    </DashboardLayout>
  );
}

function ReadingViewer({ material, onBack }: { material: any; onBack: () => void }) {
  const [startTime] = useState(Date.now());
  const [showQuiz, setShowQuiz] = useState(false);

  const handleComplete = () => {
    const timeSpent = Math.floor((Date.now() - startTime) / 1000);
    // TODO: Submit completion
    setShowQuiz(true);
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div className="flex items-center justify-between">
        <Button variant="ghost" onClick={onBack}>
          ← Back to Reading
        </Button>
        <div className="flex items-center gap-2">
          <Badge variant={
            material.difficulty === 'easy' ? 'success' :
            material.difficulty === 'medium' ? 'warning' : 'danger'
          }>
            {material.difficulty}
          </Badge>
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-2xl">{material.title}</CardTitle>
          {material.subtitle && (
            <CardDescription className="text-base">{material.subtitle}</CardDescription>
          )}
          <div className="flex items-center gap-4 text-sm text-gray-600 pt-2">
            {material.author && <span>By {material.author}</span>}
            <span>•</span>
            <span>{material.word_count} words</span>
            <span>•</span>
            <span>{material.estimated_reading_time_minutes} min read</span>
          </div>
        </CardHeader>
        <CardContent>
          <div className="prose prose-lg max-w-none">
            <div className="whitespace-pre-wrap leading-relaxed">
              {material.content}
            </div>
          </div>

          {!showQuiz && (
            <div className="mt-8 pt-6 border-t">
              <Button onClick={handleComplete} size="lg" className="w-full">
                <CheckCircle className="h-5 w-5 mr-2" />
                Mark as Complete
              </Button>
            </div>
          )}

          {showQuiz && material.has_questions && (
            <div className="mt-8 pt-6 border-t">
              <h3 className="text-xl font-bold mb-4">Comprehension Quiz</h3>
              <p className="text-gray-600">Quiz questions would appear here...</p>
              <Button onClick={onBack} className="mt-4">
                Back to Reading List
              </Button>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
