from telegram.ext import ConversationHandler
from google.auth.transport.requests import AuthorizedSession
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from bot_unnes import *
import gspread

from bot_utils_buttons import *
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)


# need  drive and spreadsheets to work
#create auth link for new user


def create_link():
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    creds = None
    link = None
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = Flow.from_client_secrets_file(
                'client_secret.json',
                scopes=scope,
                redirect_uri='urn:ietf:wg:oauth:2.0:oob')

            auth_url, _ = flow.authorization_url(prompt='consent')
            link = '{}'.format(auth_url)

    return link, flow

# create user by returned code to flow


def create_client(flow, code):
    try:
        print("creating client")
        flow.fetch_token(code=code)
        credentials = flow.credentials
        gc = gspread.Client(auth=credentials)
        gc.session = AuthorizedSession(credentials)
        drive_service = build('drive', 'v3', credentials=credentials)
        file_metadata = {
            'name': 'Attendance Bot',
            'mimeType': 'application/vnd.google-apps.folder'
        }
        try:

            response = drive_service.files().list(
                    q="name='Attendance Bot'",  spaces='drive',
                                                      fields='files(id, name)',
                                                      ).execute()
            for file in response.get('files', []):
                    # Process change
                    name = file.get('name')
                    id = file.get('id')
                    print('Found file: %s (%s)' % (name, id ))
                    folder_id = id
                    return gc, folder_id, drive_service, True
            raise "nothing to work with"
        except:
            print("can't open folder")
            file = drive_service.files().create(body=file_metadata,
                                               fields='id').execute()
        folder_id = file.get('id')

        return gc, folder_id, drive_service, False

    except:
        return None, None, None

# start,  registry of newcomer


def start(bot, update, user_data):

    link, flow = create_link()
    user_data['flow'] = flow
    # url_button = [InlineKeyboardButton(text="Авторизуватись ", callback_data=link)]
    keyboard = []
    question_dict = {"Авторизуватись " + arrow: link}

    for key, value in question_dict.items():
        keyboard.append([InlineKeyboardButton(key, url=value)])
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Відвідайте лінк для авторизації та надішліть отриманий код у відповідь",
                              reply_markup=reply_markup)

    return CHOOSING


# apply received code for authorization


def auth_code(bot, update, user_data):
    code = update.message.text
    try:
        flow = user_data['flow']

        __client, folder_id, drive_service, exists = create_client(flow, code)
        if __client is None:
            update.message.reply_text('Не вдалось отримати доступ до Google Drive.'
                                      ' Можливо спробуйте /start ще раз. ')

            return CHOOSING
        update.message.reply_text("Обробляю отриманий код")
        user = GoogleSheetsShort(__client, drive_service, folder_id, exists)
        user_data['client'] = user
        del user_data['flow']
        if user.error_message is not None:

            update.message.reply_text('Дякую, ви авторизувались. ' + user.error_message)
            user.error_message = None

        reply_markup = create_reply_markup(DICT_FOR_REGISTERED)
        update.message.reply_text(command, reply_markup=reply_markup)
        user.bot_state = REGISTERED

        return REGISTERED
    except:
        update.message.reply_text('Введений код є неправильним. Можливо спробуйте /start ще раз. ')


def help(bot, update, user_data):
    try:
        user = user_data['client']
    except:
        update.message.reply_text("Щось пішло не так:(\nВикористовуйте /start щоб розпочати роботу.")
        return
    if user.bot_state == HAVE_MARKS:
        update.message.reply_text("you are in HAVE_MARKS")
        reply_markup = create_reply_markup(DICT_FOR_HAVE_MARKS)
        update.message.reply_text(command, reply_markup=reply_markup)
    elif user.bot_state == GROUP_CHOSEN_FIRST:
        update.message.reply_text("you are in GROUP_CHOSEN_FIRST")
        reply_markup = create_reply_markup(DICT_FOR_GROUP_CHOSEN_MAIN)
    elif user.bot_state == GROUP_CHOSEN:
        update.message.reply_text("you are in GROUP_CHOSEN")
        reply_markup = create_reply_markup(DICT_FOR_GROUP_CHOSEN)
        update.message.reply_text(command, reply_markup=reply_markup)
    elif user.bot_state == CHOOSING:
        update.message.reply_text("you are in CHOOSING")
    elif user.bot_state == EDIT_STUDENTS:
        update.message.reply_text("you are in EDIT_STUDENTS")
        reply_markup = create_reply_markup(DICT_FOR_EDIT_STUDENTS)
        update.message.reply_text(command, reply_markup=reply_markup)
    elif user.bot_state == EDIT_GROUP:
        update.message.reply_text("you are in EDIT_GROUP")
        reply_markup = create_reply_markup(DICT_FOR_EDIT_GROUP)
        update.message.reply_text(command, reply_markup=reply_markup)
    elif user.bot_state == REGISTERED:
        update.message.reply_text("you are in REGISTERED")
        reply_markup = create_reply_markup(DICT_FOR_REGISTERED)
        update.message.reply_text(command, reply_markup=reply_markup)
    else:
        update.message.reply_text("Щось пішло не так:(\nВикористовуйте /start щоб розпочати роботу.")


def error(bot, update, error_):
    update.message.reply_text("Щось пішло не так:(\nВикористовуйте /start щоб розпочати роботу.")
    logger.warning(error_)


def done(bot, update, user_data):
    if 'client' in user_data:
        del user_data['client']

    update.message.reply_text("До наступної зустрічі. Всі створені матеріали все ще залишаються на Вашому Google Drive")

    user_data.clear()
    return ConversationHandler.END
