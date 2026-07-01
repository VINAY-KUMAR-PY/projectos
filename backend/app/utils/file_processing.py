from pathlib import Path
import zipfile


def extract_text_from_file(file_path: str, file_type: str | None = None) -> str:
    path = Path(file_path)
    file_type = file_type or ""
    suffix = path.suffix.lower()

    if file_type.startswith("text/") or suffix in {".txt", ".md", ".py", ".js", ".ts", ".json", ".yaml", ".yml"}:
        return path.read_text(encoding="utf-8", errors="ignore")

    if suffix == ".pdf" or file_type == "application/pdf":
        try:
            import fitz

            with fitz.open(file_path) as document:
                return "\n".join(page.get_text() for page in document)
        except Exception as exc:
            return f"[PDF extraction unavailable: {exc}]"

    if suffix == ".docx":
        try:
            from docx import Document

            document = Document(file_path)
            return "\n".join(paragraph.text for paragraph in document.paragraphs)
        except Exception as exc:
            return f"[DOCX extraction unavailable: {exc}]"

    if suffix in {".xlsx", ".xls", ".csv"}:
        try:
            import pandas as pd

            frame = pd.read_csv(file_path) if suffix == ".csv" else pd.read_excel(file_path)
            return frame.to_string()
        except Exception as exc:
            return f"[Spreadsheet extraction unavailable: {exc}]"

    if file_type.startswith("image/"):
        try:
            import pytesseract
            from PIL import Image

            return pytesseract.image_to_string(Image.open(file_path))
        except Exception:
            return "[Image uploaded - OCR not available]"

    if suffix == ".zip" or file_type == "application/zip":
        extracted = []
        with zipfile.ZipFile(file_path, "r") as archive:
            for name in archive.namelist():
                if name.endswith((".py", ".js", ".ts", ".java", ".md", ".txt", ".json", ".yaml", ".yml")):
                    with archive.open(name) as item:
                        content = item.read().decode("utf-8", errors="ignore")
                        extracted.append(f"=== {name} ===\n{content}")
        return "\n\n".join(extracted)

    return "[File type not supported for text extraction]"


def extract_video_transcript(file_path: str) -> str:
    try:
        import whisper

        model = whisper.load_model("base")
        result = model.transcribe(file_path)
        return result["text"]
    except Exception as exc:
        return f"[Transcript extraction failed: {exc}]"
