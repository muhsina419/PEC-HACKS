import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, RefreshControl } from 'react-native';
import { CarbonSnapshot, getCarbonSnapshot } from '@api';
import { Card } from '@components/Card';
import { ScorePill } from '@components/ScorePill';

interface Props {
  token: string;
}

export const DashboardScreen: React.FC<Props> = ({ token }) => {
  const [snapshot, setSnapshot] = useState<CarbonSnapshot>();
  const [refreshing, setRefreshing] = useState(false);

  const load = async () => {
    try {
      setRefreshing(true);
      const res = await getCarbonSnapshot(token);
      setSnapshot(res);
    } catch (err) {
      console.warn('Failed to load carbon snapshot', err);
    } finally {
      setRefreshing(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <ScrollView style={styles.container} refreshControl={<RefreshControl refreshing={refreshing} onRefresh={load} />}>
      <Text style={styles.heading}>EcoScore</Text>
      {snapshot ? (
        <Card>
          <Text style={styles.score}>{snapshot.eco_score}</Text>
          <Text style={styles.note}>Higher is better. Stay above 80 to keep rewards unlocked.</Text>
          <View style={styles.row}>
            <ScorePill label="Total CO₂e" value={`${snapshot.total_emissions.toFixed(2)} kg`} />
            <ScorePill label="Status" value={snapshot.eco_score >= 80 ? 'On Track' : 'Needs action'} tone={snapshot.eco_score >= 80 ? 'success' : 'warn'} />
          </View>
        </Card>
      ) : (
        <Card><Text>Loading...</Text></Card>
      )}

      <Card title="Breakdown" subtitle="Travel, energy, food and waste contributions">
        {snapshot ? (
          Object.entries(snapshot.breakdown).map(([area, value]) => (
            <View key={area} style={styles.breakdownRow}>
              <Text style={styles.breakdownLabel}>{area}</Text>
              <Text style={styles.breakdownValue}>{value.toFixed(2)} kg</Text>
            </View>
          ))
        ) : (
          <Text style={{ color: '#6b7280' }}>Loading breakdown...</Text>
        )}
      </Card>

      <Card title="Next best actions" subtitle="Personalized nudges to lower your footprint">
        {snapshot?.tips?.length ? (
          snapshot.tips.map((tip) => (
            <Text key={tip} style={styles.tip}>• {tip}</Text>
          ))
        ) : (
          <Text style={{ color: '#6b7280' }}>No tips yet. Complete a scan to unlock insights.</Text>
        )}
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
  score: {
    fontSize: 48,
    fontWeight: '800',
    color: '#16a34a',
  },
  note: {
    color: '#6b7280',
    marginTop: 4,
    marginBottom: 12,
  },
  row: {
    flexDirection: 'row',
    gap: 8,
    alignItems: 'center',
  },
  breakdownRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 6,
  },
  breakdownLabel: {
    fontWeight: '600',
    color: '#111827',
  },
  breakdownValue: {
    color: '#111827',
  },
  tip: {
    marginBottom: 6,
    color: '#111827',
  },
});
