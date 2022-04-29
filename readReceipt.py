from PIL import Image
import pytesseract, re
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

#Receives image of receipt and returns list of items
def processImage(image):
    with Image.open(image) as receiptPicture:
        totext = pytesseract.image_to_string(receiptPicture)
    receiptPicture.close()

    items = re.findall(r".*[.,]\d.*",totext)
    date = (re.findall(r"(\d+/\d+/\d+)", totext))
    items.append(date[0])

    file = open("receiptText/temp.txt", mode="w")
    file.write(totext)

    return(items)

img = "./receiptImage/receipt.jpg"
print(processImage(img))
