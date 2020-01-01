import csv
import json
import os
import urllib.request

extensoin = {}


existedExt = []
accessTokenCounter = 0
accessToken = ["ccbfaeb35388c324a8be9668332703c8cd28ede3",
               "0cc3a1c8626e242c331ced83f9b2a6131ba8285b",
               "45f8283da3a21e574ccaa9c96bf415fc6f06f6f0",
               "b3b095760fca46715bc416a24c2092267813a168"]#,
              # "c36cd5c9ab7b1abdb23771e3eebe4944533b5b36"]

with open('extension.csv', encoding="ISO-8859-1") as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')

    for row in list(readCSV):
        if row[0].strip() in extensoin:
            continue
        else:
            extensoin.update({row[0].strip(): row[1].strip()})

with open('grpcBugInducingCommits.csv', encoding="ISO-8859-1") as data:
    readData = csv.reader(data, delimiter=',')
    with open('grpcMultiLangBugInducingCommits.csv', 'w', newline='') as csvOut:
        writer = csv.writer(csvOut)
        for row in readData:
            url = "https://api.github.com/repos/grpc/grpc/commits/" + row[0] + "?access_token="+ accessToken[(accessTokenCounter%4)]
            commit = urllib.request.urlopen(url).read()
            parsCommits = json.loads(commit)
            files = parsCommits['files']
            print("====================")
            print("number of changed files is -->  " + str(len(files)))
            if len(files)>1:
                print("more than one file")
                fileType = []
                existedExt = []
                for file in files: #checking all files chaned using commit
                    filename, file_extension = os.path.splitext(file['filename'])
                    print("file Extension -- >  " + file_extension[1:])
                    if file_extension[1:].strip() in fileType:
                        print("ext is existed")
                        continue
                    else:
                        print("ext added")
                        fileType.append(file_extension[1:].strip())

                fileType = list(dict.fromkeys(fileType))  #delete duplicate items
                print("delete duplicate items")
                if len(fileType)>1:
                    print("file types more than one --> " + str(fileType))
                    for item in fileType:
                        language = extensoin.get(item,"")
                        if language != "":
                            print(language)
                            existedExt.append(language)
                    existedExt = list(dict.fromkeys(existedExt))
                    print("final file extensions -- >" + str(existedExt))

                    if (("c" in existedExt) or ("c++" in existedExt)) and ("c/c++" in existedExt):
                        existedExt.remove("c/c++")
                        print("After c or c++ deletion   -->  " + str(existedExt))
                    if len(existedExt) > 1:

                        writer.writerow([row[0]] + existedExt)
                        print(str(row[0]) + "   is related to communication between programming languages")
                        print([row[0]] + existedExt)
            print("Commit ID : " +str(accessTokenCounter))
            accessTokenCounter +=1
        csvOut.close()