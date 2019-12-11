from bot_unnes import *


def choose_one_student(bot, update, user_data):
    query = update.callback_query
    answer = query.data

    user = user_data['client']
    # answer = int(answer)
    reply_text = "{}: {} \n".format("Оцінки для", get_key(user.questions_dict, answer))
    user.questions_dict.clear()
    user.question = ""
    marks = user.update(int(answer)+1)

    bot.edit_message_text(text=reply_text,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)
    reply_text = ""
    for mark in marks:
        reply_text += mark[0] + ": " + mark[1] + "\n"
    if reply_text != "":
        bot.sendMessage(text=reply_text, chat_id=query.message.chat_id)
    else:
        bot.sendMessage(text="Немає оцінок(", chat_id=query.message.chat_id)

    reply_markup = create_reply_markup(DICT_FOR_GROUP_CHOSEN_MAIN)
    bot.sendMessage(text=command, reply_markup=reply_markup, chat_id=query.message.chat_id)
    user.bot_state = GROUP_CHOSEN_FIRST
    return GROUP_CHOSEN_FIRST


def choose_one_student_for_editing_marks(bot, update, user_data):
    query = update.callback_query
    answer = query.data

    user = user_data['client']
    # answer = int(answer)
    reply_text = "{}: {} \n".format("Оцінки ", get_key(user.questions_dict, answer))
    user.student_num = int(answer)
    user.questions_dict.clear()
    user.question = ""
    marks = user.update(int(answer)+1)

    bot.edit_message_text(text=reply_text,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)
    dict_marks = {}
    for i, mark in enumerate(marks):
        text = mark[0] + ": " + mark[1] + "\n"
        dict_marks[text] = str(i)
    if len(dict_marks.items()) != 0:
        reply_markup = create_reply_markup(dict_marks)
        user.questions_dict = dict_marks
        bot.sendMessage(text=reply_text, reply_markup=reply_markup, chat_id=query.message.chat_id)
        user.bot_state = CHANGE_MARK
        return CHANGE_MARK

    else:
        bot.sendMessage(text="Немає оцінок(", chat_id=query.message.chat_id)
        reply_markup = create_reply_markup(DICT_FOR_GROUP_CHOSEN_MAIN)
        bot.sendMessage(text=command, reply_markup=reply_markup, chat_id=query.message.chat_id)
        user.bot_state = GROUP_CHOSEN_FIRST
        return GROUP_CHOSEN_FIRST


def change_mark(bot, update, user_data):
    query = update.callback_query
    answer = query.data
    user = user_data['client']
    # answer = int(answer)
    text = get_key(user.questions_dict, answer)
    reply_text = "{}: {} \n".format("Виплавлення оцінки ", text)
    user.questions_dict.clear()
    print(text)
    user.question = int(text.split('.')[0]) + 1
    user.state = State.edit_mark
    print(user.student_num, user.question)
    bot.edit_message_text(text=reply_text,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)
    bot.sendMessage(text="Введіть нову оцінку", chat_id=query.message.chat_id)


def get_new_mark(bot, update, user_data):
    user = user_data['client']
    answer = update.message.text
    result = user.update(answer)
    user.update(result)
    if result is not None:
        update.message.reply_text(result)

    reply_markup = create_reply_markup(DICT_FOR_GROUP_CHOSEN_MAIN)
    update.message.reply_text(command, reply_markup=reply_markup)
    user.bot_state = GROUP_CHOSEN_FIRST
    return GROUP_CHOSEN_FIRST

