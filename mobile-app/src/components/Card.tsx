import React from 'react';
import { View, Text, StyleSheet, ViewProps } from 'react-native';

interface Props extends ViewProps {
  title?: string;
  subtitle?: string;
}

export const Card: React.FC<Props> = ({ title, subtitle, children, style, ...rest }) => {
  return (
    <View style={[styles.card, style]} {...rest}>
      {title && <Text style={styles.title}>{title}</Text>}
      {subtitle && <Text style={styles.subtitle}>{subtitle}</Text>}
      {children}
    </View>
  );
};

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#fff',
    padding: 16,
    borderRadius: 12,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOpacity: 0.05,
    shadowRadius: 8,
    shadowOffset: { width: 0, height: 2 },
    elevation: 2,
  },
  title: {
    fontSize: 16,
    fontWeight: '700',
    marginBottom: 4,
    color: '#111827',
  },
  subtitle: {
    fontSize: 13,
    color: '#6b7280',
    marginBottom: 8,
  },
});
