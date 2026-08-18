import os
import tempfile
import requests
# pyrefly: ignore [missing-import]
from PyQt6.QtCore import QThread, pyqtSignal
from typing import Optional, List
from src.api.models import Article
from src.api.gdrive_client import GDriveClient
from src.utils.exporter import ArticleExporter

class GDriveUploadWorker(QThread):
    """Worker thread for background upload of reference files or PDFs to Google Drive."""

    status_updated = pyqtSignal(str)
    upload_complete = pyqtSignal(dict)  # Returns uploaded file info e.g. {"name": ..., "webViewLink": ...}
    error_occurred = pyqtSignal(str)

    def __init__(
        self,
        credentials_path: str,
        token_path: str,
        folder_id: str = "",
        folder_name: str = "SearchForLens",
        # Mode 1: Local file upload
        local_file_path: Optional[str] = None,
        # Mode 2: Articles export upload
        articles: Optional[List[Article]] = None,
        export_format: Optional[str] = None,  # "bibtex", "csv", "json"
        # Mode 3: Article PDF download & upload
        pdf_article: Optional[Article] = None
    ):
        super().__init__()
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.folder_id = folder_id
        self.folder_name = folder_name
        self.local_file_path = local_file_path
        self.articles = articles
        self.export_format = export_format
        self.pdf_article = pdf_article

        self.gdrive_client = GDriveClient(credentials_path=credentials_path, token_path=token_path)

    def run(self):
        try:
            # 1. Check or establish authentication
            self.status_updated.emit("Conectando con Google Drive...")
            success, msg = self.gdrive_client.authenticate(
                credentials_path=self.credentials_path,
                token_path=self.token_path
            )
            if not success:
                self.error_occurred.emit(f"Error de autenticación en Google Drive: {msg}")
                return

            # 2. Get target folder ID
            folder_query = self.folder_id or self.folder_name or "SearchForLens"
            self.status_updated.emit(f"Buscando/verificando carpeta destino en Google Drive...")
            target_folder_id, resolved_name = self.gdrive_client.verify_or_find_folder(folder_query)

            if not target_folder_id:
                self.error_occurred.emit(f"No se pudo acceder a la carpeta destino en Google Drive: {resolved_name}")
                return

            # 3. Handle upload depending on mode
            if self.pdf_article:
                self._handle_pdf_upload(target_folder_id)
            elif self.articles and self.export_format:
                self._handle_export_upload(target_folder_id)
            elif self.local_file_path:
                self._handle_file_upload(self.local_file_path, target_folder_id)
            else:
                self.error_occurred.emit("No se especificaron datos para subir a Google Drive.")

        except Exception as e:
            self.error_occurred.emit(f"Error durante la subida a Google Drive: {str(e)}")

    def _handle_pdf_upload(self, folder_id: str):
        article = self.pdf_article
        if not article.pdf_url:
            self.error_occurred.emit("El artículo seleccionado no contiene un enlace directo a PDF.")
            return

        self.status_updated.emit(f"Descargando PDF de '{article.title[:40]}...'")

        # Create temporary file
        safe_title = "".join(c for c in article.title[:40] if c.isalnum() or c in (" ", "_", "-")).strip()
        filename = f"{safe_title}_{article.arxiv_id or article.id}.pdf"

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_filepath = os.path.join(tmpdir, filename)

            # Download PDF
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            resp = requests.get(article.pdf_url, headers=headers, stream=True, timeout=30)
            resp.raise_for_status()

            content_type = resp.headers.get("Content-Type", "").lower()
            if "html" in content_type:
                raise ValueError("El enlace especificado no devolvió un archivo PDF (se obtuvo una página web HTML). El PDF de este artículo no está disponible públicamente en arXiv o requiere acceso a través del sitio web de la editorial.")

            with open(tmp_filepath, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)

            self.status_updated.emit(f"Subiendo '{filename}' a Google Drive...")
            uploaded = self.gdrive_client.upload_file(
                file_path=tmp_filepath,
                folder_id=folder_id,
                file_name=filename,
                mime_type='application/pdf'
            )
            self.upload_complete.emit(uploaded)

    def _handle_export_upload(self, folder_id: str):
        fmt = self.export_format.lower()
        ext = "bib" if fmt == "bibtex" else fmt
        filename = f"SearchForLens_Export_{len(self.articles)}_items.{ext}"

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_filepath = os.path.join(tmpdir, filename)

            if fmt == "bibtex":
                ArticleExporter.to_bibtex(self.articles, tmp_filepath)
                mime = 'text/x-bibtex'
            elif fmt == "csv":
                ArticleExporter.to_csv(self.articles, tmp_filepath)
                mime = 'text/csv'
            else:
                ArticleExporter.to_json(self.articles, tmp_filepath)
                mime = 'application/json'

            self.status_updated.emit(f"Subiendo '{filename}' a Google Drive...")
            uploaded = self.gdrive_client.upload_file(
                file_path=tmp_filepath,
                folder_id=folder_id,
                file_name=filename,
                mime_type=mime
            )
            self.upload_complete.emit(uploaded)

    def _handle_file_upload(self, file_path: str, folder_id: str):
        filename = os.path.basename(file_path)
        self.status_updated.emit(f"Subiendo '{filename}' a Google Drive...")
        uploaded = self.gdrive_client.upload_file(file_path=file_path, folder_id=folder_id)
        self.upload_complete.emit(uploaded)
