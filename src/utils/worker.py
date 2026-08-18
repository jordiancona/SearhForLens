from PyQt6.QtCore import QThread, pyqtSignal
from typing import List, Optional
from src.api.models import Article
from src.api.arxiv_client import ArxivClient
from src.api.ads_client import AdsClient

class SearchWorker(QThread):
    """Worker thread for non-blocking execution of arXiv and NASA ADS search queries."""

    # Signals
    status_updated = pyqtSignal(str)              # Status message e.g. "Buscando en arXiv..."
    results_ready = pyqtSignal(list, str)         # (List[Article], source_summary)
    error_occurred = pyqtSignal(str)              # Error description message

    def __init__(
        self,
        preset_type: str,
        custom_query: str,
        author: str,
        start_year: Optional[int],
        end_year: Optional[int],
        source: str,            # "arxiv", "ads", or "both"
        ads_api_key: str,
        max_results: int = 50,
        sort_by: str = "date"   # "date", "citations", "relevance"
    ):
        super().__init__()
        self.preset_type = preset_type
        self.custom_query = custom_query
        self.author = author
        self.start_year = start_year
        self.end_year = end_year
        self.source = source
        self.ads_api_key = ads_api_key
        self.max_results = max_results
        self.sort_by = sort_by

        self.arxiv_client = ArxivClient()
        self.ads_client = AdsClient(api_key=self.ads_api_key)

    def run(self):
        articles: List[Article] = []
        errors: List[str] = []

        query_arxiv = self.source in ("arxiv", "both")
        query_ads = self.source in ("ads", "both")

        # --- Query arXiv ---
        if query_arxiv:
            self.status_updated.emit("Buscando en arXiv API...")
            try:
                arxiv_q = self.arxiv_client.build_preset_query(
                    preset_type=self.preset_type,
                    custom_query=self.custom_query,
                    author=self.author,
                    start_year=self.start_year,
                    end_year=self.end_year
                )
                sort_order = "submittedDate" if self.sort_by == "date" else "relevance"
                arxiv_res = self.arxiv_client.search(
                    query=arxiv_q,
                    max_results=self.max_results,
                    sort_by=sort_order
                )
                articles.extend(arxiv_res)
            except Exception as e:
                errors.append(f"arXiv: {str(e)}")

        # --- Query NASA ADS ---
        if query_ads:
            self.status_updated.emit("Buscando en NASA ADS API...")
            if not self.ads_api_key:
                errors.append("NASA ADS: Se requiere configurar una API Key en Ajustes.")
            else:
                try:
                    ads_q = self.ads_client.build_preset_query(
                        preset_type=self.preset_type,
                        custom_query=self.custom_query,
                        author=self.author,
                        start_year=self.start_year,
                        end_year=self.end_year
                    )
                    ads_sort = "date desc"
                    if self.sort_by == "citations":
                        ads_sort = "citation_count desc"
                    elif self.sort_by == "relevance":
                        ads_sort = "score desc"

                    ads_res = self.ads_client.search(
                        query=ads_q,
                        rows=self.max_results,
                        sort=ads_sort
                    )
                    articles.extend(ads_res)
                except Exception as e:
                    errors.append(f"NASA ADS: {str(e)}")

        self.status_updated.emit("Procesando y consolidando resultados...")

        # --- Deduplicate results ---
        merged_articles = self._deduplicate(articles)

        # --- Filter by year if specified ---
        if self.start_year or self.end_year:
            merged_articles = self._filter_by_year(merged_articles)

        # --- Sort results ---
        merged_articles = self._sort_articles(merged_articles)

        # Build summary
        sources_used = []
        if query_arxiv:
            sources_used.append("arXiv")
        if query_ads:
            sources_used.append("NASA ADS")

        source_str = " + ".join(sources_used)

        if errors and not merged_articles:
            self.error_occurred.emit("\n".join(errors))
        else:
            self.results_ready.emit(merged_articles, source_str)

    def _deduplicate(self, articles: List[Article]) -> List[Article]:
        """Merge identical articles from arXiv & ADS into unified records."""
        unique_map = {}

        for article in articles:
            # Create a key derived from arXiv ID, Bibcode, or Title
            key = None
            if article.arxiv_id:
                key = f"arxiv:{article.arxiv_id.split('v')[0].lower()}"
            elif article.bibcode:
                key = f"bibcode:{article.bibcode.lower()}"
            elif article.doi:
                key = f"doi:{article.doi.lower()}"
            else:
                key = f"title:{article.title.strip().lower()[:50]}"

            if key not in unique_map:
                unique_map[key] = article
            else:
                # Merge existing record with new data (preferring citation data from ADS, PDF link from arXiv)
                existing = unique_map[key]

                # Update source badge
                if existing.source != article.source:
                    existing.source = "arXiv + ADS"

                if article.citations > existing.citations:
                    existing.citations = article.citations
                if article.bibcode and not existing.bibcode:
                    existing.bibcode = article.bibcode
                if article.arxiv_id and not existing.arxiv_id:
                    existing.arxiv_id = article.arxiv_id
                if article.pdf_url and not existing.pdf_url:
                    existing.pdf_url = article.pdf_url
                if article.doi and not existing.doi:
                    existing.doi = article.doi
                if article.raw_bibtex and not existing.raw_bibtex:
                    existing.raw_bibtex = article.raw_bibtex

        return list(unique_map.values())

    def _filter_by_year(self, articles: List[Article]) -> List[Article]:
        filtered = []
        for a in articles:
            if not a.pub_date or len(a.pub_date) < 4:
                filtered.append(a)
                continue
            try:
                year = int(a.pub_date[:4])
                if self.start_year and year < self.start_year:
                    continue
                if self.end_year and year > self.end_year:
                    continue
                filtered.append(a)
            except ValueError:
                filtered.append(a)
        return filtered

    def _sort_articles(self, articles: List[Article]) -> List[Article]:
        if self.sort_by == "citations":
            return sorted(articles, key=lambda x: x.citations, reverse=True)
        elif self.sort_by == "date":
            return sorted(articles, key=lambda x: x.pub_date or "", reverse=True)
        return articles
