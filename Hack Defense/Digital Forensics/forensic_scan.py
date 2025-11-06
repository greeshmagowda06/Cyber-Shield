# forensics/forensic_metadata_scan.py
import os
import time
import hashlib
import mimetypes
import pandas as pd
import exifread
from tkinter import Tk, filedialog
from datetime import datetime

# Supported image types for EXIF extraction
IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".tiff", ".tif", ".webp")

def file_hash(path, algo="sha256"):
    """Compute SHA-256 hash for integrity verification."""
    try:
        h = hashlib.new(algo)
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None

def extract_exif(path):
    """Extract EXIF metadata (only for image files)."""
    try:
        if not path.lower().endswith(IMAGE_EXTS):
            return {}
        with open(path, "rb") as f:
            tags = exifread.process_file(f, stop_tag="UNDEF", details=False)
        return {k: str(v) for k, v in tags.items()}
    except Exception:
        return {}

def basic_metadata(path):
    """Extract basic file system metadata and timestamps."""
    try:
        st = os.stat(path)
        return {
            "size_bytes": st.st_size,
            "created_time": datetime.fromtimestamp(st.st_ctime).isoformat(),
            "modified_time": datetime.fromtimestamp(st.st_mtime).isoformat(),
            "accessed_time": datetime.fromtimestamp(st.st_atime).isoformat(),
        }
    except Exception as e:
        return {"error": str(e)}

def collect_metadata(folder):
    """Walk through folder and extract metadata for all files."""
    data = []
    print(f"\n🔍 Scanning folder: {folder}\n")

    for root, _, files in os.walk(folder):
        for fn in files:
            path = os.path.join(root, fn)
            print(f"→ Scanning: {path}")
            meta = basic_metadata(path)
            mime, _ = mimetypes.guess_type(path)
            exif = extract_exif(path)

            data.append({
                "path": path,
                "mime_type": mime or "unknown",
                "hash_sha256": file_hash(path),
                **meta,
                "exif_tags": list(exif.keys()) if exif else [],
            })

    if not data:
        print("\n⚠️ No files found or scanned.")
        return None

    df = pd.DataFrame(data)
    report_name = f"forensic_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(report_name, index=False)
    print(f"\n✅ Forensic report saved as: {report_name}")
    return report_name

def choose_folder():
    """Prompt user to select folder via GUI."""
    root = Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title="Select Folder to Scan for Metadata")
    root.destroy()
    return folder

if __name__ == "__main__":
    folder = choose_folder()
    if folder:
        collect_metadata(folder)
    else:
        print("❌ No folder selected. Exiting.")
