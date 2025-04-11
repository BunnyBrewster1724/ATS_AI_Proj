import base64
import io
import fitz  # PyMuPDF
from PIL import Image

def input_pdf_setup(uploaded_file):
    """
    Process uploaded PDF file and prepare it for Gemini API
    
    Args:
        uploaded_file: The uploaded PDF file object
        
    Returns:
        List of dicts with mime_type and base64 encoded data
    """
    if uploaded_file is not None:
        pdf_bytes = uploaded_file.read()
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        first_page = pdf_document.load_page(0)
        pix = first_page.get_pixmap()
        image_byte_arr = pix.tobytes("jpeg")
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(image_byte_arr).decode()
            }
        ]
        
        pdf_document.close()
        return pdf_parts
    else:
        raise FileNotFoundError("File not found")

def extract_text_from_pdf(uploaded_file):
    """
    Extract text content from uploaded PDF
    
    Args:
        uploaded_file: The uploaded PDF file object
        
    Returns:
        String containing all text from the PDF
    """
    if uploaded_file is not None:
        pdf_bytes = uploaded_file.read()
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = ""
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
        
        pdf_document.close()
        uploaded_file.seek(0)  # Reset file pointer
        return text
    else:
        return ""

def generate_pdf_preview(uploaded_file):
    """
    Generate a preview image of the first page of the PDF
    
    Args:
        uploaded_file: The uploaded PDF file object
        
    Returns:
        PIL Image object of the first page
    """
    try:
        pdf_bytes = uploaded_file.read()
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        first_page = pdf_document.load_page(0)
        pix = first_page.get_pixmap()
        img_data = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_data))
        uploaded_file.seek(0)
        pdf_document.close()
        return img
    except Exception as e:
        raise Exception(f"Error previewing PDF: {e}")