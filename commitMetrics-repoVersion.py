import csv
import json
import io
import pycurl
from datetime import datetime, timezone
from pydriller import GitRepository, RepositoryMining
import pytz
import math


accessTokenCounter = 0
accessToken = ["7780bc2602cf4b08f2226df2a7bd10322889e794",
               "a3faa7537be29d679d1fe4fc164cea9a868871ec",
               "9cbaddca8a3a0c7cd0392015b1aaea61b980f10f",
               "3bb16fb747687219525d25d211e6f9693cafeff4",
               "035918431202a5f530cba91ef6fabfa381ebaa9c",
               "54ad10a8f93229a8281da7aa08d1b1c51c6ed94a",
               "66370591addc2cbe18730c60049918d12114c295",
               "000bfcb24d207efc28634066d954441c6c02c42a",
               "9a485fb6b838551899bde1304035a6dfd17b8fb8",
               "464b5762578f185aebb2e1bbbe033aa7abc416d8"]


def getReleases(repo):
    repoReleases = {}
    startDate = datetime.now(timezone.utc)

    # repoReleases = {}
    pageCounter = 1
    global accessTokenCounter
    releaseCounter = 0
    while True:
        output = io.BytesIO()
        # result = ""
        conn = pycurl.Curl()
        conn.setopt(pycurl.USERPWD, "e.morovati@yahoo.com:{}".format(accessToken[accessTokenCounter % 10]))
        conn.setopt(pycurl.URL,
                    f"https://api.github.com/repos/{repo}/releases?per_page=100&page={pageCounter}")
        conn.setopt(pycurl.WRITEFUNCTION, output.write)
        conn.perform()

        accessTokenCounter += 1
        pageCounter += 1

        result = output.getvalue().decode()
        releases = json.loads(result)

        if not releases:
            break
        utc = pytz.UTC
        for release in releases:
            endDate = startDate
            startDate = datetime.strptime(release['created_at'], "%Y-%m-%dT%H:%M:%SZ")
            # print(f"release {releaseCounter} is between {startDate} and {endDate}")
            startDate = utc.localize(startDate)
            # endDate = utc.localize(endDate)
            repoReleases.update({releaseCounter: [startDate, endDate]})
            releaseCounter += 1

        repoReleases.update({releaseCounter:[utc.localize(datetime.strptime('1990-01-01T00:00:00Z', "%Y-%m-%dT%H:%M:%SZ")),startDate]})

    return repoReleases


def findRelease(commitDate , repoReleases):
    release = 0

    for item in repoReleases.keys():
        releaseDate = repoReleases.get(item)
        # if (commitDate <= utc.localize(releaseDate[1])) and (commitDate > utc.localize(releaseDate[0])):
        if (commitDate <= releaseDate[1]) and (commitDate > releaseDate[0]):
            release = item
            break

    return release


def main(commitMetricFile):
    counter = 0
    users = {}  # name of users and number of commits by each users
    projectFiles = {}  # last date of each file change
    fileContributors = {}

    repo = "apache/arrow"

    crossLangCommitList = []
    crossLangFlag = False

    # cross-language bug-inducing commits
    crossLangCommits = open('results/arrow/arrowRealCJavaCommits.csv', encoding="ISO-8859-1")
    crossLangCommitsReader = csv.reader(crossLangCommits, delimiter=',')
    for commit in crossLangCommitsReader:
        crossLangCommitList.append(commit[0])

    #get all commits
    closedCommits = open('results/arrow/arrowClosedCommits.csv', encoding="ISO-8859-1")
    closedCommitsReader = csv.reader(closedCommits, delimiter=',')

    # get all releases
    repoReleases = getReleases(repo)


    csvOut = open('results/arrow/arrowSortedCommitMetrics.csv', 'w')
    writer = csv.writer(csvOut)

    # add header to the CSV file
    writer.writerow(["commit SHA", "commit date", "release", "added LOC", "deleted LOC", "churn LOC", "entropy", "change age", "changed files",
                     "contributors", "developer-exp", "cross-lang"])

    gr = GitRepository('/home/mmm/Projects/arrow')

    for row in reversed(list(closedCommitsReader)):
        commit = gr.get_commit(row[0])
        crossLangFlag = False
        counter += 1
        rowToWrite = []
        rowToWrite.append(row[0])

        commitDate = commit.author_date
        author = commit.author.name
        rowToWrite.append(commitDate)

        rowToWrite.append(findRelease(commitDate, repoReleases))

        addedLOC = 0
        deletedLOC = 0
        churnLOC = 0
        entropy = 0
        changesAge = 0
        developerContributor = 0

        authorExperience = users.get(author, 0)
        commitfiles = commit.modifications
        changedFiles = len(commitfiles)

        for commitFile in commitfiles:
            addedLOC += commitFile.added
            deletedLOC += commitFile.removed
            churnLOC += commitFile.added + commitFile.removed
            fileName = f"{commitFile.new_path}/{commitFile.filename}"
            developerContributor = developerContributor + len(fileContributors.get(fileName, ''))
            if fileName in projectFiles.keys():
                fileLastChange = projectFiles.get(fileName)
                changesAge = changesAge + (commitDate - fileLastChange).days

        # calculating entroopy
        for commitFile in commitfiles:

            fileChanges = commitFile.added + commitFile.removed
            if fileChanges == 0:
                changedLOC = 1
            else:
                changedLOC = fileChanges

            if churnLOC == 0:
                churnLOC = changedLOC
            tmpEntropy = math.log2(changedLOC / churnLOC) * (-1)
            # print("entropy : " + str(tmpEntropy))
            entropy += tmpEntropy

        if changedFiles != 0:
            addedLOC = addedLOC / changedFiles
            deletedLOC = deletedLOC / changedFiles
            churnLOC = churnLOC / changedFiles
            changesAge = changesAge / changedFiles
            entropy = entropy / changedFiles
            developerContributor = developerContributor / changedFiles


        if row[0] in crossLangCommitList:
            crossLangFlag = True

        rowToWrite.append(addedLOC)
        rowToWrite.append(deletedLOC)
        rowToWrite.append(churnLOC)
        rowToWrite.append(entropy)
        rowToWrite.append(changesAge)
        rowToWrite.append(changedFiles)
        rowToWrite.append(developerContributor)
        rowToWrite.append(authorExperience)
        rowToWrite.append(crossLangFlag)
        writer.writerow(rowToWrite)

        print(f"{counter} commit is parsed")

        #///////////////////////////////
        # calculate author experience
        if author in users.keys():
            exp = users.get(author)
            exp += 1
            users[author] = exp
        else:
            users.update({author: 1})

        # calculate age of last change of each file & number of developer contributor in the file
        for commitfile in commitfiles:

            # age of last change of each file
            fileName = f"{commitFile.new_path}/{commitFile.filename}"
            if fileName in projectFiles.keys():
                projectFiles[fileName] = commit.author_date
            else:
                projectFiles.update({fileName: commit.author_date})

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
                fileContributors.update({fileName: contribitors})
    csvOut.close()

    return True


if __name__ == '__main__':
    main("test")