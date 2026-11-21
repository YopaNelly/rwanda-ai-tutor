import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

pdf_path = "backend/data/raw/nesa_physics_2021.pdf"
doc = fitz.open(pdf_path)

# Render page 4 (index 3) to an image
page = doc[3]
pix = page.get_pixmap(dpi=200)
img = Image.open(io.BytesIO(pix.tobytes("png")))

# OCR
text = pytesseract.image_to_string(img, lang="eng")
print("--- OCR Page 4 ---")
print(text[:600])
