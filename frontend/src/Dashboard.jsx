import React, { useState } from 'react';
import './App.css';
const Dashboard = () => {
  const [uploadedFiles, setUploadedFiles] = useState([
    {
      id: 1,
      name: 'SAMPLEPDF1.pdf',
      date: '2024-04-30',
    },
    {
      id: 2,
      name: 'SAMPLEPDF2.pdf',
      date: '2024-04-29',
    },
    {
      id: 3,
      name: 'SAMPLEPDF3.pdf',
      date: '2024-04-28',
    },
  ]);

  const handleUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const newFile = {
        id: uploadedFiles.length + 1,
        name: file.name,
        date: new Date().toISOString().split('T')[0],
      };
      setUploadedFiles([...uploadedFiles, newFile]);
    }
  };

  const handleDelete = (id) => {
    setUploadedFiles(uploadedFiles.filter((file) => file.id !== id));
  };

  const handleProcess = (file) => {
    console.log('Processing file:', file.name);
    // Call your backend API here
  };

  return (
    <div className='min-h-screen bg-teal-900 p-6 text-white'>
      <div className='max-w-4xl mx-auto'>
        <h1 className='text-4xl font-bold text-center mb-8'>Upload PDF</h1>

        <div className='flex items-center justify-center gap-4 mb-8'>
          <input
            type='file'
            accept='.pdf'
            className='block w-full max-w-xs text-sm text-gray-300
              file:mr-4 file:py-2 file:px-4
              file:rounded-full file:border-0
              file:text-sm file:font-semibold
              file:bg-teal-700 file:text-white
              hover:file:bg-teal-600'
            onChange={handleUpload}
          />
        </div>

        <div className='bg-teal-800 rounded-lg shadow p-4'>
          <table className='w-full table-auto'>
            <thead>
              <tr className='text-left border-b border-teal-600'>
                <th className='py-2 px-4'>File Name</th>
                <th className='py-2 px-4'>Date Uploaded</th>
                <th className='py-2 px-4'>Actions</th>
              </tr>
            </thead>
            <tbody>
              {uploadedFiles.map((file) => (
                <tr key={file.id} className='border-b border-teal-700'>
                  <td className='py-2 px-4'>{file.name}</td>
                  <td className='py-2 px-4'>{file.date}</td>
                  <td className='py-2 px-4 flex gap-3'>
                    <button
                      className='bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded'
                      onClick={() => handleDelete(file.id)}
                    >
                      Delete
                    </button>
                    <button
                      className='bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded'
                      onClick={() => handleProcess(file)}
                    >
                      Process
                    </button>
                  </td>
                </tr>
              ))}
              {uploadedFiles.length === 0 && (
                <tr>
                  <td colSpan='3' className='text-center py-4 text-gray-300'>
                    No files uploaded yet.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
