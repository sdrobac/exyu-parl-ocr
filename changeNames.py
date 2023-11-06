import os
import shutil
SOURCE_FILE_DIR = '/scratch/project_2004614/senka-slo/data-images/'
DEST_DIR = '/scratch/project_2004614/senka-slo/data/tesseract-ocr'

nameDict = {
"narodnaskupščina":"NarodnaSkupstina",
"narodnaskupština":"NarodnaSkupstina",
"narodnaskupština":"NarodnaSkupstina",
"narodnopredstavništvo":"NarodnoPretstavnistvo",
"narodnopretstavništvo":"NarodnoPretstavnistvo",
"PrivremenoNarodnoPredstavništvo":"PrivremenoNarodnoPredstavnistvo",
"senat":"Senat",
"zakonodajniodbor":"ZakonodajniOdbor",
}

for d in os.listdir(SOURCE_FILE_DIR):
    for k in os.listdir(os.path.join(SOURCE_FILE_DIR, d)):
        file_dir = os.path.join(SOURCE_FILE_DIR, d, k)
        # print(f'file dir: {file_dir}')
        # print (k)
        

        parts = k.split("_")
        # if len(parts) > 5:
            # print("PROBLEM!!!")
            # print(f'file dir: {file_dir}')
            # print (k)

        year = parts[0]
        month = parts[1].zfill(2)
        day = parts[2].zfill(2)
    
        formatted_date = f"{year}{month}{day}"
        
        name = nameDict[parts[3]]
        # print(parts[3], name)
        
        number = parts[4].zfill(2)
        number = number.replace("prethodni", "prethodna")
        number = number.replace("predhodna", "prethodna")

       
        if ("." in number):
            numparts = number.split(".")
            num1 = numparts[0].zfill(2)
            num2 = numparts[1]
            number = f"{num1}p{num2}"

        addition = ''
        if len(parts) == 6: 
            addition = parts[5]
       
        newName = f"{formatted_date}-{name}-{number}{addition}.tesseract"
        
        if (k == "1933_3_14-15_narodnaskupština_39.3"):
            newName = "1933031415-NarodnaSkupstina-39p3.tesseract"
            
        print(newName)
        # 19351114-NarodnaSkupstina-03.pdf
        # 19320310-NarodnaSkupstina-25ekspoze.pdf
        # 19320115-NarodnaSkupstina-prethodna4.pdf
        # 19321020-Senat-prethodna.pdf
        # /19330315-NarodnaSkupstina-40p1.pdf
        # 19380322-Senat-11p2.pdf
    
        # print(newName)
        ocrOrig = os.path.join(SOURCE_FILE_DIR, d, k, "ocr-tesseract.txt")
        # print(ocrOrig)
        
        shutil.copy(ocrOrig, os.path.join(DEST_DIR,newName))
 