ER Proof Tool for Windows

Recommended download package:
- ER_prooftool_windows_app.zip
  This is the Windows-safe bundle to download and extract.
- windows_app.zip
  Legacy duplicate bundle kept for compatibility.

Files needed to copy to another Windows machine:
- compare_ui_server.py
- compare_ui.html
- generate_diff_pdf.py
- launch_compare_app.py
- setup_windows.py
- Setup DOCX Compare App.bat
- Start DOCX Compare App.bat
- requirements.txt

Optional files:
- Open DOCX Compare App.command
  macOS launcher only, not needed on Windows.
- legacy/docx-html-qa-compare-v2.html
  Legacy browser-only comparator, not needed for the current PDF-annotation app.

Do not copy these local-only folders/files unless you want sample data or old outputs:
- local_test/
- .venv/
- __pycache__/
- ui_runs/
- ui_server.log

Windows setup:
1. Install Python 3.11+.
2. Double-click:
   Setup DOCX Compare App.bat
   The setup script installs Python packages, Chromium, and Tesseract OCR when possible.
3. If setup fails, check:
   setup_windows.log
   If the error mentions Tesseract, run:
   winget install -e --id UB-Mannheim.TesseractOCR
   then rerun setup in a new Command Prompt.
4. Start the app:
   Start DOCX Compare App.bat
5. Do not open:
   compare_ui.html
   directly from the extracted folder. That file is only the page asset. The working app is served from:
   http://127.0.0.1:8765/
   after the launcher starts the local server.

What the dependencies are for:
- playwright
  Renders the input HTML in Chromium and exports the PDF.
- pypdf
  Adds PDF comment annotations for the detected differences.
- PyMuPDF
  Used by the compare engine for PDF annotation and extraction support in the local pipeline.
- Tesseract OCR
  Installed by setup when available for local OCR-related workflows.
- Python standard library modules are used for everything else.

Runtime output:
- ui_runs\
  The app writes each compare job here.
- ui_server.log
  Server startup/runtime log.
- setup_windows.log
  Windows setup/install log.
