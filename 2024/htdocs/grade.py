from csv2html import id2item2score

hws = [f'hw{i+1}' for i in range(6)]
mids = [f'mid{i+1}' for i in range(2)]

hws_ratio = 0.25
mid1_ratio = 0.25
mid2_ratio = 0.25
final_ratio = 0.25


def get_dist(dist_from_other_class, nb_all_students, nb_of_no_show_in_exam, nb_of_withdrawed):

    # drop the end of the distribution to align our failed percentage
    nb_failed = nb_of_no_show_in_exam + nb_of_withdrawed
    failed_percentage = nb_failed / nb_all_students
    nb_to_be_removed = round(sum(dist_from_other_class) * failed_percentage)
    nb_now_removed = 0
    for i in range(len(dist_from_other_class)-1, -1, -1):
        removed_this_iter = min(
            dist_from_other_class[i], nb_to_be_removed-nb_now_removed)
        dist_from_other_class[i] -= removed_this_iter
        nb_now_removed += removed_this_iter

        if nb_now_removed == nb_to_be_removed:
            break

    # determine the distribution of student who passed
    total = sum(dist_from_other_class)
    new_dist = [int(count / total * (nb_all_students - nb_failed))
                for count in dist_from_other_class]

    residual = [(count / total * (nb_all_students - nb_failed) % 1)
                for count in dist_from_other_class]
    argsort_residual = sorted(range(len(residual)), key=residual.__getitem__)[::-1]
    nb_to_filled = nb_all_students - nb_failed - sum(new_dist)
    for idx in argsort_residual[:nb_to_filled]:
        new_dist[idx] += 1
    new_dist[-2] += nb_of_no_show_in_exam
    new_dist[-1] += nb_of_withdrawed

    return new_dist


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


# compute the average of each student
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

# determine distribution
gpa = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'F', 'withdraw']
dist_from_other_class = [26, 26, 6, 16, 19, 4, 4, 5, 6, 2, 8]
all_students = 102
nb_of_withdrawed = 13
nb_of_no_show_in_exam = len(id_avgs_without_exam_score)
dist = get_dist(dist_from_other_class, all_students,
                nb_of_no_show_in_exam, nb_of_withdrawed)
print(dist)
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
