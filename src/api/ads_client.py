import requests
from typing import List, Optional, Tuple
from src.api.models import Article

ADS_API_SEARCH_URL = "https://api.adsabs.harvard.edu/v1/search/query"
ADS_API_ME_URL = "https://api.adsabs.harvard.edu/v1/user/me"
ADS_API_BIBTEX_URL = "https://api.adsabs.harvard.edu/v1/export/bibtex"

class AdsClient:
    """Client for fetching articles and metadata from NASA ADS API."""

    def __init__(self, api_key: str = "", timeout: int = 15):
        self.api_key = api_key
        self.timeout = timeout

    def set_api_key(self, api_key: str):
        self.api_key = api_key.strip()

    def verify_api_key(self, token: Optional[str] = None) -> Tuple[bool, str]:
        """Test if the provided NASA ADS API token is valid."""
        token_to_test = token.strip() if token else self.api_key
        if not token_to_test:
            return False, "No se ha proporcionado ninguna API key de NASA ADS."

        headers = {"Authorization": f"Bearer {token_to_test}"}
        params = {"q": "star", "rows": 1, "fl": "id"}
        try:
            resp = requests.get(ADS_API_SEARCH_URL, headers=headers, params=params, timeout=self.timeout)
            if resp.status_code == 200:
                return True, "API Key válida. Conexión exitosa con NASA ADS."
            elif resp.status_code == 401:
                return False, "API Key inválida o no autorizada."
            else:
                return False, f"Respuesta inesperada del servidor NASA ADS (Código {resp.status_code})."
        except Exception as e:
            return False, f"Error de conexión con NASA ADS: {str(e)}"

    def build_preset_query(
        self,
        preset_type: str,
        custom_query: str = "",
        author: str = "",
        start_year: Optional[int] = None,
        end_year: Optional[int] = None
    ) -> str:
        """Build search query string formatted for NASA ADS search engine."""
        terms = []

        if preset_type == "strong_lensing":
            terms.append('(title:("strong gravitational lensing" OR "strong lensing") OR abstract:("strong gravitational lensing" OR "strong lensing"))')
        elif preset_type == "ai_lensing":
            lens_q = '(title:("gravitational lensing" OR "strong lensing") OR abstract:("gravitational lensing" OR "strong lensing"))'
            ai_q = 'abstract:("machine learning" OR "deep learning" OR "neural network" OR "convolutional" OR "transformer" OR "artificial intelligence")'
            terms.append(f'({lens_q} AND {ai_q})')
        else:
            if custom_query.strip():
                q_clean = custom_query.strip()
                terms.append(f'(title:"{q_clean}" OR abstract:"{q_clean}")')

        if author.strip():
            terms.append(f'author:"{author.strip()}"')

        if start_year and end_year:
            terms.append(f'year:[{start_year} TO {end_year}]')
        elif start_year:
            terms.append(f'year:[{start_year} TO 2026]')
        elif end_year:
            terms.append(f'year:[1900 TO {end_year}]')

        query_str = " AND ".join(terms) if terms else 'title:"gravitational lensing"'
        return query_str

    def search(
        self,
        query: str,
        rows: int = 50,
        start_index: int = 0,
        sort: str = "date desc"  # "date desc", "citation_count desc", "score desc"
    ) -> List[Article]:
        """Query NASA ADS search endpoint and return list of Article instances."""
        if not self.api_key:
            raise ValueError("API Key de NASA ADS no configurada. Configure su API key en los Ajustes.")

        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {
            "q": query,
            "fl": "id,bibcode,title,author,abstract,pubdate,citation_count,doi,identifier,property,pub",
            "rows": rows,
            "start": start_index,
            "sort": sort
        }

        try:
            resp = requests.get(ADS_API_SEARCH_URL, headers=headers, params=params, timeout=self.timeout)
            if resp.status_code == 401:
                raise ValueError("API Key de NASA ADS inválida. Verifique sus credenciales en Ajustes.")
            resp.raise_for_status()

            data = resp.json()
            docs = data.get("response", {}).get("docs", [])

            articles = []
            for doc in docs:
                article = self._parse_doc(doc)
                if article:
                    articles.append(article)
            return articles

        except requests.exceptions.RequestException as req_err:
            raise RuntimeError(f"Error de red al consultar NASA ADS: {str(req_err)}")
        except Exception as e:
            raise RuntimeError(f"Error al procesar resultados de NASA ADS: {str(e)}")

    def _parse_doc(self, doc: dict) -> Optional[Article]:
        """Parse raw NASA ADS document dict into Article object."""
        try:
            bibcode = doc.get("bibcode", "")
            title_list = doc.get("title", [])
            title = title_list[0] if title_list else "Sin título"
            abstract = doc.get("abstract", "Sin resumen disponible.")
            authors = doc.get("author", [])
            pubdate = doc.get("pubdate", "")
            if pubdate and len(pubdate) >= 7:
                pub_date = pubdate[:7]  # YYYY-MM
            else:
                pub_date = pubdate[:4] if pubdate else ""

            citations = doc.get("citation_count", 0)
            if citations is None:
                citations = 0

            # Extract arXiv ID & DOI from identifiers list
            arxiv_id = None
            doi = None
            identifiers = doc.get("identifier", [])
            for ident in identifiers:
                if ident.startswith("arXiv:"):
                    arxiv_id = ident.replace("arXiv:", "")
                elif "arXiv" in ident and "/" in ident:
                    arxiv_id = ident.split("arXiv:")[-1]
                elif "/" in ident and ("10." in ident):
                    doi = ident

            doi_list = doc.get("doi", [])
            if doi_list and not doi:
                doi = doi_list[0]

            journal = doc.get("pub", "NASA ADS")

            url = f"https://ui.adsabs.harvard.edu/abs/{bibcode}/abstract" if bibcode else f"https://ui.adsabs.harvard.edu"
            pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf" if arxiv_id else f"https://ui.adsabs.harvard.edu/abs/{bibcode}/pdf"

            return Article(
                id=f"ads_{bibcode}",
                title=title,
                authors=authors,
                abstract=abstract,
                pub_date=pub_date,
                source="NASA ADS",
                arxiv_id=arxiv_id,
                bibcode=bibcode,
                doi=doi,
                pdf_url=pdf_url,
                url=url,
                citations=citations,
                journal=journal
            )
        except Exception as err:
            print(f"Error parsing ADS doc: {err}")
            return None

    def fetch_bibtex(self, bibcode: str) -> Optional[str]:
        """Fetch official BibTeX entry from NASA ADS export API."""
        if not self.api_key or not bibcode:
            return None

        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {"bibcode": [bibcode]}

        try:
            resp = requests.post(ADS_API_BIBTEX_URL, headers=headers, json=payload, timeout=self.timeout)
            if resp.status_code == 200:
                return resp.json().get("export", "")
        except Exception as e:
            print(f"Error fetching BibTeX from ADS: {e}")
        return None
