import csv
import json
import string
import urllib.request
import re

keywords = ["fixed ", "fixes ", " fixed", " fixes", "crash", " resolves",
            "resolves ", "regression", "fall back", "assertion", "coverity", "reproducible",
            "stack-wanted", "steps-wanted", "testcase", "failur", "fail", "npe ",
            " npe", "except", "broken", "bug", "differential testing", "error", "addresssanitizer",
            "hang ", " hang", "permaorange", "random orange", "intermittent", "test fix",
            "steps to reproduce", "crash", "assertion", "failure", "leak", "stack trace",
            "heap overflow", "freez", "str:", "fix ", " fix", "problem ", " problem",
            " overflow", "overflow ", "avoid ", " avoid", " issue", "issue ",
            "workaround ", " workaround", "break ", " break", " stop", "stop "]

accessTokenCounter = 0
pageCounter = 0
accessToken = ["bd1be942e48b610e829e3cb2f785ba38cf798f50",
               "9b2b62a7a0b7687704b3646f6ff9e63724edc5b9",
               "fe92ac02286f55af1775075c2a42b1fe0799f81e",
               #"8c98b46c609c55f1e8aab21abbf6834beaa449e1",
               "19ec4e9f2df223aff3fce77991aea655fb42418e"]
flag = True
with open('pytorchBuggyClosedIssues.csv', 'w') as csvOut:
    writer = csv.writer(csvOut)

    while flag:
        url = "https://api.github.com/repos/tensorflow/tensorflow/commits?state=closed&per_page=100&page="+ str(pageCounter) +"&access_token="+ accessToken[(accessTokenCounter%4)]

        issues = urllib.request.urlopen(url).read()
        parsIssues = json.loads(issues)
        if not parsIssues:
            break
        for issue in parsIssues:
            #writer.writerow(row.values())
            title = str(issue['title']).lower()
            body = str(issue['body']).lower()
            for key in keywords:
                if (re.search(key, title) is not None) or (re.search(key, body) is not None):
                    writer.writerow(issue.values())
                    print("ID is: " + str(issue['number']))
                    print("Title is :" + title)
                    break

        accessTokenCounter = accessTokenCounter + 1
        pageCounter = pageCounter + 1
        print(pageCounter)

    csvOut.close()