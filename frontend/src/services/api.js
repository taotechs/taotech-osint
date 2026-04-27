import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:5000",
  timeout: 120000,
});

export const getHealth = () => api.get("/api/health");
export const getReports = () => api.get("/api/reports");
export const scanUsername = (username) =>
  api.get("/api/osint/username", { params: { username } });
export const scanEmail = (email) =>
  api.get("/api/osint/email", { params: { email } });
export const scanDomain = (domain) =>
  api.get("/api/osint/domain", { params: { domain } });

export default api;
