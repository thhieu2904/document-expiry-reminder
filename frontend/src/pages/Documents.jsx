import React, { useState, useEffect, useCallback } from 'react';
import { Table, Button, Modal, Form, Input, Select, DatePicker, Upload, message, Popconfirm, Space, Tag, Empty } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined, UploadOutlined, DownloadOutlined, SearchOutlined } from '@ant-design/icons';
import { useSearchParams } from 'react-router-dom';
import dayjs from 'dayjs';
import api from '../services/api';

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
  const [loading, setLoading] = useState(false);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [fileList, setFileList] = useState([]);
  const [form] = Form.useForm();
  const [searchParams, setSearchParams] = useSearchParams();

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

  const handleOpenModal = (record = null) => {
    if (record) {
      setEditingId(record.id);
      form.setFieldsValue({
        ...record,
        expiry_date: dayjs(record.expiry_date),
      });
      setFileList(record.file_url ? [{ uid: '-1', name: record.file_name || 'File đính kèm', status: 'done', url: record.file_url }] : []);
    } else {
      setEditingId(null);
      form.resetFields();
      setFileList([]);
    }
    setIsModalVisible(true);
  };

  const handleCancel = () => {
    setIsModalVisible(false);
    form.resetFields();
    setFileList([]);
  };

  const handleSave = async (values) => {
    try {
      const payload = {
        ...values,
        expiry_date: values.expiry_date.format('YYYY-MM-DD'),
      };
      
      let docId = editingId;
      if (editingId) {
        await api.put(`/documents/${editingId}`, payload);
        message.success('Cập nhật văn bản thành công');
      } else {
        const res = await api.post('/documents', payload);
        docId = res.data.id;
        message.success('Thêm văn bản thành công');
      }

      // Handle file upload
      const currentFile = fileList[0];
      if (currentFile && currentFile.originFileObj) {
        const formData = new FormData();
        formData.append('file', currentFile.originFileObj);
        await api.post(`/documents/${docId}/upload`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
      }

      setIsModalVisible(false);
      fetchDocuments();
    } catch (error) {
      message.error(error.response?.data?.detail || 'Lỗi khi lưu văn bản');
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
        destroyOnClose
        okText="Lưu lại"
        cancelText="Hủy bỏ"
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
          
          <Form.Item name="title" label={<span className="font-medium text-gray-700">Tên văn bản / Trích yếu</span>} rules={[{ required: true, message: 'Vui lòng nhập tên văn bản' }]}>
            <Input.TextArea rows={2} placeholder="Nhập trích yếu văn bản..." />
          </Form.Item>
          
          <div className="grid grid-cols-2 gap-4">
            <Form.Item name="expiry_date" label={<span className="font-medium text-gray-700">Ngày hết hạn</span>} rules={[{ required: true, message: 'Vui lòng chọn ngày' }]}>
              <DatePicker format="DD/MM/YYYY" className="w-full" />
            </Form.Item>
            
            <Form.Item label={<span className="font-medium text-gray-700">File đính kèm (Tối đa 10MB)</span>}>
              <Upload {...uploadProps} maxCount={1}>
                <Button icon={<UploadOutlined />} className="w-full text-left">Chọn file PDF/Word</Button>
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
