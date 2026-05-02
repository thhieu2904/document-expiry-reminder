import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Statistic, Table, message, Tag, Typography, Button } from 'antd';
import { 
  FileTextOutlined, 
  ExclamationCircleOutlined, 
  CheckCircleOutlined,
  WarningOutlined,
  MailOutlined,
  ArrowRightOutlined
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import dayjs from 'dayjs';
import api from '../services/api';

const { Title, Text } = Typography;

const Dashboard = () => {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [logs, setLogs] = useState([]);
  const [expiringDocs, setExpiringDocs] = useState([]);
  const navigate = useNavigate();

  const fetchDashboardData = async () => {
    try {
      const res = await api.get('/dashboard/summary');
      setSummary(res.data);
    } catch (error) {
      console.error("Dashboard error:", error);
      message.error('Không thể tải dữ liệu tổng quan');
    }
  };

  const fetchRecentLogs = async () => {
    try {
      const res = await api.get('/reminders/logs?limit=5');
      setLogs(res.data);
    } catch (error) {
      console.error(error);
    }
  };

  const fetchExpiringDocs = async () => {
    try {
      const res = await api.get('/dashboard/expiring-soon');
      setExpiringDocs(res.data);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    const loadAll = async () => {
      setLoading(true);
      await Promise.all([fetchDashboardData(), fetchRecentLogs(), fetchExpiringDocs()]);
      setLoading(false);
    };
    loadAll();
  }, []);

  const statCards = [
    {
      title: 'Tổng số Văn bản',
      value: summary?.documents?.total || 0,
      icon: <FileTextOutlined style={{ color: '#3b82f6', fontSize: '32px' }} />,
      bg: 'bg-blue-50',
      border: 'border-blue-100',
      onClick: () => navigate('/documents')
    },
    {
      title: 'Đang hiệu lực',
      value: summary?.documents?.active || 0,
      icon: <CheckCircleOutlined style={{ color: '#10b981', fontSize: '32px' }} />,
      bg: 'bg-green-50',
      border: 'border-green-100',
      onClick: () => navigate('/documents?status=active')
    },
    {
      title: 'Sắp hết hạn',
      value: summary?.documents?.expiring_soon || 0,
      icon: <ExclamationCircleOutlined style={{ color: '#f59e0b', fontSize: '32px' }} />,
      bg: 'bg-orange-50',
      border: 'border-orange-100',
      onClick: () => navigate('/documents?status=expiring_soon')
    },
    {
      title: 'Đã quá hạn',
      value: summary?.documents?.expired || 0,
      icon: <WarningOutlined style={{ color: '#ef4444', fontSize: '32px' }} />,
      bg: 'bg-red-50',
      border: 'border-red-100',
      onClick: () => navigate('/documents?status=expired')
    },
  ];

  const logColumns = [
    { 
      title: 'Thời gian', 
      dataIndex: 'sent_at', 
      key: 'sent_at',
      render: (val) => val ? dayjs(val).format('DD/MM/YY HH:mm') : '-'
    },
    { title: 'Email nhận', dataIndex: 'recipient_email', key: 'recipient_email' },
    { title: 'Chủ đề', dataIndex: 'subject', key: 'subject', ellipsis: true },
    { 
      title: 'Trạng thái', 
      dataIndex: 'status', 
      key: 'status',
      render: (val) => (
        <Tag color={val === 'sent' ? 'success' : 'error'}>
          {val === 'sent' ? 'Thành công' : 'Thất bại'}
        </Tag>
      )
    },
  ];

  return (
    <div className="space-y-6">
      <div>
        <Title level={3} className="!mb-1">Tổng quan Hệ thống</Title>
        <Text type="secondary">Cập nhật lúc {dayjs().format('HH:mm DD/MM/YYYY')}</Text>
      </div>

      <Row gutter={[16, 16]}>
        {statCards.map((card, idx) => (
          <Col xs={24} sm={12} lg={6} key={idx}>
            <div 
              onClick={card.onClick}
              className={`p-6 rounded-xl border ${card.border} ${card.bg} cursor-pointer transition-all duration-300 hover:-translate-y-1 hover:shadow-md flex items-center justify-between`}
            >
              <div>
                <p className="text-gray-500 font-medium mb-1">{card.title}</p>
                <h3 className="text-3xl font-bold text-gray-800 m-0">{loading ? '-' : card.value}</h3>
              </div>
              <div className="bg-white p-3 rounded-lg shadow-sm">
                {card.icon}
              </div>
            </div>
          </Col>
        ))}
      </Row>

      <Row gutter={[16, 16]}>
        <Col xs={24} lg={12}>
          <Card 
            title={<span className="font-semibold text-gray-800">Văn bản sắp hết hạn gần nhất</span>} 
            className="shadow-sm rounded-xl border-gray-100 h-full"
            extra={<Button type="link" onClick={() => navigate('/documents?status=expiring_soon')}>Xem tất cả</Button>}
          >
            <div className="space-y-4">
              {expiringDocs.length === 0 ? (
                <div className="text-center py-8 text-gray-400">Không có văn bản nào sắp hết hạn</div>
              ) : (
                expiringDocs.map(doc => {
                  const daysLeft = dayjs(doc.expiry_date).diff(dayjs(), 'day');
                  const isOverdue = daysLeft < 0;
                  return (
                    <div key={doc.id} className="flex justify-between items-center p-3 hover:bg-gray-50 rounded-lg border border-gray-100 transition-colors">
                      <div>
                        <div className="font-medium text-gray-800">{doc.title}</div>
                        <div className="text-sm text-gray-500">Số/KH: {doc.document_number || 'N/A'}</div>
                      </div>
                      <div className="text-right">
                        {isOverdue ? (
                          <Tag color="error" className="!mr-0 font-medium">Quá hạn {Math.abs(daysLeft)} ngày</Tag>
                        ) : daysLeft === 0 ? (
                          <Tag color="error" className="!mr-0 font-medium">Hết hạn hôm nay</Tag>
                        ) : (
                          <Tag color="warning" className="!mr-0 font-medium">Còn {daysLeft} ngày</Tag>
                        )}
                        <div className="text-xs text-gray-400 mt-1">{dayjs(doc.expiry_date).format('DD/MM/YYYY')}</div>
                      </div>
                    </div>
                  );
                })
              )}
            </div>
          </Card>
        </Col>

        <Col xs={24} lg={12}>
          <Card 
            title={
              <div className="flex items-center gap-2">
                <MailOutlined className="text-indigo-500" />
                <span className="font-semibold text-gray-800">Lịch sử gửi Email gần đây</span>
              </div>
            }
            extra={
              <div className="text-sm">
                <span className="text-green-500 font-medium mr-3">Thành công: {loading ? '-' : summary?.emails?.success}</span>
                <span className="text-red-500 font-medium">Thất bại: {loading ? '-' : summary?.emails?.failed}</span>
              </div>
            }
            className="shadow-sm rounded-xl border-gray-100 h-full"
          >
            <Table 
              dataSource={logs} 
              columns={logColumns} 
              rowKey="id" 
              pagination={false} 
              size="small"
              loading={loading}
              className="[&_.ant-table-thead>tr>th]:bg-gray-50"
            />
            <div className="mt-4 text-center">
              <Button type="link" onClick={() => navigate('/reminders')}>
                Xem toàn bộ lịch sử <ArrowRightOutlined />
              </Button>
            </div>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard;
