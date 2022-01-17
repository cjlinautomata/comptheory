from csv2html import id2item2score

hws = [f'hw{i+1}' for i in range(7)]
mids = [f'mid{i+1}' for i in range(2)]

hws_ratio = 0.25
mids_ratio = 0.48
final_ratio = 0.27

gpa  = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'F']
dist = [  7, 10, 9, 8, 8, 7, 5, 6, 3, 8]

def get_avg(item2score):
    avg = 0.0
    for item, score in item2score.items():
        if item != 'grade' and score != '':
            score = float(score)
            if 'hw' in item:
                avg += score / 6.5 * hws_ratio
            elif 'mid' in item:
                avg += score / 2 * mids_ratio
            elif 'final' in item :
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
