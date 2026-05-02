import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { ConfigProvider, message, notification } from 'antd';
import viVN from 'antd/locale/vi_VN';
import { AuthProvider } from './contexts/AuthContext';
import App from './App.jsx';
import './index.css';

// Global config for notifications
message.config({
  top: 60,
  duration: 3,
  maxCount: 3,
});

notification.config({
  placement: 'bottomRight',
  bottom: 50,
  duration: 3,
});

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <ConfigProvider 
        locale={viVN}
        theme={{
          token: {
            colorPrimary: '#1d4ed8', // Blue-700
            fontFamily: "'Inter', system-ui, -apple-system, sans-serif",
            borderRadius: 8,
            colorBgContainer: '#ffffff',
            colorError: '#ef4444',
            colorSuccess: '#10b981',
            colorWarning: '#f59e0b',
          },
        }}
      >
        <AuthProvider>
          <App />
        </AuthProvider>
      </ConfigProvider>
    </BrowserRouter>
  </React.StrictMode>,
);
