import os
from bottle import route, request, run, template, response
import time
import secrets
import threading
import io
from pypdf import PdfReader
import requests

db = {}
db_statusNo_lookup_dict = {
    1: "waitOnSlipUpload",
    2: "slipError_sessionExpired",
    3: "slipError_nonImageFile",
    4: "slipError_Verificationfailed",
    5: "slipVerified_printerError",
    6: "printPending",
    7: "printed"
}

data_lock = threading.Lock() # The Gatekeeper

# Create upload directory if not exists
UPLOAD_DIR = "./uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)
    
def verifySlip(uploadedSlip):
    try:
        url = "https://api.slipok.com/api/line/apikey/66527"

        headers = {
            "x-authorization": "SLIPOKDARN5DU"
        }

        files = {
            "files": (
                uploadedSlip.filename,
                uploadedSlip.file,
                uploadedSlip.content_type
            )
        }

        data = {
            "log": "true"
        }

        response = requests.post(
            url,
            headers=headers,
            files=files,
            data=data
        )

        result = response.json()

        print("---- Slip verification API response ----")
        print(result)

        if result.get("success") == True:
            ref_no = result.get("data", {}).get("transRef", "")
            return True, ref_no

        return False, ""

    except Exception as e:
        print(f"Slip verification error: {e}")
        return False, ""
    
def sendToPrinter(rid):
    return 5

def checkQueue(rid):
    return 4
    
def get_pdf_page_count_from_upload(file_upload_obj) -> int:
    """
    Takes a Bottle FileUpload object, converts it in-memory, 
    and returns the PDF page count.
    """
    try:
        # 1. Access the underlying binary stream from Bottle's FileUpload
        # upload_file.file is a file-like object, but reading raw bytes into
        # BytesIO guarantees full seeking compatibility for pypdf.
        file_bytes = file_upload_obj.file.read()
        
        memory_file = io.BytesIO(file_bytes)
        
        # 2. Pass the in-memory stream to PdfReader
        reader = PdfReader(memory_file)
        return len(reader.pages)
        
    except Exception as e:
        print(f"Error reading PDF from upload: {e}")
        return 0

@route('/')
def index():
    return template('index.html')

@route('/api/uploadpdf', method='POST')
def do_uploadpdf():
    uploadedPdf = request.files.get('print_file')
    selected_pages = request.forms.get('pages')
    color_mode = request.forms.get('colorMode')
    
    # Server-side validation (Defense in Depth)
    if not (uploadedPdf and uploadedPdf.filename.endswith('.pdf')):
        response.status = 400
        return {"status": "error", "message": "File format is not PDF."}
    
    filename = f"{secrets.token_hex(10)}.pdf"
    
    try:    
        save_path = os.path.join(UPLOAD_DIR, filename)
        uploadedPdf.save(save_path, overwrite=True)

        uploadedPdf.file.seek(0)
        
    except Exception as e:
        response.status = 500
        #return {"status": "error", "message": str(e)}
        return {"status": "error", "message": "File saving error."}
        
    timestamp = time.time()
    rid = secrets.token_hex(10)
    numpages = get_pdf_page_count_from_upload(uploadedPdf)

    if selected_pages:
        page_count = 0

        for part in selected_pages.split(','):
            part = part.strip()

            if '-' in part:
                start, end = part.split('-')
                page_count += int(end) - int(start) + 1
            else:
                page_count += 1

        page_total = page_count

    else:
        page_total = numpages


    # คำนวณราคาตามสี
    if color_mode == "colorMode_c":
        cost = page_total * 3      # สี 3 บาท/หน้า
    else:
        cost = page_total * 1      # ขาวดำ 1 บาท/หน้า
    image_qrCode_link = f"https://promptpay.io/0988501644/{cost}"
    
        
    # Safely modify the shared dictionary
    with data_lock:
        db[rid] = {
            "timestamp_start": timestamp, 
            "cost": cost, 
            "pdfFilePath": filename,
            "selected_pages": selected_pages,
            "color_mode": color_mode,
            "status": 1
        }
        
    # Debug
    with data_lock:
        db_lookup = db[rid]
    print(f"---- db[{rid}] = {db_lookup}")
    
    return {"status": "success", 
                "rid": rid, 
                "cost": cost,
                "image_qrCode_link": image_qrCode_link
            }

@route('/api/uploadslip', method='POST')
def do_uploadslip():
    uploadedSlip = request.files.get('slip_file')
    rid = request.forms.get('slipRid')

    if not uploadedSlip:
        response.status = 400
        return {
            "status": "error",
            "message": "No slip uploaded."
        }
    
    # Debug
    print(f"---- do_uploadslip, rid = {rid}")
        
    timestamp_start = -1
    with data_lock:
        if(rid in db):
            timestamp_start = db[rid]["timestamp_start"]
    
    #---- Check valid rid
    if(timestamp_start == -1):
        response.status = 400
        return {"status": "error", "message": "Request ID does not exist."}
    
    #---- Check expired session 
    timestamp_last = time.time()
    minutePassed = (timestamp_last - timestamp_start) / 60
    
    if(minutePassed > 15):
        with data_lock:
            db[rid]["status"] = 2
            db[rid]["timestamp_last"] = timestamp_last
        
        response.status = 400
        return {"status": "error", "message": "Session expired."}
    
    #---- Check slip's filename
    name, ext = os.path.splitext(uploadedSlip.filename)
    if ext.lower() not in ['.png', '.jpg', '.jpeg'] :
        with data_lock:
            db[rid]["status"] = 3
            db[rid]["timestamp_last"] = timestamp_last
        
        response.status = 400
        return {"status": "error", "message": "File format is not allowed (PNG/JPG/JPEG)."}
        
    #---- Check slip's validity
    slipVerified, ref_no = verifySlip(uploadedSlip)
    if(slipVerified):
        queue = sendToPrinter(rid)
        if(queue == -1):
            with data_lock:
                db[rid]["status"] = 5
                db[rid]["timestamp_last"] = timestamp_last
        
            response.status = 500
            return {"status": "error", "message": "Printer error."}
        else:
            with data_lock:
                if(queue == 0):
                    #---- PDF is being printed
                    db[rid]["status"] = 7
                else:
                    #---- PDF is in the queue
                    db[rid]["status"] = 6
                db[rid]["timestamp_last"] = timestamp_last    
                db[rid]["ref_no"] = ref_no  
        
            return {"status": "success", 
                        "rid": rid, 
                        "queue": queue
                    }
    else:
        with data_lock:
            db[rid]["status"] = 4
            db[rid]["timestamp_last"] = timestamp_last
    
        response.status = 400
        return {"status": "error", "message": "Slip verification failed."}

        
@route('/api/checkqueue', method='GET')
def do_checkqueue():
    rid = request.query.get('rid')
    flag = False
    with data_lock:
        if(rid in db):
            flag = True
    
    #---- Check valid rid
    if(not flag):
        response.status = 400
        return {"status": "error", "message": "Request ID does not exist."}
    
    queue = checkQueue(rid)
    if(queue <= 0):
        timestamp_last = time.time()

        with data_lock:
            db[rid]["status"] = 7
            db[rid]["timestamp_last"] = timestamp_last
    
    return {"status": "success",
            "queue": queue
            }


if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True, server='cheroot')