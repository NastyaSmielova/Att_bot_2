from bot_unnes import *


def add_lesson_button(bot, update, user_data):
    query = update.callback_query
    answer = query.data
    user = user_data['client']
    next_question, current_subjects = user.update(get_key(user.questions_dict, answer))
    reply_text = "{}: {} \n".format(command, get_key(user.questions_dict, answer))
    bot.edit_message_text(text=reply_text,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)
    if user.state == State.end:
        reply_markup = create_reply_markup(DICT_FOR_EDIT_GROUP)
        bot.sendMessage(text=command, reply_markup=reply_markup, chat_id=query.message.chat_id)
        user.bot_state = EDIT_GROUP
        return EDIT_GROUP
    else:
        if next_question == 'тип':
            user.question = "Тип"
            user.questions_dict = {"Лекція": '0', "Семінар": '1', "Практика": '2', "Лабораторна": '3', "Інше": '4'}
            reply_markup = create_reply_markup(user.questions_dict)
            bot.sendMessage(text=user.question, reply_markup=reply_markup, chat_id=query.message.chat_id)
            user.bot_state = TYPE_FOR_LESSON
            return TYPE_FOR_LESSON
        else:
            if current_subjects is not None and current_subjects:
                reply_markup = create_reply_markup(current_subjects)
                bot.sendMessage(text="Оберіть групу з наявних: ", reply_markup=reply_markup, chat_id=query.message.chat_id)
                bot.sendMessage(text="Або введіть інший" + next_question, chat_id=query.message.chat_id)
            else:
                bot.sendMessage(text="Введіть " + next_question, chat_id=query.message.chat_id)


def add_lesson(bot, update, user_data):
    user = user_data['client']
    user.state = State.add_lesson
    current_groups = user.next_step()
    if current_groups is not None and current_groups:
        reply_markup = create_reply_markup(current_groups)
        update.message.reply_text("Оберіть групу з наявних: ",reply_markup=reply_markup)
        update.message.reply_text("Або введіть назву групи: ")
    else:
        update.message.reply_text("Введіть назву групи: ")

    user.bot_state = ADD_LESSON
    return ADD_LESSON


def add_lesson_text(bot, update, user_data):
    text = update.message.text
    if len(text) <= 0 or len(text) > 50:
        update.message.reply_text('Введена назва  має бути бути не пустою та містити не більше 50 символів)'
                                  '. Спробуйте ще раз. ')

    user = user_data['client']
    next_question, current_subjects = user.update(text)
    if user.state == State.end:
        reply_markup = create_reply_markup(DICT_FOR_EDIT_GROUP)
        update.message.reply_text(command, reply_markup=reply_markup)
        user.bot_state = EDIT_GROUP
        return EDIT_GROUP
    else:
        if next_question == 'тип':
            user.question = "Тип"
            user.questions_dict = {"Лекція": '0', "Семінар": '1', "Практика": '2', "Лабораторна": '3', "Інше": '4'}
            reply_markup = create_reply_markup(user.questions_dict)
            update.message.reply_text(user.question, reply_markup=reply_markup)
            user.bot_state = TYPE_FOR_LESSON
            return TYPE_FOR_LESSON
        else:
            if current_subjects is not None and current_subjects:
                reply_markup = create_reply_markup(current_subjects)
                update.message.reply_text("Оберіть групу з наявних: ", reply_markup=reply_markup)
                update.message.reply_text("Або введіть інший" + next_question)
            else:
                update.message.reply_text("Введіть " + next_question)


def type_for_lesson(bot, update, user_data):
    query = update.callback_query
    answer = query.data
    chat_id = query.message.chat_id
    user = user_data['client']
    text = get_key(user.questions_dict, answer)
    reply_text = "{}: {} \n".format(user.question, text)
    user.questions_dict.clear()
    user.question = ""
    bot.sendMessage(text="Додаю пару до розкладу...", chat_id=chat_id, )
    bot.edit_message_text(text=reply_text,
                          chat_id=chat_id,
                          message_id=query.message.message_id)

    group, subject, type_ = user.update(text)
    bot.sendMessage(text="Додано: " + group+" " + subject+" "+ type_, chat_id=chat_id, )
    if user.state == State.end:
        reply_markup = create_reply_markup(DICT_FOR_EDIT_GROUP)
        bot.sendMessage(text="Оберіть", reply_markup=reply_markup, chat_id=chat_id,)
        user.bot_state = EDIT_GROUP
        return EDIT_GROUP

