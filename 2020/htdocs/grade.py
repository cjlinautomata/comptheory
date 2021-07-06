import csv
from csv2html import id2item2score

hws = [f'hw{i+1}' for i in range(7)]
mids = [f'mid{i+1}' for i in range(2)]

hws_ratio = 0.28
mids_ratio = 0.52
final_ratio = 0.2

gpa  = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'F']
dist = [  5,  18,    6,    2,   4,    5,    5,   6,   10,   3]

def get_avg(item2score):
    avg = 0.0
    for item, score in item2score.items():
        if item != 'grade' and score != '':
            score = float(score)
            if item in hws:
                avg += score / 7.5 * hws_ratio
            elif item in mids:
                avg += score / 2 * mids_ratio
            elif item == 'final':
                avg += score * final_ratio
    return avg

id_avgs = []
for id_, item2score in id2item2score.items():
    id_avgs.append((id_, get_avg(item2score)))
id_avgs.sort(key=lambda x: x[1], reverse=True)

with open('scores_avg.csv', 'w') as f:
    print('SID,Total Score', file=f)
    for id, avg in id_avgs:
        print(f'{id},{round(avg, 2)}', file=f)

with open('scores_grade.csv', 'w') as f:
    print('SID,Total Score', file=f)

    ids = iter(id_avg[0] for id_avg in id_avgs)
    for num, grade in zip(dist, gpa):
        for i in range(num):
            print(f'{next(ids)},{grade}', file=f)
