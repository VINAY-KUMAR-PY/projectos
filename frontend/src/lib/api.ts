import axios from "axios";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"
});

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
