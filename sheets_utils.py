import datetime


def roll_call(client, student_info):
    client.questions_dict.clear()
    client.questions_dict['присутній'] = '1'
    client.questions_dict['відстній'] = '0'
    client.question = student_info[0]


def add_item(worksheet, answer):
    num = len(worksheet.col_values(1)) + 1
    set_value(worksheet, num, 1, answer)


def edit(client, students_info):
    client.questions_dict.clear()
    num = len(students_info)
    client.question = "Оберіть кого редагувати"
    for i in range(num):
        client.questions_dict[students_info[i][0]] = i


def action_one_student(client, students_info, action):
    client.questions_dict.clear()
    num = len(students_info)
    client.question = "Оберіть кого " + action
    for i in range(num):
        client.questions_dict[students_info[i]] = i


def set_default(client):
    client.question = "Введіть бал для всіх: "


def set_mark(client, student_info):
    client.question = "Введіть бал для: " + student_info[0]


def create_file_name(group, subject, type_):
    name = group + '. ' + subject + '. ' + type_ + '.'
    return name


def create_dict(groups, subjects, types):
    num = len(groups)
    full_files = {}
    for i in range(num):
        group = groups[i]
        subject = subjects[i]
        type_ = types[i]
        if group not in full_files:
            full_files[group] = {subject: [type_]}
        else:
            dict_subjects = full_files[group]
            if subject not in dict_subjects:
                dict_subjects[subject] = [type_]
                full_files[group] = dict_subjects
            else:
                dict_types = full_files[group][subject]
                dict_types.append(type_)

    return full_files


def choose_one_from_dict(user, full_dict):
    user.questions_dict.clear()
    dict_short = list(full_dict.keys())
    num = len(dict_short)
    for i in range(num):
        user.questions_dict[dict_short[i]] = str(i)


def get_one_from_dict(full_dict, id_dict):
    dict_short = list(full_dict.keys())
    return dict_short[id_dict], full_dict[dict_short[id_dict]]


def choose_one_from_array(user, full_array):
    user.questions_dict.clear()
    num = len(full_array)

    for i in range(num):
        user.questions_dict[full_array[i]] = str(i)


def get_one_from_array(full_array, id_arr):
    return full_array[id_arr]


def most_frequent(arr):
    return max(set(arr), key=arr.count)


def get_unique(first, second, third, f,s,t):
    n = len(first)
    for i in range(1, n+1):
        if first[i] == f and second[i] == s and third[i] == t:
            return i
    return None


def get_students(sheet):
    students = sheet.col_values(1)
    students = students[1:]
    return students


def get_last_column(sheet):
    students = get_students(sheet)
    dates = sheet.row_values(1)
    update_date = len(dates)
    date = dates[update_date - 1]
    marks = []
    for i in range(len(students)):
        marks.append([students[i], sheet.cell(i + 2, update_date).value])
    return date, marks


def get_marks(sheet,line):
    dates = sheet.row_values(1)[1:]
    marks = sheet.row_values(line)[1:]
    n = len(dates)
    marks_with_dates = []
    for i in range(n):
        marks_with_dates.append([dates[i],marks[i]])
    return marks_with_dates

def delete_one_line(sheet, line):
    sheet.delete_row(line)


def set_values(sheet):
    students = get_students(sheet)
    now = datetime.datetime.now()
    dates = sheet.row_values(1)
    new_date = len(dates) + 1
    date = "%d.  %d / %d " % (new_date - 1, now.day, now.month)

    sheet.update_cell(1, new_date, date)
    students_info = []
    for i in range(len(students)):
        student = list()
        student.append(students[i])
        student.append(i+2)
        student.append(new_date)
        students_info.append(student)

    return students_info


def set_value(sheet, row, column, answer):
    sheet.update_cell(row, column, answer)


def find_item(sheet, item):
    cell = sheet.find(item)
    return cell.row, cell.column


def get_lessons_dates(sheet):
    list_of_titles = sheet.row_values[1:]
    return list_of_titles


def print_row_values(sheet):
    list_of_titles = sheet.row_values(1)
    print(list_of_titles)
