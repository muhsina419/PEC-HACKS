import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, RefreshControl } from 'react-native';
import { getLeaderboard, LeaderboardEntry } from '@api';
import { Card } from '@components/Card';
import { ScorePill } from '@components/ScorePill';

interface Props {
  token: string;
}

const Section: React.FC<{ title: string; entries: LeaderboardEntry[] }> = ({ title, entries }) => (
  <Card title={title}>
    {entries.map((entry) => (
      <View key={`${title}-${entry.rank}-${entry.name}`} style={styles.row}>
        <Text style={styles.rank}>#{entry.rank}</Text>
        <View style={{ flex: 1 }}>
          <Text style={styles.name}>{entry.name}</Text>
          <Text style={styles.city}>{entry.city}</Text>
          <Text style={styles.headline}>{entry.headline}</Text>
        </View>
        <ScorePill label="Score" value={entry.eco_score} tone={entry.rank === 1 ? 'success' : 'info'} />
      </View>
    ))}
  </Card>
);

export const LeaderboardScreen: React.FC<Props> = ({ token }) => {
  const [global, setGlobal] = useState<LeaderboardEntry[]>([]);
  const [city, setCity] = useState<LeaderboardEntry[]>([]);
  const [refreshing, setRefreshing] = useState(false);

  const load = async () => {
    try {
      setRefreshing(true);
      const res = await getLeaderboard(token);
      setGlobal(res.global);
      setCity(res.city);
    } catch (err) {
      console.warn('Failed to load leaderboard', err);
    } finally {
      setRefreshing(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <ScrollView style={styles.container} refreshControl={<RefreshControl refreshing={refreshing} onRefresh={load} />}>
      <Text style={styles.heading}>EcoRank</Text>
      <Section title="Global" entries={global} />
      <Section title="City" entries={city} />
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
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    paddingVertical: 8,
  },
  rank: {
    width: 34,
    height: 34,
    borderRadius: 12,
    backgroundColor: '#e5e7eb',
    textAlign: 'center',
    textAlignVertical: 'center',
    fontWeight: '800',
    color: '#111827',
  },
  name: {
    fontWeight: '700',
    color: '#111827',
  },
  city: {
    color: '#6b7280',
  },
  headline: {
    color: '#2563eb',
    fontSize: 12,
  },
});
