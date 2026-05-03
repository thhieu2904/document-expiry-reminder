import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './contexts/AuthContext';
import AppLayout from './components/Layout';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';

import Departments from './pages/Departments';
import Users from './pages/Users';
import Documents from './pages/Documents';
import DeletedDocuments from './pages/DeletedDocuments';
import Reminders from './pages/Reminders';

const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();
  if (loading) return null; // or loading spinner
  if (!user) return <Navigate to="/login" replace />;
  return children;
};

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      
      <Route 
        path="/" 
        element={
          <ProtectedRoute>
            <AppLayout />
          </ProtectedRoute>
        }
      >
        <Route index element={<Dashboard />} />
        <Route path="documents" element={<Documents />} />
        <Route path="departments" element={<Departments />} />
        <Route path="users" element={<Users />} />
        <Route path="reminders" element={<Reminders />} />
        <Route path="deleted-documents" element={<DeletedDocuments />} />
      </Route>

      
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default App;
