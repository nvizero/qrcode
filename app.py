from flask import Flask, request, jsonify, abort,send_from_directory
import zxing
import os
import sys
import traceback
import matplotlib.pyplot as plt
import qrcode
from PIL import Image
from io import BytesIO
from functools import wraps

allowed_hosts_global = []

def abort_msg(e):
    """500 bad request for exception

    Returns:
        500 and msg which caused problems
    """
    error_class = e.__class__.__name__ # 引發錯誤的 class
    detail = e.args[0] # 得到詳細的訊息
    cl, exc, tb = sys.exc_info() # 得到錯誤的完整資訊 Call Stack
    lastCallStack = traceback.extract_tb(tb)[-1] # 取得最後一行的錯誤訊息
    fileName = lastCallStack[0] # 錯誤的檔案位置名稱
    lineNum = lastCallStack[1] # 錯誤行數 
    funcName = lastCallStack[2] # function 名稱
    # generate the error message
    errMsg = "Exception raise in file: {}, line {}, in {}: [{}] {}. Please contact the member who is the person in charge of project!".format(fileName, lineNum, funcName, error_class, detail)
    # return 500 code
    abort(500, errMsg)

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"parsed": 'qww'})

def restrict_hosts(allowed_hosts):
    global allowed_hosts_global
    allowed_hosts_global = allowed_hosts  # Keep track of the allowed hosts
    print(allowed_hosts_global)
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.remote_addr not in allowed_hosts:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/qrcode')
@restrict_hosts(['192.168.1.1','127.0.0.1', '10.0.0.1'])
def create_qr_code():
    # Get the text from the query parameter 'code'
    text = request.args.get('code', 'Default Text')
    file_path = "uploads/"+text+".png"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)
    # Create an image from the QR Code instance
    img = qr.make_image(fill_color="black", back_color="white")
    # Save it somewhere, change the extension as needed
    img.save(file_path)
    return jsonify({"img": file_path})



@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        if file:
            # 保存文件到服务器
            filename = os.path.join('./', file.filename)
            file.save(filename)

            # 使用 zxing 来解析二维码
            reader = zxing.BarCodeReader()
            barcode = reader.decode(filename)
            
            if barcode is None:
                return jsonify({"error": "QR code not found"}), 404

            return jsonify({"parsed": barcode.parsed})

    except Exception as e:
        abort_msg(e)

def create_qr_code(text, file_path):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    # Create an image from the QR Code instance
    img = qr.make_image(fill_color="black", back_color="white")
    # Save it somewhere, change the extension as needed
    img.save(file_path)
        
if __name__ == '__main__':
    app.debug = True
    # 要轉換成 QR 碼的文字
    # text_to_encode = "要轉換成 QR 碼的文字 Your text goes here"

    # # 設定 QR 碼圖片的保存路徑
    # output_file = "qr_code.png"

    # # 創建 QR 碼
    # create_qr_code(text_to_encode, output_file)

    # # 顯示 QR 碼圖片
    # img = Image.open(output_file)
    # plt.imshow(img)
    # plt.axis('off')
    # plt.show()

    app.run(host="0.0.0.0",port=5002,debug=True)
