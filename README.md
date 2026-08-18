# SearchForLens 🔭

Una aplicación de escritorio moderna desarrollada con **PyQt6** para buscar, recuperar, visualizar, exportar y gestionar artículos científicos sobre **Lentes Gravitacionales Fuertes** (*Strong Gravitational Lensing*) y **Aplicaciones de Inteligencia Artificial / Machine Learning en Lentes Gravitacionales** utilizando las APIs oficiales de **arXiv**, **NASA ADS** y la integración con **Google Drive API**.

---

## 🌟 Características Principales

1. **Consultas Predefinidas y Personalizadas**:
   - 🌌 **Lentes Gravitacionales Fuertes**: Búsqueda optimizada sobre *Strong Gravitational Lensing* y modelado de lentes.
   - 🧠 **IA en Lentes Gravitacionales**: Consultas cruzadas que combinan lentes gravitacionales con Redes Neuronales, Deep Learning, CNNs y Transformers.
   - 🔍 **Búsqueda Personalizada**: Filtros por palabras clave, autor, rango de años y ordenamiento (por fecha, número de citas o relevancia).

2. **Integración con arXiv, NASA ADS y Google Drive**:
   - **arXiv API**: Consultas directas sin requerir API Token.
   - **NASA ADS API**: Autenticación por token, conteo de citas y exportación de BibTeX oficial.
   - **☁️ Google Drive API**: Autenticación OAuth 2.0 para subir citas (`.bib`, `.csv`, `.json`) y PDFs de artículos directamente a una carpeta en Google Drive (`SearchForLens`).
   - **Consolidación Inteligente**: Desduplicación automática de artículos presentes en múltiples plataformas.

3. **Ejecución Asíncrona (`QThread`)**:
   - Las consultas a las APIs y las subidas a Google Drive se realizan en segundo plano, manteniendo la interfaz fluida sin congelamientos.

4. **Visor de Artículos y Citas BibTeX**:
   - Tarjetas de artículos con badges de origen (`arXiv`, `NASA ADS`), citas y resumen.
   - Modal con resumen completo, identificadores (arXiv ID, Bibcode, DOI), enlace a PDF, botón **"☁️ PDF a Drive"** y visor de BibTeX con copia en un clic.

5. **Gestor de Favoritos y Exportación en la Nube**:
   - Marcadores locales para guardar artículos de interés.
   - Exportación local o directa a Google Drive en formatos **BibTeX (`.bib`)**, **CSV** y **JSON**.

6. **Interfaz con Tema Oscuro (*Dark Mode*)**:
   - Diseño visual pulido con tipografía clara, transiciones suaves y botón de cierre (`🚪 Salir`) con confirmación.

---

## 🚀 Instalación y Uso

### Prerrequisitos
El proyecto cuenta con su propio entorno virtual en la carpeta `searchforlens/`.

Para verificar la instalación de dependencias en el entorno virtual:
```bash
searchforlens/bin/python -m pip list
```

Las dependencias requeridas incluyen `PyQt6`, `requests`, `feedparser`, `google-api-python-client`, `google-auth-httplib2` y `google-auth-oauthlib`.

---

### 🖥️ Ejecución de la Aplicación

Para iniciar la aplicación usando el entorno virtual:

```bash
searchforlens/bin/python main.py
```

---

## ⚙️ Configuración de APIs y Google Drive

1. Abre la aplicación y haz clic en **⚙️ Configuración** en la barra superior.

### 🚀 NASA ADS API:
- Pega tu Token de NASA ADS en la pestaña **NASA ADS API** y presiona **🧪 Probar API Key NASA ADS**.

### ☁️ Google Drive API:
1. En Google Cloud Console, crea un proyecto e habilita la **Google Drive API**.
2. Configura las credenciales de pantalla de consentimiento OAuth y descarga el archivo **`credentials.json`** (Tipo: Aplicación de escritorio / Desktop app).
3. En la pestaña **Google Drive API** dentro de la app, selecciona la ruta a tu archivo `credentials.json`.
4. Haz clic en **🔗 Conectar Cuenta de Google Drive** para iniciar sesión en tu navegador y autorizar el acceso.
5. Presiona **📂 Verificar / Crear Carpeta en Drive** para crear o vincular la carpeta de destino (`SearchForLens`).
6. Guarda los cambios.

---

## 📂 Estructura del Código

```
SearchForLens/
├── main.py                     # Punto de entrada de la aplicación
├── requirements.txt            # Dependencias del proyecto
├── README.md                   # Manual y documentación
├── config.json                 # Configuración y favoritos (generado automáticamente)
├── token.json                  # Token de sesión de Google Drive (generado al autenticarse)
├── searchforlens/              # Entorno virtual de Python
└── src/
    ├── api/
    │   ├── models.py           # Clase de datos unificada Article
    │   ├── arxiv_client.py     # Cliente HTTP/Atom para arXiv API
    │   ├── ads_client.py       # Cliente REST para NASA ADS API
    │   └── gdrive_client.py    # Cliente API OAuth 2.0 y uploader para Google Drive
    ├── gui/
    │   ├── styles.py           # Hoja de estilos QSS (Tema oscuro)
    │   ├── search_panel.py     # Panel de filtros y preconfiguraciones
    │   ├── results_view.py     # Vista de lista de tarjetas de artículos
    │   ├── article_detail.py   # Modal de detalles, resumen, BibTeX y subida de PDF
    │   ├── favorites_panel.py # Panel de gestión de favoritos
    │   ├── settings_dialog.py # Diálogo de configuración (NASA ADS & Google Drive)
    │   └── main_window.py      # Ventana principal de la GUI
    └── utils/
        ├── config.py           # Gestor de configuración y almacenamiento local
        ├── exporter.py         # Módulo de exportación (BibTeX, CSV, JSON)
        ├── worker.py           # Hilo QThread para consultas a arXiv/ADS
        └── gdrive_worker.py    # Hilo QThread para descargas y subidas a Google Drive
```
