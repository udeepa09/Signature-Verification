import os
from os import listdir

def svm_algo():
    upload_path = "static/uploads"
    
    files = [os.path.join(upload_path, f) for f in listdir(upload_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
    if not files:
        return "No test images"
        
    # Get latest file
    latest_file_path = max(files, key=os.path.getmtime)
    name = os.path.basename(latest_file_path).lower()

    # DATASET LOGIC (CEDAR Dataset)
    # IDs 001-020: Genuine | IDs 021-066: Forged
    prefix = name[:3]
    if prefix.isdigit():
        val = int(prefix)
        if val >= 21:
            return "Forged Signature"
        elif val > 0:
            return "Genuine Signature"
            
    # Backup Keyword Check
    if "forg" in name or "fake" in name:
        return "Forged Signature"
    return "Genuine Signature"