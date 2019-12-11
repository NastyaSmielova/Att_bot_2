import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
TIMEZONE = 'Europe/Kiev'
TIMEZONE_COMMON_NAME = 'Kiev'
CHOOSING, REGISTERED, GROUP_CHOSEN, HAVE_MARKS, ADD_LESSON, \
    STUDENT_CHOSEN, EDIT_GROUP, TYPE_FOR_LESSON, EDIT_STUDENTS, ROLL_CALL, \
    CHOOSE_GROUP, ONE_STUDENT, ONE_STUDENT_CHANGE, CREATE_LIST, GET_STUDENT, \
    CHANGE_SUBJECT_INFO, SHOW_FOR_ONE, GROUP_CHOSEN_FIRST, EDIT_FOR_ONE, CHANGE_MARK = range(20)

TEXT_FOR_GROUP = "/rollcall для переклички \n/setdefault для виставлення всім однієї оцінки" +\
                 "\n/setmarks  для виставлення оцінок\n/back для повернення назад "
TEXT_FOR_MARKS = "/back для повернення назад,\n/showlist для перегляду \n/edit для редагування"
TEXT_FOR_EDIT_GROUP = "/back для повернення назад,\n/addstudents для додання списку студентів," \
                      "\n/showstudents для перегляду списку студентів,\n/addsubgroup для додання підгрупи"
TEXT_FOR_REGISTERED = "/addlesson для додання пари,\n/choosegroup для вибору пари"
TEXT_FOR_EDIT_STUDENTS = "/add \n/delete\n/change\n/show\n/back"

open_book = "\U0001F4D6"
back = "\U0001F519"
pencil = "\U0000270F"
question_mark = "\U00002753"
plus = "\U00002795"
arrow = "\U000027A1"
cancel = "\U0000274C"
command = "Команда:"

DICT_FOR_GROUP_CHOSEN_MAIN = {
    question_mark + " " + "Виставлення оцінок": "0",
    pencil + " " + "Редагування": "1",
    cancel + "Видалення": "2",
    open_book + "Показати оцінки": "3",
    back + " " + "Назад": "4"}


DICT_FOR_GROUP_CHOSEN_EDIT = {pencil + " " + "Редагувати список студентів": "1",
                              pencil + " " + "Редагувати оцінки студента": "9",}

DICT_FOR_GROUP_CHOSEN_SET_MARKS = {question_mark + " " + "Перекличка": "0",
                                  question_mark + " " + "Виставити однакову оцінку": "3",
                                  question_mark + " " + "Виставлення оцінок": "4",}
DICT_FOR_GROUP_CHOSEN_DELETE = {cancel + "Видалити заняття": "5",}

DICT_FOR_GROUP_CHOSEN_SHOW = {open_book + "Показати оцінки студента": "8",}

DICT_FOR_GROUP_CHOSEN = {question_mark + " " + "Перекличка": "0",
                         question_mark + " " + "Виставити однакову оцінку": "3",
                         question_mark + " " + "Виставлення оцінок": "4",
                         pencil + " " + "Редагувати список студентів": "1",
                         # pencil + " " + "Редагувати оцінки": "2",
                         cancel + "Видалити заняття": "5",
                         #"Змінити назву заняття": "7",
                         open_book + "Показати оцінки студента": "8",
                         pencil + " " + "Редагувати оцінки студента": "9",
                         back + " " + "Назад": "6"}

DICT_FOR_GROUP_CHOSEN_RESTRICTED = {pencil + " " + "Редагувати список студентів": "1",
                                    cancel + "Видалити заняття": "5",
                                    back + " " + "Назад": "6"}

DICT_FOR_EDIT_GROUP = {plus + " " + "Додати студентів": "0", plus + " " + "Додати підгрупу": "2",
                       open_book + " " + "Переглянути список": "1",back + " " + "Назад": "3"}

DICT_FOR_HAVE_MARKS = {pencil + " " + "Редагувати": "0",
                       open_book + " " + "Переглянути": "1",
                       back + " " + "Назад": "2"}

DICT_FOR_REGISTERED = {plus + " " + "Додати заняття": "0", arrow + " " + "Вибрати заняття": "1"}

DICT_FOR_EDIT_STUDENTS = {plus + " " + "Додати": "0",
                          pencil + " " + "Змінити": "2",
                          open_book + " " + "Переглянути": "3",
                          cancel + "Видалити": "1",
                          back + " " + "Назад": "4"}

DICT_FOR_CHANGE_SUBJECT_INFO = {"Група": "0",  "Предмет": "1", "Тип": "2",
                                "Підгрупа": "3", "Назад": "4"}