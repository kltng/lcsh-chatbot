"""
File Utilities Module - Handles file uploads and text extraction
"""
import base64
import io
from typing import Tuple, Optional, List, Dict
import streamlit as st
from PIL import Image
import docx
from pypdf import PdfReader

def extract_text_from_txt(file) -> str:
    """Extract text from a .txt file"""
    return file.read().decode('utf-8')

def extract_text_from_docx(file) -> str:
    """Extract text from a .docx file"""
    doc = docx.Document(file)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])

def extract_text_from_pdf(file) -> str:
    """Extract text from a PDF file"""
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def process_uploaded_file(uploaded_file) -> Tuple[Optional[str], Optional[str]]:
    """
    Process an uploaded file and extract text or encode image
    
    Args:
        uploaded_file: The uploaded file from Streamlit
        
    Returns:
        Tuple of (extracted_text, encoded_image)
    """
    if uploaded_file is None:
        return None, None
        
    file_type = uploaded_file.type
    
    # Text files
    if file_type == "text/plain":
        return extract_text_from_txt(uploaded_file), None
    
    # Word documents
    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(uploaded_file), None
    
    # PDF files
    elif file_type == "application/pdf":
        return extract_text_from_pdf(uploaded_file), None
    
    # Image files
    elif file_type.startswith("image/"):
        # For images, we need to encode them for Gemini
        image = Image.open(uploaded_file)
        
        # Convert to bytes
        buffered = io.BytesIO()
        image.save(buffered, format=image.format)
        img_bytes = buffered.getvalue()
        
        # Encode to base64
        encoded_image = base64.b64encode(img_bytes).decode('utf-8')
        return None, encoded_image
    
    else:
        st.error(f"Unsupported file type: {file_type}")
        return None, None

def process_multiple_files(uploaded_files) -> List[Dict[str, any]]:
    """
    Process multiple uploaded files and extract text or encode images
    
    Args:
        uploaded_files: List of uploaded files from Streamlit
        
    Returns:
        List of dictionaries containing file information and extracted content
    """
    if not uploaded_files:
        return []
    
    processed_files = []
    
    for uploaded_file in uploaded_files:
        extracted_text, encoded_image = process_uploaded_file(uploaded_file)
        
        processed_files.append({
            "filename": uploaded_file.name,
            "file_type": uploaded_file.type,
            "text": extracted_text,
            "image": encoded_image,
            "size": uploaded_file.size
        })
    
    return processed_files

def combine_file_contents(processed_files) -> Tuple[Optional[str], Optional[str]]:
    """
    Combine the contents of multiple files into a single text and image
    
    Args:
        processed_files: List of processed file dictionaries
        
    Returns:
        Tuple of (combined_text, first_image)
    """
    if not processed_files:
        return None, None
    
    # Combine all text content
    text_parts = []
    first_image = None
    
    for file in processed_files:
        if file["text"]:
            text_parts.append(f"--- File: {file['filename']} ---\n{file['text']}\n")
        
        # Use the first image we find
        if file["image"] and first_image is None:
            first_image = file["image"]
    
    combined_text = "\n".join(text_parts) if text_parts else None
    
    return combined_text, first_image 