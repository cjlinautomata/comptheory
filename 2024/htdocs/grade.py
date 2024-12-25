from csv2html import id2item2score
import numpy as np

hws = [f'hw{i+1}' for i in range(6)]
mids = [f'mid{i+1}' for i in range(2)]

hws_ratio = 0.1
mid1_ratio = 0.3
mid2_ratio = 0.3
final_ratio = 0.3

def cal_GPA(dist):
    GPA_list = [4.3, 4.0, 3.7, 3.3, 3.0, 2.7, 2.3, 2.0, 1.7, 0, 0]
    GPA = 0
    for idx in range(len(dist)-1):
        GPA += GPA_list[idx] * dist[idx]
    return GPA / sum(dist[:-1])


def get_avg(item2score):
    avg = 0.0
    for item, score in item2score.items():
        if item != 'grade' and score != '':
            score = float(score)
            if 'hw' in item:
                avg += score / 6 * hws_ratio
            elif 'mid1' in item:
                avg += score * mid1_ratio
            elif 'mid2' in item:
                avg += score * mid2_ratio
            elif 'final' in item:
                avg += score * final_ratio
    return avg

# Compute the average of each student
id_avgs = []
id_avgs_without_exam_score = []
for id_, item2score in id2item2score.items():
    keys = item2score.keys()
    if 'mid1' in keys and 'mid2' in keys and 'final' in keys:
        id_avgs.append((id_, get_avg(item2score)))
    else:
        id_avgs_without_exam_score.append((id_, get_avg(item2score)))
id_avgs.sort(key=lambda x: x[1], reverse=True)
id_avgs_without_exam_score.sort(key=lambda x: x[1], reverse=True)
id_avgs += id_avgs_without_exam_score

# Determine distribution
gpa = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'F', 'withdraw']

all_students = 111
nb_of_withdrawed = 5+1
nb_of_no_show_in_exam = len(id_avgs_without_exam_score)

dist = [20, 23, 17, 16, 10, 4, 7, 4, 1, 3, 6]
print("Distributions:", dist, "Number of students:", sum(dist))
print("Avg GPA:", cal_GPA(dist))

with open('scores_avg.csv', 'w') as f:
    print('SID,Total Score', file=f)
    for id, avg in id_avgs:
        print(f'{id},{round(avg, 2)}', file=f)

with open('scores_grade.csv', 'w') as f:
    print('SID,Total Score', file=f)

    ids = iter(id_avg[0] for id_avg in id_avgs)
    for num, grade in zip(dist[:-1], gpa[:-1]):
        for i in range(num):
            print(f'{next(ids)},{grade}', file=f)
