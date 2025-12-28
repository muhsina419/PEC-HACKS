import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, RefreshControl } from 'react-native';
import { Circle, getCircles } from '@api';
import { Card } from '@components/Card';

interface Props {
  token: string;
}

export const CommunityScreen: React.FC<Props> = ({ token }) => {
  const [circles, setCircles] = useState<Circle[]>([]);
  const [refreshing, setRefreshing] = useState(false);

  const load = async () => {
    try {
      setRefreshing(true);
      const res = await getCircles(token);
      setCircles(res.circles);
    } catch (err) {
      console.warn('Failed to load circles', err);
    } finally {
      setRefreshing(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <ScrollView style={styles.container} refreshControl={<RefreshControl refreshing={refreshing} onRefresh={load} />}>
      <Text style={styles.heading}>EcoCircle</Text>
      {circles.map((circle) => (
        <Card key={circle.id} title={circle.name} subtitle={`${circle.city} • ${circle.members} members`}>
          {circle.upcoming_events?.map((event) => (
            <Text key={event} style={styles.event}>• {event}</Text>
          )) || <Text style={styles.muted}>No events announced yet</Text>}
        </Card>
      ))}
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
  event: {
    marginBottom: 4,
    color: '#111827',
  },
  muted: {
    color: '#6b7280',
  },
});
