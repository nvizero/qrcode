import requests
import zxing

# URL of the image to be decoded
image_url = "http://example.com/qr.png"

# Send HTTP request to get the image
response = requests.get(image_url)

# Check if the request was successful
if response.status_code == 200:
    # Save the image content to a temporary file
    with open("temp_qr.png", "wb") as f:
        f.write(response.content)

    # Use zxing to decode the QR code
    reader = zxing.BarCodeReader()
    barcode = reader.decode("temp_qr.png")
    print(barcode.parsed)
else:
    print("Failed to retrieve the image")

import zxing

reader = zxing.BarCodeReader()
barcode = reader.decode("qr.png")
print(barcode.parsed)

