import React from 'react';
import { Routes, Route } from 'react-router-dom';
import UsersList from './pages/Users/UsersList';
import CreateUser from './pages/Users/CreateUser';
import UserDetail from './pages/Users/UserDetail';
import EditUser from './pages/Users/EditUser';

import Register from './pages/Auth/Register.jsx';
import Login from './pages/Auth/Login.jsx';
import AuthMe  from './pages/Auth/AuthMe.jsx';

import Roles from './pages/Roles/Roles.jsx';
import FilesPage from './pages/Files/FilesPage.jsx';

import ProcessTask from './pages/Tasks/ProcessTask.jsx';
import UploadTask from './pages/Tasks/UploadTask.jsx';


const App = () => {
  return (
    <Routes>
      <Route path="/users/list" element={<UsersList />} />
      <Route path="/users/create" element={<CreateUser />} />
      <Route path="/users/:id" element={<UserDetail />} />
      <Route path="/users/:id/edit" element={<EditUser />} />

      <Route path="/auth/register" element={<Register />} />
      <Route path="/auth/login" element={<Login />} />
      <Route path="/auth/me" element={<AuthMe />} />

      <Route path="/roles" element={<Roles />} />
      <Route path="/files" element={<FilesPage />} />

      <Route path="/tasks/process" element={<ProcessTask />} />
      <Route path="/tasks/upload" element={<UploadTask />} />
    </Routes>
  );
};

export default App;
