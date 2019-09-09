import telebot
import Connectionmodule

connection = Connectionmodule.getConnection()
bot = telebot.TeleBot('975577758:AAF_WPl14UpqYYCZby7RFF_TZfp22Z3Yx_Y')
bot.delete_webhook()



def listener(messages):
    print("listener received")
    for m in messages:
        checkuser(m)
        text = m.text
        continue



def checkuser(message):
 uid = message.chat.id
 with connection.cursor() as cur:
     cur.execute("select * from riddle_users where id = %s", uid)
     data = cur.fetchone()
     uid1 = data["id"]
     uname = data["username"]
     if data == None:
         bot.send_message(uid, "Я тебя раньше не видел")
         print("checkuser")
         bot.send_message(uid, "Начинаем новую игру")
         question(message)
     else:
         checkanswer(message)


def question(message):
    uid = message.chat.id
    with connection.cursor() as cur:
        cur.execute("select * from riddle_questions where id NOT IN (select questionId from riddle_answers where userId= %s) order by rand() limit 1", uid)
        data = cur.fetchone()
        q = data["question"]
        bot.send_message(uid, "Загадка: " + q)
        cur.execute("insert into riddle_answers values ()")
    print("question")


def checkanswer():
    print("checkanswer")


@bot.message_handler(commands=['reset'])
def reset_user(message):
    print("start reset")


@bot.message_handler(commands=['start'])
def start_message(message):
    print("start start")

bot.set_update_listener(listener)  # register listener
name = bot.get_me()
print(name.username + ". С подключением. Все в порядке")
bot.polling()