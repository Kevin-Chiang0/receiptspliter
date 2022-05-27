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
    cleanToJson(allFloat, date[0], tax[0])

#TODO set up JSON TIP: rsplit to separate name and cost
#Cleans data and returns JSON file
def cleanToJson(allFloat, date, tax):
    taxcalc =  1 + float(tax.strip("%"))/100  
    banned = ["VISA", "CHANGE", "TOTAL", "TAX", "AMOUNT", "BOTTLE", "MASTERCARD", "DISCOVER", "CHASE", "CAPITALONE"]
    items = []
    cost = []

    cleanedList = [entry.replace(",",".") for entry in allFloat]

    for item in range(len(cleanedList)):

        if not any(bword in cleanedList[item] for bword in banned):
            if cleanedList[item][-1] == "A":
                cleanedList[item] = (addBottleTax(cleanedList[item],cleanedList[item+1]))
            splitItems = cleanedList[item].split()
            if splitItems[0] == "E":
                items.append(" ".join(splitItems[2:-1]))
                cost.append(round(float(splitItems[-1]) * taxcalc,2))
            else:
                items.append(" ".join(splitItems[1:-1]))
                cost.append(float(splitItems[-1]))

    jsonDict = {"items": items,
                "cost": cost,
                "tax": tax,
                "date": date}

    with open("./receiptText/receipt.json","w") as outfile:
        json.dump(jsonDict, outfile)


#Combines drink cost and bottle tax
def addBottleTax(drink, canTax):
    splitItems1 = drink.split()
    splitItems2 = canTax.split()
    combinedcost = float(splitItems1[-2]) + float(splitItems2[-1])
    return " ".join(splitItems1[:-2]) + " " + str(combinedcost)

# img = "./receiptImage/receipt.jpg"
img = "./receiptText/splitItems.txt"
processImage(img)
