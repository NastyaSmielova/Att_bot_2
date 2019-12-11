from bot_utils_buttons import *
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start_text(bot, update, user_data):
    # bot.sendMessage("Введіть групу, предмет та тип предмету (по черзі, в різних повідомленнях)/nГрупа:",
    #                 chat_id=update.message.chat_id)
    update.message.reply_text("Введіть /start, щоб розпочати роботу.")


def choose_group(bot, update, user_data):
    user = user_data['client']
    user.state = State.start
    error_text = user.next_step()

    if user.state == State.end:
        if error_text is not None:
            update.message.reply_text(error_text)
            reply_markup = create_reply_markup(DICT_FOR_GROUP_CHOSEN_RESTRICTED)
            update.message.reply_text(command, reply_markup=reply_markup)
        reply_markup = create_reply_markup(DICT_FOR_GROUP_CHOSEN_MAIN)
        update.message.reply_text(command, reply_markup=reply_markup)
        user.bot_state = GROUP_CHOSEN_FIRST
        return GROUP_CHOSEN_FIRST

    if error_text is not None:
        update.message.reply_text(error_text)
        reply_markup = create_reply_markup(DICT_FOR_REGISTERED)
        update.message.reply_text(command, reply_markup=reply_markup)
        return
    reply_markup = create_reply_markup(user.questions_dict)
    update.message.reply_text(user.question, reply_markup=reply_markup)
    user.bot_state = CHOOSE_GROUP
    return CHOOSE_GROUP
    # if user.state == State.end:
    #     update.message.reply_text(TEXT_FOR_GROUP)
    #     return GROUP_CHOSEN


def get_marks(bot, update, user_data):
    user = user_data['client']
    answer = update.message.text
    user.update(answer)
    user.next_step()

    update.message.reply_text(user.question)
    if user.state == State.end:
        reply_markup = create_reply_markup(DICT_FOR_HAVE_MARKS)
        update.message.reply_text(command, reply_markup=reply_markup)
        user.bot_state = HAVE_MARKS
        return HAVE_MARKS


def show_list(bot, update, user_data):
    user = user_data['client']

    date, marks = get_last_column(user.sheet)
    reply_text = create_file_name(user.group, user.subject, user.type_) + "  " + date + ":\n"
    for student, mark in marks:
        reply_text += student + " " + str(mark) + "\n"
    update.message.reply_text(reply_text)
    reply_markup = create_reply_markup(DICT_FOR_HAVE_MARKS)
    update.message.reply_text(command, reply_markup=reply_markup)


def get_one_surname(bot, update, user_data):
    user = user_data['client']
    answer = update.message.text
    user.update(answer)
    reply_markup = create_reply_markup(DICT_FOR_EDIT_STUDENTS)
    update.message.reply_text(command, reply_markup=reply_markup)
    user.bot_state = EDIT_STUDENTS
    return EDIT_STUDENTS


def back_to_group(bot, update, user_data):
    user = user_data['client']
    reply_markup = create_reply_markup(DICT_FOR_GROUP_CHOSEN_MAIN)
    update.message.reply_text(command, reply_markup=reply_markup)
    user.bot_state = GROUP_CHOSEN_FIRST
    return GROUP_CHOSEN_FIRST


def back_to_edit_students(bot, update, user_data):
    user = user_data['client']
    reply_markup = create_reply_markup(DICT_FOR_EDIT_STUDENTS)
    update.message.reply_text(command, reply_markup=reply_markup)
    user.bot_state = EDIT_STUDENTS
    return EDIT_STUDENTS




def back_to_registered(bot, update, user_data):
    user = user_data['client']
    user.clear_all()
    reply_markup = create_reply_markup(DICT_FOR_REGISTERED)
    update.message.reply_text(command, reply_markup=reply_markup)
    user.bot_state = REGISTERED

    return REGISTERED


def change_file_name(bot, update):
    update.message.reply_text("Введіть нову назву файла. Довжина не більше 50 символів")

