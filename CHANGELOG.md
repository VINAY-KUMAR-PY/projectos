# Changelog

## Stage 1 Completion

### Backend Endpoints Added

- `POST /api/files/{file_id}/analyze-video`
- `POST /api/projects/{project_id}/generate-document`
- `POST /api/projects/{project_id}/generate-ppt`
- `POST /api/projects/{project_id}/generate-diagram?type=...`
- `POST /api/projects/{project_id}/build-code`
- `POST /api/projects/{project_id}/review`
- `POST /api/projects/{project_id}/generate-deployment?target=...`
- `POST /api/collaboration/projects/{project_id}/members`
- `GET /api/collaboration/projects/{project_id}/members`
- `POST /api/collaboration/projects/{project_id}/comments`
- `GET /api/collaboration/projects/{project_id}/comments`
- `POST /api/collaboration/projects/{project_id}/task-assignments`
- `POST /api/collaboration/projects/{project_id}/approvals`
- `POST /api/collaboration/approvals/{approval_id}/decision`
- `POST /api/agents/learning/{action}`
- `GET /api/marketplace`
- `POST /api/marketplace`
- `POST /api/marketplace/{item_id}/use`
- `GET /api/integrations`
- `GET /api/integrations/github/oauth-url`
- `GET /api/integrations/google-drive/oauth-url`
- `POST /api/integrations/link`
- `GET /api/integrations/linked`
- `POST /api/integrations/github/import`
- `POST /api/integrations/github/push-code`
- `POST /api/integrations/google-drive/import`
- `POST /api/integrations/google-drive/export`
- `POST /api/users/me/2fa/enable`
- `POST /api/users/me/2fa/verify`
- `POST /api/users/me/2fa/disable`
- `GET /api/users/me/export`
- `DELETE /api/users/me`
- `POST /api/billing/razorpay/create`

### Frontend Pages Added Or Wired

- `/projects/[id]/workspace`
- `/projects/[id]/docs`
- `/projects/[id]/ppt`
- `/projects/[id]/diagrams`
- `/projects/[id]/code`
- `/projects/[id]/learn`
- `/marketplace`

### Notes

- Mock AI remains the default provider.
- Optional OCR/video/document dependencies stay outside the default backend install.
- Usage caps are enforced for projects, agent runs, generated outputs, and storage-related flows.
