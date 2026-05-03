import React, { useState, useEffect, useCallback } from 'react';
import { Table, Button, Modal, Form, Input, Select, DatePicker, Upload, message, Popconfirm, Space, Tag, Empty } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined, UploadOutlined, DownloadOutlined, SearchOutlined } from '@ant-design/icons';
import { useSearchParams } from 'react-router-dom';
import dayjs from 'dayjs';
import api from '../services/api';
import { useAuth } from '../contexts/AuthContext';

const { Search } = Input;
const { Option } = Select;

// Helper to format file size
const formatBytes = (bytes, decimals = 2) => {
  if (!bytes) return '0 Bytes';
  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
};

const Documents = () => {
  const [documents, setDocuments] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [users, setUsers] = useState([]);
  const [loadingUsers, setLoadingUsers] = useState(false);
  const [loading, setLoading] = useState(false);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [fileList, setFileList] = useState([]);
  const [form] = Form.useForm();
  const [searchParams, setSearchParams] = useSearchParams();
  const { user: currentUser } = useAuth();
  const selectedDepartmentId = Form.useWatch('department_id', form);

  // Filters state
  const [searchText, setSearchText] = useState('');
  const [statusFilter, setStatusFilter] = useState(searchParams.get('status') || '');
  const [departmentFilter, setDepartmentFilter] = useState('');

  const fetchDocuments = useCallback(async () => {
    setLoading(true);
    try {
      const params = {};
      if (statusFilter) params.status_filter = statusFilter;
      if (departmentFilter) params.department_id = departmentFilter;
      if (searchText) params.search = searchText;

      const res = await api.get('/documents', { params });
      setDocuments(res.data);
    } catch (error) {
      message.error('Lỗi khi tải danh sách văn bản');
    } finally {
      setLoading(false);
    }
  }, [statusFilter, departmentFilter, searchText]);

  const fetchDepartments = async () => {
    try {
      const res = await api.get('/departments');
      setDepartments(res.data.items || []);
    } catch (error) {
      console.error(error);
    }
  };

  const fetchUsersByDepartment = async (deptId) => {
    const currentOwnerId = form.getFieldValue('owner_id');
    
    // Xóa danh sách cũ ngay lập tức để không bị lỗi hiển thị danh sách cũ (chỉ giữ lại người đang được chọn để không bị lỗi hiện UUID)
    setUsers(prev => {
      const owner = prev.find(u => u.id === currentOwnerId);
      return owner ? [owner] : [];
    });

    if (!deptId) {
      return;
    }
    setLoadingUsers(true);
    try {
      const res = await api.get(`/users?department_id=${deptId}&page_size=100`);
      const fetchedUsers = res.data.items || [];
      
      setUsers(prev => {
        const owner = prev.find(u => u.id === currentOwnerId);
        // Đảm bảo người đang được chọn luôn có trong danh sách
        if (owner && !fetchedUsers.find(u => u.id === owner.id)) {
          return [...fetchedUsers, owner];
        }
        return fetchedUsers;
      });
    } catch (error) {
      console.error(error);
    } finally {
      setLoadingUsers(false);
    }
  };

  useEffect(() => {
    fetchUsersByDepartment(selectedDepartmentId);
  }, [selectedDepartmentId]);

  // Listen to URL changes for status
  useEffect(() => {
    const statusFromUrl = searchParams.get('status') || '';
    if (statusFilter !== statusFromUrl) {
      setStatusFilter(statusFromUrl);
    }
  }, [searchParams]);

  useEffect(() => {
    fetchDocuments();
  }, [fetchDocuments]);

  useEffect(() => {
    fetchDepartments();
  }, []);

  const handleOpenModal = async (record = null) => {
    if (record) {
      setEditingId(record.id);
      form.setFieldsValue({
        ...record,
        expiry_date: dayjs(record.expiry_date),
      });
      setFileList(record.file_url ? [{ uid: '-1', name: record.file_name || 'File đính kèm', status: 'done', url: record.file_url }] : []);
      
      // Explicitly fetch the owner's details if they exist so their name displays properly
      // even before the department users finish loading or if they belong to another dept.
      if (record.owner_id) {
        try {
          const res = await api.get(`/users/${record.owner_id}`);
          setUsers(prev => {
            const exists = prev.find(u => u.id === res.data.id);
            if (exists) return prev;
            return [...prev, res.data];
          });
        } catch (e) {
          console.error("Could not fetch owner details", e);
        }
      }
    } else {
      setEditingId(null);
      form.resetFields();
      if (currentUser) {
        form.setFieldsValue({ owner_id: currentUser.id }); // Default to current user
        setUsers([currentUser]); // Đảm bảo currentUser có sẵn trong danh sách để không bị hiện UUID thô
      }
      setFileList([]);
    }
    setIsModalVisible(true);
  };

  const handleCancel = () => {
    setIsModalVisible(false);
    form.resetFields();
    setFileList([]);
  };

  const [saving, setSaving] = useState(false);

  const handleSave = async (values) => {
    setSaving(true);
    try {
      const payload = {
        ...values,
        expiry_date: values.expiry_date.format('YYYY-MM-DD'),
      };
      
      let docId = editingId;
      if (editingId) {
        await api.put(`/documents/${editingId}`, payload);
      } else {
        const res = await api.post('/documents', payload);
        docId = res.data.id;
      }

      // Handle file upload
      const currentFile = fileList[0];
      // Nếu là file mới chọn từ máy tính, nó có thể là File object hoặc có thuộc tính originFileObj
      const actualFileToUpload = currentFile?.originFileObj || (currentFile instanceof File ? currentFile : null);
      
      if (actualFileToUpload) {
        try {
          const formData = new FormData();
          formData.append('file', actualFileToUpload);
          await api.post(`/documents/${docId}/upload`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          });
          message.success(editingId ? 'Cập nhật văn bản và tải file thành công!' : 'Thêm văn bản và tải file thành công!');
        } catch (uploadErr) {
          message.warning('Đã lưu văn bản nhưng tải file thất bại: ' + (uploadErr.response?.data?.detail || uploadErr.message));
        }
      } else {
        message.success(editingId ? 'Cập nhật văn bản thành công!' : 'Thêm văn bản thành công!');
      }

      setIsModalVisible(false);
      fetchDocuments();
    } catch (error) {
      message.error(error.response?.data?.detail || 'Lỗi khi lưu văn bản');
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (id) => {
    try {
      await api.delete(`/documents/${id}`);
      message.success('Đã xóa văn bản');
      fetchDocuments();
    } catch (error) {
      message.error('Lỗi khi xóa văn bản');
    }
  };

  const uploadProps = {
    onRemove: (file) => {
      setFileList([]);
    },
    beforeUpload: (file) => {
      const isLt10M = file.size / 1024 / 1024 < 10;
      if (!isLt10M) {
        message.error('Dung lượng file phải nhỏ hơn 10MB!');
        return Upload.LIST_IGNORE;
      }
      setFileList([file]);
      return false; // Prevent auto upload
    },
    fileList,
    accept: ".pdf,.doc,.docx"
  };

  const getStatusTag = (status) => {
    switch (status) {
      case 'active': return <Tag color="success">Còn hiệu lực</Tag>;
      case 'expiring_soon': return <Tag color="warning">Sắp hết hạn</Tag>;
      case 'expired': return <Tag color="error">Đã hết hạn</Tag>;
      default: return <Tag>{status}</Tag>;
    }
  };

  const columns = [
    { 
      title: 'Số/Ký hiệu', 
      dataIndex: 'document_number', 
      key: 'document_number',
      sorter: (a, b) => (a.document_number || '').localeCompare(b.document_number || '')
    },
    { 
      title: 'Tên/Trích yếu', 
      dataIndex: 'title', 
      key: 'title', 
      width: '30%',
      sorter: (a, b) => a.title.localeCompare(b.title)
    },
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
      title: 'Ngày hết hạn', 
      dataIndex: 'expiry_date', 
      key: 'expiry_date',
      sorter: (a, b) => dayjs(a.expiry_date).unix() - dayjs(b.expiry_date).unix(),
      defaultSortOrder: 'ascend',
      render: (date) => <span className="font-medium text-gray-700">{dayjs(date).format('DD/MM/YYYY')}</span>
    },
    { 
      title: 'Trạng thái', 
      dataIndex: 'status', 
      key: 'status',
      render: (status) => getStatusTag(status)
    },
    {
      title: 'File đính kèm',
      key: 'file',
      render: (_, record) => record.file_url ? (
        <a href={record.file_url} target="_blank" rel="noopener noreferrer" className="flex items-center gap-1 text-indigo-600 hover:text-indigo-800">
          <DownloadOutlined />
          <span className="text-xs">{record.file_size ? formatBytes(record.file_size) : 'Tải xuống'}</span>
        </a>
      ) : <span className="text-gray-400 text-xs">Không có file</span>
    },
    {
      title: 'Hành động',
      key: 'action',
      render: (_, record) => (
        <Space size="small">
          <Button type="text" icon={<EditOutlined />} onClick={() => handleOpenModal(record)} className="text-gray-600 hover:text-indigo-600" />
          <Popconfirm
            title="Bạn có chắc chắn muốn xóa văn bản này?"
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
        <h2 className="text-2xl font-bold text-gray-800 m-0">Quản lý Văn bản</h2>
        <Button type="primary" icon={<PlusOutlined />} onClick={() => handleOpenModal()} size="large" className="rounded-lg shadow-sm">
          Thêm Văn bản
        </Button>
      </div>

      <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-100 space-y-4">
        <div className="flex flex-col md:flex-row gap-4">
          <Search
            placeholder="Tìm kiếm theo Tên hoặc Số/Ký hiệu..."
            allowClear
            onSearch={(value) => setSearchText(value)}
            style={{ maxWidth: 400 }}
            size="large"
            className="flex-1"
          />
          <div className="flex gap-4">
            <Select
              allowClear
              placeholder="Chọn Phòng ban"
              style={{ width: 200 }}
              size="large"
              value={departmentFilter || undefined}
              onChange={(value) => setDepartmentFilter(value)}
            >
              {departments.map(dept => (
                <Option key={dept.id} value={dept.id}>{dept.name}</Option>
              ))}
            </Select>
            <Select
              allowClear
              placeholder="Trạng thái"
              style={{ width: 160 }}
              size="large"
              value={statusFilter || undefined}
              onChange={(value) => {
                setStatusFilter(value);
                if (value) {
                  setSearchParams({ status: value });
                } else {
                  setSearchParams({});
                }
              }}
            >
              <Option value="active">Còn hiệu lực</Option>
              <Option value="expiring_soon">Sắp hết hạn</Option>
              <Option value="expired">Đã quá hạn</Option>
            </Select>
          </div>
        </div>

        <Table
          columns={columns}
          dataSource={documents}
          rowKey="id"
          loading={loading}
          locale={{
            emptyText: <Empty description="Không tìm thấy văn bản nào" />
          }}
          className="[&_.ant-table-thead>tr>th]:bg-gray-50 [&_.ant-table-thead>tr>th]:text-gray-600 [&_.ant-table-thead>tr>th]:font-semibold"
        />
      </div>

      <Modal
        title={<span className="text-lg font-semibold">{editingId ? 'Sửa Văn bản' : 'Thêm Văn bản mới'}</span>}
        open={isModalVisible}
        onCancel={handleCancel}
        onOk={() => form.submit()}
        width={650}
        destroyOnHidden
        okText={saving ? "Đang lưu..." : "Lưu lại"}
        cancelText="Hủy bỏ"
        confirmLoading={saving}
        cancelButtonProps={{ disabled: saving }}
      >
        <Form form={form} layout="vertical" onFinish={handleSave} className="mt-4">
          <div className="grid grid-cols-2 gap-4">
            <Form.Item name="document_number" label={<span className="font-medium text-gray-700">Số/Ký hiệu</span>}>
              <Input placeholder="VD: 101/QĐ-TVU" />
            </Form.Item>
            <Form.Item name="department_id" label={<span className="font-medium text-gray-700">Phòng ban phụ trách</span>} rules={[{ required: true, message: 'Vui lòng chọn phòng ban' }]}>
              <Select placeholder="Chọn phòng ban">
                {departments.map(dept => (
                  <Option key={dept.id} value={dept.id}>{dept.name}</Option>
                ))}
              </Select>
            </Form.Item>
          </div>
          
          <Form.Item name="owner_id" label={<span className="font-medium text-gray-700">Người phụ trách (Nhận nhắc nhở)</span>} rules={[{ required: true, message: 'Vui lòng chọn người phụ trách' }]}>
            <Select 
              placeholder={loadingUsers ? "Đang tải danh sách..." : "Chọn người nhận mail"} 
              showSearch
              disabled={loadingUsers}
              optionFilterProp="filterName"
              options={users
                .filter(u => !selectedDepartmentId || u.department_id === selectedDepartmentId || u.id === form.getFieldValue('owner_id'))
                .map(u => ({
                  label: (
                    <div className="flex justify-between items-center w-full">
                      <span className="truncate pr-2">{u.full_name} <span className="text-gray-400 text-xs">({u.email})</span></span>
                      <div className="flex-shrink-0">
                        {u.id === currentUser?.id && <Tag color="blue" className="m-0 border-0">Bạn</Tag>}
                        {u.role === 'admin' && u.id !== currentUser?.id && <Tag color="purple" className="m-0 border-0">Admin</Tag>}
                      </div>
                    </div>
                  ),
                  value: u.id,
                  filterName: `${u.full_name} ${u.email}`
                }))
              }
            />
          </Form.Item>
          
          <Form.Item name="title" label={<span className="font-medium text-gray-700">Tên văn bản / Trích yếu</span>} rules={[{ required: true, message: 'Vui lòng nhập tên văn bản' }]}>
            <Input.TextArea rows={2} placeholder="Nhập trích yếu văn bản..." />
          </Form.Item>
          
          <div className="grid grid-cols-2 gap-4">
            <Form.Item name="expiry_date" label={<span className="font-medium text-gray-700">Ngày hết hạn</span>} rules={[{ required: true, message: 'Vui lòng chọn ngày' }]}>
              <DatePicker format="DD/MM/YYYY" className="w-full" />
            </Form.Item>
            
            <Form.Item label={<span className="font-medium text-gray-700">File đính kèm (Tối đa 10MB)</span>}>
              <Upload {...uploadProps} maxCount={1}>
                <Button icon={<UploadOutlined />} className="w-full text-left">
                  {editingId && fileList.length > 0 && fileList[0].url && !fileList[0].originFileObj 
                    ? "Tải file mới lên (để thay thế)" 
                    : "Chọn file PDF/Word"}
                </Button>
              </Upload>
            </Form.Item>
          </div>
          
          <Form.Item name="description" label={<span className="font-medium text-gray-700">Ghi chú thêm</span>} className="mb-0">
            <Input.TextArea rows={2} placeholder="Ghi chú thêm (tùy chọn)..." />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default Documents;
