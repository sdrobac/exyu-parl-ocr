from parse_word_file import parse_word, order_lines
from fuzzywuzzy import fuzz, process
import cyrtranslit
import re, json

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



# The larger string
larger_string = "In the quiet of the evening, the stars began to twinkle above, casting their gentle light upon the serene landscape. The rustling leaves of the ancient trees whispered secrets of the forest, and the night held a sense of mystery that beckoned the curious to explore its depths. A gentle breeze carried the scent of blooming wildflowers, and in the distance, the soft hoot of an owl echoed through the night, a reminder of nature's timeless beauty and wonder."


# "In the quriet of the evenng, the stas begnn to twinkel abuve, csting ther gntle ligt upn the serene lancape. The rustln leves of the anciemt tres whisperd secres of the forst, and the nigt hld a sence of msery that bekon'd the cris to esplor its depts. A gentl breze caried the snt of bloomin wildfowrs, and in the disntce, the soft hoot of an owl echod thru the nigt, a remin'dr of nture's timeles btuy and wndr.


# from difflib import SequenceMatcher as SM
# from nltk.util import ngrams
# import codecs

# needle = "this is the string we want to find"
# hay    = "text text lots of text and more and more this string is the one we wanted to find and here is some more and even more still"

# needle_length  = len(needle.split())
# max_sim_val    = 0
# max_sim_string = u""

# for ngram in ngrams(hay.split(), needle_length + int(.2*needle_length)):
    # hay_ngram = u" ".join(ngram)
    # similarity = SM(None, hay_ngram, needle).ratio() 
    # if similarity > max_sim_val:
        # max_sim_val = similarity
        # max_sim_string = hay_ngram

# print (max_sim_val, max_sim_string)

# exit()
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

            # print('found BOLD')
            # print(current_text)
            # print('---------')
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
            print(text[i-10:i] + "  PAGE_BREAK!!!!      " + text[i+12:i+22])
            # # If [PAGE_BREAK] is found, add the current text to pairs
            # # and mark a page break
            # add_to_pairs(current_text, current_format)
            # current_text = ''
            # pairs.append(('', {'page_break': True}))
            
            if(current_text != ''):
                pairs.append((current_text, {}))
            current_text = ''
            pairs.append(('', {'page_break': True}))
            i += 12
        else:
            # Otherwise, append the character to the current text
            current_text += text[i]
            
            i += 1

    # print (i, current_text)
    # Add any remaining text to pairs
    # pairs.append((current_text, {}))
    if(current_text != ''):
        pairs.append((current_text, {}))

    return pairs

# Define a function to add the current text and format to pairs
def add_to_pairs(text, format):
    if text:
        pairs.append((text, format))

paragraphs_raw = parse_word('19210923-ZakonodajniOdbor-11.docx')
with open('ocr-tesseract-corrected.txt', 'r', encoding='utf-8') as file:
    tessText = file.read()
    
tessParagraphs = connect_lines_and_get_paragraphs(tessText)
tessText = '\n\n'.join(tessParagraphs)

count = 0
allBolds = set()
boldList=[]
foundTess=0
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
            
            # # Use regular expressions to find text within <BOLD> tags
            # bold_texts = re.findall(r'<BOLD>(.*?)</BOLD>', concatenated_string)
            # print (bold_texts[0])
            
            
            # Use regular expressions to find text within <BOLD> tags
            bold_matches = re.findall(r'<BOLD>(.*?)</BOLD>(.{0,10})', concatenated_string)

            for match in bold_matches:
                bold_text, context = match
                context = context.replace("<BOLD>", "") # if new bold after, remove tag
                # print(f"{bold_text} \t\t {context}")
                textContext = bold_text + context
                textContext = textContext.replace("(","")
                textContext = textContext.replace(")","")
                bold_text = bold_text.replace("(","")
                bold_text = bold_text.replace(")","")
                # print (textContext)
    
                allBolds.add(bold_text)
                boldList.append(bold_text)

                
                # print('---TESS----')
                bold_matchesTess = re.findall(rf'({bold_text})(.*)', tessText)
                if (bold_matchesTess):
                    foundTess += 1
                    
                # for match in bold_matchesTess:
                    # bold_text_tess, context_tess = match
                    # print(f"{bold_text_tess} \t\t {context_tess}")
                    
                # print('******')
                    
            # # Print the text inside <BOLD> tags and two consecutive words after each tag
            # for bold_text in bold_matches:
                # bold_text = bold_text.replace("(","")
                # allBolds.add(bold_text)
                # boldList.append(bold_text)
                # print(f"Text inside <BOLD> tags: {bold_text}")
                
                # bold_matchesTess = re.findall(rf'{bold_text}', tessText)
                # if (bold_matchesTess):
                    # foundTess += 1
                # # print ('FOUND ', len(bold_matchesTess))

                # print(f"Text inside <BOLD> tags: {bold_text}")
                
                
                # # text_after_bold = re.search(rf'{re.escape(bold_match)}\s+([^<\s]+)', concatenated_string)
                # text_after_bold = re.search(rf'<BOLD>{re.escape(bold_match)}</BOLD>\s+([^<\s]+)', concatenated_string)
                # print (text_after_bold)
                # if text_after_bold:
                    # print(f"Text after <BOLD>: {text_after_bold.group(1)}")
                    # ten_chars_after_bold = text_after_bold.group(1)[:10]
                    # print(f"Text after <BOLD>: {text_after_bold.strip('</BOLD>')}")



            # # The larger string
            # larger_string = tessText

            # # The target string you want to find
            # target_string = concatenated_string

            # # Find the best matching substring
            # best_match = process.extractOne(target_string, larger_string)

            # # Print the original and matching parts
            # original_part = best_match[0]
            # matching_part = best_match[1]
            # print("Original part:")
            # print(original_part)
            # print("Matching part:")
            # print(matching_part)




        # if count == 25: break
# print (count)
# print (len(paragraphs_raw))
print(len(allBolds))

for bold_text in allBolds:
    tessText = tessText.replace(bold_text, "<BOLD>"+bold_text+"</BOLD>")

print(len(boldList))
print(foundTess)



paragraphs = tessText.split("\n\n")

newParagraphs = []
for i, paragraph in enumerate(paragraphs):
    
    # Initialize paragraph-specific variables
    
    pairs = []
    current_text = ''
    current_format = {}
    
    if (('<BOLD>' in paragraph) or ('[PAGE_PREAK]' in paragraph)):
        print('Rearange')
        print(paragraph)
        print('--')
        result = transform_text(paragraph)
        print("Result:", result)
        print('----------')
        newParagraphs.append(result)
    else:
        print("Bold or page breaks not found")
        newParagraphs.append([(paragraph, {})])
        
        
    # if(i == 30):
        # break
    # current_text = ''
    # current_format = {}
print('****************')
# print(newParagraphs)

# Save the result as a JSON file
with open("output.json", "w", encoding="utf-8") as json_file:
    json.dump(newParagraphs, json_file, ensure_ascii=False, indent=1)

exit()

with open('ocr-tesseract-corrected-bold.txt', "w") as file:
    file.write(tessText)
# # Convert the set to a sorted list
# sorted_list = sorted(allBolds)

# # Print the sorted elements
# for element in sorted_list:
    # print(element)



