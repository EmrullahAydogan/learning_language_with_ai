'use client';

import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api/client';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { LoadingSpinner } from '@/components/ui/Loading';
import { useAuthStore } from '@/stores/authStore';
import { User, Bell, Globe, Shield, Save } from 'lucide-react';

export default function SettingsPage() {
  const { user } = useAuthStore();
  const [activeTab, setActiveTab] = useState<'profile' | 'preferences' | 'languages' | 'account'>('profile');

  const tabs = [
    { id: 'profile', label: 'Profile', icon: User },
    { id: 'preferences', label: 'Preferences', icon: Bell },
    { id: 'languages', label: 'Languages', icon: Globe },
    { id: 'account', label: 'Account', icon: Shield },
  ];

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold">Settings</h1>
          <p className="text-gray-600 mt-1">Manage your account and preferences</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Tabs */}
          <Card className="lg:col-span-1">
            <CardContent className="p-4">
              <nav className="space-y-1">
                {tabs.map((tab) => {
                  const Icon = tab.icon;
                  return (
                    <button
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id as any)}
                      className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg transition ${
                        activeTab === tab.id
                          ? 'bg-blue-50 text-blue-600'
                          : 'text-gray-700 hover:bg-gray-50'
                      }`}
                    >
                      <Icon className="h-5 w-5" />
                      <span className="font-medium">{tab.label}</span>
                    </button>
                  );
                })}
              </nav>
            </CardContent>
          </Card>

          {/* Content */}
          <div className="lg:col-span-3">
            {activeTab === 'profile' && <ProfileSettings />}
            {activeTab === 'preferences' && <PreferencesSettings />}
            {activeTab === 'languages' && <LanguagesSettings />}
            {activeTab === 'account' && <AccountSettings />}
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}

function ProfileSettings() {
  const queryClient = useQueryClient();
  const { data: profile, isLoading } = useQuery({
    queryKey: ['userProfile'],
    queryFn: () => apiClient.getUserProfile(),
  });

  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    bio: '',
  });

  const updateMutation = useMutation({
    mutationFn: (data: any) => apiClient.updateProfile(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['userProfile'] });
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    updateMutation.mutate(formData);
  };

  if (isLoading) {
    return (
      <Card>
        <CardContent className="py-12 text-center">
          <LoadingSpinner size="lg" />
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Profile Information</CardTitle>
        <CardDescription>Update your personal information</CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            label="First Name"
            value={formData.first_name}
            onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
            placeholder="John"
          />
          <Input
            label="Last Name"
            value={formData.last_name}
            onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
            placeholder="Doe"
          />
          <div>
            <label className="block text-sm font-medium mb-2">Bio</label>
            <textarea
              value={formData.bio}
              onChange={(e) => setFormData({ ...formData, bio: e.target.value })}
              rows={4}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Tell us about yourself..."
            />
          </div>
          <Button type="submit" isLoading={updateMutation.isPending}>
            <Save className="h-4 w-4 mr-2" />
            Save Changes
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}

function PreferencesSettings() {
  const queryClient = useQueryClient();
  const { data: preferences, isLoading } = useQuery({
    queryKey: ['userPreferences'],
    queryFn: () => apiClient.getPreferences(),
  });

  const [formData, setFormData] = useState({
    daily_goal_minutes: 15,
    daily_goal_xp: 50,
    new_words_per_day: 10,
    email_notifications: true,
    push_notifications: true,
    reminder_time: '',
  });

  const updateMutation = useMutation({
    mutationFn: (data: any) => apiClient.updatePreferences(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['userPreferences'] });
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    updateMutation.mutate(formData);
  };

  if (isLoading) {
    return (
      <Card>
        <CardContent className="py-12 text-center">
          <LoadingSpinner size="lg" />
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Learning Preferences</CardTitle>
        <CardDescription>Customize your learning experience</CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <h3 className="font-medium mb-4">Daily Goals</h3>
            <div className="space-y-4">
              <Input
                label="Study Time Goal (minutes)"
                type="number"
                value={formData.daily_goal_minutes}
                onChange={(e) =>
                  setFormData({ ...formData, daily_goal_minutes: parseInt(e.target.value) })
                }
              />
              <Input
                label="XP Goal"
                type="number"
                value={formData.daily_goal_xp}
                onChange={(e) =>
                  setFormData({ ...formData, daily_goal_xp: parseInt(e.target.value) })
                }
              />
              <Input
                label="New Words Per Day"
                type="number"
                value={formData.new_words_per_day}
                onChange={(e) =>
                  setFormData({ ...formData, new_words_per_day: parseInt(e.target.value) })
                }
              />
            </div>
          </div>

          <div>
            <h3 className="font-medium mb-4">Notifications</h3>
            <div className="space-y-3">
              <label className="flex items-center gap-3">
                <input
                  type="checkbox"
                  checked={formData.email_notifications}
                  onChange={(e) =>
                    setFormData({ ...formData, email_notifications: e.target.checked })
                  }
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span className="text-sm">Email Notifications</span>
              </label>
              <label className="flex items-center gap-3">
                <input
                  type="checkbox"
                  checked={formData.push_notifications}
                  onChange={(e) =>
                    setFormData({ ...formData, push_notifications: e.target.checked })
                  }
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span className="text-sm">Push Notifications</span>
              </label>
            </div>
          </div>

          <Button type="submit" isLoading={updateMutation.isPending}>
            <Save className="h-4 w-4 mr-2" />
            Save Preferences
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}

function LanguagesSettings() {
  const { data: languages } = useQuery({
    queryKey: ['languages'],
    queryFn: () => apiClient.getLanguages(),
  });

  const { data: userLanguages } = useQuery({
    queryKey: ['userLanguages'],
    queryFn: () => apiClient.getUserLanguages(),
  });

  return (
    <Card>
      <CardHeader>
        <CardTitle>My Languages</CardTitle>
        <CardDescription>Manage languages you're learning</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {userLanguages && userLanguages.length > 0 ? (
            userLanguages.map((ul: any) => (
              <div
                key={ul.id}
                className="flex items-center justify-between p-4 border border-gray-200 rounded-lg"
              >
                <div>
                  <h4 className="font-medium">{ul.language?.name}</h4>
                  <p className="text-sm text-gray-600">Level: {ul.proficiency_level?.name}</p>
                </div>
                <Button variant="outline" size="sm">
                  Settings
                </Button>
              </div>
            ))
          ) : (
            <p className="text-gray-600 text-center py-8">No languages added yet</p>
          )}

          <Button className="w-full">Add New Language</Button>
        </div>
      </CardContent>
    </Card>
  );
}

function AccountSettings() {
  const { user } = useAuthStore();

  return (
    <Card>
      <CardHeader>
        <CardTitle>Account Settings</CardTitle>
        <CardDescription>Manage your account security</CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <div>
          <h3 className="font-medium mb-2">Email</h3>
          <p className="text-gray-600">{user?.email}</p>
        </div>

        <div>
          <h3 className="font-medium mb-4">Change Password</h3>
          <div className="space-y-3">
            <Input type="password" label="Current Password" placeholder="••••••••" />
            <Input type="password" label="New Password" placeholder="••••••••" />
            <Input type="password" label="Confirm New Password" placeholder="••••••••" />
          </div>
          <Button className="mt-4">Update Password</Button>
        </div>

        <div className="pt-6 border-t">
          <h3 className="font-medium text-red-600 mb-2">Danger Zone</h3>
          <p className="text-sm text-gray-600 mb-4">
            Once you delete your account, there is no going back. Please be certain.
          </p>
          <Button variant="danger">Delete Account</Button>
        </div>
      </CardContent>
    </Card>
  );
}
