import re
import cyrtranslit

def has_running_text(input_string):
    pattern = r"[a-zA-Z]{2,}"
    return bool(re.search(pattern, cyrtranslit.to_latin(input_string)))

def no_header_words(input_string):
    #TODO add other words, like dates for example. check other documents
    words = ['Стено', 'седница ', 'Стеногр.', 'белешке', 'септембра', 'Отеногр.', 'седница\n', 'седница.']
    for w in words:
        if w in input_string:
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
        if j <= len(tessLines):
            if has_running_text(tessLines[j]) and no_header_words(tessLines[j]) or  contains_only_spaces_or_newline(tessLines[j]):
                newBlockList.append(tessLines[j])
            originalBlockList.append(tessLines[j])
    newBlockList = remove_extra_consecutive_newlines(newBlockList)
    newBlock = ''.join(newBlockList)
    originalBlock = ''.join(originalBlockList)
    return originalBlock, newBlock

with open('ocr-tesseract.txt', 'r', encoding='utf-8') as file:
    tessLines = file.readlines()
with open('ocr-tesseract.txt', 'r', encoding='utf-8') as file:
    tessText = file.read()

# paragraphsTess = tessText.split('\n\n') 
for i, line in enumerate(tessLines, start=0):
    # print(line)
    # Check first 6 lines
    originalBlock, newBlock = getBlocksForChange(0, 6, tessLines)
    
    tessText  = tessText.replace(originalBlock, newBlock)

    if ('[PAGE_BREAK]' in line):
        # print (cyrtranslit.to_latin(line.strip("[PAGE_BREAK]")))
        
        # The 5 lines before the line with [PAGE_BREAK]
        originalBlock, newBlock = getBlocksForChange(i-5, i, tessLines)
        # tessText  = tessText.replace(originalBlock, newBlock)

        # A line with "[PAGE_BREAK]"
        if has_running_text(line.strip("[PAGE_BREAK]")) and no_header_words(line) :
            newBlock = newBlock + line
        else:
            newBlock = newBlock + "[PAGE_BREAK]"
        originalBlock = originalBlock + line

        # # The 5 lines after the line with [PAGE_BREAK]
        originalBlockAfter, newBlockAfter = getBlocksForChange(i+1, i+7, tessLines)
        
        newBlock = newBlock + newBlockAfter
        originalBlock = originalBlock + originalBlockAfter
        
        print('*******NEW*******')
        print(newBlock)
        print('******ORIGINAL*******')
        print(originalBlock)
        print("-------------------")
        
        tessText  = tessText.replace(originalBlock, newBlock)
        
        # for j in range(i+1, i+7):
            # if j <= len(tessLines):
                # # print(f"Line {j}: {tessLines[j]}")
                # if has_running_text(tessLines[j]) and no_header_words(tessLines[j]) or  contains_only_spaces_or_newline(tessLines[j]):
                    # # print ("Save me")
                    # newBlockList.append(tessLines[j])
                # originalBlockList.append(tessLines[j])
        # # print (newBlockList)
        # newBlockList = remove_extra_consecutive_newlines(newBlockList)

        
        # newBlock = ' '.join(newBlockList)
        # originalBlock = ' '.join(originalBlockList)
        
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
            
            
    with open('ocr-tesseract-corrected.txt', "w") as file:
        file.write(tessText)


# new_paragraphs = []
# for paragraph in paragraphs:
    # lines = paragraph.strip().split('\n')
    # cleaned_lines = [line for line in lines if "[PP]" not in line]
    # new_paragraph = '\n'.join(cleaned_lines)
    # new_paragraphs.append(new_paragraph)
    
    
# # Print the paragraphs
# for i, paragraph in enumerate(paragraphsTess, start=1):
    # if (i < 3):
        # print(f"Paragraph {i}:\n{paragraph.strip()}\n")
        # # for match,index in fuzzy_extract(newStrings[0], paragraph, 30):
            # # print('Query: ' + newStrings[0])
            # # print('Result: '+ tessFile[index:index + len(match)])
    # if ('[PAGE_BREAK]' in paragraph):
        # print ("Paragraph: ", paragraph)
                # lines = paragraph.strip().split('\n')
        # cleaned_lines = [line for line in lines if "седница" or "Стено" not in line]
        # for 
        # new_paragraph = '\n'.join(cleaned_lines)
        # new_paragraphs.append(new_paragraph)
        # # for line in lines:
            # # if "[PAGE_BREAK]" in line:
                # # print(f"Paragraph {i} (line {lines.index(line) + 1}): {line}")
                # # print(line)
                # # break  # Stop checking other lines in this paragraph
        # # # print(f"Paragraph {i}:\n{paragraph.strip()}\n")
        # # if i < len(paragraphsTess):
            # # next_paragraph = paragraphsTess[i]
            # # next_paragraph_lines = next_paragraph.strip().split('\n')
            # # if next_paragraph_lines:
                # # print(f"Next Paragraph (first line): {next_paragraph_lines[0]}")
                # # print(next_paragraph_lines[0])
                # # # if len(next_paragraph_lines) > 1:
                    # # # print(f"Next Paragraph (second line): {next_paragraph_lines[1]}")
    # else:
        # new_paragraphs.append(paragraph)
# exit()
    
# for query_string in newStrings:

# # large_string = "thelargemanhatanproject is a great project in themanhattincity"
# # query_string = "manhattan"
    # # print('query: {}\nstring: {}'.format(query_string, tessFile))
    # print('Query: {}'.format(query_string))
    # for match,index in fuzzy_extract(query_string, tessFile, 30):
        # # print('match: {}\nindex: {}'.format(match, index))
        # print('Result: '+ tessFile[index:index + len(match)])



# large_string = "thelargemanhatanproject is a great project in themanhattincity"
# query_string = "manhattan"

# def fuzzy_extract(qs, ls, threshold):
    # '''fuzzy matches 'qs' in 'ls' and returns list of 
    # tuples of (word,index)
    # '''
    # for word, _ in process.extractBests(qs, (ls,), score_cutoff=threshold):
        # # print('word {}'.format(word))
        # for match in find_near_matches(qs, word, max_l_dist=1):
            # match = word[match.start:match.end]
            # # print('match {}'.format(match))
            # index = ls.find(match)
            # yield (match, index)

# query_string = "citi"
# print('query: {}\nstring: {}'.format(query_string, large_string))
# for match,index in fuzzy_extract(query_string, large_string, 30):
    # print('match: {}\nindex: {}'.format(match, index))
# # print(large_string[index:index + len(match)])






    
# # Path to the text document where you want to save the unique lines
# output_path = 'unique_lines.txt'

# # Write the unique lines from both documents to the output file
# with open(output_path, 'w', encoding='utf-8') as output_file:
    # output_file.write("Unique lines in Document 1:\n")
    # output_file.writelines(unique_to_document1)
    # output_file.write("\nUnique lines in Document 2:\n")
    # output_file.writelines(unique_to_document2)

# print("Unique lines have been written to 'unique_lines.txt'")
