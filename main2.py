
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler,\
    RegexHandler, MessageHandler, Filters

from bot_utils import *
from edit_group import *
from edit_students import *
from group_chosen import *
from have_marks import *
from change_subject_info import *
from show_for_one import *
from add_lesson import *

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)




def main():
    # Create the Updater and pass it your bot's token.
    updater = TOKEN
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start, pass_user_data=True),
                      MessageHandler(Filters.text,
                                     start_text,
                                     pass_user_data=True),
                      ],

        states={
            CHOOSING: [
                CommandHandler('start', start, pass_user_data=True),
                # CallbackQueryHandler(set_command_REGISTERED_button, pass_user_data=True),
                MessageHandler(Filters.text, auth_code, pass_user_data=True),
                       ],

            REGISTERED: [
                            CommandHandler('addlesson', add_lesson, pass_user_data=True),
                            CommandHandler('choosegroup', choose_group, pass_user_data=True),
                            CallbackQueryHandler(set_command_REGISTERED_button, pass_user_data=True),
            ],

            ONE_STUDENT: [
                MessageHandler(Filters.text, get_one_surname, pass_user_data=True),
                CallbackQueryHandler(delete_student_button, pass_user_data=True),
                CommandHandler('back', back_to_edit_students, pass_user_data=True),
            ],

            ONE_STUDENT_CHANGE: [
                MessageHandler(Filters.text, get_one_surname, pass_user_data=True),
                CallbackQueryHandler(change_student_button, pass_user_data=True),
                CommandHandler('back', back_to_edit_students, pass_user_data=True),
            ],

            CHOOSE_GROUP: [
                CallbackQueryHandler(group_button, pass_user_data=True),
                CommandHandler('back', back_to_registered, pass_user_data=True),

            ],

            TYPE_FOR_LESSON: [
                CallbackQueryHandler(type_for_lesson, pass_user_data=True),
                CommandHandler('back', back_to_registered, pass_user_data=True),

            ],

            EDIT_GROUP: [
                CommandHandler('back', back_to_registered, pass_user_data=True),
                CommandHandler('addstudents', add_students, pass_user_data=True),
                CommandHandler('showstudents', show_students, pass_user_data=True),
                CommandHandler('addsubgroup', add_subgroup, pass_user_data=True),
                CommandHandler('stop', stop_addition, pass_user_data=True),

                CallbackQueryHandler(set_command_EDIT_GROUP_button, pass_user_data=True),

                MessageHandler(Filters.text, add_student, pass_user_data=True),
            ],

            CREATE_LIST: [
                MessageHandler(Filters.text,
                               add_student,
                               pass_user_data=True),
                CommandHandler('stop', stop_addition, pass_user_data=True),
            ],

            ADD_LESSON: [
                MessageHandler(Filters.text, add_lesson_text, pass_user_data=True),
                CommandHandler('back', back_to_registered, pass_user_data=True),
                CallbackQueryHandler(add_lesson_button, pass_user_data=True)

            ],

            EDIT_STUDENTS: [
                CommandHandler('add',
                               add_one_student,
                               pass_user_data=True),
                CommandHandler('delete',
                                delete_one_student,
                                pass_user_data=True),
                CommandHandler('change',
                               change_one_student,
                               pass_user_data=True),
                CommandHandler('show',
                               show_students,
                               pass_user_data=True),
                CommandHandler('back',
                               back_to_group,
                               pass_user_data=True),
                CallbackQueryHandler(set_command_EDIT_STUDENTS_button, pass_user_data=True)
            ],
            GROUP_CHOSEN_FIRST:[
                CommandHandler('back',
                               back_to_registered,
                               pass_user_data=True),
                CallbackQueryHandler(set_command_GROUP_CHOSEN_FIRTST_button, pass_user_data=True)
            ],

            GROUP_CHOSEN: [CommandHandler('rollcall',
                                          start_rolcall,
                                          pass_user_data=True),
                           CommandHandler('editstudents',
                                          edit_students,
                                          pass_user_data=True),
                           # CommandHandler('edit',
                           #                edit_old_data,
                           #                pass_user_data=True),
                           CommandHandler('delete', delete_subject,pass_user_data=True),
                           CommandHandler('change', change_subject_info, pass_user_data=True),
                           CommandHandler('showmarks', show_marks, pass_user_data=True),
                           CommandHandler('setdefault',
                                          set_default,
                                          pass_user_data=True),
                           CommandHandler('setmarks',
                                          set_marks,
                                          pass_user_data=True),
                           MessageHandler(Filters.text,
                                          get_marks,
                                          pass_user_data=True),
                           CommandHandler('back',
                                          back_to_registered,
                                          pass_user_data=True),
                           CallbackQueryHandler(set_command_GROUP_CHOSEN_button, pass_user_data=True)
            ],

            CHANGE_SUBJECT_INFO: [
                CommandHandler('back', back_to_group, pass_user_data=True),
                MessageHandler(Filters.text, get_new_name, pass_user_data=True),
                CallbackQueryHandler(set_command_CHANGE_SUBJECT_button, pass_user_data=True),
            ],

            ROLL_CALL: [
                CallbackQueryHandler(rollcall_button, pass_user_data=True),
                CommandHandler('back', back_to_group, pass_user_data=True),
            ],

            HAVE_MARKS: [CommandHandler('edit', edit_group, pass_user_data=True),

                         CallbackQueryHandler(set_command_HAVE_MARKS_button, pass_user_data=True),

                         CommandHandler('showlist', show_list, pass_user_data=True),

                         CommandHandler('back', back_to_group, pass_user_data=True),
            ],

            GET_STUDENT: [
                CallbackQueryHandler(edit_button, pass_user_data=True),
            ],
            SHOW_FOR_ONE: [
                CallbackQueryHandler(choose_one_student, pass_user_data=True),
                CommandHandler('back',
                               back_to_group,
                               pass_user_data=True),
            ],
            EDIT_FOR_ONE:[
                CallbackQueryHandler(choose_one_student_for_editing_marks, pass_user_data=True),
                CommandHandler('back',
                               back_to_group,
                               pass_user_data=True),
            ],
            CHANGE_MARK:[
                MessageHandler(Filters.text, get_new_mark, pass_user_data=True),
                CallbackQueryHandler(change_mark, pass_user_data=True),
                CommandHandler('back',
                               back_to_group,
                               pass_user_data=True),
            ],

            STUDENT_CHOSEN: [
                MessageHandler(Filters.text,
                               get_marks,
                               pass_user_data=True),
            ]
        },

        fallbacks=[RegexHandler('^[D,d]one$', done, pass_user_data=True)]
    )

    updater.dispatcher.add_handler(conv_handler)

    updater.dispatcher.add_handler(CommandHandler('help', help, pass_user_data=True))
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    print("bot started")

    updater.idle()


if __name__ == '__main__':
    main()
