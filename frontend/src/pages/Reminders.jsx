import React, { useState, useEffect } from 'react';
import { Table, Button, Modal, Form, InputNumber, Switch, message, Tabs, Space, Tag, Typography } from 'antd';
import { EditOutlined, SendOutlined } from '@ant-design/icons';
import dayjs from 'dayjs';
import api from '../services/api';

const { Title } = Typography;

const Reminders = () => {
  const [rules, setRules] = useState([]);
  const [logs, setLogs] = useState([]);
  const [loadingRules, setLoadingRules] = useState(false);
  const [loadingLogs, setLoadingLogs] = useState(false);
  const [triggering, setTriggering] = useState(false);

  // Edit Modal State
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [editingRule, setEditingRule] = useState(null);
  const [form] = Form.useForm();

  const fetchRules = async () => {
    setLoadingRules(true);
    try {
      const res = await api.get('/reminders/rules');
      setRules(res.data);
    } catch (error) {
      message.error('Lỗi khi tải cấu hình nhắc nhở');
    } finally {
      setLoadingRules(false);
    }
  };

  const fetchLogs = async () => {
    setLoadingLogs(true);
    try {
      const res = await api.get('/reminders/logs?limit=50');
      setLogs(res.data);
    } catch (error) {
      message.error('Lỗi khi tải lịch sử gửi mail');
    } finally {
      setLoadingLogs(false);
    }
  };

  useEffect(() => {
    fetchRules();
    fetchLogs();
  }, []);

  const handleTrigger = async () => {
    setTriggering(true);
    try {
      await api.post('/reminders/trigger');
      message.success('Đã chạy luồng kiểm tra và gửi mail thành công!');
      fetchLogs(); // refresh logs
    } catch (error) {
      message.error('Lỗi khi kích hoạt luồng nhắc nhở');
    } finally {
      setTriggering(false);
    }
  };

  const handleOpenModal = (rule) => {
    setEditingRule(rule);
    form.setFieldsValue({
      days_before: rule.days_before,
      is_active: rule.is_active,
    });
    setIsModalVisible(true);
  };

  const handleSaveRule = async (values) => {
    try {
      await api.put(`/reminders/rules/${editingRule.id}`, values);
      message.success('Cập nhật quy tắc thành công');
      setIsModalVisible(false);
      fetchRules();
    } catch (error) {
      message.error('Lỗi khi cập nhật quy tắc');
    }
  };

  const toggleRule = async (checked, rule) => {
    try {
      await api.put(`/reminders/rules/${rule.id}`, { is_active: checked });
      message.success(`Đã ${checked ? 'bật' : 'tắt'} quy tắc: ${rule.name}`);
      fetchRules();
    } catch (error) {
      message.error('Lỗi khi thay đổi trạng thái');
    }
  };

  const ruleColumns = [
    { title: 'Tên Quy tắc', dataIndex: 'name', key: 'name' },
    { 
      title: 'Số ngày báo trước', 
      dataIndex: 'days_before', 
      key: 'days_before',
      render: (val, record) => record.is_overdue_rule ? 'Ngay khi quá hạn (0)' : `${val} ngày`
    },
    { 
      title: 'Trạng thái', 
      dataIndex: 'is_active', 
      key: 'is_active',
      render: (val, record) => (
        <Switch 
          checked={val} 
          onChange={(checked) => toggleRule(checked, record)} 
        />
      )
    },
    {
      title: 'Hành động',
      key: 'action',
      render: (_, record) => (
        <Button 
          type="text" 
          icon={<EditOutlined />} 
          onClick={() => handleOpenModal(record)} 
          disabled={record.is_overdue_rule} // Don't let them edit days for overdue
        >Sửa</Button>
      ),
    },
  ];

  const logColumns = [
    { 
      title: 'Ngày gửi', 
      dataIndex: 'sent_at', 
      key: 'sent_at',
      render: (val) => val ? dayjs(val).format('DD/MM/YYYY HH:mm') : '-'
    },
    { title: 'Tên Văn bản', dataIndex: 'document_title', key: 'document_title' },
    { title: 'Quy tắc', dataIndex: 'rule_name', key: 'rule_name' },
    { title: 'Email Người nhận', dataIndex: 'recipient_email', key: 'recipient_email' },
    { 
      title: 'Trạng thái', 
      dataIndex: 'status', 
      key: 'status',
      render: (val) => (
        <Tag color={val === 'sent' ? 'green' : 'red'}>
          {val === 'sent' ? 'Thành công' : 'Thất bại'}
        </Tag>
      )
    },
  ];

  const items = [
    {
      key: '1',
      label: 'Cấu hình Quy tắc Nhắc nhở',
      children: (
        <div>
          <Table columns={ruleColumns} dataSource={rules} rowKey="id" loading={loadingRules} pagination={false} />
        </div>
      ),
    },
    {
      key: '2',
      label: 'Lịch sử Gửi Email',
      children: (
        <Table columns={logColumns} dataSource={logs} rowKey="id" loading={loadingLogs} />
      ),
    },
  ];

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
        <Title level={3}>Cấu hình Nhắc nhở & Email</Title>
        <Button 
          type="primary" 
          danger 
          icon={<SendOutlined />} 
          loading={triggering}
          onClick={handleTrigger}
        >
          Chạy Nhắc nhở Ngay
        </Button>
      </div>

      <Tabs defaultActiveKey="1" items={items} />

      <Modal
        title={`Sửa Quy tắc: ${editingRule?.name}`}
        open={isModalVisible}
        onCancel={() => setIsModalVisible(false)}
        onOk={() => form.submit()}
      >
        <Form form={form} layout="vertical" onFinish={handleSaveRule}>
          <Form.Item 
            name="days_before" 
            label="Số ngày báo trước (trước ngày hết hạn)" 
            rules={[{ required: true }]}
          >
            <InputNumber min={1} max={365} style={{ width: '100%' }} />
          </Form.Item>
          <Form.Item name="is_active" label="Kích hoạt" valuePropName="checked">
            <Switch />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default Reminders;
