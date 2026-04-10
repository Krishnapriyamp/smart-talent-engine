import pdfplumber
import docx
try:
    import pytesseract
    from PIL import Image
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False
    print("⚠️ Tesseract not available, OCR will be skipped")

try:
    from ontology import normalize_skills
    from experience_extractor import extract_experience_details
except ImportError:
    from ontology import normalize_skills
    from experience_extractor import extract_experience_details


# =========================
# 📄 TEXT EXTRACTION
# =========================

def extract_text(file):
    print(f"📄 Extracting text from: {file.filename}")
    text = ""
    filename = file.filename.lower()

    try:
        # 📄 PDF FILE
        if filename.endswith(".pdf"):
            file.file.seek(0)
            print("📄 Opening PDF with pdfplumber")
            with pdfplumber.open(file.file) as pdf:
                print(f"📄 PDF has {len(pdf.pages)} pages")
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + " "
                        print(f"📄 Extracted {len(extracted)} chars from page")
                    else:
                        print("⚠️ No text extracted from page")
                        if TESSERACT_AVAILABLE:
                            print("Trying OCR...")
                            # OCR fallback
                            page_image = page.to_image(resolution=150).original
                            ocr_text = pytesseract.image_to_string(page_image)
                            text += ocr_text + " "
                            print(f"📄 OCR extracted {len(ocr_text)} chars")
                        else:
                            print("⚠️ OCR skipped (Tesseract not installed)")

        # 📄 DOCX FILE
        elif filename.endswith(".docx"):
            file.file.seek(0)
            print("📄 Opening DOCX")
            doc = docx.Document(file.file)
            for para in doc.paragraphs:
                text += para.text + " "

        # 🖼️ IMAGE FILE
        elif filename.endswith((".png", ".jpg", ".jpeg")):
            file.file.seek(0)
            print("📄 Processing image")
            if TESSERACT_AVAILABLE:
                img = Image.open(file.file)
                text = pytesseract.image_to_string(img)
                print(f"📄 OCR extracted {len(text)} chars from image")
            else:
                print("⚠️ Image OCR skipped (Tesseract not installed)")

        print(f"📄 Total extracted text length: {len(text)}")

    except Exception as e:
        print("❌ Error extracting text:", e)

    return text


# =========================
# 🧠 PROFILE EXTRACTION
# =========================

def extract_profile(file):
    text = extract_text(file)

    # 🔥 CLEAN TEXT (VERY IMPORTANT)
    if text:
        text = text.replace("\n", " ").replace("\r", " ")
        text = " ".join(text.split())  # remove extra spaces
        text = text.lower()  # normalize

    # 🔥 DEBUG (TEMP - REMOVE LATER)
    print("\n" + "="*50)
    print("PARSER DEBUG")
    print("="*50)
    print("TEXT SAMPLE:\n", text[:500])
    print("TEXT LENGTH:", len(text))
    print("="*50)

    # 🧠 Extract features
    skills = normalize_skills(text)
    exp_details = extract_experience_details(text)

    return {
        "raw_text": text,
        "skills": skills,
        "experience": exp_details,
        "exp_details": exp_details
    }