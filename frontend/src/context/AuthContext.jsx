import React, { createContext, useContext, useState, useEffect } from 'react';
import { loginUser } from '../api/apiClient';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if token exists in localStorage on mount
    const token = localStorage.getItem('access_token');
    if (token) {
      // In a full implementation, you might want to fetch `/api/v1/users/me` here
      // to validate the token and get user details. For now, we'll just set an object.
      setUser({ authenticated: true });
    }
    setLoading(false);

    // Listen for the custom auth-expired event from apiClient
    const handleAuthExpired = () => {
      setUser(null);
    };
    window.addEventListener('auth-expired', handleAuthExpired);
    return () => window.removeEventListener('auth-expired', handleAuthExpired);
  }, []);

  const login = async (email, password) => {
    try {
      const data = await loginUser(email, password);
      if (data.access_token) {
        localStorage.setItem('access_token', data.access_token);
        setUser({ authenticated: true });
        return { success: true };
      }
      return { success: false, error: "Invalid token received" };
    } catch (error) {
      return { success: false, error: error.message };
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    setUser(null);
  };

  if (loading) {
    return <div>Loading...</div>; // Could be a nicer spinner
  }

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  return useContext(AuthContext);
};
