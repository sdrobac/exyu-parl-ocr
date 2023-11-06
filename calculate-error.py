# on puhti: module load biopythontools/11.3.0_3.10.6
import cyrtranslit
from jiwer import wer, cer

# gtText = ''
# with open("corrected.txt") as my_file:
    # gtText = my_file.read()

# abbyText = ''
# with open("abby.txt") as my_file:
    # abbyText = my_file.read()
# tessText = ''
# with open("tess.txt") as my_file:
    # tessText = my_file.read()
    
gtText = ''
with open("par1.corr") as my_file:
    gtText = my_file.read()

abbyText = ''
with open("par1.abby") as my_file:
    abbyText = my_file.read()
tessText = ''
with open("par1.tess") as my_file:
    tessText = my_file.read()
with open("par1.gpt") as my_file:
    gptText = my_file.read()
    
print("Gt vs tess")
error = wer(gtText, tessText)
print ("WER: ", error)
cerror= cer(gtText, tessText)
print ("CER: ", cerror)


print("Gt vs Abby")
error = wer(gtText, abbyText)
print ("WER: ", error)
cerror= cer(gtText, abbyText)
print ("CER: ", cerror)

print("Gt vs GPT")
error = wer(gtText, gptText)
print ("WER: ", error)
cerror= cer(gtText, gptText)
print ("CER: ", cerror)

# print("Abby vs tess")
# error = wer(abbyText, tessText)
# print ("WER: ", error)
# cerror= cer(abbyText, tessText)
# print ("CER: ", cerror)

# # transliterate
# with open('tess-lat.txt', 'w', encoding='utf-8') as f:
    # f.write(cyrtranslit.to_latin(tessText))
# with open('abby-lat.txt', 'w', encoding='utf-8') as f:
    # f.write(cyrtranslit.to_latin(abbyText))
# with open('corrected-lat.txt', 'w', encoding='utf-8') as f:
    # f.write(cyrtranslit.to_latin(gtText))

# remove hyphens
tessText = tessText.replace("-\n", "")
# remove [PAGE_BREAK]
tessText = tessText.replace("[PAGE_BREAK]", "")
# print(tessText)
# print(cyrtranslit.to_latin(tessText))
# print("-----\n")

# print(cyrtranslit.to_latin(gtText))
# print("-----\n")

