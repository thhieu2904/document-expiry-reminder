import React from 'react';
import { Layout, Menu, Button, Dropdown, theme } from 'antd';
import { 
  DashboardOutlined, 
  FileTextOutlined, 
  TeamOutlined, 
  BankOutlined,
  BellOutlined,
  LogoutOutlined,
  UserOutlined,
  DeleteOutlined
} from '@ant-design/icons';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const { Header, Sider, Content, Footer } = Layout;

const AppLayout = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const {
    token: { colorPrimary },
  } = theme.useToken();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const userMenu = {
    items: [
      {
        key: 'profile',
        icon: <UserOutlined />,
        label: `Hồ sơ (${user?.full_name})`,
      },
      { type: 'divider' },
      {
        key: 'logout',
        icon: <LogoutOutlined />,
        label: 'Đăng xuất',
        onClick: handleLogout,
        danger: true,
      },
    ],
  };

  const menuItems = [
    {
      key: '/',
      icon: <DashboardOutlined />,
      label: 'Tổng quan',
      onClick: () => navigate('/'),
    },
    { type: 'divider' },
    {
      key: '/documents',
      icon: <FileTextOutlined />,
      label: 'Văn bản',
      onClick: () => navigate('/documents'),
    },
    {
      key: '/departments',
      icon: <BankOutlined />,
      label: 'Phòng ban',
      onClick: () => navigate('/departments'),
    },
    {
      key: '/users',
      icon: <TeamOutlined />,
      label: 'Nhân viên',
      onClick: () => navigate('/users'),
    },
    { type: 'divider' },
    {
      key: '/reminders',
      icon: <BellOutlined />,
      label: 'Cấu hình nhắc hạn',
      onClick: () => navigate('/reminders'),
    },
  ];

  if (user?.role === 'admin') {
    menuItems.push({ type: 'divider' });
    menuItems.push({
      key: '/deleted-documents',
      icon: <DeleteOutlined />,
      label: 'Thùng rác',
      onClick: () => navigate('/deleted-documents'),
    });
  }

  return (
    <div className="flex flex-col min-h-screen bg-[#f8fafc] font-sans">
      {/* ===== TOP HEADER ===== */}
      <header className="sticky top-0 z-30 bg-white shadow-sm border-b border-gray-200">
        <div className="flex items-center justify-between w-full px-6 py-3 relative">
          
          {/* Spacer for Flexbox balance (Left) */}
          <div className="flex-1 hidden lg:block"></div>

          {/* Title Section (Center) - Logo & Title Together */}
          <div className="flex items-center justify-center flex-shrink-0 gap-3 z-10">
            <img 
              src="/LOGO_HCC.jpg" 
              alt="Logo Trung tâm Hành chính công" 
              className="w-11 h-11 object-contain"
            />
            <h1 className="m-0 text-[17px] font-bold text-[#dc2626] leading-tight uppercase tracking-wide">
              TRUNG TÂM PHỤC VỤ HÀNH CHÍNH CÔNG XÃ LONG PHÚ
            </h1>
          </div>

          {/* System Info Section (Right) */}
          <div className="flex-1 flex justify-end items-center flex-shrink-0 pr-2">
            <div className="text-right">
              <div className="font-semibold text-[#1d4ed8] text-[15px] leading-tight">Hệ thống Nhắc hạn Văn bản</div>
              <div className="text-gray-500 text-[13px] font-medium leading-tight mt-1">DocReminder v2.0</div>
            </div>
          </div>
        </div>
      </header>

      {/* ===== BODY ===== */}
      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar */}
        <Sider 
          width={260} 
          theme="light" 
          breakpoint="lg" 
          collapsedWidth="0"
          className="z-20 shadow-[1px_0_8px_rgba(0,0,0,0.04)]"
          style={{ background: '#fff' }}
        >
          <div className="flex flex-col h-full">
            <div className="flex-1 overflow-y-auto">
              <Menu 
                theme="light" 
                mode="inline" 
                selectedKeys={[location.pathname]} 
                items={menuItems}
                className="border-none pt-4 px-3 [&_.ant-menu-item]:rounded-lg [&_.ant-menu-item]:text-[15px] [&_.ant-menu-item]:font-medium [&_.ant-menu-item-selected]:bg-blue-50 [&_.ant-menu-item-selected]:text-blue-700 [&_.ant-menu-item-selected]:font-semibold"
              />
            </div>
            
            {/* ChatGPT-style Profile at bottom left */}
            <div className="px-3 border-t border-gray-200 mt-auto h-[76px] flex items-center bg-white">
              <Dropdown menu={userMenu} placement="topRight" trigger={['click']}>
                <button className="flex items-center w-full gap-3 px-3 py-2 text-sm rounded-xl hover:bg-gray-100 transition-colors cursor-pointer border-none bg-transparent outline-none">
                  <div className="w-9 h-9 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center flex-shrink-0 font-bold text-lg shadow-sm border border-blue-200">
                    {user?.full_name ? user.full_name.charAt(0).toUpperCase() : <UserOutlined />}
                  </div>
                  <div className="flex flex-col text-left flex-1 overflow-hidden">
                    <span className="truncate text-[14px] font-semibold text-gray-800 leading-tight">
                      {user?.full_name || 'Người dùng'}
                    </span>
                    <span className="truncate text-[12px] text-gray-500 leading-tight mt-0.5">
                      {user?.email || 'Admin'}
                    </span>
                  </div>
                </button>
              </Dropdown>
            </div>
          </div>
        </Sider>

        {/* Main Content Area */}
        <div className="flex flex-col flex-1 bg-[#f8fafc] overflow-y-auto">
          {/* Outlet Wrapper - Tối ưu padding ~10px */}
          <main className="flex-1 p-2 md:p-3 flex flex-col">
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 md:p-5 flex-grow">
              <Outlet />
            </div>
          </main>

          {/* Footer - Sát dưới cùng, nền trắng, cao bằng Profile */}
          <footer className="bg-white border-t border-gray-200 w-full px-6 flex flex-col justify-center mt-auto h-[76px]">
            <div className="text-center text-gray-500 text-[13px] leading-relaxed">
              <div className="mb-0.5">
                <span className="font-semibold text-gray-700">Cơ quan chủ quản:</span> TRUNG TÂM PHỤC VỤ HÀNH CHÍNH CÔNG XÃ LONG PHÚ
              </div>
              <div>
                <span className="font-semibold text-gray-700">Địa chỉ:</span> Ấp 4, xã Long Phú, TP Cần Thơ
                <span className="mx-2 text-gray-300">|</span>
                <span className="font-semibold text-gray-700">Điện thoại:</span> 0907007397
              </div>
            </div>
          </footer>
        </div>
      </div>
    </div>
  );
};

export default AppLayout;
