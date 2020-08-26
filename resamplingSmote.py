import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE
from matplotlib import pyplot
from sklearn.model_selection import train_test_split
from numpy import where
from collections import Counter
import csv
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.metrics import confusion_matrix, classification_report

def separateTestTrain(repo):

    testPercentage = 20

    testData = open(f'results/{repo}/{repo}TestData.csv', 'w')
    testDataWriter = csv.writer(testData)
    testDataWriter.writerow(
        ["commitSHA", "commitDate", "release", "releaseID", "addedLOC", "deletedLOC", "churnLOC", "entropy",
         "changeAge", "changedFiles",
         "contributors", "developerExp", "maxPreviousBug", "maxPreviousCrossLangBug", "crossLang"])


    trainData = open(f'results/{repo}/{repo}TrainData.csv', 'w')
    trainDataWriter = csv.writer(trainData)
    trainDataWriter.writerow(
        ["commitSHA", "commitDate", "release", "releaseID", "addedLOC", "deletedLOC", "churnLOC", "entropy",
         "changeAge", "changedFiles",
         "contributors", "developerExp", "maxPreviousBug", "maxPreviousCrossLangBug", "crossLang"])

    commitMetrics = open(f'results/{repo}/{repo}SortedCommitMetrics.csv', encoding="ISO-8859-1")
    commitMetricsReader = csv.reader(commitMetrics, delimiter=',')

    commitNumber = len(list(commitMetricsReader)) - 1
    testNumer = int(commitNumber * (testPercentage / 100))

    counter = 1
    commitMetrics.seek(0)

    for row in reversed(list(commitMetricsReader)):
        # print(counter)
        # for ommitting header
        if counter > commitNumber:
            break

        if counter <= testNumer:
            testDataWriter.writerow(row)
        else:
            trainDataWriter.writerow(row)

        counter += 1
    print(f"{repo} is separated to test and train....")

def resampling(repo):
    data = pd.read_csv(f"results/{repo}/{repo}TrainData.csv")
    data['crossLang'] = data['crossLang'].map({False: 0, True: 1})
    X = data.drop(['commitSHA', 'commitDate', 'releaseID', 'crossLang'], axis=1)
    y = data.crossLang

    smt = SMOTE()
    X_train, y_train = smt.fit_sample(X, y)

    # print(type(X_train), type(y_train))
    # print(y_train.shape)
    # print(X_train.shape)
    newData = pd.concat([X_train, y_train], axis=1)
    newData.to_csv(f"results/{repo}/{repo}TrainDataRebalanced.csv", index=False)

    print(f"{repo} Train data is resampled...")

def combineTrainsTests(repo):

    testData = open(f'results/TestData.csv', 'a')
    testDataWriter = csv.writer(testData)

    repoTestData = open(f'results/{repo}/{repo}TestData.csv', encoding="ISO-8859-1")
    repoTestDataReader = csv.reader(repoTestData, delimiter=',')

    next(repoTestDataReader, None)

    for row in repoTestDataReader:
        writeToFile = [row[2], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14]]
        testDataWriter.writerow(writeToFile)

    testData.close()

    trainData = open(f'results/TrainData.csv', 'a')
    trainDataWriter = csv.writer(trainData)

    repoTrainData = open(f'results/{repo}/{repo}TrainDataRebalanced.csv', encoding="ISO-8859-1")
    repoTrainDataReader = csv.reader(repoTrainData, delimiter=',')

    next(repoTrainDataReader, None)

    for row in repoTrainDataReader:
        trainDataWriter.writerow(row)

    trainData.close()

    print(f"{repo} data is added to the whole data")

def randomForest():
    trainData = pd.read_csv('results/TrainData.csv', low_memory=False)
    testData = pd.read_csv('results/TestData.csv', low_memory=False)

    feature_names = [#"release", "addedLOC", "deletedLOC",
                     "churnLOC", "entropy","changeAge", "changedFiles",
                     "contributors", "developerExp", "maxPreviousBug"
                                                     ''', "maxPreviousCrossLangBug"'''
    ]

    y_train = trainData["crossLang"]
    X_train = trainData.drop(["release","crossLang", "addedLOC","deletedLOC","maxPreviousCrossLangBug"], axis=1)

    y_test = testData["crossLang"]
    X_test = testData.drop(["release","crossLang", "addedLOC","deletedLOC","maxPreviousCrossLangBug"], axis=1)

    # print(X_test.head())
    # print(y_test.head())
    #
    # print(X_test.columns.values)
    # print(y_test.columns.values)
    clf = RandomForestClassifier(n_estimators=433, criterion="gini")
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
    #
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))
    #
    feature_imp = pd.Series(clf.feature_importances_, index=feature_names).sort_values(ascending=False)
    print(feature_imp)

def main():

    # repositories = ["omim", "react-native", "libgdx", "openj9", "rocksdb", "realm-java", "jmonkeyengine", "arrow",
    #                 # "conscrypt",
    #                 "jna"]
    # #
    # for repo in repositories:
    #     separateTestTrain(repo)
    #     resampling(repo)
    #     combineTrainsTests(repo)
    #
    #
    # testData = open(f'results/TestData.csv', 'w')
    # testDataWriter = csv.writer(testData)
    # testDataWriter.writerow(
    #     ["release", "addedLOC", "deletedLOC", "churnLOC", "entropy",
    #      "changeAge", "changedFiles",
    #      "contributors", "developerExp", "maxPreviousBug", "maxPreviousCrossLangBug", "crossLang"])
    #
    # trainData = open(f'results/TrainData.csv', 'w')
    # trainDataWriter = csv.writer(trainData)
    # trainDataWriter.writerow(
    #     ["release", "addedLOC", "deletedLOC", "churnLOC", "entropy",
    #      "changeAge", "changedFiles",
    #      "contributors", "developerExp", "maxPreviousBug", "maxPreviousCrossLangBug", "crossLang"])
    #
    # for repo in repositories:
    #     combineTrainsTests(repo)

    # /////////////////////
    # separateTestTrain("conscrypt")
    # resampling("conscrypt")
    # combineTrainsTests("conscrypt")

    randomForest()

    print("everything is done")

if __name__ == '__main__':
    main()