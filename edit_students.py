from bot_unnes import  *


def add_one_student(bot, update, user_data):
    user = user_data['client']
    user.state = State.add_one_student
    update.message.reply_text("Введіть ПІБ")
    user.bot_state = ONE_STUDENT
    return ONE_STUDENT


def delete_one_student(bot, update, user_data):
    user = user_data['client']
    user.state = State.delete_one_student
    user.next_step()
    reply_markup = create_reply_markup(user.questions_dict)
    update.message.reply_text(user.question, reply_markup=reply_markup)
    user.bot_state = ONE_STUDENT
    return ONE_STUDENT


def change_one_student(bot, update, user_data):
    user = user_data['client']
    user.state = State.change_one_student
    user.next_step()
    reply_markup = create_reply_markup(user.questions_dict)
    update.message.reply_text(user.question, reply_markup=reply_markup)
    user.bot_state = ONE_STUDENT_CHANGE
    return ONE_STUDENT_CHANGE



def set_command_EDIT_STUDENTS_button(bot, update, user_data):
    query = update.callback_query
    answer = query.data
    chat_id = query.message.chat_id
    user = user_data['client']
    reply_text = "{}: {} \n".format(command, get_key(DICT_FOR_EDIT_STUDENTS, answer))
    user.questions_dict.clear()
    user.question = ""
    bot.edit_message_text(text=reply_text,
                          chat_id=chat_id,
                          message_id=query.message.message_id)
    if answer == '0':
        user.state = State.add_one_student
        bot.sendMessage(text="Введіть ПІБ", chat_id=chat_id)
        user.bot_state = ONE_STUDENT
        return ONE_STUDENT
    elif answer == '1':
        user.state = State.delete_one_student
        user.next_step()
        reply_markup = create_reply_markup(user.questions_dict)
        bot.sendMessage(text=user.question, reply_markup=reply_markup, chat_id=chat_id)
        user.bot_state = ONE_STUDENT
        return ONE_STUDENT
    elif answer == '2':
        user.state = State.change_one_student
        user.next_step()
        reply_markup = create_reply_markup(user.questions_dict)
        bot.sendMessage(text=user.question, reply_markup=reply_markup, chat_id=chat_id)

        user.bot_state = ONE_STUDENT_CHANGE
        return ONE_STUDENT_CHANGE
    elif answer == '3':
        students = get_students(user.sheet)
        students = '\n'.join(students)
        reply_markup = create_reply_markup(DICT_FOR_EDIT_STUDENTS)
        bot.sendMessage(text="Студенти: \n" + students, chat_id=chat_id)
        bot.sendMessage(text=command, reply_markup=reply_markup, chat_id=chat_id)
    elif answer == '4':
        reply_markup = create_reply_markup(DICT_FOR_GROUP_CHOSEN_MAIN)
        bot.sendMessage(text=command, reply_markup=reply_markup, chat_id=chat_id)
        user.bot_state = GROUP_CHOSEN_FIRST
        return GROUP_CHOSEN_FIRST

