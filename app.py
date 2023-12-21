from flask import Flask, request, jsonify, abort
import zxing
import os
import sys
import traceback

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
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"parsed": 'qww'})


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

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0",port=5002,debug=True)
