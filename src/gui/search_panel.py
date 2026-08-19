from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QRadioButton, QButtonGroup, QSpinBox,
    QComboBox, QGroupBox, QFrame, QScrollArea
)
from PyQt6.QtCore import pyqtSignal, Qt

class SearchPanel(QWidget):
    """Panel containing preset quick searches and custom query form."""

    # Signal emitted when user triggers a search request
    search_requested = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.active_preset = "strong_lensing"  # "strong_lensing", "ai_lensing", "custom"
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        # Header
        header_layout = QVBoxLayout()
        header_layout.setSpacing(2)
        title_label = QLabel("SearchForLens")
        title_label.setObjectName("AppHeaderTitle")
        subtitle_label = QLabel("Recuperador de Lentes Gravitacionales e IA")
        subtitle_label.setObjectName("AppHeaderSubtitle")
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        layout.addLayout(header_layout)

        # --- PRESETS SECTION ---
        presets_group = QGroupBox("Consultas Predefinidas")
        presets_layout = QVBoxLayout()
        presets_layout.setSpacing(8)

        self.btn_preset_strong = QPushButton("🌌  Lentes Gravitacionales Fuertes")
        self.btn_preset_strong.setObjectName("PresetButton")
        self.btn_preset_strong.setCheckable(True)
        self.btn_preset_strong.setChecked(True)
        self.btn_preset_strong.clicked.connect(lambda: self._select_preset("strong_lensing"))

        self.btn_preset_ai = QPushButton("🧠  IA en Lentes Gravitacionales")
        self.btn_preset_ai.setObjectName("PresetButton")
        self.btn_preset_ai.setCheckable(True)
        self.btn_preset_ai.clicked.connect(lambda: self._select_preset("ai_lensing"))

        self.btn_preset_custom = QPushButton("🔍  Búsqueda Personalizada")
        self.btn_preset_custom.setObjectName("PresetButton")
        self.btn_preset_custom.setCheckable(True)
        self.btn_preset_custom.clicked.connect(lambda: self._select_preset("custom"))

        self.preset_group = QButtonGroup(self)
        self.preset_group.setExclusive(True)
        self.preset_group.addButton(self.btn_preset_strong)
        self.preset_group.addButton(self.btn_preset_ai)
        self.preset_group.addButton(self.btn_preset_custom)

        presets_layout.addWidget(self.btn_preset_strong)
        presets_layout.addWidget(self.btn_preset_ai)
        presets_layout.addWidget(self.btn_preset_custom)
        presets_group.setLayout(presets_layout)
        layout.addWidget(presets_group)

        # --- FILTERS & PARAMETERS SECTION ---
        filters_group = QGroupBox("Filtros de Búsqueda")
        filters_layout = QVBoxLayout()
        filters_layout.setSpacing(12)

        # Custom search input
        self.query_label = QLabel("Palabra clave / Título:")
        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText("Ej. lens modeling, dark matter, neural net")
        self.query_input.returnPressed.connect(self._on_search_clicked)
        filters_layout.addWidget(self.query_label)
        filters_layout.addWidget(self.query_input)

        # Author input
        author_label = QLabel("Autor (Opcional):")
        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Ej. Treu, Suyu, Koopmans")
        self.author_input.returnPressed.connect(self._on_search_clicked)
        filters_layout.addWidget(author_label)
        filters_layout.addWidget(self.author_input)

        # Year Range
        year_layout = QHBoxLayout()
        year_layout.setSpacing(8)

        start_lbl = QLabel("Desde:")
        self.spin_start_year = QSpinBox()
        self.spin_start_year.setRange(1900, 2026)
        self.spin_start_year.setValue(2015)

        end_lbl = QLabel("Hasta:")
        self.spin_end_year = QSpinBox()
        self.spin_end_year.setRange(1900, 2026)
        self.spin_end_year.setValue(2026)

        year_layout.addWidget(start_lbl)
        year_layout.addWidget(self.spin_start_year)
        year_layout.addWidget(end_lbl)
        year_layout.addWidget(self.spin_end_year)
        filters_layout.addLayout(year_layout)

        # Source Selection (Todas, arXiv, ADS, INSPIRE-HEP)
        source_lbl = QLabel("Fuente de Datos:")
        filters_layout.addWidget(source_lbl)

        source_btn_layout = QHBoxLayout()
        self.radio_all = QRadioButton("Todas")
        self.radio_arxiv = QRadioButton("arXiv")
        self.radio_ads = QRadioButton("NASA ADS")
        self.radio_inspire = QRadioButton("INSPIRE")
        self.radio_all.setChecked(True)

        self.source_group = QButtonGroup(self)
        self.source_group.addButton(self.radio_all)
        self.source_group.addButton(self.radio_arxiv)
        self.source_group.addButton(self.radio_ads)
        self.source_group.addButton(self.radio_inspire)

        source_btn_layout.addWidget(self.radio_all)
        source_btn_layout.addWidget(self.radio_arxiv)
        source_btn_layout.addWidget(self.radio_ads)
        source_btn_layout.addWidget(self.radio_inspire)
        filters_layout.addLayout(source_btn_layout)

        # Options: Sort By & Max Results
        opts_layout = QHBoxLayout()
        
        sort_lbl = QLabel("Ordenar:")
        self.combo_sort = QComboBox()
        self.combo_sort.addItem("Fecha (Recientes)", "date")
        self.combo_sort.addItem("Más Citados", "citations")
        self.combo_sort.addItem("Relevancia", "relevance")

        max_lbl = QLabel("Límite:")
        self.spin_max_results = QSpinBox()
        self.spin_max_results.setRange(10, 200)
        self.spin_max_results.setSingleStep(10)
        self.spin_max_results.setValue(50)

        opts_layout.addWidget(sort_lbl)
        opts_layout.addWidget(self.combo_sort)
        opts_layout.addWidget(max_lbl)
        opts_layout.addWidget(self.spin_max_results)
        filters_layout.addLayout(opts_layout)

        filters_group.setLayout(filters_layout)
        layout.addWidget(filters_group)

        # --- SEARCH BUTTON ---
        self.btn_search = QPushButton("🔎  BUSCAR ARTÍCULOS")
        self.btn_search.setObjectName("PrimaryButton")
        self.btn_search.setMinimumHeight(42)
        self.btn_search.clicked.connect(self._on_search_clicked)
        layout.addWidget(self.btn_search)

        layout.addStretch()

        # Update initial inputs state
        self._update_input_states()

    def _select_preset(self, preset_type: str):
        self.active_preset = preset_type
        self._update_input_states()

    def _update_input_states(self):
        # Enable query input for custom preset, placeholder info for predefined presets
        if self.active_preset == "strong_lensing":
            self.query_input.setEnabled(False)
            self.query_input.setPlaceholderText("Consulta automática: Strong Gravitational Lensing")
        elif self.active_preset == "ai_lensing":
            self.query_input.setEnabled(False)
            self.query_input.setPlaceholderText("Consulta automática: IA y ML en Lentes Gravitacionales")
        else:
            self.query_input.setEnabled(True)
            self.query_input.setPlaceholderText("Ej. lens modeling, dark matter, neural net")
            self.query_input.setFocus()

    def _on_search_clicked(self):
        source = "all"
        if self.radio_arxiv.isChecked():
            source = "arxiv"
        elif self.radio_ads.isChecked():
            source = "ads"
        elif self.radio_inspire.isChecked():
            source = "inspire"

        params = {
            "preset_type": self.active_preset,
            "custom_query": self.query_input.text().strip(),
            "author": self.author_input.text().strip(),
            "start_year": self.spin_start_year.value(),
            "end_year": self.spin_end_year.value(),
            "source": source,
            "sort_by": self.combo_sort.currentData(),
            "max_results": self.spin_max_results.value()
        }
        self.search_requested.emit(params)
