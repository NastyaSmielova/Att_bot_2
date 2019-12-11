from bot_unnes import *


def start_rolcall(bot, update, user_data):
    user = user_data['client']
    user.state = State.roll_call
    user.next_step()

    reply_markup = create_reply_markup(user.questions_dict)
    update.message.reply_text(user.question, reply_markup=reply_markup)

    if user.state == State.end:
        reply_markup = create_reply_markup(DICT_FOR_HAVE_MARKS)
        update.message.reply_text(command, reply_markup=reply_markup)
        user.bot_state = HAVE_MARKS
        return HAVE_MARKS
    user.bot_state = ROLL_CALL
    return ROLL_CALL


def show_marks(bot, update, user_data):
    user = user_data['client']
    user.state = State.show_marks
    user.next_step()

    reply_markup = create_reply_markup(user.questions_dict)
    update.message.reply_text(user.question, reply_markup=reply_markup)
    user.bot_state = SHOW_FOR_ONE

    return SHOW_FOR_ONE


def edit_students(bot, update, user_data):
    user = user_data['client']
    reply_markup = create_reply_markup(DICT_FOR_EDIT_STUDENTS)
    update.message.reply_text(command, reply_markup=reply_markup)
    user.bot_state = EDIT_STUDENTS
    return EDIT_STUDENTS


def delete_subject(bot, update, user_data):
    user = user_data['client']
    user.state = State.delete_subject
    user.next_step()
    update.message.reply_text("Предмет видалено")

    reply_markup = create_reply_markup(DICT_FOR_REGISTERED)
    update.message.reply_text("Предмет видалено.\n" + command, reply_markup=reply_markup)
    user.bot_state = REGISTERED
    return REGISTERED


def set_default(bot, update, user_data):
    user = user_data['client']
    user.state = State.set_default
    user.next_step()

    update.message.reply_text("Введіть оцінку для всіх ")
    if user.state == State.end:
        reply_markup = create_reply_markup(DICT_FOR_HAVE_MARKS)
        update.message.reply_text(command, reply_markup=reply_markup)
        user.bot_state = HAVE_MARKS
        return HAVE_MARKS


def set_marks(bot, update, user_data):
    user = user_data['client']
    user.state = State.marks
    user.next_step()

    update.message.reply_text(user.question)
    if user.state == State.end:
        reply_markup = create_reply_markup(DICT_FOR_HAVE_MARKS)
        update.message.reply_text(command, reply_markup=reply_markup)
        user.bot_state = HAVE_MARKS
        return HAVE_MARKS


def change_subject_info(bot, update, user_data):
    user = user_data['client']
    user.state = State.change_subject_info
    reply_markup = create_reply_markup(DICT_FOR_CHANGE_SUBJECT_INFO)
    update.message.reply_text(command, reply_markup=reply_markup)
    user.bot_state = CHANGE_SUBJECT_INFO
    return CHANGE_SUBJECT_INFO


def set_command_GROUP_CHOSEN_button(bot, update, user_data):
    query = update.callback_query
    chat_id = query.message.chat_id
    answer = query.data
    user = user_data['client']
    reply_text = "{}: {} \n".format(command, get_key(DICT_FOR_GROUP_CHOSEN, answer))
    user.questions_dict.clear()
    user.question = ""
    bot.edit_message_text(text=reply_text,
                          chat_id=chat_id,
                          message_id=query.message.message_id)
    if answer == '0':
        # bot.sendMessage(text="/rollcall", chat_id=query.message.chat_id)
        user.state = State.roll_call
        user.next_step()
        error = user.error_message
        if error is not None:
            reply_markup = create_reply_markup(DICT_FOR_GROUP_CHOSEN_RESTRICTED)
            bot.sendMessage(text=error, reply_markup=reply_markup, chat_id=chat_id)
            user.bot_state = GROUP_CHOSEN
            return GROUP_CHOSEN
        reply_markup = create_reply_markup(user.questions_dict)
        bot.sendMessage(text=user.question, reply_markup=reply_markup, chat_id=chat_id)

        if user.state == State.end:
            reply_markup = create_reply_markup(DICT_FOR_HAVE_MARKS)
            bot.sendMessage(text=command, reply_markup=reply_markup, chat_id=chat_id)
            user.bot_state = HAVE_MARKS
            return HAVE_MARKS
        user.bot_state = ROLL_CALL
        return ROLL_CALL
    elif answer == '1':
        reply_markup = create_reply_markup(DICT_FOR_EDIT_STUDENTS)
        bot.sendMessage(text=command, reply_markup=reply_markup, chat_id=chat_id)
        user.bot_state = EDIT_STUDENTS
        return EDIT_STUDENTS
    elif answer == '2':
        bot.sendMessage(text="/edit", chat_id=chat_id)
    elif answer == '3':
        user.state = State.set_default
        user.next_step()

        bot.sendMessage(text="Введіть оцінку для всіх ", chat_id=chat_id)
        if user.state == State.end:
            reply_markup = create_reply_markup(DICT_FOR_HAVE_MARKS)
            bot.sendMessage(text=command, reply_markup=reply_markup, chat_id=chat_id)
            user.bot_state = HAVE_MARKS
            return HAVE_MARKS
        # bot.sendMessage(text="/setdefault", chat_id=query.message.chat_id)
    elif answer == '4':
        # bot.sendMessage(text="/setmarks", chat_id=query.message.chat_id)
        user.state = State.marks
        user.next_step()

        bot.sendMessage(text=user.question, chat_id=chat_id)
        if user.state == State.end:
            reply_markup = create_reply_markup(DICT_FOR_HAVE_MARKS)
            bot.sendMessage(text=command, reply_markup=reply_markup, chat_id=chat_id)
            user.bot_state = HAVE_MARKS
            return HAVE_MARKS
    elif answer == '5':
        user.state = State.delete_subject
        user.next_step()
        reply_markup = create_reply_markup(DICT_FOR_REGISTERED)
        bot.sendMessage(text="Предмет видалено.\n"+command, reply_markup=reply_markup, chat_id=chat_id)
        user.bot_state = REGISTERED
        return REGISTERED
    elif answer == '6':
        # bot.sendMessage(text="/back", chat_id=chat_id)
        user.clear_all()
        reply_markup = create_reply_markup(DICT_FOR_REGISTERED)
        bot.sendMessage(text=command, reply_markup=reply_markup, chat_id=chat_id)
        user.bot_state = REGISTERED
        return REGISTERED
    elif answer == '7':
        bot.sendMessage(text="may be implemented soon", chat_id=chat_id)
        # bot.sendMessage(text="/change", chat_id=chat_id)
        # user.clear_all()
        # reply_markup = create_reply_markup(DICT_FOR_REGISTERED)
        # bot.sendMessage(text=command, reply_markup=reply_markup, chat_id=chat_id)
        # return REGISTERED

    elif answer == "8":
        user = user_data['client']
        user.state = State.show_marks
        user.next_step()

        reply_markup = create_reply_markup(user.questions_dict)
        bot.sendMessage(text=user.question, reply_markup=reply_markup, chat_id=chat_id)
        user.bot_state = SHOW_FOR_ONE

        return SHOW_FOR_ONE
    elif answer == "9":
        user = user_data['client']
        user.state = State.edit_marks
        user.next_step()

        reply_markup = create_reply_markup(user.questions_dict)
        bot.sendMessage(text=user.question, reply_markup=reply_markup, chat_id=chat_id)
        user.bot_state = EDIT_FOR_ONE

        return EDIT_FOR_ONE

def set_command_GROUP_CHOSEN_FIRTST_button(bot, update, user_data):
    query = update.callback_query
    chat_id = query.message.chat_id
    answer = query.data
    user = user_data['client']
    reply_text = "{}: {} \n".format(command, get_key(DICT_FOR_GROUP_CHOSEN_MAIN, answer))
    user.questions_dict.clear()
    user.question = command
    bot.edit_message_text(text=reply_text,
                          chat_id=chat_id,
                          message_id=query.message.message_id)
    if answer == '0':
        reply_markup = create_reply_markup(DICT_FOR_GROUP_CHOSEN_SET_MARKS)
        bot.sendMessage(text=user.question, reply_markup=reply_markup, chat_id=chat_id)
        user.bot_state = GROUP_CHOSEN
        return GROUP_CHOSEN
    elif answer == '1':
        reply_markup = create_reply_markup(DICT_FOR_GROUP_CHOSEN_EDIT)
        bot.sendMessage(text=user.question, reply_markup=reply_markup, chat_id=chat_id)
        user.bot_state = GROUP_CHOSEN
        return GROUP_CHOSEN
    elif answer == '2':
        reply_markup = create_reply_markup(DICT_FOR_GROUP_CHOSEN_DELETE)
        bot.sendMessage(text=user.question, reply_markup=reply_markup, chat_id=chat_id)
        user.bot_state = GROUP_CHOSEN
        return GROUP_CHOSEN
    elif answer == '3':
        reply_markup = create_reply_markup(DICT_FOR_GROUP_CHOSEN_SHOW)
        bot.sendMessage(text=user.question, reply_markup=reply_markup, chat_id=chat_id)
        user.bot_state = GROUP_CHOSEN
        return GROUP_CHOSEN
    elif answer == '4':
        # bot.sendMessage(text="/setmarks", chat_id=query.message.chat_id)
        reply_markup = create_reply_markup(DICT_FOR_REGISTERED)
        bot.sendMessage(text=command, reply_markup=reply_markup, chat_id=chat_id)
        user.bot_state = REGISTERED
        return REGISTERED




