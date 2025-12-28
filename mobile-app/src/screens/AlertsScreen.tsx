import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, RefreshControl, TextInput, TouchableOpacity, Alert as RNAlert } from 'react-native';
import { Alert, getAlerts, submitAlert } from '@api';
import { Card } from '@components/Card';
import { formatDate } from '@api';

interface Props {
  token: string;
}

export const AlertsScreen: React.FC<Props> = ({ token }) => {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [refreshing, setRefreshing] = useState(false);
  const [title, setTitle] = useState('');
  const [photo, setPhoto] = useState('');

  const load = async () => {
    try {
      setRefreshing(true);
      const res = await getAlerts(token);
      setAlerts(res.alerts);
    } catch (err) {
      console.warn('Failed to load alerts', err);
    } finally {
      setRefreshing(false);
    }
  };

  const handleSubmit = async () => {
    if (!title) return;
    try {
      await submitAlert(token, title, photo || undefined);
      setTitle('');
      setPhoto('');
      load();
    } catch (err: any) {
      RNAlert.alert('Submission failed', err.message || 'Try again');
    }
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <ScrollView style={styles.container} refreshControl={<RefreshControl refreshing={refreshing} onRefresh={load} />}>
      <Text style={styles.heading}>EcoAlert</Text>
      <Card title="Report an issue" subtitle="Illegal dumps or unusual waste">
        <TextInput placeholder="Title" value={title} onChangeText={setTitle} style={styles.input} />
        <TextInput placeholder="Photo proof URL (optional)" value={photo} onChangeText={setPhoto} style={styles.input} />
        <TouchableOpacity style={styles.button} onPress={handleSubmit}>
          <Text style={styles.buttonText}>Submit</Text>
        </TouchableOpacity>
      </Card>

      {alerts.map((a) => (
        <Card key={a.id} title={a.title} subtitle={`Status: ${a.status}`}>
          <Text style={styles.reward}>Reward: +{a.reward} EcoPoints</Text>
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
    backgroundColor: '#2563eb',
    paddingVertical: 12,
    borderRadius: 12,
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontWeight: '700',
  },
  reward: {
    color: '#16a34a',
    fontWeight: '700',
  },
});
