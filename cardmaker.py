import csv


with open('sample_questions.csv') as questionFile:
    questions = csv.reader(questionFile, delimiter=',')

    with open('sample_answers.csv',encoding="utf8") as answerFile:
        answers = csv.reader(answerFile, delimiter=',')
        for question in questions:
            q_a = []

            q_a.append("=HYPERLINK(\"https://stackoverflow.com/questions/"+str(question[2])+"\")")
            print(question[2])
            answerFile.seek(0)
            for answer in answers:
                if question[2] == answer[1]:
                    q_a.append("=HYPERLINK(\"https://stackoverflow.com/questions/"+str(answer[2])+"\")")
            print(q_a)
            with open('LinksSample_post_500.csv', 'a') as csvOut:
                writer = csv.writer(csvOut)
                writer.writerow(q_a)
            csvOut.close()