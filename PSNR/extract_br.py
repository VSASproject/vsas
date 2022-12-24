import re
import csv

File_List = ["longdress_1", "loot", "redandblack", "soldier"]


pattern = r'SUMMARY*'
pattern2= r'mseF,PSNR'

for file_name in File_List:
    with open("Output/" + file_name + ".csv", "w") as csvfile:
        br = [["QP", "Br", "PSNR"]]
        counter = 0
        csvwriter = csv.writer(csvfile)
        with open("nohup_records/"+ file_name +".out", "r", encoding='UTF-8') as longdress_br:
            flag = 0
            for line in longdress_br.readlines():
                if re.match(pattern, line):
                    flag += 2
                    continue
                if flag == 2:
                    flag -= 1
                    continue
                if flag == 1:
                    counter += 1
                    flag = 0
                    if counter%3 == 0:
                        br.append([str(15+counter//3 - 1), line.split()[2], line.split()[-1]])
        csvwriter.writerows(br)


for file_name in File_List:
    with open("Output/GP_" + file_name + ".csv", "w") as csvfile:
        br = [["QP", "Br", "PSNR"]]
        counter = 0
        csvwriter = csv.writer(csvfile)
        with open("nohup_records/"+ file_name +".out", "r", encoding='UTF-8') as longdress_br:
            flag = 0
            flag_2 = 0
            for line in longdress_br.readlines():
                if flag_2 == 1 and re.search(pattern2, line):
                    br[-1].append(line.split()[-1])
                    flag_2= 0
                if re.match(pattern, line):
                    flag += 2
                    continue
                if flag == 2:
                    flag -= 1
                    continue
                if flag == 1:
                    counter += 1
                    flag = 0
                    if counter%3 == 0:
                        br.append([str(15+counter//3 - 1), line.split()[2]])
                        flag_2 = 1

        csvwriter.writerows(br)