import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

function UserDashboard() {
  const [files, setFiles] = useState([]);
  const [error, setError] = useState('');
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    fetchFiles();
  }, []);

  const fetchFiles = async () => {
    try {
      const response = await fetch('http://0.0.0.0:80/user/files', {
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
      } else {
        setError('Failed to fetch files');
      }
    } catch (err) {
      setError('An error occurred while fetching files');
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

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>User Dashboard</h1>
        <button onClick={() => {
          logout();
          navigate('/login');
        }} className="logout-btn">
          Logout
        </button>
      </header>
      
      {error && <div className="error-message">{error}</div>}
      
      <div className="files-container">
        <h2>Your Available Files</h2>
        {files.length === 0 ? (
          <p>No files available for download</p>
        ) : (
          <table className="files-table">
            <thead>
              <tr>
                <th>Filename</th>
                <th>Upload Date</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {files.map((file) => (
                <tr key={file.id}>
                  <td>{file.filename}</td>
                  <td>{new Date(file.upload_date).toLocaleDateString()}</td>
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

export default UserDashboard;