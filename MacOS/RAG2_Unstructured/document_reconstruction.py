import json

def reconstruct_document(data):
    reconstructed_document = ""

    # 1. Reconstruct text segments
    if 'filtered_segments' in data:
        for segment in data['filtered_segments']:
            reconstructed_document += segment + "\n\n"  # Assuming each segment is separated by double newline

    # 2. Reconstruct tables (if any)
    if 'tables' in data:
        for table in data['tables']:
            # Append table formatting or structure here
            pass

    # 3. Append OCR texts (if any)
    if 'ocr_texts' in data:
        for ocr_text in data['ocr_texts']:
            reconstructed_document += "OCR Text:\n" + ocr_text + "\n\n"

    # 4. Append enhanced images metadata (if any)
    if 'image_metadata' in data:
        reconstructed_document += "Image Metadata:\n"
        for image_meta in data['image_metadata']:
            reconstructed_document += f"Page {image_meta['page_number']}, Size: {image_meta['width']} x {image_meta['height']}\n"
            # Include other metadata as needed

    return reconstructed_document

def save_reconstructed_document(reconstructed_content, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(reconstructed_content)
    print(f"Reconstructed document saved to: {output_path}")

# Example usage:
json_file_path = 'extracted_data.json'
output_document_path = 'reconstructed_document.txt'

# Load extracted data from JSON
with open(json_file_path, 'r', encoding='utf-8') as file:
    extracted_data = json.load(file)

# Reconstruct the document
reconstructed_content = reconstruct_document(extracted_data)

# Save reconstructed document
save_reconstructed_document(reconstructed_content, output_document_path)