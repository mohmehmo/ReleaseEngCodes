import csv
import json
import string
import urllib.request


accessTokenCounter = 0
pageCounter = 0
accessToken = ["bd1be942e48b610e829e3cb2f785ba38cf798f50",
               "9b2b62a7a0b7687704b3646f6ff9e63724edc5b9",
               "fe92ac02286f55af1775075c2a42b1fe0799f81e",
               #"8c98b46c609c55f1e8aab21abbf6834beaa449e1",
               "19ec4e9f2df223aff3fce77991aea655fb42418e"]
flag = True
with open('tensorflowClosedPRs.csv', 'w') as csvOut:
    writer = csv.writer(csvOut)
    while flag== True:
        url = "https://api.github.com/repos/tensorflow/docs/pulls?state=closed&per_page=100&page="+ str(pageCounter) +"&access_token="+ accessToken[(accessTokenCounter%4)]
        pull_req = urllib.request.urlopen(url).read()
        parsData = json.loads(pull_req)
        if not parsData:
            flag = False
            break
        for row in parsData:
            writer.writerow(row.values())

        accessTokenCounter = accessTokenCounter + 1
        pageCounter = pageCounter + 1
        print(pageCounter)

    csvOut.close()