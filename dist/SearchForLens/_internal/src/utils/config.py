import os
import json
from typing import Dict, Any, List
from src.api.models import Article

CONFIG_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config.json")

DEFAULT_CONFIG: Dict[str, Any] = {
    "ads_api_key": "",
    "default_source": "both",  # "arxiv", "ads", or "both"
    "max_results": 50,
    "theme": "dark",
    "gdrive_credentials_path": "",
    "gdrive_token_path": os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "token.json"),
    "gdrive_folder_id": "",
    "gdrive_folder_name": "SearchForLens",
    "favorites": []  # List of article dicts
}

class ConfigManager:
    """Manages application configuration, persistent settings, and favorites."""

    def __init__(self, file_path: str = CONFIG_FILE_PATH):
        self.file_path = file_path
        self._config: Dict[str, Any] = DEFAULT_CONFIG.copy()
        self.load()

    def load(self) -> None:
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    self._config.update(loaded)
            except Exception as e:
                print(f"Error loading config file: {e}")
                self.save()
        else:
            self.save()

    def save(self) -> None:
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving config file: {e}")

    def get_ads_api_key(self) -> str:
        return self._config.get("ads_api_key", "")

    def set_ads_api_key(self, api_key: str) -> None:
        self._config["ads_api_key"] = api_key.strip()
        self.save()

    def get_max_results(self) -> int:
        return self._config.get("max_results", 50)

    def set_max_results(self, val: int) -> None:
        self._config["max_results"] = val
        self.save()

    def get_default_source(self) -> str:
        return self._config.get("default_source", "both")

    def set_default_source(self, source: str) -> None:
        self._config["default_source"] = source
        self.save()

    # --- Google Drive Settings ---
    def get_gdrive_credentials_path(self) -> str:
        return self._config.get("gdrive_credentials_path", "")

    def set_gdrive_credentials_path(self, path: str) -> None:
        self._config["gdrive_credentials_path"] = path.strip()
        self.save()

    def get_gdrive_token_path(self) -> str:
        default_token = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "token.json")
        return self._config.get("gdrive_token_path", default_token)

    def set_gdrive_token_path(self, path: str) -> None:
        self._config["gdrive_token_path"] = path.strip()
        self.save()

    def get_gdrive_folder_id(self) -> str:
        return self._config.get("gdrive_folder_id", "")

    def set_gdrive_folder_id(self, folder_id: str) -> None:
        self._config["gdrive_folder_id"] = folder_id.strip()
        self.save()

    def get_gdrive_folder_name(self) -> str:
        return self._config.get("gdrive_folder_name", "SearchForLens")

    def set_gdrive_folder_name(self, name: str) -> None:
        self._config["gdrive_folder_name"] = name.strip()
        self.save()

    # --- Favorites System ---
    def get_favorites(self) -> List[Article]:
        fav_dicts = self._config.get("favorites", [])
        return [Article.from_dict(d) for d in fav_dicts]

    def is_favorite(self, article_id: str) -> bool:
        fav_dicts = self._config.get("favorites", [])
        return any(d.get("id") == article_id for d in fav_dicts)

    def toggle_favorite(self, article: Article) -> bool:
        """Add if not present, remove if present. Returns True if now favorite, False if removed."""
        fav_dicts = self._config.get("favorites", [])
        existing_index = None
        for i, d in enumerate(fav_dicts):
            if d.get("id") == article.id:
                existing_index = i
                break

        if existing_index is not None:
            fav_dicts.pop(existing_index)
            self._config["favorites"] = fav_dicts
            self.save()
            return False
        else:
            fav_dicts.append(article.to_dict())
            self._config["favorites"] = fav_dicts
            self.save()
            return True

    def remove_favorite(self, article_id: str) -> None:
        fav_dicts = self._config.get("favorites", [])
        self._config["favorites"] = [d for d in fav_dicts if d.get("id") != article_id]
        self.save()
