import { create } from "zustand";

type ProjectState = {
  currentProjectId: number | null;
  setCurrentProjectId: (projectId: number | null) => void;
};

export const useProjectStore = create<ProjectState>((set) => ({
  currentProjectId: null,
  setCurrentProjectId: (currentProjectId) => set({ currentProjectId })
}));
