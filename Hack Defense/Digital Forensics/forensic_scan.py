# forensics/forensic_scan.py
import exifread, os, sys, pandas as pd, time

def extract_exif(path):
    try:
        with open(path,"rb") as f:
            tags = exifread.process_file(f, stop_tag="UNDEF", details=False)
        return {k:str(tags[k]) for k in tags}
    except Exception:
        return {}

def scan_folder(folder):
    rows=[]
    for root,_,files in os.walk(folder):
        for fn in files:
            p=os.path.join(root,fn)
            st=os.stat(p)
            ex=extract_exif(p)
            rows.append({"path":p,"size":st.st_size,"mtime":time.ctime(st.st_mtime),"exif_keys":list(ex.keys())})
    df=pd.DataFrame(rows)
    df.to_csv("forensic_report.csv", index=False)
    print("Written forensic_report.csv")

if __name__=="__main__":
    scan_folder(sys.argv[1] if len(sys.argv)>1 else ".")
