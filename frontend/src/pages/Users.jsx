import React, { useState, useEffect, useMemo } from 'react';
import { Table, Button, Modal, Form, Input, Select, message, Popconfirm, Space } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import { useLocation } from 'react-router-dom';
import api from '../services/api';

const { Search } = Input;
const { Option } = Select;

const Users = () => {
  const [users, setUsers] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [searchText, setSearchText] = useState('');
  
  // Lấy department_id từ URL nếu có
  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const initialDeptId = searchParams.get('department_id');
  const [departmentFilter, setDepartmentFilter] = useState(initialDeptId || null);

  const [form] = Form.useForm();

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const res = await api.get('/users');
      setUsers(res.data.items || []);
    } catch (error) {
      message.error('Lỗi khi tải danh sách người dùng');
    } finally {
      setLoading(false);
    }
  };

  const fetchDepartments = async () => {
    try {
      const res = await api.get('/departments');
      setDepartments(res.data.items || []);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    fetchUsers();
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
      // By default users created here can't login (just receivers)
      const data = { ...values, can_login: false, status: 'active' };
      if (editingId) {
        await api.put(`/users/${editingId}`, data);
        message.success('Cập nhật người dùng thành công');
      } else {
        await api.post('/users', data);
        message.success('Thêm người dùng thành công');
      }
      setIsModalVisible(false);
      fetchUsers();
    } catch (error) {
      message.error(error.response?.data?.detail || 'Lỗi khi lưu người dùng');
    }
  };

  const handleDelete = async (id) => {
    try {
      await api.delete(`/users/${id}`);
      message.success('Đã xóa người dùng');
      fetchUsers();
    } catch (error) {
      message.error('Lỗi khi xóa người dùng');
    }
  };

  const filteredUsers = useMemo(() => {
    let filtered = users.filter(u => u.can_login === false);
    
    // Filter by department
    if (departmentFilter) {
      filtered = filtered.filter(u => u.department_id === departmentFilter);
    }
    
    // Filter by search text
    if (searchText) {
      const lowerSearch = searchText.toLowerCase();
      filtered = filtered.filter(u => 
        (u.full_name && u.full_name.toLowerCase().includes(lowerSearch)) ||
        (u.email && u.email.toLowerCase().includes(lowerSearch))
      );
    }
    
    return filtered;
  }, [users, searchText, departmentFilter]);

  const columns = [
    { title: 'Họ tên', dataIndex: 'full_name', key: 'full_name', sorter: (a, b) => a.full_name.localeCompare(b.full_name) },
    { title: 'Email', dataIndex: 'email', key: 'email' },
    { 
      title: 'Phòng ban', 
      dataIndex: 'department_id', 
      key: 'department_id',
      render: (deptId) => {
        const dept = departments.find(d => d.id === deptId);
        return dept ? dept.name : '-';
      }
    },
    {
      title: 'Hành động',
      key: 'action',
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
        <h2 className="text-2xl font-bold text-gray-800 m-0">Quản lý Nhân viên</h2>
        <Button type="primary" icon={<PlusOutlined />} onClick={() => handleOpenModal()} size="large" className="rounded-lg shadow-sm">
          Thêm Nhân viên
        </Button>
      </div>

      <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-100 space-y-4">
        <div className="flex gap-4">
          <Search
            placeholder="Tìm kiếm theo tên hoặc email..."
            allowClear
            onChange={(e) => setSearchText(e.target.value)}
            style={{ maxWidth: 400 }}
            size="large"
          />
          <Select
            placeholder="Lọc theo phòng ban"
            allowClear
            size="large"
            value={departmentFilter}
            onChange={(val) => setDepartmentFilter(val)}
            style={{ minWidth: 250 }}
            options={departments.map(d => ({ label: d.name, value: d.id }))}
          />
        </div>

        <Table
          columns={columns}
          dataSource={filteredUsers}
          rowKey="id"
          loading={loading}
          className="[&_.ant-table-thead>tr>th]:bg-gray-50 [&_.ant-table-thead>tr>th]:text-gray-600 [&_.ant-table-thead>tr>th]:font-semibold"
        />
      </div>

      <Modal
        title={<span className="text-lg font-semibold">{editingId ? 'Sửa Người nhận' : 'Thêm Người nhận mới'}</span>}
        open={isModalVisible}
        onCancel={handleCancel}
        onOk={() => form.submit()}
        destroyOnHidden
        okText="Lưu lại"
        cancelText="Hủy bỏ"
      >
        <Form form={form} layout="vertical" onFinish={handleSave} className="mt-4">
          <Form.Item name="full_name" label={<span className="font-medium text-gray-700">Họ và tên</span>} rules={[{ required: true }]}>
            <Input placeholder="Nhập họ và tên..." />
          </Form.Item>
          <Form.Item name="email" label={<span className="font-medium text-gray-700">Email nhận thông báo</span>} rules={[{ required: true, type: 'email' }]}>
            <Input placeholder="VD: user@tvu.edu.vn" />
          </Form.Item>
          <Form.Item name="department_id" label={<span className="font-medium text-gray-700">Phòng ban</span>} rules={[{ required: true }]}>
            <Select placeholder="Chọn phòng ban">
              {departments.map(dept => (
                <Option key={dept.id} value={dept.id}>{dept.name}</Option>
              ))}
            </Select>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default Users;
