from parse_word_file import parse_word, order_lines
from fuzzywuzzy import fuzz, process
import cyrtranslit
import re, json, sys, os
from bs4 import BeautifulSoup

def has_bold_elements(data):
    for item, attributes in data:
        if 'bold' in attributes and attributes['bold']:
            return True
    return False
def concatenate_with_bold(data):
    result = ""
    for item, attributes in data:
        if 'bold' in attributes and attributes['bold']:
            result += f"<BOLD>{item}</BOLD>"
        else:
            result += item
    return result
def concatenate_with_bold_tags(data):
    result = ""
    is_in_bold = False

    for item, attributes in data:
        if 'bold' in attributes and attributes['bold']:
            if not is_in_bold:
                result += "<BOLD>"
                is_in_bold = True
            result += item
        else:
            if is_in_bold:
                result += "</BOLD>"
                is_in_bold = False
            result += item

    if is_in_bold:
        result += "</BOLD>"
    return result 
def count_bold_segments(new_string):
    bold_open = 0
    bold_close = 0
    bold_segments = 0

    inside_bold = False
    for i in range(len(new_string)):
        if new_string[i:i + 6] == "<BOLD>":
            bold_open += 1
            if not inside_bold:
                bold_segments += 1
                inside_bold = True
        elif new_string[i:i + 7] == "</BOLD>":
            bold_close += 1
            if bold_close == bold_open:
                inside_bold = False
    return bold_segments

def connect_lines_and_get_paragraphs(text):
    # Replace hyphens with empty spaces
    text = text.replace('-\n', '')

    # Split the text into lines
    lines = text.split('\n')

    # Initialize variables
    paragraphs = []
    current_paragraph = ""

    # Iterate through the lines
    for line in lines:
        # If the line is empty or contains only whitespace, it's a paragraph break
        if not line.strip():
            if current_paragraph:
                # Append the current paragraph to the list
                paragraphs.append(current_paragraph.strip())
                # Reset the current paragraph
                current_paragraph = ""
        else:
            # Join non-empty lines to the current paragraph
            current_paragraph += line + ' '

    # Append the last paragraph if it exists
    if current_paragraph:
        paragraphs.append(current_paragraph.strip())

    return paragraphs

def transform_text(text):
    pairs = []
    current_text = ''
    current_format = {}

    i = 0
    while i < len(text):
    
        # print(text[i:i+7])
        if text[i:i + 6] == '<BOLD>':
            # If <BOLD> tag is found, add the current text to pairs
            # without the tags and start tracking bold formatting
            if(current_text != ''):
                pairs.append((current_text, {}))
            current_text = ''
            i += 6

            # Skip ahead to the closing </BOLD> tag
            while text[i:i + 7] != '</BOLD>' and i < len(text):
                current_text += text[i]
                i += 1

            if text[i:i + 7] == '</BOLD>':
                # print('found CLosing bold')
                pairs.append((current_text, {'bold': True}))
                # print(current_text)
                i += 7  # Skip the closing tag
                current_text = ''
                # print("after BOLD", text[i:i+5])
            else:
                # If no closing tag is found, raise an error or handle it as needed
                raise ValueError("Unclosed <BOLD> tag.")

        elif text[i:i + 12] == '[PAGE_BREAK]':
            # print(text[i-10:i] + "  PAGE_BREAK!!!!      " + text[i+12:i+22])
            # # If [PAGE_BREAK] is found, add the current text to pairs
            # # and mark a page break

            if(current_text != ''):
                pairs.append((current_text, {}))
            current_text = ''
            pairs.append(('', {'page_break': True}))
            i += 12
        else:
            # Otherwise, append the character to the current text
            current_text += text[i]
            i += 1
    # Add any remaining text to pairs
    if(current_text != ''):
        pairs.append((current_text, {}))

    return pairs


# Define a function to add the current text and format to pairs
def add_to_pairs(text, format):
    if text:
        pairs.append((text, format))
def replaceLongestMatch(text, word_set):
    # Sort the words in descending order of length to prioritize longer matches
    sorted_words = sorted(word_set, key=lambda word: len(word), reverse=True)

    # Create a regular expression pattern to match any of the words in the set
    pattern = re.compile('|'.join(map(re.escape, sorted_words)))

    # Use re.sub with a custom replacement function to wrap the longest match in <BOLD> tags
    def replace(match):
        matched_word = match.group(0)
        if matched_word in word_set:
            return f'<BOLD>{matched_word}</BOLD>'
        return matched_word

    result = pattern.sub(replace, text)
    return result
def main(args):
    DIR = '/scratch/project_2004614/senka-slo/data/tesseract-intermidiate-new/'
    OUTDIR = '/scratch/project_2004614/senka-slo/data/tesseract-cyrilic-results'
    OUTDIR = '/scratch/project_2004614/senka-slo/data/tesseract-cyrilic-results-new'
    
    i = 0
    for filename in os.listdir(DIR):
        if filename.endswith(".tesseract"):
        # if (filename == '19350718-NarodnaSkupstina-04.tesseract'):
        # if (filename == '19320218-NarodnaSkupstina-10.tesseract'):
        # if (filename == '19210922-ZakonodajniOdbor-10.tesseract'):
            
            
            # tessPath = os.path.join(DIR, '19210923-ZakonodajniOdbor-11.tesseract')   
            tessPath = os.path.join(DIR, filename)   
                    
            # wordPath = os.path.join(DIR, '19210923-ZakonodajniOdbor-11.docx')
            wordPath = os.path.join(DIR, os.path.splitext(filename)[0] + ".docx")
            paragraphs_raw = parse_word(wordPath)
            
            outputJson = os.path.join(OUTDIR, os.path.splitext(filename)[0] + ".json")
            outputTxt = os.path.join(OUTDIR, os.path.splitext(filename)[0] + ".txt")
            
            print(outputJson)

        
            with open(tessPath, 'r', encoding='utf-8') as file:
                tessText = file.read()
                
            tessParagraphs = connect_lines_and_get_paragraphs(tessText)
            tessText = '\n\n'.join(tessParagraphs)

            count = 0
            allBolds = set()
            # boldList=[]
            # foundTess=0
            for paragraph in paragraphs_raw:
                if has_bold_elements(paragraph):
                    # print(paragraph)
                    
                    count += 1
                    # concatenated_string1 = concatenate_with_bold(paragraph)
                    
                    concatenated_string = concatenate_with_bold_tags(paragraph)
                    if (count_bold_segments(concatenated_string) == 1):
                        # print("-------------------")
                        # # print(concatenated_string1)
                        # print(concatenated_string)
                        # print("-------------------")
                        
                        # Use regular expressions to find text within <BOLD> tags
                        bold_matches = re.findall(r'<BOLD>(.*?)</BOLD>(.{0,10})', concatenated_string)

                        for match in bold_matches:
                            bold_text, context = match
                            # # To replace with context, not implemented
                            # context = context.replace("<BOLD>", "") # if new bold after, remove tag
                            # print(f"{bold_text} \t\t {context}")
                            # textContext = bold_text + context   
                            # textContext = textContext.replace("(","")
                            # textContext = textContext.replace(")","")
                            bold_text = bold_text.replace("(","")
                            bold_text = bold_text.replace(")","")
                            bold_text = bold_text.strip()
                            
                            # bold text has to be at least 4 chars without spaces or punctiation
                            cleanedBold = ''.join(char for char in bold_text if char.isalnum())
                            if (len(cleanedBold)> 3):
                                allBolds.add(bold_text)
                            # boldList.append(bold_text)


            # replace bolds
            tessText = replaceLongestMatch(tessText, allBolds)

            # print("bold set: ", len(allBolds))
            # for bold in allBolds:
                # print (bold)
            # print("bold list: ", len(boldList))

            with open(outputTxt, "w") as file:
                file.write(tessText)

            ## Second part - Convert to paragraphs and json

            paragraphs = tessText.split("\n\n")

            newParagraphs = []
            for i, paragraph in enumerate(paragraphs):
                
                # Initialize paragraph-specific variables
                pairs = []
                current_text = ''
                current_format = {}
                
                if ('<BOLD>' in paragraph) or ('[PAGE_BREAK]' in paragraph):
                    # print('Rearange')
                    # print(paragraph)
                    # print('--')
                    
                    result = transform_text(paragraph)
                    # print("Result:", result)
                    # print('----------')
                    
                    newParagraphs.append(result)
                else:
                    # Bold or page breaks not found
                    newParagraphs.append([(paragraph, {})])
                # if(i == 30):
                    # break

            # # Save the result as a JSON file
            with open(outputJson, "w", encoding="utf-8") as json_file:
                json.dump(newParagraphs, json_file, ensure_ascii=False, indent=1)
        # if (i == 50):
            # break
        # i += 1



if __name__ == '__main__':
    main(sys.argv)


