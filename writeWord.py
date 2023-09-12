import docx
document = docx.Document("/users/drobacs1/slovenci-scripts/tmp-data/test.docx")

# allParagraphs = document.paragraphs
# len(allParagraphs)
# for para in allParagraphs:
    # # if (para.text.strip()): 
        # print(para.text)
        # print("-------")
        
        
shapes = document.inline_shapes
len(shapes)
for shape in shapes:
    # if (para.text.strip()): 
        print(shape.text)
        print("-------")