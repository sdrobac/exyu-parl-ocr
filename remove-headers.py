import re
import cyrtranslit
import sys, os

def has_running_text(input_string):
    pattern = r"[a-zA-Z]{4,}"
    return bool(re.search(pattern, cyrtranslit.to_latin(input_string)))

def no_header_words(input_string):
    #TODO add other words, like dates for example. check other documents
    words = ['Стено', 'седница ', 'Стеногр.', 'белешке', 'септембра', 'Отеногр.', 'седница\n', 'седница.',  'ред. саст.', 'ред. сает.', 'јануара', 'фебруара','марта','априла', 'маја', 'ред: саст', 'јипа', 'јуна', 'јула', 'августа', 'септембра', 'октобра', 'новембра', 'децембра', 'Степорр', 'јуда', '__________', '466' , '456', 'Степогр', 'ред. заст',  '2 “ УУ А, 4', 'ред. еаст', 'ред. саст', 'ред. саот.', 'Стенотрафске_бедешке', 'СРТОГРАФЕКЕ', 'Пед.', 'децембра', 'Ц ———   ', 'РЕВАОАКА', 'БАБТАМАК', 'БАЗТАМАК' , 'ВЕГЕ5КЕ', 'ВЕШЕЗКЕ', 'БАЗТАМАК', 'КЕРрОУМГ', 'БАЗБТАМАК', 'СРТОГРАФЕКЕ', 'БЕЛЕШКЕ', 'Стенотрафске_бедешке', '_а———аан——–—', 'ред. саот', 'САСТАНАК', 'ПРЕТХОДНИ', 'Отеногр', 'Ц ———       ', '—=_____________', 'РЕДОВНИ', 'СТЕНОГРАФСКЕ БЕЛЕШКЕ' ]

    for w in words:
        if w in input_string:
            return False
        if w.upper() in input_string:
            return False
    # print("No matching words found in the input_string.")
    return True
def contains_only_spaces_or_newline(input_string):
    for char in input_string:
        if not char.isspace():
            return False
    return True
def remove_extra_consecutive_newlines(input_list):
    output_list = []
    consecutive_newlines = 0

    for item in input_list:
        if item == '\n':
            consecutive_newlines += 1
            if consecutive_newlines <= 1:
                output_list.append(item)
        else:
            consecutive_newlines = 0
            output_list.append(item)

    return output_list
def getBlocksForChange(firstLine, endLine, tessLines):
    newBlockList = []
    originalBlockList = []
    for j in range(firstLine, endLine):
        if j < len(tessLines):
            if has_running_text(tessLines[j]) and no_header_words(tessLines[j]) or  contains_only_spaces_or_newline(tessLines[j]):
                newBlockList.append(tessLines[j])
            originalBlockList.append(tessLines[j])
    newBlockList = remove_extra_consecutive_newlines(newBlockList)
    newBlock = ''.join(newBlockList)
    originalBlock = ''.join(originalBlockList)
    return originalBlock, newBlock
    
def getBlocksForLighterChange(firstLine, endLine, tessLines):
    newBlockList = []
    originalBlockList = []
    for j in range(firstLine, endLine):
        if j < len(tessLines):
            if has_running_text(tessLines[j]) or  contains_only_spaces_or_newline(tessLines[j]):
                newBlockList.append(tessLines[j])
            originalBlockList.append(tessLines[j])
    newBlockList = remove_extra_consecutive_newlines(newBlockList)
    newBlock = ''.join(newBlockList)
    originalBlock = ''.join(originalBlockList)
    return originalBlock, newBlock


def main(args):
    
    DIR1 = '/scratch/project_2004614/senka-slo/data/tesseract-cyrilic-corrected/'
    DIR2 = '/scratch/project_2004614/senka-slo/data/tesseract-cyrilic-corrected2/'
    DIR3 = '/scratch/project_2004614/senka-slo/data/tesseract-cyrilic-corrected3/'
    DIR4 = '/scratch/project_2004614/senka-slo/data/tesseract-cyrilic-noncorrected/'
    # OUTPUTDIR = '/scratch/project_2004614/senka-slo/data/tesseract-intermidiate/'
    OUTPUTDIR = '/scratch/project_2004614/senka-slo/data/tesseract-intermidiate-new/'
    # fileName = '19190322-PrivremenoNarodnoPredstavnistvo-05.tesseract'
    # fileName = '19210728-ZakonodajniOdbor-03.tesseract'
    # fileName = '19211104-ZakonodajniOdbor-05.tesseract'
    for DIR in [DIR4, DIR3, DIR1, DIR2]:
        for root, dirs, files in os.walk(DIR):
            for file in files:  
                if file.endswith(".tesseract"):
                # print(file)
                # if (file == "19370722-Senat-25.tesseract"):
                # if (file == '19210922-ZakonodajniOdbor-10.tesseract'):

                    
                    fullFileName = os.path.join(root, file)
                    outputPath = os.path.join(OUTPUTDIR, file)
                    
                    print(fullFileName)
                    print(outputPath)
                
                    # fullFileName = os.path.join (DIR, fileName)
                    with open(fullFileName, 'r', encoding='utf-8') as file:
                        tessLines = file.readlines()
                    with open(fullFileName, 'r', encoding='utf-8') as file:
                        tessText = file.read()

                    # paragraphsTess = tessText.split('\n\n') 
                    for i, line in enumerate(tessLines, start=0):
                        # print(line)
                        # Check first 6 lines
                        # originalBlock, newBlock = getBlocksForChange(0, 6, tessLines)
                        originalBlock, newBlock = getBlocksForLighterChange(0, 6, tessLines)
                        
                        tessText  = tessText.replace(originalBlock, newBlock)

                        if ('[PAGE_BREAK]' in line):
                            # print (cyrtranslit.to_latin(line.strip("[PAGE_BREAK]")))
                            
                            # The 5 lines before the line with [PAGE_BREAK]
                            originalBlock, newBlock = getBlocksForChange(i-5, i, tessLines)

                            # A line with "[PAGE_BREAK]"
                            if has_running_text(line.strip("[PAGE_BREAK]")) and no_header_words(line) :
                                newBlock = newBlock + line
                            else:
                                newBlock = newBlock + "[PAGE_BREAK]"
                            originalBlock = originalBlock + line

                            # # The 5 lines after the line with [PAGE_BREAK]
                            originalBlockAfter, newBlockAfter = getBlocksForChange(i+1, i+10, tessLines)
                            
                            newBlock = newBlock + newBlockAfter
                            originalBlock = originalBlock + originalBlockAfter
                            
                            # print('*******NEW*******')
                            # print(newBlock)
                            # print('******ORIGINAL*******')
                            # print(originalBlock)
                            # print("-------------------")
                            
                            tessText  = tessText.replace(originalBlock, newBlock)
                            

                            
                            
                    with open(outputPath, "w") as file:
                        file.write(tessText)

                            
                            # # print('*******NEW*******')
                            # # print(cyrtranslit.to_latin(newBlock))
                            # # print('******ORIGINAL*******')
                            # # print(cyrtranslit.to_latin(originalBlock))
                            # # print("-------------------")
                            
                            # # print('*******NEW*******')
                            # # print(newBlock)
                            # # print('******ORIGINAL*******')
                            # # print(originalBlock)
                            # # print("-------------------")
                            # # if has_running_text(line.strip("[PAGE_BREAK]")) and no_header_words(line) :
                                # # print("NO DELETE: ",line)
                            # # else:
                                # # print("YA DELETE: ", line)
if __name__ == '__main__':
    main(sys.argv)