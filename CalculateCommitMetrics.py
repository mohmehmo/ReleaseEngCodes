import csv
import json
import math
import urllib.request
from datetime import datetime

accessTokenCounter = 0

multiLangCommits = [] # ok

bugInducingCommits = [] # ok

users = {} # name of users and number of commits by each users

projectFiles = {} # last date of each file change

fileContributors = {} # contributor developers in each file

extensions = [] #

accessToken = ["ccbfaeb35388c324a8be9668332703c8cd28ede3",
               "0cc3a1c8626e242c331ced83f9b2a6131ba8285b",
               "45f8283da3a21e574ccaa9c96bf415fc6f06f6f0",
               "b3b095760fca46715bc416a24c2092267813a168"]

# load multi-labguage bug inducing commits
with open('react-nativeMultiLangBugInducingCommits.csv', encoding="ISO-8859-1") as multiLangCommitsfile:
    readCSV = csv.reader(multiLangCommitsfile, delimiter=',')
    for row in readCSV:
        multiLangCommits.append(row[0])

# load all bug inducing commits
with open('react-nativeBugInducingCommits.csv', encoding="ISO-8859-1") as bugInducingCommitsfile:
    readCSV = csv.reader(bugInducingCommitsfile, delimiter=',')
    for row in readCSV:
        bugInducingCommits.append(row[0])
        # print(row[0])
bugInducingCommitsCounter = 0
bugInducingMultiLangCommitsCounter = 0
# load all important extensions
# with open('extension.csv', encoding="ISO-8859-1") as extensionsFile:
#     readCSV = csv.reader(extensionsFile, delimiter=',')
#     for row in readCSV:
#         extensions.append(row[0])

with open('react-nativeClosedCommits.csv', encoding="ISO-8859-1") as bugInducingCommitsfile:
    readCSV = csv.reader(bugInducingCommitsfile, delimiter=',')
    with open('react-nativeBugInducingCommitsMetrics.csv', 'w', newline='') as csvOut:
        writer = csv.writer(csvOut)
        for row in reversed(list(readCSV)):
            url = "https://api.github.com/repos/facebook/react-native/commits/" + row[0] + "?access_token=" + accessToken[(accessTokenCounter % 4)]
            rowToWrite = []
            accessTokenCounter += 1
            commit = urllib.request.urlopen(url).read()
            parsCommits = json.loads(commit)
            commitDate = datetime.strptime(parsCommits['commit']['author']['date'], "%Y-%m-%dT%H:%M:%SZ")
            commitSha = parsCommits['sha']
            author = parsCommits['commit']['author']['name']
            multiLangFlag = False
            print("============================")
            print("commit sha is : " + commitSha)
            print("commit id is : " + str(accessTokenCounter))

            # calculations for bug inducing commits
            if commitSha in bugInducingCommits:
                bugInducingCommitsCounter +=1
                print("bug inducing commit number : " + str(bugInducingCommitsCounter))
                addedLOC = 0
                deletedLOC = 0
                churnLOC = 0
                entropy = 0
                changesAge = 0
                authorExperience = users.get(author,0)
                print( "author experience : " + str(authorExperience))
                developerContributor = 0
                commitfiles = parsCommits['files']
                changedFiles = len(commitfiles)

                print("number of changed files : " + str(changedFiles))

                entropy = 0
                for commitFile in commitfiles:
                    addedLOC = addedLOC + commitFile['additions']
                    deletedLOC = deletedLOC + commitFile['deletions']
                    churnLOC = churnLOC + commitFile['changes']
                    developerContributor = developerContributor + len(fileContributors.get(commitFile['filename'],''))
                    if commitFile['filename'] in projectFiles.keys():
                        fileLastChange = datetime.strptime(projectFiles.get(commitFile['filename']), "%Y-%m-%dT%H:%M:%SZ")
                        changesAge = changesAge + (commitDate - fileLastChange).days

                print("Total added LOC : " + str(addedLOC))
                print("Total deleted LOC : " + str(deletedLOC))
                print("Total churn LOC : " + str(churnLOC))
                print("Total developer contributor : " + str(developerContributor))
                print("Total change age of files : " + str(changesAge))

                # calculating entroopy
                for commitFile in commitfiles:
                    print("Number of changes" + str(commitFile['changes']))
                    if commitFile['changes'] == 0:
                        changedLOC = 1
                    else:
                        changedLOC = commitFile['changes']
                    if churnLOC == 0:
                        churnLOC = changedLOC
                    tmpEntropy = math.log2(changedLOC/churnLOC)*(-1)
                    print("entropy : " + str(tmpEntropy))
                    entropy += tmpEntropy

                print("Total entropy is : " + str(entropy))

                addedLOC = addedLOC / changedFiles
                deletedLOC = deletedLOC / changedFiles
                churnLOC = churnLOC / changedFiles
                changesAge = changesAge / changedFiles
                entropy = entropy / changedFiles
                developerContributor = developerContributor / changedFiles

                print("Average added LOC : " + str(addedLOC))
                print("Average deleted LOC : " + str(deletedLOC))
                print("Average churn LOC : " + str(churnLOC))
                print("Average developer contributor : " + str(developerContributor))
                print("Average change age of files : " + str(changesAge))
                print("Average entropy is : " + str(entropy))

                if commitSha in multiLangCommits:
                    multiLangFlag = True
                    bugInducingMultiLangCommitsCounter +=1
                    print("bug Inducing Multi Langugae Commit Numebr : " + str(bugInducingMultiLangCommitsCounter))

                rowToWrite.append(addedLOC)
                rowToWrite.append(deletedLOC)
                rowToWrite.append(churnLOC)
                rowToWrite.append(entropy)
                rowToWrite.append(changesAge)
                rowToWrite.append(changedFiles)
                rowToWrite.append(developerContributor)
                rowToWrite.append(authorExperience)
                rowToWrite.append(multiLangFlag)
                writer.writerow(rowToWrite)

            # ==================================
            # calculate author experience
            if author in users.keys():
                exp = users.get(author)
                exp += 1
                users[author] = exp
            else:
                users.update({author:1})

            # ==========================
            # calculate age of last change of each file & number of develoer contributor in the file
            files = parsCommits['files']
            for file in files:
                # age of last change of each file
                fileName = file['filename']
                if fileName in projectFiles.keys():
                    projectFiles[fileName] = parsCommits['commit']['author']['date']
                else:
                    projectFiles.update({fileName:parsCommits['commit']['author']['date']})

                # number of contributor in each file
                contribitors = []
                if fileName in fileContributors.keys():
                    contribitors = fileContributors.get(fileName)
                    if author in contribitors:
                        break
                    else:
                        contribitors.append(author)
                        fileContributors[fileName] = contribitors
                else:
                    contribitors.append(author)
                    fileContributors.update({fileName:contribitors})
        csvOut.close()
