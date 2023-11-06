# on puhti: module load biopythontools/11.3.0_3.10.6
import cyrtranslit
from genalog.text import alignment
from genalog.text import anchor


# gt_txt = "New York is big"
# noise_txt = "New Yo rkis "

# # These two methods are interchangeable, but work best at different character length as mentioned above
# aligned_gt, aligned_noise = anchor.align_w_anchor(gt_txt, noise_txt, gap_char="@")

# print(f"Aligned ground truth: {aligned_gt}")
# print(f"Aligned noise:        {aligned_noise}")


with open("/users/drobacs1/slovenci-scripts/exyu-parl-ocr/data-align/19210923-ZakonodajniOdbor-11/19210923-ZakonodajniOdbor-11.txt") as my_file:
    abbyText = my_file.read()
with open("/users/drobacs1/slovenci-scripts/exyu-parl-ocr/data-align/19210923-ZakonodajniOdbor-11/19210923-ZakonodajniOdbor-11.docx.txt") as my_file:
    abbyDocText = my_file.read()

with open("/users/drobacs1/slovenci-scripts/exyu-parl-ocr/data-align/19210923-ZakonodajniOdbor-11/ocr-tesseract.txt") as my_file:
    tessText = my_file.read()

aligned_abbyDoc, aligned_abbyTxt = anchor.align_w_anchor(abbyDocText, abbyText, gap_char="@")

with open('/users/drobacs1/slovenci-scripts/exyu-parl-ocr/data-align/19210923-ZakonodajniOdbor-11/abby-align-docx.txt', 'w', encoding='utf-8') as f:
    f.write(aligned_abbyDoc)
with open('/users/drobacs1/slovenci-scripts/exyu-parl-ocr/data-align/19210923-ZakonodajniOdbor-11/abby-align-txt.txt', 'w', encoding='utf-8') as f:
    f.write(aligned_abbyTxt)



exit()


aligned_abby, aligned_tess = anchor.align_w_anchor(abbyText, tessText, gap_char="@")
# print(f"Aligned abby: {cyrtranslit.to_latin(aligned_abby)}")
# print(f"Aligned tess:  {cyrtranslit.to_latin(aligned_tess)}")

print(len(aligned_abby))
print(len(aligned_tess))


with open('/users/drobacs1/slovenci-scripts/exyu-parl-ocr/data-align/19210923-ZakonodajniOdbor-11/aligned-abby.txt', 'w', encoding='utf-8') as f:
    f.write(aligned_abby)
with open('/users/drobacs1/slovenci-scripts/exyu-parl-ocr/data-align/19210923-ZakonodajniOdbor-11/aligned-tess.txt', 'w', encoding='utf-8') as f:
    f.write(aligned_tess)
