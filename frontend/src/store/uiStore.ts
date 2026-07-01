import { create } from "zustand";

export const useUiStore = create<{ sidebarOpen: boolean; setSidebarOpen: (open: boolean) => void }>((set) => ({
  sidebarOpen: false,
  setSidebarOpen: (sidebarOpen) => set({ sidebarOpen })
}));
