import { FileUploadZone } from "@/components/files/FileUploadZone";

export default function ProjectFilesPage({ params }: { params: { id: string } }) {
  return <FileUploadZone projectId={Number(params.id)} />;
}
