import React, { useState } from 'react';
import { NavigationContainer, DefaultTheme } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { StatusBar } from 'expo-status-bar';
import { LoginScreen } from './src/screens/LoginScreen';
import { RegisterScreen } from './src/screens/RegisterScreen';
import { DashboardScreen } from './src/screens/DashboardScreen';
import { LeaderboardScreen } from './src/screens/LeaderboardScreen';
import { CommunityScreen } from './src/screens/CommunityScreen';
import { AlertsScreen } from './src/screens/AlertsScreen';
import { ProfileScreen } from './src/screens/ProfileScreen';

const Tab = createBottomTabNavigator();
const Stack = createNativeStackNavigator();

type AuthMode = 'login' | 'register';

const AppTabs: React.FC<{ token: string }> = ({ token }) => (
  <Tab.Navigator screenOptions={{ headerShown: false }}>
    <Tab.Screen name="Dashboard">{() => <DashboardScreen token={token} />}</Tab.Screen>
    <Tab.Screen name="Leaderboard">{() => <LeaderboardScreen token={token} />}</Tab.Screen>
    <Tab.Screen name="Community">{() => <CommunityScreen token={token} />}</Tab.Screen>
    <Tab.Screen name="Alerts">{() => <AlertsScreen token={token} />}</Tab.Screen>
    <Tab.Screen name="Profile">{() => <ProfileScreen token={token} />}</Tab.Screen>
  </Tab.Navigator>
);

export default function App() {
  const [token, setToken] = useState<string | null>(null);
  const [authMode, setAuthMode] = useState<AuthMode>('login');
  const theme = {
    ...DefaultTheme,
    colors: { ...DefaultTheme.colors, background: '#f3f4f6' },
  };

  return (
    <SafeAreaProvider>
      <NavigationContainer theme={theme}>
        <StatusBar style="dark" />
        <Stack.Navigator screenOptions={{ headerShown: false }}>
          {token ? (
            <Stack.Screen name="App">{() => <AppTabs token={token} />}</Stack.Screen>
          ) : authMode === 'login' ? (
            <Stack.Screen name="Login">
              {() => <LoginScreen onAuthenticated={setToken} goToRegister={() => setAuthMode('register')} />}
            </Stack.Screen>
          ) : (
            <Stack.Screen name="Register">
              {() => <RegisterScreen onAuthenticated={setToken} goToLogin={() => setAuthMode('login')} />}
            </Stack.Screen>
          )}
        </Stack.Navigator>
      </NavigationContainer>
    </SafeAreaProvider>
  );
}
