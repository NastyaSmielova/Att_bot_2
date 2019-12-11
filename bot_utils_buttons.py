from constants import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Message
from googlesheets import *


def link_button(bot, update, user_data):
    query = update.callback_query
    pass


def delete_student_button(bot, update, user_data):
    query = update.callback_query
    answer = int(query.data)

    user = user_data['client']
    user.student_num = answer
    user.update(answer)
    reply_text = "{}: {} \n".format(user.question, get_key(user.questions_dict, answer))
    user.questions_dict.clear()
    user.question = ""

    bot.edit_message_text(text=reply_text,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)
    reply_markup = create_reply_markup(DICT_FOR_EDIT_STUDENTS)
    bot.sendMessage(text=command,reply_markup=reply_markup, chat_id=query.message.chat_id)
    user.bot_state = EDIT_GROUP
    return EDIT_STUDENTS


def change_student_button(bot, update, user_data):
    query = update.callback_query
    answer = int(query.data)

    user = user_data['client']
    user.student_num = answer
    reply_text = "{}: {} \n".format(user.question, get_key(user.questions_dict, answer))
    user.questions_dict.clear()
    user.question = ""

    bot.edit_message_text(text=reply_text,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)

    bot.sendMessage(text="Введіть новий ПІБ", chat_id=query.message.chat_id)
    user.bot_state = ONE_STUDENT
    return ONE_STUDENT


def group_button(bot, update, user_data):
    query = update.callback_query
    answer = query.data

    user = user_data['client']

    reply_text = "{}: {} \n".format(user.question, get_key(user.questions_dict, answer))
    user.questions_dict.clear()
    user.question = ""
    user.update(int(answer))
    reply_markup = create_reply_markup(user.questions_dict)
    bot.edit_message_text(text=reply_text,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)

    bot.sendMessage(text=user.question, chat_id=query.message.chat_id, reply_markup=reply_markup)

    if user.state == State.end:
        reply_markup = create_reply_markup(DICT_FOR_GROUP_CHOSEN_MAIN)
        bot.sendMessage(text=command, chat_id=query.message.chat_id, reply_markup=reply_markup)
        user.bot_state = GROUP_CHOSEN_FIRST
        return GROUP_CHOSEN_FIRST


def get_key(question_dict, answer):
    for key, value in question_dict.items():
        if value == answer:
            return key
    return "something strange"


def create_reply_markup(question_dict):
    keyboard = []
    for key, value in question_dict.items():
        keyboard.append([InlineKeyboardButton(key, callback_data=value)])

    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


def universal_button(bot, update, user_data):
    query = update.callback_query
    answer = query.data

    user = user_data['client']

    reply_text = "{}: {} \n".format(user.question, get_key(user.questions_dict, answer))
    user.questions_dict.clear()
    user.question = ""
    user.update(int(answer))
    reply_markup = create_reply_markup(user.questions_dict)
    bot.edit_message_text(text=reply_text,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)

    bot.sendMessage(text=user.question, chat_id=query.message.chat_id, reply_markup=reply_markup)

def rollcall_button(bot, update, user_data):

    query = update.callback_query
    answer = query.data

    user = user_data['client']

    reply_text = "{}: {} \n".format(user.question, get_key(user.questions_dict, answer))
    user.questions_dict.clear()
    user.question = ""
    user.update(int(answer))
    reply_markup = create_reply_markup(user.questions_dict)
    bot.edit_message_text(text=reply_text,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)

    bot.sendMessage(text=user.question, chat_id=query.message.chat_id, reply_markup=reply_markup)

    if user.state == State.end:
        reply_markup = create_reply_markup(DICT_FOR_HAVE_MARKS)
        bot.sendMessage(text=command, reply_markup =reply_markup, chat_id=query.message.chat_id)
        user.bot_state = HAVE_MARKS
        return HAVE_MARKS


def set_command_REGISTERED_button(bot, update, user_data):
    query = update.callback_query
    answer = query.data
    chat_id = query.message.chat_id
    user = user_data['client']
    reply_text = "{}: {} \n".format(command, get_key(DICT_FOR_REGISTERED, answer))
    user.questions_dict.clear()
    user.question = ""
    bot.edit_message_text(text=reply_text,
                          chat_id=chat_id,
                          message_id=query.message.message_id)
    if answer == '0':
        user = user_data['client']
        user.state = State.add_lesson
        current_groups = user.next_step()
        if current_groups is not None and current_groups:
            reply_markup = create_reply_markup(current_groups)
            bot.sendMessage(text="Оберіть групу з наявних: ", reply_markup=reply_markup,chat_id=chat_id)
            bot.sendMessage(text="Або введіть назву групи: ",chat_id=chat_id,)
        else:
            bot.sendMessage(text="Введіть назву групи: ",chat_id=chat_id,)

        user.bot_state = ADD_LESSON
        return ADD_LESSON
    elif answer == '1':
        user = user_data['client']
        user.state = State.start
        user.next_step()
        if user.state == State.end:
            if user.error_message is not None:
                bot.sendMessage(text=user.error_message, chat_id=chat_id)
                reply_markup = create_reply_markup(DICT_FOR_GROUP_CHOSEN_MAIN)
                bot.sendMessage(text=command, reply_markup=reply_markup, chat_id=chat_id)
                user.bot_state = GROUP_CHOSEN_FIRST
                return GROUP_CHOSEN_FIRST
            reply_markup = create_reply_markup(DICT_FOR_GROUP_CHOSEN_MAIN)
            bot.sendMessage(text=command, reply_markup=reply_markup, chat_id=chat_id)
            user.bot_state = GROUP_CHOSEN_FIRST
            return GROUP_CHOSEN_FIRST

        if user.error_message is not None:
            bot.sendMessage(text=user.error_message , chat_id=chat_id)
            reply_markup = create_reply_markup(DICT_FOR_REGISTERED)
            bot.sendMessage(text=command, reply_markup=reply_markup, chat_id=chat_id)
            return
        reply_markup = create_reply_markup(user.questions_dict)
        bot.sendMessage(text = user.question, reply_markup=reply_markup, chat_id=chat_id)
        user.bot_state = GROUP_CHOSEN_FIRST
        return CHOOSE_GROUP





