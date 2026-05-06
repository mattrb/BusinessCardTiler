import streamlit as st
from PIL import Image, ImageDraw, ImageOps
from pdf2image import convert_from_path
import tempfile
import io
import os

# --- Page Configuration ---
st.set_page_config(page_title="BC Tiler", page_icon="📇")
st.title("📇 Business Card Tiler (85mm x 55mm)")
st.markdown("Upload a card (PDF or Image). I'll tile it to A4 with cut marks.")

def process_tiling(input_file):
    # A4 @ 300 DPI
    A4_SIZE = (2480, 3508)
    # UK/EU Standard 85mm x 55mm @ 300 DPI
    CARD_SIZE = (1004, 650) 
    
    # Platform-aware Poppler Path
    p_path = "/opt/homebrew/bin" if os.path.exists("/opt/homebrew/bin") else None

    if input_file.name.lower().endswith('.pdf'):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(input_file.getbuffer())
            tmp.flush()
            try:
                images = convert_from_path(tmp.name, dpi=300, poppler_path=p_path)
                card = images[0].convert("RGB")
            finally:
                tmp_name = tmp.name
            if os.path.exists(tmp_name):
                os.remove(tmp_name)
    else:
        card = Image.open(input_file).convert("RGB")
    
    # Center crop for bleed
    card = ImageOps.fit(card, CARD_SIZE, Image.Resampling.LANCZOS)
    
    sheet = Image.new("RGB", A4_SIZE, (255, 255, 255))
    draw = ImageDraw.Draw(sheet)
    
    cols, rows = 2, 5
    margin_x = (A4_SIZE[0] - (cols * CARD_SIZE[0])) // 2
    margin_y = (A4_SIZE[1] - (rows * CARD_SIZE[1])) // 2
    
    for r in range(rows):
        for c in range(cols):
            x = margin_x + (c * CARD_SIZE[0])
            y = margin_y + (r * CARD_SIZE[1])
            sheet.paste(card, (x, y))
            
            # Cut Marks
            off, lgth = 15, 65
            marks = [
                (x, y-off, x, y-lgth), (x-off, y, x-lgth, y), # TL
                (x+CARD_SIZE[0], y-off, x+CARD_SIZE[0], y-lgth), # TR
                (x+CARD_SIZE[0]+off, y, x+CARD_SIZE[0]+lgth, y),
                (x, y+CARD_SIZE[1]+off, x, y+CARD_SIZE[1]+lgth), # BL
                (x-off, y+CARD_SIZE[1], x-lgth, y+CARD_SIZE[1]),
                (x+CARD_SIZE[0], y+CARD_SIZE[1]+off, x+CARD_SIZE[0], y+CARD_SIZE[1]+lgth), # BR
                (x+CARD_SIZE[0]+off, y+CARD_SIZE[1], x+CARD_SIZE[0]+lgth, y+CARD_SIZE[1])
            ]
            for m in marks:
                draw.line([(m[0], m[1]), (m[2], m[3])], fill="black", width=3)
    
    return sheet

uploaded_file = st.file_uploader("Upload Card", type=['png', 'jpg', 'jpeg', 'pdf'])

if uploaded_file:
    try:
        with st.spinner('Processing...'):
            result_image = process_tiling(uploaded_file)
            st.image(result_image, use_container_width=True)
            
            buf = io.BytesIO()
            result_image.save(buf, format="JPEG", quality=100, dpi=(300, 300))
            
            st.download_button(
                label="📥 Download A4 Sheet",
                data=buf.getvalue(),
                file_name="Business_Cards_Print_Sheet.jpg",
                mime="image/jpeg"
            )
            
            # --- Printing Instructions Section ---
            st.divider()
            st.subheader("🖨️ Printing Instructions")
            st.info("""
            **To ensure your cards are the correct size (85mm x 55mm):**
            1. **Scale Setting:** When the print dialog opens, set **Scale** to **100%** or **Actual Size**. 
            2. **Do NOT 'Fit to Page':** Using 'Fit' or 'Shrink to Fit' will make your cards smaller than intended.
            3. **Paper:** Use heavy cardstock (250gsm - 350gsm).
            4. **Cutting:** Use the black 'L' marks as your guide. Use a metal ruler and craft knife for the most precise results.
            """)
            
    except Exception as e:
        st.error(f"Something went wrong: {e}")