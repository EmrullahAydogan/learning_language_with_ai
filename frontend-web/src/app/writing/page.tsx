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
import { Edit3, Send, Eye } from 'lucide-react';

export default function WritingPage() {
  const { currentLanguage } = useLanguageStore();
  const [view, setView] = useState<'list' | 'write' | 'view'>('list');
  const [selectedSubmission, setSelectedSubmission] = useState<any>(null);

  const { data: submissions, isLoading } = useQuery({
    queryKey: ['writingSubmissions', currentLanguage?.id],
    queryFn: () => apiClient.getWritingSubmissions(currentLanguage?.id),
    enabled: !!currentLanguage,
  });

  if (!currentLanguage) {
    return (
      <DashboardLayout>
        <Card>
          <CardContent className="py-8 text-center">
            <p className="text-gray-600">Please select a language to start writing</p>
          </CardContent>
        </Card>
      </DashboardLayout>
    );
  }

  if (view === 'write') {
    return (
      <DashboardLayout>
        <WritingEditor
          languageId={currentLanguage.id}
          onBack={() => setView('list')}
          onSubmitted={() => setView('list')}
        />
      </DashboardLayout>
    );
  }

  if (view === 'view' && selectedSubmission) {
    return (
      <DashboardLayout>
        <WritingViewer
          submission={selectedSubmission}
          onBack={() => {
            setView('list');
            setSelectedSubmission(null);
          }}
        />
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold">Writing</h1>
            <p className="text-gray-600 mt-1">Improve your writing with AI feedback</p>
          </div>
          <Button onClick={() => setView('write')}>
            <Edit3 className="h-4 w-4 mr-2" />
            New Writing
          </Button>
        </div>

        {isLoading ? (
          <Card>
            <CardContent className="py-12 text-center">
              <LoadingSpinner size="lg" />
            </CardContent>
          </Card>
        ) : submissions && submissions.length > 0 ? (
          <div className="space-y-4">
            {submissions.map((submission: any) => (
              <Card
                key={submission.id}
                hover
                className="cursor-pointer"
                onClick={() => {
                  setSelectedSubmission(submission);
                  setView('view');
                }}
              >
                <CardContent className="py-4">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <h3 className="font-medium text-lg">
                        {submission.title || 'Untitled'}
                      </h3>
                      <p className="text-sm text-gray-600 mt-1 line-clamp-2">
                        {submission.content.substring(0, 150)}...
                      </p>
                      <div className="flex items-center gap-3 mt-2 text-sm text-gray-500">
                        <span>{submission.word_count} words</span>
                        <span>•</span>
                        <span>{new Date(submission.submitted_at).toLocaleDateString()}</span>
                        <Badge>{submission.writing_type}</Badge>
                      </div>
                    </div>
                    <Button variant="ghost" size="sm">
                      <Eye className="h-4 w-4" />
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        ) : (
          <Card>
            <CardContent className="py-12 text-center">
              <Edit3 className="mx-auto h-12 w-12 text-gray-400" />
              <p className="mt-4 text-gray-600">No writings yet</p>
              <Button onClick={() => setView('write')} className="mt-4">
                Start Writing
              </Button>
            </CardContent>
          </Card>
        )}
      </div>
    </DashboardLayout>
  );
}

function WritingEditor({
  languageId,
  onBack,
  onSubmitted,
}: {
  languageId: number;
  onBack: () => void;
  onSubmitted: () => void;
}) {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [writingType, setWritingType] = useState('essay');

  const submitMutation = useMutation({
    mutationFn: (data: any) => apiClient.submitWriting(data),
    onSuccess: () => {
      onSubmitted();
    },
  });

  const handleSubmit = () => {
    submitMutation.mutate({
      language_id: languageId,
      title: title || undefined,
      content,
      writing_type: writingType,
      time_spent_seconds: 0,
    });
  };

  const wordCount = content.trim().split(/\s+/).filter(Boolean).length;

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">New Writing</h2>
        <Button variant="ghost" onClick={onBack}>
          Cancel
        </Button>
      </div>

      <Card>
        <CardContent className="space-y-4 pt-6">
          <div>
            <label className="block text-sm font-medium mb-2">Writing Type</label>
            <select
              value={writingType}
              onChange={(e) => setWritingType(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="essay">Essay</option>
              <option value="email">Email</option>
              <option value="creative">Creative Writing</option>
              <option value="diary">Diary Entry</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Title (Optional)</label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Enter a title..."
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <div>
            <div className="flex items-center justify-between mb-2">
              <label className="block text-sm font-medium">Content</label>
              <span className="text-sm text-gray-500">{wordCount} words</span>
            </div>
            <textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder="Start writing..."
              rows={15}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            />
          </div>

          <Button
            onClick={handleSubmit}
            disabled={!content.trim() || submitMutation.isPending}
            isLoading={submitMutation.isPending}
            size="lg"
            className="w-full"
          >
            <Send className="h-4 w-4 mr-2" />
            Submit for Review
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}

function WritingViewer({
  submission,
  onBack,
}: {
  submission: any;
  onBack: () => void;
}) {
  const { data: evaluation, isLoading } = useQuery({
    queryKey: ['writingEvaluation', submission.id],
    queryFn: () => apiClient.getWritingEvaluation(submission.id),
  });

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Writing Details</h2>
        <Button variant="ghost" onClick={onBack}>
          ← Back
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>{submission.title || 'Untitled'}</CardTitle>
          <CardDescription>
            {new Date(submission.submitted_at).toLocaleDateString()} • {submission.word_count} words
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="prose max-w-none">
            <div className="whitespace-pre-wrap">{submission.content}</div>
          </div>
        </CardContent>
      </Card>

      {isLoading ? (
        <Card>
          <CardContent className="py-12 text-center">
            <LoadingSpinner size="lg" />
            <p className="mt-4 text-gray-600">Loading evaluation...</p>
          </CardContent>
        </Card>
      ) : evaluation ? (
        <Card>
          <CardHeader>
            <CardTitle>AI Feedback</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="grid grid-cols-4 gap-4">
              {[
                { label: 'Overall', score: evaluation.overall_score, color: 'blue' },
                { label: 'Grammar', score: evaluation.grammar_score, color: 'green' },
                { label: 'Vocabulary', score: evaluation.vocabulary_score, color: 'purple' },
                { label: 'Coherence', score: evaluation.coherence_score, color: 'orange' },
              ].map((item) => (
                <div key={item.label} className="text-center p-4 bg-gray-50 rounded-lg">
                  <p className={`text-3xl font-bold text-${item.color}-600`}>
                    {Math.round(item.score || 0)}%
                  </p>
                  <p className="text-sm text-gray-600 mt-1">{item.label}</p>
                </div>
              ))}
            </div>

            {evaluation.ai_feedback && (
              <div>
                <h4 className="font-medium mb-2">Feedback</h4>
                <p className="text-gray-700">{evaluation.ai_feedback}</p>
              </div>
            )}

            {evaluation.corrected_version && (
              <div>
                <h4 className="font-medium mb-2">Corrected Version</h4>
                <div className="p-4 bg-gray-50 rounded-lg">
                  <p className="whitespace-pre-wrap text-gray-700">{evaluation.corrected_version}</p>
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      ) : null}
    </div>
  );
}
