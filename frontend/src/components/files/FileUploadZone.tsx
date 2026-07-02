"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { FileText, Loader2, Trash2, UploadCloud } from "lucide-react";

import { filesApi } from "@/lib/api";

type ProjectFile = {
  id: number;
  file_name: string;
  file_type?: string | null;
  file_size?: number | null;
  summary?: string | null;
};

type FileUploadZoneProps = {
  projectId?: number;
};

export function FileUploadZone({ projectId }: FileUploadZoneProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [files, setFiles] = useState<ProjectFile[]>([]);
  const [loading, setLoading] = useState(Boolean(projectId));
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadFiles = useCallback(async () => {
    if (!projectId) return;
    setLoading(true);
    setError(null);
    try {
      const response = await filesApi.list(projectId);
      setFiles(response.data.items || []);
    } catch {
      setError("Could not load project files.");
    } finally {
      setLoading(false);
    }
  }, [projectId]);

  useEffect(() => {
    loadFiles();
  }, [loadFiles]);

  const uploadFile = async (file: File) => {
    if (!projectId) return;
    setUploading(true);
    setError(null);
    const formData = new FormData();
    formData.append("upload", file);
    try {
      await filesApi.upload(projectId, formData);
      await loadFiles();
    } catch {
      setError("Upload failed. Check the file type and size, then try again.");
    } finally {
      setUploading(false);
      if (inputRef.current) inputRef.current.value = "";
    }
  };

  const deleteFile = async (fileId: number) => {
    setError(null);
    try {
      await filesApi.delete(fileId);
      setFiles((current) => current.filter((file) => file.id !== fileId));
    } catch {
      setError("Could not delete that file.");
    }
  };

  if (!projectId) {
    return (
      <div className="panel border-dashed p-8 text-center text-sm text-slate-600">
        Open a project to upload and analyze files.
      </div>
    );
  }

  return (
    <section className="space-y-5">
      <div
        className="panel border-dashed p-8 text-center"
        onDragOver={(event) => event.preventDefault()}
        onDrop={(event) => {
          event.preventDefault();
          const file = event.dataTransfer.files.item(0);
          if (file) uploadFile(file);
        }}
      >
        <UploadCloud className="mx-auto mb-3 h-8 w-8 text-blue-600" />
        <p className="font-medium text-slate-900">Drop files here or choose a file.</p>
        <p className="mt-1 text-sm text-slate-500">PDF, DOCX, PPTX, XLSX, CSV, images, ZIP, audio, and video are supported.</p>
        <input
          ref={inputRef}
          type="file"
          className="hidden"
          onChange={(event) => {
            const file = event.target.files?.item(0);
            if (file) uploadFile(file);
          }}
        />
        <button className="btn-primary mt-4" type="button" onClick={() => inputRef.current?.click()} disabled={uploading}>
          {uploading ? <Loader2 className="h-4 w-4 animate-spin" /> : <UploadCloud className="h-4 w-4" />}
          {uploading ? "Uploading" : "Choose File"}
        </button>
      </div>

      {error && <div className="rounded-md border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">{error}</div>}

      <div className="panel p-5">
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-lg font-semibold">Project Files</h2>
          {loading && <Loader2 className="h-4 w-4 animate-spin text-slate-400" />}
        </div>
        {files.length === 0 && !loading ? (
          <p className="text-sm text-slate-500">No files uploaded yet.</p>
        ) : (
          <div className="space-y-3">
            {files.map((file) => (
              <div key={file.id} className="flex items-start justify-between gap-3 rounded-md border border-slate-200 p-3">
                <div className="flex min-w-0 gap-3">
                  <FileText className="mt-1 h-5 w-5 shrink-0 text-slate-500" />
                  <div className="min-w-0">
                    <p className="truncate font-medium text-slate-900">{file.file_name}</p>
                    <p className="text-xs text-slate-500">{file.file_type || "unknown"} · {formatBytes(file.file_size || 0)}</p>
                    {file.summary && <p className="mt-1 line-clamp-2 text-sm text-slate-600">{file.summary}</p>}
                  </div>
                </div>
                <button
                  className="btn-secondary shrink-0 px-3"
                  type="button"
                  aria-label={`Delete ${file.file_name}`}
                  onClick={() => deleteFile(file.id)}
                >
                  <Trash2 className="h-4 w-4" />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </section>
  );
}

function formatBytes(bytes: number) {
  if (!bytes) return "0 B";
  const units = ["B", "KB", "MB", "GB"];
  const index = Math.min(Math.floor(Math.log(bytes) / Math.log(1024)), units.length - 1);
  return `${(bytes / 1024 ** index).toFixed(index === 0 ? 0 : 1)} ${units[index]}`;
}
