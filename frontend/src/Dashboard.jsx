import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './App.css';
const Dashboard = () => {
  const [processingFileId, setProcessingFileId] = useState(null);
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
  ]);

  // Handle file upload and store file metadata in state
  const handleUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const newFile = {
        id: uploadedFiles.length + 1, // Unique ID for each uploaded file
        name: file.name, // File name
        date: new Date().toISOString().split('T')[0],
        file: file, // Actual file object to pass to the backend
      };
      setUploadedFiles([...uploadedFiles, newFile]); // Add new file to state
    }
  };
  // Handle file delete by removing file from state using ID
  const handleDelete = (id) => {
    setUploadedFiles(uploadedFiles.filter((file) => file.id !== id));
  };

  // Navigate hook to redirect user after successful processing
  const navigate = useNavigate();

  // Handle PDF processing: upload file to backend and navigate to chat page
  const handleProcess = async (file) => {
    const formData = new FormData(); // Prepare form data for file upload
    setProcessingFileId(file.id); // Set loading state for UI feedback

    try {
      formData.append('file', file.file);

      // Send POST request to backend API to process PDF
      const response = await fetch('http://127.0.0.1:8000/process', {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) throw new Error('Upload Failed');
      else {
        // On success, navigate to chat route with file info
        const data = await response.json();
        navigate(`/chat/${file.id}`, {
          state: { filename: file.name },
        });
      }
    } catch (error) {
      // Handle upload errors
      console.error('Error:', error);
    } finally {
      // Reset loading state
      setProcessingFileId(null);
    }
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
                      disabled={processingFileId === file.id}
                    >
                      {processingFileId === file.id ? (
                        <>
                          <svg
                            className='animate-spin h-3 w-3 text-white'
                            xmlns='http://www.w3.org/2000/svg'
                            fill='none'
                            viewBox='0 0 24 24'
                          >
                            <circle
                              className='opacity-25'
                              cx='12'
                              cy='12'
                              r='10'
                              stroke='currentColor'
                              strokeWidth='4'
                            />
                            <path
                              className='opacity-75'
                              fill='currentColor'
                              d='M4 12a8 8 0 018-8v4l3-3-3-3v4a8 8 0 11-8 8z'
                            />
                          </svg>
                          Processing...
                        </>
                      ) : (
                        'Process'
                      )}
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
