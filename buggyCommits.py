import csv
import json
import string
import urllib.request
import re
import os.path

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
accessToken = ["b5ae1d0a9a20081f47c36a0425c9f8cab320029b",
               "360972ba69e3b4777b89351b9df152e76d48b1f7",
               "28950f5d0e3b80fafecd23a78fe941a57e086ad7",
               #"8c98b46c609c55f1e8aab21abbf6834beaa449e1",
               "b4ba9a2826bf6f5db3f540776c0dcb6d5ad3c5ec"]
flag = True
with open('tensorflowBuggyClosedcommits.csv', 'w') as csvOut:
    writer = csv.writer(csvOut)

    while flag:
        url = "https://api.github.com/repos/tensorflow/tensorflow/commits?state=closed&per_page=100&page="+ str(pageCounter) +"&access_token="+ accessToken[(accessTokenCounter%4)]

        commits = urllib.request.urlopen(url).read()
        accessTokenCounter = accessTokenCounter + 1
        parsCommits = json.loads(commits)
        if not parsCommits:
            break
        for commit in parsCommits:
            message = str(commit['commit']['message']).lower()
            commitUrl = commit['url'] +"?access_token="+ accessToken[(accessTokenCounter%4)]
            accessTokenCounter = accessTokenCounter + 1
            filesFormat = []
            for key in keywords:
                if re.search(key, message) is not None:
                    singleCommit = urllib.request.urlopen(commitUrl).read()
                    parsedSingleCommit = json.loads(singleCommit)
                    changedFiles = parsedSingleCommit['files']
                    #writer.writerow(commit.values())
                    if len(changedFiles)>1:
                        for file in changedFiles:
                            extension = os.path.splitext(file['filename'])[1]
                            if not extension:
                                continue
                            else:
                                filesFormat.append(extension.strip().lower())
                        filesFormat = list(dict.fromkeys(filesFormat))
                    if len(filesFormat)>1:
                        writer.writerow(commit)
                        print(filesFormat)
                    break
        pageCounter = pageCounter + 1
        print("Page Counter = " + str(pageCounter))

    csvOut.close()