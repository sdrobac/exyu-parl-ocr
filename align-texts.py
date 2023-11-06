# on puhti: module load biopythontools/11.3.0_3.10.6
import cyrtranslit
from genalog.text import alignment
from genalog.text import anchor
from jiwer import wer, cer

gt_txt = "New York is big"
noise_txt = "New Yo rkis "

# These two methods are interchangeable, but work best at different character length as mentioned above
aligned_gt, aligned_noise = anchor.align_w_anchor(gt_txt, noise_txt, gap_char="@")

print(f"Aligned ground truth: {aligned_gt}")
print(f"Aligned noise:        {aligned_noise}")
# aligned_gt = aligned_gt.replace("@", "")
# aligned_noise = aligned_noise.replace("@", "")
# print(f"Aligned ground truth: {aligned_gt}")
# print(f"Aligned noise:        {aligned_noise}")
# Aligned ground truth: New Yo@rk is big
# Aligned noise:        New Yo rk@is @@@

# aligned_gt, aligned_noise = alignment.align(gt_txt, noise_txt, gap_char="@")
# print(f"Aligned ground truth: {aligned_gt}")
# print(f"Aligned noise:        {aligned_noise}")
# # Aligned ground truth: New Yo@rk is big
# # Aligned noise:        New Yo rk@is @@@


# with open('data-align/19190322-PrivremenoNarodnoPredstavnistvo-05.docx.txt', 'r') as abby_f:
    # abby-text = abby_f.readlines()
    
# print (abby-text)


# with open("hello.txt") as my_file:
    # print(my_file.read())

# abbyText = ''
# with open("data-align/abbyPage1.txt") as my_file:
    # abbyText = my_file.read()
# tessText = ''
# with open("data-align/tessPage1.txt") as my_file:
    # tessText = my_file.read()

# abbyText = ''
# with open("data-align/19190322-PrivremenoNarodnoPredstavnistvo-05.docx.txt") as my_file:
    # abbyText = my_file.read()
# tessText = ''
# with open("data-align/ocr-tesseract.txt") as my_file:
    # tessText = my_file.read()

gtText = ''
with open("data-align/1933_2_14_senat_16/corrected.txt") as my_file:
    gtText = my_file.read()

abbyText = ''
with open("data-align/1933_2_14_senat_16/abby-page2.txt") as my_file:
    abbyText = my_file.read()
tessText = ''
with open("data-align/1933_2_14_senat_16/tess-page2.txt") as my_file:
    tessText = my_file.read()
    
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

print("Abby vs tess")
error = wer(abbyText, tessText)
print ("WER: ", error)
cerror= cer(abbyText, tessText)
print ("CER: ", cerror)



# remove hyphens
tessText = tessText.replace("-\n", "")
# remove [PAGE_BREAK]
tessText = tessText.replace("[PAGE_BREAK]", "")
# print(tessText)
# print(cyrtranslit.to_latin(tessText))
# print("-----\n")

# print(cyrtranslit.to_latin(gtText))
# print("-----\n")



aligned_abby, aligned_tess = anchor.align_w_anchor(abbyText, tessText, gap_char="@")
# print(f"Aligned abby: {cyrtranslit.to_latin(aligned_abby)}")
# print(f"Aligned tess:  {cyrtranslit.to_latin(aligned_tess)}")

print(len(aligned_abby))
print(len(aligned_tess))


with open('data-align/1933_2_14_senat_16/aligned-abby.txt', 'w', encoding='utf-8') as f:
    f.write(aligned_abby)
with open('data-align/1933_2_14_senat_16/aligned-tess.txt', 'w', encoding='utf-8') as f:
    f.write(aligned_tess)
