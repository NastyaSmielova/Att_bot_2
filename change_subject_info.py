from bot_unnes import *


def get_new_name(bot, update, user_data):
    user = user_data['client']
    answer = update.message.text
    result = user.update(answer)
    if result is not None:
        update.message.reply_text(result)
    reply_markup = create_reply_markup(DICT_FOR_GROUP_CHOSEN_MAIN)
    update.message.reply_text(command, reply_markup=reply_markup)
    user.bot_state = GROUP_CHOSEN_FIRST
    return GROUP_CHOSEN_FIRST


def set_command_CHANGE_SUBJECT_button(bot, update, user_data):
    query = update.callback_query
    answer = query.data
    chat_id = query.message.chat_id
    user = user_data['client']
    reply_text = "{}: {} \n".format(command, get_key(DICT_FOR_CHANGE_SUBJECT_INFO, answer))
    user.questions_dict.clear()
    user.question = ""
    bot.edit_message_text(text=reply_text,
                          chat_id=chat_id,
                          message_id=query.message.message_id)
    if answer == '0':
     # group
        user.question = "Група"
    elif answer == '1':
    # subject
        user.question = "Предмет"
    elif answer == '2':
        # type
        user.question = "Тип"
    elif answer == '3':
    # subgroup
        user.question = "Підгрупа"

    elif answer == '4':
        # back
        reply_markup = create_reply_markup(DICT_FOR_GROUP_CHOSEN_MAIN)
        bot.sendMessage(text=command, reply_markup=reply_markup, chat_id=chat_id)
        user.bot_state = GROUP_CHOSEN_FIRST
        return GROUP_CHOSEN_FIRST
    bot.sendMessage(text="Введіть нову назву", chat_id=chat_id)


