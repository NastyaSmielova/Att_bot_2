from bot_unnes import  *

def edit_group(bot, update, user_data):
    user = user_data['client']
    user.state = State.edit
    user.next_step()
    reply_markup = create_reply_markup(user.questions_dict)
    update.message.reply_text(user.question, reply_markup=reply_markup)
    return GET_STUDENT


def edit_button(bot, update, user_data):
    query = update.callback_query
    answer = query.data

    user = user_data['client']
    user.student_num = int(answer)

    reply_text = "{}: {} \n".format(user.question, user.students_info[user.student_num][0])
    user.questions_dict.clear()
    user.question = ""

    bot.edit_message_text(text=reply_text,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)

    bot.sendMessage(text="Введіть бал", chat_id=query.message.chat_id)
    user.bot_state = STUDENT_CHOSEN

    return STUDENT_CHOSEN


def set_command_HAVE_MARKS_button(bot, update, user_data):
    query = update.callback_query
    answer = query.data
    chat_id = query.message.chat_id
    user = user_data['client']
    reply_text = "{}: {} \n".format(command, get_key(DICT_FOR_HAVE_MARKS, answer))
    user.questions_dict.clear()
    user.question = ""
    bot.edit_message_text(text=reply_text,
                          chat_id=chat_id,
                          message_id=query.message.message_id)
    if answer == '0':
        user.state = State.edit
        user.next_step()
        reply_markup = create_reply_markup(user.questions_dict)
        bot.sendMessage(text=user.question, reply_markup=reply_markup, chat_id=chat_id)
        user.bot_state = GET_STUDENT

        return GET_STUDENT

    elif answer == '1':

        date, marks = get_last_column(user.sheet)
        reply_text = create_file_name(user.group, user.subject, user.type_) + "  " + date + ":\n"
        for student, mark in marks:
            reply_text += student + " " + str(mark) + "\n"

        bot.sendMessage(text = reply_text, chat_id=chat_id)
        reply_markup = create_reply_markup(DICT_FOR_HAVE_MARKS)
        bot.sendMessage(text=command, reply_markup=reply_markup, chat_id=chat_id)

    elif answer == '2':

        reply_markup = create_reply_markup(DICT_FOR_GROUP_CHOSEN_MAIN)
        bot.sendMessage(text=command, reply_markup=reply_markup, chat_id=chat_id)
        user.bot_state = GROUP_CHOSEN_FIRST
        return GROUP_CHOSEN_FIRST



