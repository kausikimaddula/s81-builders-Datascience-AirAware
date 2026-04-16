import axios from "axios";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8001";

const client = axios.create({
  baseURL: API_BASE,
});

export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append("file", file);
  const { data } = await client.post("/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
};

export const getProgress = async () => {
  const { data } = await client.get("/progress");
  return data;
};

export const getStats = async () => {
  const { data } = await client.get("/stats");
  return data;
};

export const getCleanedData = async (params = {}) => {
  const { data } = await client.get("/cleaned-data", { params });
  return data;
};

export const downloadCleanedData = () => `${API_BASE}/download`;

export const getMappings = async () => {
  const { data } = await client.get("/mappings");
  return data;
};

export const updateMappings = async (mapping) => {
  const { data } = await client.put("/mappings", mapping);
  return data;
};

export const scanDuplicates = async (payload = {}) => {
  const { data } = await client.post("/duplicates/scan", payload);
  return data;
};

export const trainModel = async () => {
  const { data } = await client.post("/ml/train");
  return data;
};

export const predictCategories = async (issues = []) => {
  const { data } = await client.post("/ml/predict", { issues });
  return data;
};

export const imputeComplaint = async (payload) => {
  const { data } = await client.post("/ml/impute", payload);
  return data;
};
