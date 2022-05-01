from PIL import Image
import pytesseract, re, json

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Receives image and returns text version
def processImage(image):
    # with Image.open(image) as receiptPicture:
    #     totext = pytesseract.image_to_string(receiptPicture)
    # receiptPicture.close()
    with open("./receiptText/temp.txt", "r") as totext:
        file = totext.read().upper()
        allFloat = re.findall(r".*\d[.,]\d.*", file)
        date = re.findall(r"(\d+/\d+/\d+)", file)
        tax = re.findall(r"(\d+[.,]\d+[%])", file)
    # file = open("receiptText/temp.txt", mode="w")
    # file.write(totext)
    cleanToJson(allFloat, date, tax)

#TODO set up JSON TIP: rsplit to separate name and cost
#Cleans data and returns JSON file
def cleanToJson(allFloat, date, tax):    
    banned = ["VISA", "CHANGE", "TOTAL", "TAX", "AMOUNT", "BOTTLE", "MASTERCARD", "DISCOVER", "CHASE", "CAPITALONE"]
    items = []
    cleanedFloat = [entry.replace(",",".") for entry in allFloat]
    for item in range(len(cleanedFloat)):
        if cleanedFloat[item][-1] == "A":
            items.append(addBottleTax(cleanedFloat[item],cleanedFloat[item+1]))
            continue
        if not any(bword in cleanedFloat[item] for bword in banned):
            items.append(cleanedFloat[item])
    print(items)

#Combines drink cost and bottle tax
def addBottleTax(drink, canTax):
    temp1 = drink.split()
    temp2 = canTax.split()
    return (" ".join(temp1[:-2]) + " " + str(float(temp1[-2]) + float(temp2[-1])))    

# img = "./receiptImage/receipt.jpg"
img = "./receiptText/temp.txt"
processImage(img)
