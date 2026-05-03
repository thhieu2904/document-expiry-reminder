import React, { useState, useEffect } from 'react';
import { Table, Button, Modal, Form, InputNumber, Switch, message, Tabs, Space, Tag, Typography, Input, Card, TimePicker, Divider } from 'antd';
import { EditOutlined, SendOutlined } from '@ant-design/icons';
import dayjs from 'dayjs';
import api from '../services/api';

const { Title } = Typography;

const Reminders = () => {
  const [rules, setRules] = useState([]);
  const [logs, setLogs] = useState([]);
  const [loadingRules, setLoadingRules] = useState(false);
  const [loadingLogs, setLoadingLogs] = useState(false);
  const [loadingCron, setLoadingCron] = useState(false);
  const [triggering, setTriggering] = useState(false);
  
  // Cron Settings State
  const [cronForm] = Form.useForm();
  const [isCronEnabled2, setIsCronEnabled2] = useState(true);

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

  const fetchCronSettings = async () => {
    setLoadingCron(true);
    try {
      const res = await api.get('/settings/cron');
      const data = res.data;
      setIsCronEnabled2(data.cron_enabled_2);
      cronForm.setFieldsValue({
        cron_time_1: dayjs(data.cron_time_1, 'HH:mm'),
        cron_time_2: dayjs(data.cron_time_2, 'HH:mm'),
        cron_enabled_2: data.cron_enabled_2,
      });
    } catch (error) {
      message.error('Lỗi khi tải cấu hình cron');
    } finally {
      setLoadingCron(false);
    }
  };

  useEffect(() => {
    fetchRules();
    fetchLogs();
    fetchCronSettings();
  }, []);

  const handleSaveCronSettings = async (values) => {
    try {
      const payload = {
        cron_time_1: values.cron_time_1.format('HH:mm'),
        cron_time_2: values.cron_time_2 ? values.cron_time_2.format('HH:mm') : '14:00',
        cron_enabled_2: values.cron_enabled_2,
      };
      await api.put('/settings/cron', payload);
      message.success('Cập nhật lịch gửi tự động thành công!');
    } catch (error) {
      message.error('Lỗi khi cập nhật lịch gửi tự động');
    }
  };

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

  const DEFAULT_SUBJECT = '[{{rule_name}}] {{document_number}} - {{document_title}}';
  const DEFAULT_BODY = `Kính gửi {{owner_name}},

Hệ thống tự động thông báo: Văn bản số {{document_number}} - "{{document_title}}" thuộc {{department_name}} sẽ hết hạn vào ngày {{expiry_date}} (còn {{days_left}} ngày).

Vui lòng kiểm tra và xử lý kịp thời.`;

  const handleOpenModal = (rule) => {
    setEditingRule(rule);
    form.setFieldsValue({
      days_before: rule.days_before,
      is_active: rule.is_active,
      subject_template: rule.subject_template || DEFAULT_SUBJECT,
      body_template: rule.body_template || DEFAULT_BODY,
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

  const copyTag = (tag) => {
    navigator.clipboard.writeText(tag);
    message.success(`Đã copy ${tag}`);
  };

  const availableTags = [
    { tag: '{{document_title}}', desc: 'Tên văn bản' },
    { tag: '{{document_number}}', desc: 'Số/Ký hiệu' },
    { tag: '{{department_name}}', desc: 'Phòng ban' },
    { tag: '{{expiry_date}}', desc: 'Ngày hết hạn' },
    { tag: '{{rule_name}}', desc: 'Tên quy tắc' },
    { tag: '{{days_left}}', desc: 'Số ngày còn lại' },
    { tag: '{{owner_name}}', desc: 'Người phụ trách' },
  ];

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
        >Cấu hình</Button>
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

      <Card 
        title="Lịch Gửi Tự Động (Cronjob)" 
        size="small" 
        className="mb-6 border-blue-200 shadow-sm"
        headStyle={{ backgroundColor: '#f0f9ff', color: '#0369a1' }}
      >
        <Form 
          form={cronForm} 
          layout="vertical" 
          onFinish={handleSaveCronSettings}
          className="flex flex-col md:flex-row gap-6 md:items-end"
        >
          <div className="flex-1 border p-3 rounded bg-gray-50 border-gray-200">
            <div className="flex items-center justify-between mb-2">
              <span className="font-medium text-gray-700"><span className="text-red-500 mr-1">*</span>Lần 1 (Bắt buộc)</span>
              <Form.Item className="mb-0" style={{ visibility: 'hidden' }}>
                <Switch />
              </Form.Item>
            </div>
            <Form.Item 
              name="cron_time_1" 
              rules={[{ required: true }]}
              className="mb-0"
            >
              <TimePicker format="HH:mm" style={{ width: '120px' }} minuteStep={15} />
            </Form.Item>
          </div>
          
          <div className="flex-1 border p-3 rounded bg-gray-50 border-gray-200">
            <div className="flex items-center justify-between mb-2">
              <span className="font-medium text-gray-700">Lần 2 (Tùy chọn)</span>
              <Form.Item name="cron_enabled_2" valuePropName="checked" className="mb-0">
                <Switch onChange={(checked) => setIsCronEnabled2(checked)} />
              </Form.Item>
            </div>
            <Form.Item name="cron_time_2" className="mb-0">
              <TimePicker format="HH:mm" style={{ width: '120px' }} minuteStep={15} disabled={!isCronEnabled2} />
            </Form.Item>
          </div>
          
          <Button type="primary" htmlType="submit" loading={loadingCron}>
            Lưu Lịch Gửi
          </Button>
        </Form>
      </Card>

      <Tabs defaultActiveKey="1" items={items} />

      <Modal
        title={`Cấu hình Quy tắc: ${editingRule?.name}`}
        open={isModalVisible}
        onCancel={() => setIsModalVisible(false)}
        onOk={() => form.submit()}
        width={700}
      >
        <Form form={form} layout="vertical" onFinish={handleSaveRule}>
          <div className="grid grid-cols-2 gap-4">
            <Form.Item 
              name="days_before" 
              label="Số ngày báo trước (trước ngày hết hạn)" 
              rules={[{ required: true }]}
            >
              <InputNumber min={1} max={365} style={{ width: '100%' }} disabled={editingRule?.is_overdue_rule} />
            </Form.Item>
            <Form.Item name="is_active" label="Kích hoạt Quy tắc" valuePropName="checked">
              <Switch />
            </Form.Item>
          </div>

          <div className="bg-blue-50 border border-blue-100 p-4 rounded-lg mb-4">
            <h4 className="text-sm font-semibold text-blue-800 mb-1">Biến nội dung — Bấm vào thẻ để Copy, rồi Paste vào ô bên dưới</h4>
            <div className="flex flex-wrap gap-2 mb-3">
              {availableTags.map((t, idx) => (
                <Tag 
                  key={idx} 
                  color="blue" 
                  className="cursor-pointer hover:opacity-80 m-0 text-sm py-1"
                  onClick={() => copyTag(t.tag)}
                >
                  {t.desc} <span className="font-mono text-xs opacity-70 ml-1">{t.tag}</span>
                </Tag>
              ))}
            </div>
            <div className="bg-white border border-blue-200 rounded p-3 text-xs text-gray-600">
              <p className="font-semibold text-gray-700 mb-1">Ví dụ cách dùng:</p>
              <p className="mb-1"><span className="text-blue-700">Bạn nhập:</span> <code className="bg-gray-100 px-1 rounded">Kính gửi {'{{owner_name}}'}, văn bản {'{{document_number}}'} sắp hết hạn sau {'{{days_left}}'} ngày.</code></p>
              <p className="mb-0"><span className="text-green-700">Kết quả gửi đi:</span> <code className="bg-gray-100 px-1 rounded">Kính gửi Nguyễn Văn A, văn bản GP-2025-001 sắp hết hạn sau 5 ngày.</code></p>
            </div>
            <p className="text-xs text-blue-500 mt-2 mb-0">Để trống cả hai ô = dùng mẫu mặc định của hệ thống. Nội dung sẽ được tự động bọc trong khung Email chuẩn.</p>
          </div>

          <Form.Item 
            name="subject_template" 
            label="Tiêu đề Email (Để trống sẽ dùng mặc định)"
          >
            <Input placeholder="Ví dụ: [Cảnh báo] Văn bản {{document_title}} sắp hết hạn" />
          </Form.Item>
          
          <Form.Item 
            name="body_template" 
            label="Nội dung Email (Để trống sẽ dùng mặc định)"
          >
            <Input.TextArea rows={6} placeholder="Xin chào {{owner_name}}, văn bản {{document_number}} của phòng {{department_name}} sắp hết hạn sau {{days_left}} ngày nữa..." />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default Reminders;
