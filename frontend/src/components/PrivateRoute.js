import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

function PrivateRoute({ children, role }) {
  const { user } = useAuth();

  if (!user) {
    return <Navigate to="/login" />;
  }

  if (role === 'admin' && !user.is_admin) {
    return <Navigate to="/user-dashboard" />;
  }

  if (role === 'user' && user.is_admin) {
    return <Navigate to="/admin-dashboard" />;
  }

  return children;
}

export default PrivateRoute;