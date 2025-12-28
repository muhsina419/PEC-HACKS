import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

export const ScorePill: React.FC<{ label: string; value: string | number; tone?: 'success' | 'warn' | 'info' }> = ({ label, value, tone = 'info' }) => {
  const colors = {
    success: '#16a34a',
    warn: '#f59e0b',
    info: '#2563eb',
  } as const;

  return (
    <View style={[styles.container, { backgroundColor: `${colors[tone]}15`, borderColor: colors[tone] }]}> 
      <Text style={[styles.label, { color: colors[tone] }]}>{label}</Text>
      <Text style={[styles.value, { color: colors[tone] }]}>{value}</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 999,
    borderWidth: 1,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  label: {
    fontSize: 13,
    fontWeight: '600',
  },
  value: {
    fontSize: 13,
    fontWeight: '700',
  },
});
