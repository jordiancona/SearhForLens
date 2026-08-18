"""
Modern Dark Mode QSS Stylesheet for SearchForLens.
Designed for high contrast, clean visual hierarchy, smooth hover states, and glassmorphic touches.
"""

DARK_STYLESHEET = """
/* Global Window & Base Widgets */
QMainWindow, QDialog {
    background-color: #0f172a;
    color: #f8fafc;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    font-size: 13px;
}

QWidget {
    color: #e2e8f0;
}

/* ScrollBars */
QScrollBar:vertical {
    border: none;
    background: #1e293b;
    width: 8px;
    margin: 0px;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: #334155;
    min-height: 20px;
    border-radius: 4px;
}
QScrollBar::handle:vertical:hover {
    background: #475569;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    border: none;
    background: #1e293b;
    height: 8px;
    margin: 0px;
    border-radius: 4px;
}
QScrollBar::handle:horizontal {
    background: #334155;
    min-width: 20px;
    border-radius: 4px;
}
QScrollBar::handle:horizontal:hover {
    background: #475569;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* Sidebar & Navigation Panels */
QFrame#SidebarFrame {
    background-color: #1e293b;
    border-right: 1px solid #334155;
}

QLabel#AppHeaderTitle {
    font-size: 18px;
    font-weight: 700;
    color: #38bdf8;
    letter-spacing: 0.5px;
}

QLabel#AppHeaderSubtitle {
    font-size: 11px;
    color: #94a3b8;
}

/* Headings */
QLabel#SectionTitle {
    font-size: 14px;
    font-weight: 600;
    color: #f1f5f9;
    padding-bottom: 4px;
}

QLabel#CardTitle {
    font-size: 15px;
    font-weight: 700;
    color: #38bdf8;
    line-height: 1.3;
}

QLabel#CardAuthors {
    font-size: 12px;
    font-weight: 500;
    color: #cbd5e1;
}

QLabel#CardMeta {
    font-size: 11px;
    color: #94a3b8;
}

/* GroupBox & Cards */
QGroupBox {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 8px;
    margin-top: 12px;
    font-weight: 600;
    color: #38bdf8;
    padding: 12px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 2px 8px;
    background-color: #0f172a;
    border: 1px solid #334155;
    border-radius: 4px;
}

QFrame#ArticleCard {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 14px;
}
QFrame#ArticleCard:hover {
    border: 1px solid #38bdf8;
    background-color: #26334d;
}

/* Inputs & Form Controls */
QLineEdit, QSpinBox, QComboBox, QTextEdit {
    background-color: #0f172a;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 8px 12px;
    color: #f8fafc;
    selection-background-color: #0284c7;
}
QLineEdit:focus, QSpinBox:focus, QComboBox:focus, QTextEdit:focus {
    border: 1px solid #38bdf8;
    background-color: #0f172a;
}
QLineEdit::placeholder {
    color: #64748b;
}

QComboBox::drop-down {
    border: none;
    width: 24px;
}
QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid #94a3b8;
    margin-right: 8px;
}

/* Push Buttons */
QPushButton {
    background-color: #334155;
    color: #f8fafc;
    border: 1px solid #475569;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: 600;
}
QPushButton:hover {
    background-color: #475569;
    border-color: #64748b;
}
QPushButton:pressed {
    background-color: #1e293b;
}

/* Primary Accent Button */
QPushButton#PrimaryButton {
    background-color: #0284c7;
    color: #ffffff;
    border: 1px solid #38bdf8;
    font-size: 13px;
    font-weight: 700;
}
QPushButton#PrimaryButton:hover {
    background-color: #0369a1;
    border-color: #7dd3fc;
}
QPushButton#PrimaryButton:pressed {
    background-color: #075985;
}

/* Preset Quick Action Buttons */
QPushButton#PresetButton {
    background-color: #1e293b;
    color: #e2e8f0;
    border: 1px solid #334155;
    text-align: left;
    padding: 10px 14px;
    border-radius: 8px;
    font-size: 12px;
}
QPushButton#PresetButton:hover {
    background-color: #273549;
    border-color: #38bdf8;
    color: #38bdf8;
}
QPushButton#PresetButton:checked {
    background-color: #0369a1;
    border-color: #38bdf8;
    color: #ffffff;
}

/* Action Icon Buttons on Cards */
QPushButton#CardActionButton {
    background-color: #0f172a;
    color: #cbd5e1;
    border: 1px solid #334155;
    border-radius: 5px;
    padding: 5px 10px;
    font-size: 11px;
    font-weight: 500;
}
QPushButton#CardActionButton:hover {
    background-color: #1e293b;
    color: #38bdf8;
    border-color: #38bdf8;
}

QPushButton#FavoriteButton {
    background-color: #0f172a;
    color: #fbbf24;
    border: 1px solid #b45309;
    border-radius: 5px;
    padding: 5px 10px;
    font-size: 11px;
}
QPushButton#FavoriteButton:hover {
    background-color: #78350f;
    color: #fef08a;
}

/* Radio Buttons & Checkboxes */
QRadioButton, QCheckBox {
    color: #e2e8f0;
    spacing: 8px;
    font-weight: 500;
}
QRadioButton::indicator, QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border-radius: 3px;
    border: 1px solid #475569;
    background-color: #0f172a;
}
QRadioButton::indicator:checked, QCheckBox::indicator:checked {
    background-color: #0284c7;
    border: 1px solid #38bdf8;
}

/* Tab Widget */
QTabWidget::pane {
    border: 1px solid #334155;
    background-color: #0f172a;
    border-radius: 8px;
    top: -1px;
}
QTabBar::tab {
    background-color: #1e293b;
    color: #94a3b8;
    border: 1px solid #334155;
    border-bottom: none;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    padding: 8px 16px;
    font-weight: 600;
    margin-right: 4px;
}
QTabBar::tab:selected {
    background-color: #0f172a;
    color: #38bdf8;
    border-top: 2px solid #38bdf8;
}
QTabBar::tab:hover:!selected {
    background-color: #273549;
    color: #e2e8f0;
}

/* Status Bar & Progress Bar */
QStatusBar {
    background-color: #1e293b;
    color: #94a3b8;
    border-top: 1px solid #334155;
}

QProgressBar {
    border: 1px solid #334155;
    border-radius: 4px;
    text-align: center;
    background-color: #0f172a;
    color: #f8fafc;
    height: 12px;
}
QProgressBar::chunk {
    background-color: #0284c7;
    border-radius: 3px;
}

/* Badges */
QLabel#BadgeArxiv {
    background-color: #991b1b;
    color: #fef2f2;
    border-radius: 4px;
    padding: 2px 6px;
    font-size: 10px;
    font-weight: 700;
}
QLabel#BadgeAds {
    background-color: #1e40af;
    color: #eff6ff;
    border-radius: 4px;
    padding: 2px 6px;
    font-size: 10px;
    font-weight: 700;
}
QLabel#BadgeBoth {
    background-color: #065f46;
    color: #ecfdf5;
    border-radius: 4px;
    padding: 2px 6px;
    font-size: 10px;
    font-weight: 700;
}
/* Exit / Danger Button */
QPushButton#ExitButton {
    background-color: #7f1d1d;
    color: #fef2f2;
    border: 1px solid #ef4444;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: 600;
}
QPushButton#ExitButton:hover {
    background-color: #991b1b;
    border-color: #f87171;
}
QPushButton#ExitButton:pressed {
    background-color: #450a0a;
}
"""
