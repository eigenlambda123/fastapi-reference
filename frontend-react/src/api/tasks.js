import api from "./axios";

// Start a background task
export const runBackgroundTask = async (data) => {
  const res = await api.post("/tasks/process", data);
  return res.data;
};

// Upload file for task
export const uploadFileTask = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const res = await api.post("/tasks/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return res.data;
};
