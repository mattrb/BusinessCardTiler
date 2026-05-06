# Business Card Tiler Pro (UK/EU Edition)

A professional-grade web application built with Python and Streamlit to transform a single business card (Image or PDF) into a print-ready A4 sheet. The tool automates precision tiling, smart-cropping for bleed, and the placement of standard cut marks.

## 🚀 Live Features
- **Multi-Format Support:** Accepts `.pdf`, `.png`, `.jpg`, and `.jpeg`.
- **EU/UK Standard Sizing:** Outputs cards at exactly **85mm x 55mm**.
- **Smart Bleed Handling:** Uses center-cropping (`ImageOps.fit`) to ensure designs fill the card area without distortion, even if the source aspect ratio is slightly off.
- **Print Accuracy:** Generates a **300 DPI** JPEG with built-in cut marks for manual trimming.
- **Cloud Ready:** Configured for seamless deployment on Streamlit Community Cloud.

---

## 🛠 Project Structure
To recreate or deploy this project, ensure your GitHub repository contains these three files:

1.  **`app.py`**: The core Python script containing the Streamlit UI and the Pillow/pdf2image processing logic.
2.  **`requirements.txt`**: Lists the Python dependencies:
    - Pillow
    - pdf2image
    - streamlit
3.  **`packages.txt`**: Vital for PDF processing on Linux servers (Streamlit Cloud):
    - poppler-utils

---

## 💻 Local Setup & Installation (macOS)

1. **Install System Dependencies:**
   ```bash
   brew install poppler
