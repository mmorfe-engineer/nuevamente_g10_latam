"""
Módulo de Ingestión de Documentos Técnicos.
Extrae texto de archivos PDF, Markdown (.md) y Texto Plano (.txt).
"""
import io
import os
from pathlib import Path
from typing import Union

class DocumentLoader:
    @staticmethod
    def clean_text(text: str) -> str:
        """Limpia y normaliza el texto extraído eliminando artefactos y saltos redundantes."""
        if not text:
            return ""
        import re
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r"[ \t]+", " ", text)
        return text.strip()

    @staticmethod
    def extract_from_bytes(filename: str, content: bytes) -> str:
        """Extrae texto a partir de un flujo de bytes según su extensión."""
        ext = Path(filename).suffix.lower()
        if ext == ".pdf":
            raw = DocumentLoader._extract_from_pdf_bytes(content)
        elif ext in [".md", ".markdown"]:
            raw = content.decode("utf-8", errors="replace")
        elif ext in [".txt", ".rst", ".json"]:
            raw = content.decode("utf-8", errors="replace")
        else:
            raw = content.decode("utf-8", errors="replace")
        return DocumentLoader.clean_text(raw)

    @staticmethod
    def extract_from_file(file_path: Union[str, Path]) -> str:
        """Lee un archivo del sistema de archivos local y extrae su texto."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"El archivo no existe: {file_path}")

        with open(path, "rb") as f:
            content = f.read()

        return DocumentLoader.extract_from_bytes(path.name, content)

    @staticmethod
    def _extract_from_pdf_bytes(content: bytes) -> str:
        """Extrae texto de un archivo PDF usando pypdf o PyMuPDF."""
        text_parts = []
        try:
            import pypdf
            reader = pypdf.PdfReader(io.BytesIO(content))
            for i, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(f"--- [Página {i+1}] ---\n" + page_text.strip())
            return "\n\n".join(text_parts)
        except Exception as e:
            # Fallback opcional con fitz (PyMuPDF)
            try:
                import fitz
                doc = fitz.open(stream=content, filetype="pdf")
                for i, page in enumerate(doc):
                    text_parts.append(f"--- [Página {i+1}] ---\n" + page.get_text().strip())
                return "\n\n".join(text_parts)
            except Exception as e2:
                raise RuntimeError(f"Error procesando PDF: {e} / {e2}")

doc_loader = DocumentLoader()
