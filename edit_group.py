from bot_unnes import *


def add_students(bot, update, user_data):
    user = user_data['client']
    user.state = State.add_students

    update.message.reply_text("Вводьте ПІБ студентів (по одному студенту в повідомленні)"
                              ". По закінченню введіть /stop")
    user.bot_state = CREATE_LIST
    return CREATE_LIST


def add_student(bot, update, user_data):
    user = user_data['client']
    answer = update.message.text
    # if answer == "кінець" or answer == "Кінець":
    #     user.state = State.end
    #     update.message.reply_text("Список сформовано")
    #     reply_markup = create_reply_markup(DICT_FOR_EDIT_GROUP)
    #     update.message.reply_text(command, reply_markup=reply_markup)
    #     return EDIT_GROUP
    user.update(answer)

    update.message.reply_text("Додано. Якщо бажаєте закінчити введіть /stop ")
    if user.state == State.end:
        reply_markup = create_reply_markup(DICT_FOR_EDIT_GROUP)
        update.message.reply_text(command, reply_markup=reply_markup)
        user.bot_state = EDIT_GROUP
        return EDIT_GROUP


def show_students(bot, update, user_data):
    user = user_data['client']
    students = get_students(user.sheet)
    students = '\n'.join(students)
    update.message.reply_text("Студенти: \n" + students)
    reply_markup = create_reply_markup(DICT_FOR_EDIT_STUDENTS)
    update.message.reply_text(command, reply_markup=reply_markup)


def add_subgroup(bot, update, user_data):
    user = user_data['client']
    num = user.add_subgroup()
    update.message.reply_text("Підгрупу № " + str(num) + "створено")

    reply_markup = create_reply_markup(DICT_FOR_EDIT_GROUP)
    update.message.reply_text(command, reply_markup=reply_markup)


def stop_addition(bot, update, user_data):
    user = user_data['client']
    user.state = State.end
    update.message.reply_text("Список сформовано")
    reply_markup = create_reply_markup(DICT_FOR_EDIT_GROUP)
    update.message.reply_text(command, reply_markup=reply_markup)
    user.bot_state = EDIT_GROUP
    return EDIT_GROUP
    # user.update(answer)


def set_command_EDIT_GROUP_button(bot, update, user_data):
    query = update.callback_query
    chat_id = query.message.chat_id
    answer = query.data
    user = user_data['client']
    reply_text = "{}: {} \n".format(command, get_key(DICT_FOR_EDIT_GROUP, answer))
    user.questions_dict.clear()
    user.question = ""
    bot.edit_message_text(text=reply_text,
                          chat_id=chat_id,
                          message_id=query.message.message_id)
    if answer == '0':
        user.state = State.add_students

        bot.sendMessage(text="Вводьте ПІБ студентів (по одному студенту в повідомленні)"+
                             ". По закінченню введіть /stop", chat_id=chat_id)
        user.bot_state = CREATE_LIST
        return CREATE_LIST

    elif answer == '1':
        students = get_students(user.sheet)
        students = '\n'.join(students)
        bot.sendMessage(text="Студенти: \n" + students, chat_id=chat_id)
        reply_markup = create_reply_markup(DICT_FOR_EDIT_GROUP)
        bot.sendMessage(text=command, reply_markup=reply_markup, chat_id=chat_id)
    elif answer == '2':

        num = user.add_subgroup()
        bot.sendMessage(text="Підгрупу № "+str(num) + " створено", chat_id=chat_id)
        reply_markup = create_reply_markup(DICT_FOR_EDIT_GROUP)
        bot.sendMessage(text="Оберіть", reply_markup=reply_markup, chat_id=chat_id)
    elif answer == '3':
        user.clear_all()
        reply_markup = create_reply_markup(DICT_FOR_REGISTERED)
        bot.sendMessage(text=command, reply_markup=reply_markup, chat_id=chat_id)
        user.bot_state = REGISTERED
        return REGISTERED
