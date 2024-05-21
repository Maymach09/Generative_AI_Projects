import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from unstructured.partition.pdf import partition_pdf
import fitz  # PyMuPDF
import pdfplumber
import re
import pytesseract
from PIL import Image
from PIL import ImageEnhance
import io


# Initialize spaCy's English model
nlp = spacy.load("en_core_web_sm")

def extract_text_with_unstructured(pdf_path):
    elements = partition_pdf(pdf_path)
    text_segments = []
    tables = []
    for element in elements:
        if isinstance(element, dict) and element.get('type') == 'Text':
            text_segments.append(element['text'])
        elif isinstance(element, dict) and element.get('type') == 'Table':
            tables.append(element['table'])
    return text_segments, tables

def extract_text_with_pymupdf(pdf_path):
    doc = fitz.open(pdf_path)
    text_segments = []
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text_segments.append(page.get_text())
    return text_segments, []

def extract_text_with_pdfplumber(pdf_path):
    text_segments = []
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text_segments.append(page.extract_text())
            page_tables = page.extract_tables()
            if page_tables:
                tables.extend(page_tables)
    return text_segments, tables

def extract_text_and_tables_from_pdf(pdf_path):
    text_segments, tables = extract_text_with_unstructured(pdf_path)
    if not text_segments:  # Fallback to PyMuPDF if unstructured fails
        text_segments, tables = extract_text_with_pymupdf(pdf_path)
    if not text_segments:  # Fallback to pdfplumber if PyMuPDF fails
        text_segments, tables = extract_text_with_pdfplumber(pdf_path)
    return text_segments, tables

def clean_and_process_text(text_segments):
    cleaned_segments = []
    for segment in text_segments:
        if not segment.strip():
            continue
        cleaned_segments.append(segment.strip())
    return cleaned_segments

def remove_noise(text_segments):
    noise_patterns = ["header", "footer", "page number", "copyright", "disclaimer"]
    noise_regex = re.compile(r'|'.join(noise_patterns), re.IGNORECASE)
    
    filtered_segments = []
    for segment in text_segments:
        # Remove noise patterns
        segment = re.sub(noise_regex, '', segment)
        filtered_segments.append(segment.strip())
        
    return filtered_segments

def tokenize_and_lemmatize(text_segments):
    processed_segments = []
    for segment in text_segments:
        doc = nlp(segment)
        tokens = []
        for token in doc:
            if token.text.lower() not in STOP_WORDS and token.is_alpha:
                # Retain only non-entities or entities that are not of specific types
                if token.ent_type_ == '' or token.ent_type_ not in ['DATE', 'PERSON', 'ORG', 'GPE']:
                    tokens.append(token.lemma_)
        processed_segments.append(" ".join(tokens))
    return processed_segments

#Image Extraction:
def extract_images_from_pdf(pdf_path):
    images = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_images = page.images
            if page_images:
                images.extend(page_images)
    return images

# Optical Character Recognition (OCR):
def ocr_images(images):
    extracted_text = []
    for image in images:
        img_data = image['stream'].get('Data')
        if img_data:
            try:
                img = Image.open(io.BytesIO(img_data))
                text = pytesseract.image_to_string(img)
                extracted_text.append(text)
            except Exception as e:
                print(f"Error processing OCR for image: {e}")
        else:
            print("Empty or missing image data.")
    return extracted_text

# Image Enhancement:
def enhance_image(img_data):
    try:
        img = Image.open(io.BytesIO(img_data))
        # Example of enhancing image contrast
        enhancer = ImageEnhance.Contrast(img)
        enhanced_img = enhancer.enhance(1.5)  # Increase contrast
        return enhanced_img
    except Exception as e:
        print(f"Error enhancing image: {e}")
        return None  # Return None if enhancement fails


# Metadata Extraction:
def extract_image_metadata(pdf_path):
    image_metadata = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            for img in page.images:
                metadata = {
                    'page_number': page_num + 1,
                    'width': img['width'],
                    'height': img['height'],
                    'dpi': img.get('dpi', None),  # Use get() to handle missing 'dpi'
                    'colorspace': img.get('colorspace', None),
                    # Add more metadata fields as needed
                }
                image_metadata.append(metadata)
    return image_metadata

# Main function:
def extract_clean_and_process_pdf(pdf_path):
    print("Extracting text and tables from PDF...")
    text_segments, tables = extract_text_and_tables_from_pdf(pdf_path)
    print(f"Extracted {len(text_segments)} text segments and {len(tables)} tables.")
    
    print("Cleaning text segments...")
    cleaned_segments = clean_and_process_text(text_segments)
    print(f"Cleaned {len(cleaned_segments)} text segments.")
    
    print("Removing noise...")
    noise_free_segments = remove_noise(cleaned_segments)
    print(f"Filtered down to {len(noise_free_segments)} noise-free text segments.")
    
    print("Tokenizing and lemmatizing text segments...")
    processed_segments = tokenize_and_lemmatize(noise_free_segments)
    print(f"Processed {len(processed_segments)} text segments.")
    
    print("Extracting images from PDF...")
    images = extract_images_from_pdf(pdf_path)
    print(f"Extracted {len(images)} images.")
    
    print("Applying OCR to images...")
    ocr_texts = ocr_images(images)
    print(f"Extracted OCR texts from {len(ocr_texts)} images.")
    
    print("Enhancing images...")
    enhanced_images = [enhance_image(image['stream'].get('Data')) for image in images if 'stream' in image]
    print(f"Enhanced {len(enhanced_images)} images.")
    
    print("Extracting image metadata...")
    image_metadata = extract_image_metadata(pdf_path)
    print(f"Extracted metadata for {len(image_metadata)} images.")
    
    return processed_segments, tables, ocr_texts, enhanced_images, image_metadata


pdf_path = 'data/SoftwareRequirementsSpecification.pdf'
processed_text_segments, tables, ocr_texts, enhanced_images, image_metadata = extract_clean_and_process_pdf(pdf_path)

for i, segment in enumerate(processed_text_segments):
    print(f"Processed Segment {i + 1}:")
    print(segment)
    print("\n---\n")
