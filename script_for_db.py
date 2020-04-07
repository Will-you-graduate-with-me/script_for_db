# excel 파일 모두 csv 파일로 변경해야함
import csv
import glob

import pandas as pd

files = glob.glob('./resource/scriptNotPreprocessed/*.csv')  # 디렉토리 하위에 파일 확인
file_write = open('./resource/scriptPreprocessed/db.txt', 'w', encoding='utf-8')


def saveWholeID(part_no, unit_no, sentence_no, case_no, language, sentence):
    script_id = "p" + str(part_no) + "_u" + str(unit_no) + "_" + sentence_no + "_" + str(case_no) + "_" + language
    string = script_id + "," + str(part_no) + "," + str(unit_no) + "," + sentence_no + "," + str(
        case_no) + "," + language + "," + "\"" + sentence + "\""
    return string


for fn in files:

    file_open = open(fn, 'r')
    texts = csv.reader(file_open)

    for line in texts:

        # print(line)

        case_no = 1  # default

        if "PART" in line[0]:
            part_no = line[0][5:]  # 파트 번호만 추출
            pass  # 파트만 나오는 줄 넘어가기

        elif "UNIT" in line[0]:
            unit_no = line[0][5:]  # 유닛 번호만 추출
            pass  # 유닛만 나오는 줄 넘어가기

        else:
            sentence_no = line[0]
            language = line[1][0:1]
            sentence = line[2]
            file_write.write(saveWholeID(part_no, unit_no, sentence_no, case_no, language, sentence) + "\n")

            # print(len(line))
            #print(line)

            if (line[3] != ""):
                case_no = 2
                sentence = line[3]
                file_write.write(saveWholeID(part_no, unit_no, sentence_no, case_no, language, sentence) + "\n")
                # print("길이 4")

            if (len(line) == 5):
                if (line[4] != ""):
                    case_no = 3
                    sentence = line[4]
                    file_write.write(saveWholeID(part_no, unit_no, sentence_no, case_no, language, sentence) + "\n")
                    #print("길이 5")

    file_open.close()
file_write.close()  # 모든 파일 한 번에 저장

scripts_text = pd.read_csv('./resource/scriptPreprocessed/db.txt', quotechar='"', quoting=2, delimiter=",",
                           names=['script_id', 'part_no', 'unit_no', 'sentence_no', 'case_no', 'language', 'sentence'])
scripts_text.to_csv('./resource/scriptPreprocessed/db.csv', quotechar='"', quoting=2, index=None)

#os.remove('./resource/scriptPreprocessed/db.txt')  # 임시로 만든 txt 파일 삭제
