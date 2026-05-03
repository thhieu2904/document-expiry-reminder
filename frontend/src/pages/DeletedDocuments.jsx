import React, { useState, useEffect, useMemo } from 'react';
import { Table, Input, Select, Tag, Empty } from 'antd';
import { DownloadOutlined } from '@ant-design/icons';
import dayjs from 'dayjs';
import api from '../services/api';

const { Search } = Input;
const { Option } = Select;

const DeletedDocuments = () => {
  const [documents, setDocuments] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchText, setSearchText] = useState('');
  const [departmentFilter, setDepartmentFilter] = useState(null);

  const fetchDepartments = async () => {
    try {
      const res = await api.get('/departments');
      setDepartments(res.data.items || []);
    } catch (error) {
      console.error(error);
    }
  };

  const fetchUsers = async () => {
    try {
      const res = await api.get('/users');
      setUsers(res.data.items || []);
    } catch (error) {
      console.error(error);
    }
  };

  const fetchDocuments = async () => {
    setLoading(true);
    try {
      // Explicitly request deleted status
      const res = await api.get('/documents?status_filter=deleted');
      setDocuments(res.data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDepartments();
    fetchUsers();
    fetchDocuments();
  }, []);

  const filteredDocuments = useMemo(() => {
    let filtered = documents;
    if (departmentFilter) {
      filtered = filtered.filter(d => d.department_id === departmentFilter);
    }
    if (searchText) {
      const lowerSearch = searchText.toLowerCase();
      filtered = filtered.filter(d => 
        (d.title && d.title.toLowerCase().includes(lowerSearch)) ||
        (d.document_number && d.document_number.toLowerCase().includes(lowerSearch))
      );
    }
    return filtered;
  }, [documents, searchText, departmentFilter]);

  const columns = [
    {
      title: 'Số hiệu',
      dataIndex: 'document_number',
      key: 'document_number',
      width: '12%',
      render: text => <span className="font-medium text-gray-700">{text || '-'}</span>,
    },
    {
      title: 'Tên văn bản / Trích yếu',
      dataIndex: 'title',
      key: 'title',
      width: '28%',
      render: (text, record) => (
        <div className="flex flex-col">
          <span className="font-medium text-gray-900">{text}</span>
          {record.description && <span className="text-gray-500 text-xs mt-1 truncate">{record.description}</span>}
        </div>
      ),
    },
    {
      title: 'Phòng ban',
      key: 'department',
      width: '15%',
      render: (_, record) => {
        const dept = departments.find(d => d.id === record.department_id);
        return <span className="text-sm">{dept ? dept.name : '-'}</span>;
      }
    },
    {
      title: 'Người phụ trách',
      key: 'owner',
      width: '15%',
      render: (_, record) => {
        const owner = users.find(u => u.id === record.owner_id);
        return owner ? (
          <div className="flex flex-col">
            <span className="text-sm font-medium">{owner.full_name}</span>
            <span className="text-xs text-gray-500">{owner.email}</span>
          </div>
        ) : <span className="text-gray-400">Không tìm thấy</span>;
      }
    },
    {
      title: 'Ngày hết hạn',
      dataIndex: 'expiry_date',
      key: 'expiry_date',
      width: '12%',
      render: date => (
        <span className="text-sm font-medium text-gray-700">
          {date ? dayjs(date).format('DD/MM/YYYY') : '-'}
        </span>
      ),
      sorter: (a, b) => new Date(a.expiry_date) - new Date(b.expiry_date),
    },
    {
      title: 'Trạng thái',
      key: 'status',
      width: '18%',
      render: () => <Tag color="error" className="rounded-md px-2 py-1 border-0">Đã xóa</Tag>,
    }
  ];

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h2 className="text-2xl font-bold text-gray-800 m-0">Thùng rác</h2>
          <p className="text-gray-500 m-0 mt-1">Quản lý các văn bản đã bị xóa (Chỉ xem)</p>
        </div>
      </div>

      <div className="bg-white p-4 md:p-5 rounded-xl shadow-sm border border-gray-200">
        <div className="flex flex-col md:flex-row gap-4 mb-5 bg-gray-50 p-4 rounded-lg border border-gray-100">
          <div className="flex-1">
            <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1.5">Tìm kiếm</label>
            <Search
              placeholder="Nhập số hiệu hoặc tên văn bản..."
              allowClear
              size="large"
              onChange={(e) => setSearchText(e.target.value)}
              className="w-full shadow-sm"
            />
          </div>
          <div className="w-full md:w-64">
            <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1.5">Phòng ban</label>
            <Select
              allowClear
              placeholder="Tất cả phòng ban"
              size="large"
              value={departmentFilter || undefined}
              onChange={(value) => setDepartmentFilter(value)}
              className="w-full shadow-sm"
            >
              {departments.map(dept => (
                <Option key={dept.id} value={dept.id}>{dept.name}</Option>
              ))}
            </Select>
          </div>
        </div>

        <Table
          columns={columns}
          dataSource={filteredDocuments}
          rowKey="id"
          loading={loading}
          pagination={{ 
            pageSize: 10,
            showSizeChanger: true,
            showTotal: (total, range) => `${range[0]}-${range[1]} của ${total} văn bản`
          }}
          locale={{
            emptyText: <Empty description="Thùng rác trống" />
          }}
          className="[&_.ant-table-thead>tr>th]:bg-gray-50 [&_.ant-table-thead>tr>th]:text-gray-600 [&_.ant-table-thead>tr>th]:font-semibold"
        />
      </div>
    </div>
  );
};

export default DeletedDocuments;
