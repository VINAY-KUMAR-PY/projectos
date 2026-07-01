import axios from "axios";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"
});

export const apiBaseUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

api.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("token");
    if (token) config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authApi = {
  login: (email: string, password: string) => api.post("/api/auth/login", { email, password }),
  register: (name: string, email: string, password: string) => api.post("/api/auth/register", { name, email, password }),
  me: () => api.get("/api/auth/me")
};

export const projectsApi = {
  list: () => api.get("/api/projects"),
  create: (data: unknown) => api.post("/api/projects", data),
  get: (id: number) => api.get(`/api/projects/${id}`),
  update: (id: number, data: unknown) => api.put(`/api/projects/${id}`, data),
  delete: (id: number) => api.delete(`/api/projects/${id}`)
};

export const agentsApi = {
  list: () => api.get("/api/agents"),
  run: (projectId: number, agentType: string, userInput: string) =>
    api.post("/api/agents/run", { project_id: projectId, agent_type: agentType, user_input: userInput }),
  runAll: (projectId: number) => api.post("/api/agents/run-all", { project_id: projectId }),
  history: (projectId: number) => api.get(`/api/agents/runs/${projectId}`),
  chat: (projectId: number, message: string) => api.post("/api/agents/chat", { project_id: projectId, message })
};

export const filesApi = {
  upload: (projectId: number, formData: FormData) => api.post(`/api/files/upload/${projectId}`, formData),
  list: (projectId: number) => api.get(`/api/files/${projectId}`),
  delete: (fileId: number) => api.delete(`/api/files/${fileId}`)
};

export const outputsApi = {
  list: (projectId: number) => api.get(`/api/outputs/${projectId}`),
  get: (outputId: number) => api.get(`/api/outputs/item/${outputId}`),
  export: (outputId: number, format: string) => api.post(`/api/outputs/${outputId}/export`, { format })
};

export const generationApi = {
  document: (projectId: number) => api.post(`/api/projects/${projectId}/generate-document`),
  ppt: (projectId: number) => api.post(`/api/projects/${projectId}/generate-ppt`),
  diagram: (projectId: number, type: string) => api.post(`/api/projects/${projectId}/generate-diagram?type=${type}`),
  code: (projectId: number, data: unknown) => api.post(`/api/projects/${projectId}/build-code`, data),
  review: (projectId: number) => api.post(`/api/projects/${projectId}/review`, {}),
  deployment: (projectId: number, target: string) => api.post(`/api/projects/${projectId}/generate-deployment?target=${target}`)
};

export const collaborationApi = {
  members: (projectId: number) => api.get(`/api/collaboration/projects/${projectId}/members`),
  invite: (projectId: number, data: unknown) => api.post(`/api/collaboration/projects/${projectId}/members`, data),
  comments: (projectId: number) => api.get(`/api/collaboration/projects/${projectId}/comments`),
  addComment: (projectId: number, data: unknown) => api.post(`/api/collaboration/projects/${projectId}/comments`, data)
};

export const learningApi = {
  run: (action: string, projectId: number, message: string) =>
    api.post(`/api/agents/learning/${action}`, { project_id: projectId, message })
};

export const marketplaceApi = {
  list: (search?: string) => api.get(`/api/marketplace${search ? `?search=${encodeURIComponent(search)}` : ""}`),
  use: (itemId: number) => api.post(`/api/marketplace/${itemId}/use`, {})
};

export const securityApi = {
  enable2fa: () => api.post("/api/users/me/2fa/enable"),
  verify2fa: (code: string) => api.post("/api/users/me/2fa/verify", { code }),
  exportData: () => api.get("/api/users/me/export")
};

export const tasksApi = {
  list: (projectId: number) => api.get(`/api/tasks/${projectId}`),
  create: (projectId: number, data: unknown) => api.post(`/api/tasks/${projectId}`, data),
  update: (taskId: number, data: unknown) => api.put(`/api/tasks/${taskId}`, data),
  delete: (taskId: number) => api.delete(`/api/tasks/${taskId}`),
  generate: (projectId: number) => api.post(`/api/tasks/generate/${projectId}`)
};

export const dashboardApi = { stats: () => api.get("/api/dashboard") };
export const subscriptionsApi = {
  plans: () => api.get("/api/subscriptions/plans"),
  myPlan: () => api.get("/api/subscriptions/my-plan"),
  createCheckout: (plan: string) => api.post("/api/subscriptions/create", { plan })
};

export default api;
