import telebot
import Connectionmodule

connection = Connectionmodule.getConnection()
bot = telebot.TeleBot('975577758:AAF_WPl14UpqYYCZby7RFF_TZfp22Z3Yx_Y')
bot.delete_webhook()



def listener(messages):
    print("def Listener get params")
    for m in messages:
        if m.text.startswith("/"):
            continue
        checkuser(m)
        text = m.text
        continue



def checkuser(message):
 uid = message.chat.id
 with connection.cursor() as cur:
     cur.execute("select * from riddle_users where id = %s", uid)
     user = cur.fetchone()
     uid1 = user["id"]
     uname = user["username"]
     if user == None:
         bot.send_message(uid, "Я тебя раньше не видел")
         print("def Checkuser 1 get params")
         bot.send_message(uid, "Начинаем новую игру")
         question(message)
     else:
         cur.execute("select * from riddle_answers where userid = %s and answer is null limit 1", uid)
         questioncheck = cur.fetchone()
         print("def Checkuser 2 get params")
         if questioncheck == None:
             bot.send_message(uid, "Для начала игры набери /start")
             print("def Checkuser 21 get params")
         else:
             print("def Checkuser 22 get params")
             checkanswer(message)


def question(message):
    uid = message.chat.id
    with connection.cursor() as cur:
        cur.execute("select * from riddle_questions where id NOT IN (select questionId from riddle_answers where userId= %s) order by rand() limit 1", uid)
        data = cur.fetchone()
        q = data["question"]
        bot.send_message(uid, "Загадка: " + q)
        #cur.execute("insert into riddle_answers values ()")
    print("def Question get params")


def checkanswer(message):

    print("def Checkanswer get params")


@bot.message_handler(commands=['reset'])
def reset_user(message):
    print("def Reset get params")


@bot.message_handler(commands=['start'])
def start_message(message):
    print("def Start get params")

bot.set_update_listener(listener)  # register listener
name = bot.get_me()
print(name.username + ". С подключением. Все в порядке")
bot.polling()