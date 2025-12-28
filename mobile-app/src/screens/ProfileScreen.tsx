import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, RefreshControl, TextInput, TouchableOpacity } from 'react-native';
import { getProfile, updateProfile, getBadges, getReminders, getRecommendations, Reminder, Badge, Recommendation } from '@api';
import { Card } from '@components/Card';
import { formatDate } from '@api';

interface Props {
  token: string;
}

export const ProfileScreen: React.FC<Props> = ({ token }) => {
  const [name, setName] = useState('');
  const [city, setCity] = useState('');
  const [avatar, setAvatar] = useState('');
  const [badges, setBadges] = useState<Badge[]>([]);
  const [reminders, setReminders] = useState<Reminder[]>([]);
  const [recs, setRecs] = useState<Recommendation[]>([]);
  const [refreshing, setRefreshing] = useState(false);

  const load = async () => {
    try {
      setRefreshing(true);
      const profile = await getProfile(token);
      setName(profile.user.name || '');
      setCity((profile.user as any).city || '');
      setAvatar((profile.user as any).avatar_url || '');
      const [badgeRes, reminderRes, recRes] = await Promise.all([
        getBadges(token),
        getReminders(token),
        getRecommendations(token),
      ]);
      setBadges(badgeRes.badges);
      setReminders(reminderRes.reminders);
      setRecs(recRes.recommendations);
    } catch (err) {
      console.warn('Failed to load profile data', err);
    } finally {
      setRefreshing(false);
    }
  };

  const saveProfile = async () => {
    try {
      await updateProfile(token, { name, city, avatar_url: avatar || undefined });
    } catch (err) {
      console.warn('Profile update failed', err);
    }
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <ScrollView style={styles.container} refreshControl={<RefreshControl refreshing={refreshing} onRefresh={load} />}>
      <Text style={styles.heading}>Profile</Text>
      <Card title="Account">
        <TextInput placeholder="Name" style={styles.input} value={name} onChangeText={setName} />
        <TextInput placeholder="City" style={styles.input} value={city} onChangeText={setCity} />
        <TextInput placeholder="Avatar URL" style={styles.input} value={avatar} onChangeText={setAvatar} />
        <TouchableOpacity style={styles.button} onPress={saveProfile}>
          <Text style={styles.buttonText}>Save</Text>
        </TouchableOpacity>
      </Card>

      <Card title="Badges">
        {badges.length ? badges.map((b) => (
          <View key={b.id} style={styles.row}>
            <Text style={styles.badgeTitle}>{b.title}</Text>
            <Text style={styles.badgeDate}>{formatDate(b.awarded_at)}</Text>
          </View>
        )) : <Text style={styles.muted}>Earn badges by recycling, choosing local, and logging daily.</Text>}
      </Card>

      <Card title="Reminders">
        {reminders.length ? reminders.map((r) => (
          <View key={r.id} style={styles.row}>
            <Text style={styles.badgeTitle}>{r.title}</Text>
            <Text style={styles.badgeDate}>{formatDate(r.next_trigger_at)}</Text>
          </View>
        )) : <Text style={styles.muted}>Set EcoNudges from the dashboard to avoid expiry or missed logs.</Text>}
      </Card>

      <Card title="Recommendations" subtitle="EcoShop picks tied to your scans">
        {recs.length ? recs.map((r) => (
          <View key={r.id} style={{ marginBottom: 8 }}>
            <Text style={styles.badgeTitle}>{r.title}</Text>
            <Text style={styles.muted}>{r.savings}{r.partner ? ` • ${r.partner}` : ''}</Text>
          </View>
        )) : <Text style={styles.muted}>Scan items to unlock personalized tips.</Text>}
      </Card>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f3f4f6',
    padding: 16,
  },
  heading: {
    fontSize: 24,
    fontWeight: '800',
    marginBottom: 12,
    color: '#111827',
  },
  input: {
    borderWidth: 1,
    borderColor: '#e5e7eb',
    borderRadius: 12,
    paddingHorizontal: 12,
    paddingVertical: 10,
    marginBottom: 12,
    backgroundColor: '#fff',
  },
  button: {
    backgroundColor: '#16a34a',
    paddingVertical: 12,
    borderRadius: 12,
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontWeight: '700',
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 6,
  },
  badgeTitle: {
    fontWeight: '700',
    color: '#111827',
  },
  badgeDate: {
    color: '#6b7280',
  },
  muted: {
    color: '#6b7280',
  },
});
