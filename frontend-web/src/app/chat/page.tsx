'use client';

import { useState, useRef, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api/client';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Badge } from '@/components/ui/Badge';
import { LoadingSpinner } from '@/components/ui/Loading';
import { useLanguageStore } from '@/stores/languageStore';
import { MessageCircle, Send, Plus, Bot, User } from 'lucide-react';

export default function ChatPage() {
  const { currentLanguage } = useLanguageStore();
  const [selectedConversation, setSelectedConversation] = useState<any>(null);
  const [showNewConversation, setShowNewConversation] = useState(false);

  const { data: conversations, isLoading } = useQuery({
    queryKey: ['conversations', currentLanguage?.id],
    queryFn: () => apiClient.getConversations(currentLanguage?.id),
    enabled: !!currentLanguage,
  });

  if (!currentLanguage) {
    return (
      <DashboardLayout>
        <Card>
          <CardContent className="py-8 text-center">
            <p className="text-gray-600">Please select a language to start chatting</p>
          </CardContent>
        </Card>
      </DashboardLayout>
    );
  }

  if (selectedConversation) {
    return (
      <DashboardLayout>
        <ChatInterface
          conversation={selectedConversation}
          onBack={() => setSelectedConversation(null)}
        />
      </DashboardLayout>
    );
  }

  if (showNewConversation) {
    return (
      <DashboardLayout>
        <NewConversationForm
          languageId={currentLanguage.id}
          onBack={() => setShowNewConversation(false)}
          onCreated={(conv) => {
            setSelectedConversation(conv);
            setShowNewConversation(false);
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
            <h1 className="text-3xl font-bold">AI Chat Partner</h1>
            <p className="text-gray-600 mt-1">Practice conversation with AI</p>
          </div>
          <Button onClick={() => setShowNewConversation(true)}>
            <Plus className="h-4 w-4 mr-2" />
            New Conversation
          </Button>
        </div>

        {isLoading ? (
          <Card>
            <CardContent className="py-12 text-center">
              <LoadingSpinner size="lg" />
              <p className="mt-4 text-gray-600">Loading conversations...</p>
            </CardContent>
          </Card>
        ) : conversations && conversations.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {conversations.map((conv: any) => (
              <Card
                key={conv.id}
                hover
                className="cursor-pointer"
                onClick={() => setSelectedConversation(conv)}
              >
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <CardTitle className="text-lg">
                        {conv.scenario_name || 'Free Conversation'}
                      </CardTitle>
                      <CardDescription className="mt-2">
                        {conv.conversation_type === 'scenario' ? 'Scenario' : 'Free Chat'}
                      </CardDescription>
                    </div>
                    <Badge variant={conv.is_active ? 'success' : 'default'}>
                      {conv.is_active ? 'Active' : 'Ended'}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center justify-between text-sm text-gray-500">
                    <span>{conv.messages?.length || 0} messages</span>
                    <span>{new Date(conv.started_at).toLocaleDateString()}</span>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        ) : (
          <Card>
            <CardContent className="py-12 text-center">
              <MessageCircle className="mx-auto h-12 w-12 text-gray-400" />
              <p className="mt-4 text-gray-600">No conversations yet</p>
              <p className="text-sm text-gray-500 mt-2">
                Start a new conversation to practice!
              </p>
              <Button onClick={() => setShowNewConversation(true)} className="mt-4">
                <Plus className="h-4 w-4 mr-2" />
                Start Chatting
              </Button>
            </CardContent>
          </Card>
        )}
      </div>
    </DashboardLayout>
  );
}

function NewConversationForm({
  languageId,
  onBack,
  onCreated,
}: {
  languageId: number;
  onBack: () => void;
  onCreated: (conv: any) => void;
}) {
  const [conversationType, setConversationType] = useState('free');
  const [scenario, setScenario] = useState('');
  const [character, setCharacter] = useState('friendly_tutor');

  const createMutation = useMutation({
    mutationFn: (data: any) => apiClient.createConversation(data),
    onSuccess: (data) => {
      onCreated(data);
    },
  });

  const scenarios = [
    { value: 'restaurant', label: 'Restaurant' },
    { value: 'airport', label: 'Airport' },
    { value: 'job_interview', label: 'Job Interview' },
    { value: 'shopping', label: 'Shopping' },
    { value: 'doctor', label: 'Doctor Visit' },
  ];

  const characters = [
    { value: 'friendly_tutor', label: 'Friendly Tutor' },
    { value: 'strict_teacher', label: 'Strict Teacher' },
    { value: 'native_speaker', label: 'Native Speaker' },
    { value: 'professional', label: 'Professional' },
  ];

  const handleSubmit = () => {
    createMutation.mutate({
      language_id: languageId,
      conversation_type: conversationType,
      scenario_name: conversationType === 'scenario' ? scenario : undefined,
      ai_character: character,
      difficulty_level: 'medium',
    });
  };

  return (
    <div className="space-y-6 max-w-2xl mx-auto">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">New Conversation</h2>
        <Button variant="ghost" onClick={onBack}>
          Cancel
        </Button>
      </div>

      <Card>
        <CardContent className="space-y-6 pt-6">
          <div>
            <label className="block text-sm font-medium mb-3">Conversation Type</label>
            <div className="grid grid-cols-2 gap-3">
              <button
                onClick={() => setConversationType('free')}
                className={`p-4 rounded-lg border-2 transition ${
                  conversationType === 'free'
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <p className="font-medium">Free Conversation</p>
                <p className="text-sm text-gray-600 mt-1">Chat about anything</p>
              </button>
              <button
                onClick={() => setConversationType('scenario')}
                className={`p-4 rounded-lg border-2 transition ${
                  conversationType === 'scenario'
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <p className="font-medium">Scenario</p>
                <p className="text-sm text-gray-600 mt-1">Practice specific situations</p>
              </button>
            </div>
          </div>

          {conversationType === 'scenario' && (
            <div>
              <label className="block text-sm font-medium mb-3">Choose Scenario</label>
              <select
                value={scenario}
                onChange={(e) => setScenario(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Select a scenario...</option>
                {scenarios.map((s) => (
                  <option key={s.value} value={s.value}>
                    {s.label}
                  </option>
                ))}
              </select>
            </div>
          )}

          <div>
            <label className="block text-sm font-medium mb-3">AI Character</label>
            <select
              value={character}
              onChange={(e) => setCharacter(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              {characters.map((c) => (
                <option key={c.value} value={c.value}>
                  {c.label}
                </option>
              ))}
            </select>
          </div>

          <Button
            onClick={handleSubmit}
            disabled={conversationType === 'scenario' && !scenario}
            isLoading={createMutation.isPending}
            className="w-full"
          >
            Start Conversation
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}

function ChatInterface({
  conversation,
  onBack,
}: {
  conversation: any;
  onBack: () => void;
}) {
  const [message, setMessage] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const queryClient = useQueryClient();

  const { data: fullConversation } = useQuery({
    queryKey: ['conversation', conversation.id],
    queryFn: () => apiClient.getConversation(conversation.id),
    refetchInterval: 2000, // Refresh every 2 seconds
  });

  const sendMutation = useMutation({
    mutationFn: (content: string) => apiClient.sendMessage(conversation.id, content),
    onSuccess: () => {
      setMessage('');
      queryClient.invalidateQueries({ queryKey: ['conversation', conversation.id] });
    },
  });

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [fullConversation?.messages]);

  const handleSend = () => {
    if (message.trim()) {
      sendMutation.mutate(message);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const messages = fullConversation?.messages || conversation.messages || [];

  return (
    <div className="flex flex-col h-[calc(100vh-12rem)]">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <Button variant="ghost" onClick={onBack}>
            ← Back
          </Button>
          <div>
            <h2 className="text-xl font-bold">
              {conversation.scenario_name || 'Free Conversation'}
            </h2>
            <p className="text-sm text-gray-600">{conversation.ai_character}</p>
          </div>
        </div>
        <Badge variant={conversation.is_active ? 'success' : 'default'}>
          {conversation.is_active ? 'Active' : 'Ended'}
        </Badge>
      </div>

      <Card className="flex-1 flex flex-col">
        <CardContent className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages
            .filter((msg: any) => msg.role !== 'system')
            .map((msg: any) => (
              <div
                key={msg.id}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[70%] rounded-lg p-4 ${
                    msg.role === 'user'
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-900'
                  }`}
                >
                  <div className="flex items-start gap-2">
                    {msg.role === 'assistant' && (
                      <Bot className="h-5 w-5 mt-0.5 flex-shrink-0" />
                    )}
                    {msg.role === 'user' && (
                      <User className="h-5 w-5 mt-0.5 flex-shrink-0" />
                    )}
                    <div className="flex-1">
                      <p className="whitespace-pre-wrap">{msg.content}</p>
                      {msg.corrections && msg.corrections.length > 0 && (
                        <div className="mt-2 pt-2 border-t border-gray-200">
                          <p className="text-xs font-medium mb-1">Corrections:</p>
                          {msg.corrections.map((corr: any, idx: number) => (
                            <p key={idx} className="text-xs">
                              "{corr.original}" → "{corr.corrected}"
                            </p>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          {sendMutation.isPending && (
            <div className="flex justify-start">
              <div className="bg-gray-100 rounded-lg p-4">
                <LoadingSpinner size="sm" />
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </CardContent>

        <div className="border-t p-4">
          <div className="flex gap-2">
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message..."
              disabled={!conversation.is_active || sendMutation.isPending}
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <Button
              onClick={handleSend}
              disabled={!message.trim() || !conversation.is_active || sendMutation.isPending}
              isLoading={sendMutation.isPending}
            >
              <Send className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </Card>
    </div>
  );
}
