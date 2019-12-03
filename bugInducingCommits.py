import csv
from pydriller import GitRepository, RepositoryMining
import json
import urllib.request
import os.path

accessTokenCounter = 0
buggyCommitCounter = 0
bugInducingCommitCounter = 0
accessToken = ["b5ae1d0a9a20081f47c36a0425c9f8cab320029b",
               "360972ba69e3b4777b89351b9df152e76d48b1f7",
               "28950f5d0e3b80fafecd23a78fe941a57e086ad7",
               #"8c98b46c609c55f1e8aab21abbf6834beaa449e1",
               "b4ba9a2826bf6f5db3f540776c0dcb6d5ad3c5ec"]
commit_sha = []
with open('tensorflowClosedBuggyCommits.csv', encoding="ISO-8859-1") as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    with open('tensorflowBugInducingCommits.csv', 'w') as csvOut:
        writer = csv.writer(csvOut)
        for row in list(readCSV):
            buggyCommitCounter += 1
            print("Buggy commit counter : " + str(buggyCommitCounter))
            print("Main commit is : " + row[0])
            for commit in RepositoryMining('/home/mmm/Projects/tensorflow', only_commits=row[0]).traverse_commits():
                BuggyCommit = GitRepository("/home/mmm/Projects/tensorflow").get_commits_last_modified_lines(commit)
                print(BuggyCommit)
                for value in BuggyCommit.values():
                    for val in value:
                        if val in commit_sha:
                            print(val + " is exist")
                            continue
                        else:
                            commit_sha.append(val)
                            writer.writerow(val)
                            bugInducingCommitCounter += 1
                            print("bug Inducing Counter : " + str(bugInducingCommitCounter))
                            print("appended commit is " + val)
        csvOut.close()