from sheets_utils import *
from enum import Enum
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

class State(Enum):
    start = 0
    group_is_chosen = 2
    subject_is_chosen = 3
    type_is_chosen = 4
    sheet_is_chosen = 5
    roll_call = 6
    marks = 7
    edit = 8
    end = 9
    set_default = 10
    add_lesson = 11
    add_students = 12
    add_one_student = 13
    delete_one_student = 14
    change_one_student = 15
    delete_subject = 16
    change_subject_info = 17
    show_marks = 18
    edit_marks = 19
    edit_mark = 20


class GoogleSheetsShort:

    def change_filename(self,filename):
        self.main_file_name = filename
        self.clear_all()

    def create_file_by_name(self, filename):
        sh = self.__client.create(filename)

        ans = self.drive_service.files().update(fileId=sh.id,
                                                addParents=self.folder_id,
                                                fields='id').execute()
        return sh

    def create_file(self):
            sh = self.create_file_by_name(self.main_file_name)
            worksheet = sh.get_worksheet(0)
            set_value(worksheet, 1, 1, "Група")
            set_value(worksheet, 1, 2, "Предмет")
            set_value(worksheet, 1, 3, "Тип")

    def _batch(self, requests, sheetId):
        body = {
            'requests': requests
        }
        return self.drive_service.spreadsheets().batchUpdate(spreadsheetId=sheetId, body=body).execute()

    def rename_sheet(self, sheetId, newName):
        return self._batch({
            "updateSheetProperties": {
                "properties": {
                    "sheetId": sheetId,
                    "title": newName,
                },
                "fields": "title",
                "sheetId": sheetId,
            }
        },sheetId = sheetId )

    def rename(self, number, name):
        filename = create_file_name(self.group, self.subject, self.type_)
        sh = self.__client.open(filename)
        sheetId = sh.id
        new_name = ""
        if number == 0:
            new_name = create_file_name(name, self.subject, self.type_)
        elif number == 1:
            new_name = create_file_name(self.group, name, self.type_)
        else:
            new_name = create_file_name(self.group, self.subject, name)
        self.rename_sheet(sheetId=sheetId,newName=new_name)
        sh = self.__client.open(self.main_file_name)
        worksheet = sh.get_worksheet(0)
        groups = worksheet.col_values(1)
        subjects = worksheet.col_values(2)
        types = worksheet.col_values(3)
        n = get_unique(groups, subjects, types, self.group, self.subject, self.type_)
        worksheet.update_cell(n, number + 2, name)
        try:

            pass
        except:
            return "Не вийшло("

    def add_subgroup(self):
        filename = create_file_name(self.group, self.subject, self.type_)
        sh = self.__client.open(filename)
        num_worksheets = len(sh.worksheets()) + 1
        worksheet = sh.add_worksheet(title="Підгрупа " + str(num_worksheets),  rows="100", cols="50")
        set_value(worksheet, 1, 1, "Прізвище")
        self.sheet = worksheet
        return num_worksheets

    def add_lesson(self):
        sh = self.__client.open(self.main_file_name)
        worksheet = sh.get_worksheet(0)
        num = len(worksheet.col_values(1)) + 1
        set_value(worksheet, num, 1, self.group)
        set_value(worksheet, num, 2, self.subject)
        set_value(worksheet, num, 3, self.type_)

    def create_sheet(self):
        filename = create_file_name(self.group, self.subject, self.type_)
        sh = self.create_file_by_name(filename)
        worksheet_to_del = sh.get_worksheet(0)
        worksheet = sh.add_worksheet(title="Підгрупа 1", rows="100", cols="50")
        sh.del_worksheet(worksheet_to_del)
        set_value(worksheet, 1, 1, "Прізвище")
        self.sheet = worksheet

    def delete_worksheet(self):
            filename = create_file_name(self.group, self.subject, self.type_)
            sh = self.__client.open(filename)
            worksheet_list = sh.worksheets()
            if len(worksheet_list) == 1:
                self.drive_service.files().delete(fileId=sh.id).execute()
                sh = self.__client.open(self.main_file_name)
                worksheet = sh.get_worksheet(0)
                cell1 = worksheet.findall(self.group)
                cell1.extend(worksheet.findall(self.subject))
                cell1.extend(worksheet.findall(self.type_))
                cells = []

                for cell in cell1:
                    cells.append(cell.row)
                row_num = most_frequent(cells)
                worksheet.delete_row(row_num)
            else:
                sh.del_worksheet(self.sheet)

    def __init__(self, client, drive_service, folder_id, exists):
        self.main_file_name = "MainFile"
        self.__client = client
        self.folder_id = folder_id
        self.drive_service = drive_service
        if not exists:
            self.create_file()

        self.questions_dict = {}
        self.question = None
        self.error_message = None
        self.group_info = None
        self.group = None
        self.subject_info = None
        self.subject = None
        self.type_ = None
        self.sheet = None
        self.sheets = None
        self.students_info = None
        self.student_num = None
        self.state = State.start
        self.full_files = None
        self.bot_state = ""

    def clear_all(self):
        self.questions_dict = {}
        self.question = None
        self.error_message = None
        self.full_files = None
        self.main_file_name = "MainFile"
        try:
            sheet = self.__client.open(self.main_file_name).sheet1
            groups = sheet.col_values(1)[1:]
            subjects = sheet.col_values(2)[1:]
            types = sheet.col_values(3)[1:]
            if len(groups) == 0 or len(subjects) == 0 or len(types) == 0:
                self.error_message = "Ваш файл не відповідає потрібному формату"
                return
        except:
            self.error_message = "Ваш файл не відповідає потрібному формату"
            return
        self.full_files = create_dict(groups, subjects, types)
        self.state = State.start
        self.group_info = None
        self.group = None
        self.subject_info = None
        self.subject = None
        self.type_ = None
        self.sheet = None
        self.sheets = None
        self.students_info = None
        self.student_num = None

    def next_step(self):
        self.questions_dict.clear()
        self.error_message = None
        self.question = 'Зроблено!'
        print(self.state)
        if self.state == State.start:
            self.clear_all()
            if self.full_files is None:
                self.error_message = "Додайте пари для роботи"
                return "Додайте пари для роботи"
            if len(self.full_files) > 1:
                self.question = 'Група'
                choose_one_from_dict(self, self.full_files)
            else:
                self.update(answer=0)

        elif self.state == State.group_is_chosen:
            if len(self.group_info) > 1:
                self.question = 'Предмет'
                choose_one_from_dict(self, self.group_info)
            else:
                self.update(answer=0)

        elif self.state == State.subject_is_chosen:
            if len(self.subject_info) > 1:
                self.question = 'Тип'
                choose_one_from_array(self, self.subject_info)
            else:
                self.update(answer=0)

        elif self.state == State.type_is_chosen:
            file_name = create_file_name(self.group, self.subject, self.type_)
            file = self.__client.open(file_name)
            self.sheets = file.worksheets()
            if len(self.sheets) == 1:
                self.sheet = file.sheet1
                self.state = State.sheet_is_chosen
                self.next_step()
            else:
                sheets_tittles = []
                for sheet in self.sheets:
                    sheets_tittles.append(sheet.title)
                self.question = 'Підгрупа'
                choose_one_from_array(self, sheets_tittles)
        elif self.state == State.delete_subject:
            self.delete_worksheet()
            self.clear_all()
        elif self.state == State.sheet_is_chosen:
            self.student_num = 0
            self.state = State.end
            # self.set_students_info()
            # num = len(self.students_info)
            # # print(num)
            # if num == 0:
            #     self.error_message = "В групі немає жодного студента!"
            #     return "В групі немає жодного студента!"

        elif self.state == State.add_lesson:
            self.group = None
            self.subject = None
            self.type_ = None
            sheet = self.__client.open(self.main_file_name).sheet1
            groups = sheet.col_values(1)[1:]
            current_groups = {}
            n = 1
            for group in groups:
                current_groups[group] = str(n)
                n = n + 1
            self.questions_dict = current_groups
            return current_groups

        elif self.state == State.add_students:
            pass
        elif self.state == State.add_one_student:
            pass
        elif self.state == State.roll_call:

            if self.student_num == 0:
                self.set_students_info()
                if len(self.students_info) == 0:
                    self.error_message = "В групі немає жодного студента!"
                    return "В групі немає жодного студента!"
            roll_call(self, self.students_info[self.student_num])
        elif self.state == State.show_marks:
            self.question = "Оберіть"
            students = get_students(self.sheet)
            dict_students = {}
            for i in range(0, len(students)):
                dict_students[students[i]] = str(i)
            self.questions_dict = dict_students

        elif self.state == State.edit_marks:
            self.question = "Оберіть"
            students = get_students(self.sheet)
            dict_students = {}
            for i in range(0, len(students)):
                dict_students[students[i]] = str(i)
            self.questions_dict = dict_students

        elif self.state == State.edit:
            edit(self, self.students_info)

        elif self.state == State.delete_one_student:
            action_one_student(self, get_students(self.sheet), "видалити")

        elif self.state == State.change_one_student:
            # self.set_students_info()
            action_one_student(self, get_students(self.sheet), "редагувати")

        elif self.state == State.marks:
            if self.student_num == 0:
                self.set_students_info()
                if len(self.students_info) == 0:
                    self.error_message = "В групі немає жодного студента!"
            set_mark(self,self.students_info[self.student_num])

        elif self.state == State.set_default:
            self.set_students_info()
            set_default(self)

    def set_students_info(self):
        self.students_info = set_values(self.sheet)
        self.student_num = 0

    def update(self, answer):
        if self.state == State.start:
            self.group, self.group_info = get_one_from_dict(self.full_files, answer)
            self.state = State.group_is_chosen
            self.next_step()

        elif self.state == State.group_is_chosen:
            self.subject, self.subject_info = get_one_from_dict(self.group_info, answer)
            self.state = State.subject_is_chosen
            self.next_step()

        elif self.state == State.subject_is_chosen:
            self.type_ = get_one_from_array(self.subject_info, answer)
            self.state = State.type_is_chosen
            self.next_step()

        elif self.state == State.type_is_chosen:

            self.sheet = self.sheets[answer]
            self.state = State.sheet_is_chosen
            self.next_step()

        elif self.state == State.sheet_is_chosen:
            self.state = State.end
            # self.set_students_info()
            # num = len(self.students_info)
            # if num == 0:
            #     self.error_message = "В групі немає жодного студента!"
            #     return "В групі немає жодного студента!"

        elif self.state == State.add_lesson:
            if self.group is None:
                self.group = answer
                current_lessons = {}
                sheet = self.__client.open(self.main_file_name).sheet1
                lessons = sheet.col_values(2)[1:]
                n = 1
                for lesson in lessons:
                    current_lessons[lesson] = str(n)
                    n = n + 1
                self.questions_dict = current_lessons
                return "предмет", current_lessons
            elif self.subject is None:
                self.subject = answer
                return "тип", None
            else:
                self.type_ = answer
                self.add_lesson()
                self.state = State.end
                self.create_sheet()
                return self.group, self.subject, self.type_

        elif self.state == State.add_students:
            add_item(self.sheet, answer)

        elif self.state == State.add_one_student:
            add_item(self.sheet, answer)
            self.state = State.end

        elif self.state == State.change_one_student:
            set_value(self.sheet, self.student_num+2, 1, answer)
            self.state = State.end
            self.student_num = 0

        elif self.state == State.delete_one_student:
            delete_one_line(self.sheet, answer+2)
            self.state = State.end
            self.student_num = 0

        elif self.state == State.roll_call:
            set_value(self.sheet, self.students_info[self.student_num][1],
                      self.students_info[self.student_num][2], answer)
            self.student_num = self.student_num + 1
            if self.student_num >= len(self.students_info):
                self.state = State.end
                self.student_num = 0
            self.next_step()

        elif self.state == State.edit:
            set_value(self.sheet, self.students_info[self.student_num][1],
                      self.students_info[self.student_num][2], answer)
            self.state = State.end
            self.student_num = 0
            self.next_step()

        elif self.state == State.marks:

            set_value(self.sheet, self.students_info[self.student_num][1],
                      self.students_info[self.student_num][2], answer)
            self.student_num = self.student_num + 1
            if self.student_num >= len(self.students_info):
                self.state = State.end
                self.student_num = 0
            self.next_step()

        elif self.state == State.set_default:

            num = len(self.students_info)
            for i in range(num):
                set_value(self.sheet, self.students_info[i][1],
                          self.students_info[i][2], answer)
            self.student_num = 0
            self.state = State.end
        elif self.state == State.show_marks:
            marks = get_marks(self.sheet, answer+1)
            return marks

        elif self.state == State.edit_marks:
            marks = get_marks(self.sheet, answer + 1)
            return marks
            # self.next_step()

        elif self.state == State.edit_mark:
            # item = self.question
            # row, column = find_item(self.sheet, item)
            set_value(self.sheet, self.student_num+2, self.question, answer)

        elif self.state == State.change_subject_info:
            if self.question == "Група":
                new_subjects = self.full_files.get(answer,None)
                if new_subjects is None:
                    result = self.rename(0, answer)
                else:
                    new_subjects = new_subjects.get(self.subject,None)
                    if new_subjects is None:
                        result = self.rename(0, answer)
                    else:
                        new_subjects = new_subjects.get(self.type_,None)
                        if new_subjects is None:
                            result = self.rename(0, answer)
                        else:
                            return "Вибачте, такий предмет вже існує."

            elif self.question == "Предмет":
                new_subjects = self.full_files.get(self.group, None)
                new_subjects = new_subjects.get(answer, None)
                if new_subjects is None:
                        result = self.rename(1, answer)
                else:
                    new_subjects = new_subjects.get(self.type_, None)
                    if new_subjects is None:
                         result = self.rename(1, answer)
                    else:
                        return "Вибачте, такий предмет вже існує."
            elif self.question == "Тип":
                new_subjects = self.full_files.get(self.group, None)
                new_subjects = new_subjects.get(self.subject, None)
                new_subjects = new_subjects[answer]
                if new_subjects is None:
                        result = self.rename(2, answer)

                else:
                        return "Вибачте, такий предмет вже існує."
            elif self.question == "Підгрупа":
                filename = create_file_name(self.group, self.subject, self.type_)
                sh = self.__client.open(filename)
                worksheet_list = sh.worksheets()
                if answer in worksheet_list:
                    return "Вибачте, така підгрупа вже існує."
                else:
                    self.sheet.duplicate( new_sheet_name = answer)
                    sh.del_worksheet(self.sheet)
            # if result is not None:
            #     return result


