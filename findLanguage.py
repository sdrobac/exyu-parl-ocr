import os

diretory = '/scratch/project_2004614/senka-slo/data/yu1Parl.TEI/yu1Parl.TEI/'

i = 0

for filename in os.listdir(diretory):
    # print (filename)
    with open(os.path.join(diretory, filename), "r") as file:
        text = file.read()
        countLangSr = text.count("lang=\"sr\"")
        if (countLangSr > 0 ): # when == 0 is non serbian
            countLangHr = text.count("lang=\"hr\"")
            countLangSl = text.count("lang=\"sl\"")
            # # mixed ser/cro/slo
            # if (countLangSr > countLangHr+countLangSl and countLangHr+countLangSl > 100):
                # print(filename, countLangSr, countLangHr, countLangSl )            
            # serbian
            if (countLangSr > countLangHr+countLangSl and countLangHr+countLangSl < 100):
                print(filename, countLangSr, countLangHr, countLangSl )

            


    # i += 1
    # if (i == 100):
        # exit()
