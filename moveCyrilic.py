import os
import shutil
SOURCE_DIR = '/scratch/project_2004614/senka-slo/data/tesseract-ocr'
DEST_DIR = '/scratch/project_2004614/senka-slo/data/tesseract-cyrilic'

xml_names = []

with open("list-serbian", "r") as file:
    for line in file:
        # Split each line by space and take the first part (the XML name)
        parts = line.split()
        if len(parts) >= 1:
            xml_name = parts[0]
            # Remove the ".xml" extension
            xml_name = xml_name.rstrip(".xml")
            xml_names.append(xml_name)
            
# Now xml_names contains a list of XML names without the ".xml" extension

# /scratch/project_2004614/senka-slo/data/yu1Parl-source/1919/19190
SOURCE_DIR = '/scratch/project_2004614/senka-slo/data/yu1Parl-source/'
DEST_DIR = '/scratch/project_2004614/senka-slo/data/tesseract-cyrilic'


# pdf,docx
for name in xml_names:
    year = name[0:4]
    origAbby = os.path.join(SOURCE_DIR, year, name+".docx")
    newDestFile = os.path.join(DEST_DIR)
    print(origAbby)
    shutil.copy(origAbby, newDestFile)
    
# # tesseract
# for name in xml_names:
    # origTessFile = os.path.join(SOURCE_DIR, name+".tesseract")
    # newDestFile = os.path.join(DEST_DIR)
    # print(origTessFile)
    # shutil.copy(origTessFile, newDestFile)
