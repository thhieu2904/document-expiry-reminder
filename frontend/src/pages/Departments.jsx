import React, { useState, useEffect, useMemo } from 'react';
import { Table, Button, Modal, Form, Input, message, Popconfirm, Space } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import api from '../services/api';

const { Search } = Input;

const Departments = () => {
  const [departments, setDepartments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [searchText, setSearchText] = useState('');
  const [form] = Form.useForm();

  const fetchDepartments = async () => {
    setLoading(true);
    try {
      const res = await api.get('/departments');
      setDepartments(res.data.items || []);
    } catch (error) {
      message.error('Lỗi khi tải danh sách phòng ban');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDepartments();
  }, []);

  const handleOpenModal = (record = null) => {
    if (record) {
      setEditingId(record.id);
      form.setFieldsValue(record);
    } else {
      setEditingId(null);
      form.resetFields();
    }
    setIsModalVisible(true);
  };

  const handleCancel = () => {
    setIsModalVisible(false);
    form.resetFields();
  };

  const handleSave = async (values) => {
    try {
      if (editingId) {
        await api.put(`/departments/${editingId}`, values);
        message.success('Cập nhật phòng ban thành công');
      } else {
        await api.post('/departments', values);
        message.success('Thêm phòng ban thành công');
      }
      setIsModalVisible(false);
      fetchDepartments();
    } catch (error) {
      message.error(error.response?.data?.detail || 'Lỗi khi lưu phòng ban');
    }
  };

  const handleDelete = async (id) => {
    try {
      await api.delete(`/departments/${id}`);
      message.success('Đã xóa phòng ban');
      fetchDepartments();
    } catch (error) {
      message.error('Lỗi khi xóa. Có thể phòng ban này đang được sử dụng.');
    }
  };

  const filteredDepartments = useMemo(() => {
    let filtered = departments;
    if (searchText) {
      const lowerSearch = searchText.toLowerCase();
      filtered = filtered.filter(d => 
        (d.name && d.name.toLowerCase().includes(lowerSearch)) ||
        (d.code && d.code.toLowerCase().includes(lowerSearch))
      );
    }
    return filtered;
  }, [departments, searchText]);

  const columns = [
    { title: 'Mã phòng ban', dataIndex: 'code', key: 'code', width: '20%', sorter: (a, b) => (a.code || '').localeCompare(b.code || '') },
    { title: 'Tên phòng ban', dataIndex: 'name', key: 'name', sorter: (a, b) => a.name.localeCompare(b.name) },
    {
      title: 'Hành động',
      key: 'action',
      width: '15%',
      render: (_, record) => (
        <Space size="small">
          <Button type="text" icon={<EditOutlined />} onClick={() => handleOpenModal(record)} className="text-gray-600 hover:text-indigo-600" />
          <Popconfirm
            title="Bạn có chắc chắn muốn xóa?"
            onConfirm={() => handleDelete(record.id)}
            okText="Xóa"
            cancelText="Hủy"
          >
            <Button type="text" danger icon={<DeleteOutlined />} />
          </Popconfirm>
        </Space>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <h2 className="text-2xl font-bold text-gray-800 m-0">Quản lý Phòng ban</h2>
        <Button type="primary" icon={<PlusOutlined />} onClick={() => handleOpenModal()} size="large" className="rounded-lg shadow-sm">
          Thêm Phòng ban
        </Button>
      </div>

      <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-100 space-y-4">
        <Search
          placeholder="Tìm kiếm theo Tên hoặc Mã phòng ban..."
          allowClear
          onChange={(e) => setSearchText(e.target.value)}
          style={{ maxWidth: 400 }}
          size="large"
        />

        <Table
          columns={columns}
          dataSource={filteredDepartments}
          rowKey="id"
          loading={loading}
          className="[&_.ant-table-thead>tr>th]:bg-gray-50 [&_.ant-table-thead>tr>th]:text-gray-600 [&_.ant-table-thead>tr>th]:font-semibold"
        />
      </div>

      <Modal
        title={<span className="text-lg font-semibold">{editingId ? 'Sửa Phòng ban' : 'Thêm Phòng ban mới'}</span>}
        open={isModalVisible}
        onCancel={handleCancel}
        onOk={() => form.submit()}
        destroyOnClose
        okText="Lưu lại"
        cancelText="Hủy bỏ"
      >
        <Form form={form} layout="vertical" onFinish={handleSave} className="mt-4">
          <Form.Item name="code" label={<span className="font-medium text-gray-700">Mã phòng ban (Tùy chọn)</span>}>
            <Input placeholder="VD: HCSN" />
          </Form.Item>
          <Form.Item name="name" label={<span className="font-medium text-gray-700">Tên phòng ban</span>} rules={[{ required: true, message: 'Vui lòng nhập tên phòng ban' }]}>
            <Input placeholder="VD: Phòng Hành chính Sự nghiệp" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default Departments;
