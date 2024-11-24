import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

function AdminDashboard() {
  const [files, setFiles] = useState([]);
  const [users, setUsers] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    fetchFiles();
    fetchUsers();
  }, []);

  const fetchFiles = async () => {
    try {
      const response = await fetch('http://0.0.0.0:80/admin/files', {
        headers: {
          'Authorization': `Bearer ${user.access_token}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        setFiles(data);
      } else if (response.status === 401) {
        logout();
        navigate('/login');
      }
    } catch (err) {
      setError('Failed to fetch files');
    }
  };

  const fetchUsers = async () => {
    try {
      const response = await fetch('http://0.0.0.0:80/admin/users', {
        headers: {
          'Authorization': `Bearer ${user.access_token}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        setUsers(data);
      }
    } catch (err) {
      setError('Failed to fetch users');
    }
  };

  const handleFileUpload = async (e) => {
    e.preventDefault();
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch('http://0.0.0.0:80/admin/upload', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${user.access_token}`
        },
        body: formData
      });

      if (response.ok) {
        setSuccess('File uploaded successfully');
        setSelectedFile(null);
        fetchFiles();
      } else {
        setError('Failed to upload file');
      }
    } catch (err) {
      setError('An error occurred while uploading the file');
    }
  };
  
  const handleDownload = async (fileId) => {
    try {
      const response = await fetch(`http://0.0.0.0:80/user/download/${fileId}`, {
        headers: {
          'Authorization': `Bearer ${user.access_token}`
        }
      });
      
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `file-${fileId}`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
      } else {
        setError('Failed to download file');
      }
    } catch (err) {
      setError('An error occurred while downloading the file');
    }
  };

  const handleDelete = async (fileId) => {
    try {
      const response = await fetch(`http://0.0.0.0:80/admin/files/${fileId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${user.access_token}`
        }
      });

      if (response.ok) {
        setSuccess('File deleted successfully');
        fetchFiles();
      } else {
        setError('Failed to delete file');
      }
    } catch (err) {
      setError('An error occurred while deleting the file');
    }
  };

  const handleGrantAccess = async (fileId, userId) => {
    try {
      const response = await fetch('http://0.0.0.0:80/admin/grant-access', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${user.access_token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          file_id: fileId,
          user_id: userId
        })
      });

      if (response.ok) {
        setSuccess('Access granted successfully');
      } else {
        setError('Failed to grant access');
      }
    } catch (err) {
      setError('An error occurred while granting access');
    }
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Admin Dashboard</h1>
        <button onClick={() => {
          logout();
          navigate('/login');
        }} className="logout-btn">
          Logout
        </button>
      </header>

      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">{success}</div>}

      <div className="upload-section">
        <h2>Upload New File</h2>
        <form onSubmit={handleFileUpload}>
          <input
            type="file"
            onChange={(e) => setSelectedFile(e.target.files[0])}
            className="file-input"
          />
          <button type="submit" disabled={!selectedFile} className="upload-btn">
            Upload
          </button>
        </form>
      </div>

      <div className="files-container">
        <h2>Manage Files</h2>
        {files.length === 0 ? (
          <p>No files uploaded yet</p>
        ) : (
          <table className="files-table">
            <thead>
              <tr>
                <th>Filename</th>
                <th>Download Count</th>   
                <th>Upload Date</th>
                <th>Grant Access</th>
                <th>Actions</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {files.map((file) => (
                <tr key={file.id}>
                  <td>{file.filename}</td>
                  <td>{file.download_count}</td>
                  <td>{new Date(file.upload_date).toLocaleDateString()}</td>
                  <td>
                    <select
                      onChange={(e) => handleGrantAccess(file.id, e.target.value)}
                      className="user-select"
                    >
                      <option value="">Select User</option>
                      {users.map((user) => (
                        <option key={user.id} value={user.id}>
                          {user.username}
                        </option>
                      ))}
                    </select>
                  </td>
                  <td>
                    <button
                      onClick={() => handleDelete(file.id)}
                      className="delete-btn"
                    >
                      Delete
                    </button>
                  </td>
                  <td>
                    <button
                      onClick={() => handleDownload(file.id)}
                      className="download-btn"
                    >
                      Download
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default AdminDashboard;
