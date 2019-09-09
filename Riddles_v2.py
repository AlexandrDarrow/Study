import telebot
import Connectionmodule



def listener(messages):
    print("listener received")
    for m in messages:
        if m.text.startswith('/'):
            continue
        checkanswer(m)
        Question(m.chat.id)

def Question(id):
    with connection.cursor() as cur:
        cur.execute("select * from riddle_questions where id NOT IN (select questionId from riddle_answers where userId= %s) order by rand() limit 1", id)
        data = cur.fetchone()
        if data == None:
            print("Загадки закончились")
            bot.send_message(id,"Загадки кончились")
            checktotal(id)
        else:
            utext = data['question']
            qid = data['id']
            bot.send_message(id, utext)
            cur.execute("insert into riddle_answers values (%s, %s, NOW(), %s)", (id, qid, 0))
            connection.commit()
    print("I'm Happy!" + str(id))
    #checkanswer(id)

def checkanswer(message):
    #@bot.message_handler(content_types=['text'])
    #def getanswer(message):
    with connection.cursor() as cursor:
        uanswer = message.text
        id = message.chat.id
        print(uanswer,id)
        #uid = message.chat.id
        q = "select * from riddle_questions where id = (select questionid from riddle_answers where userid = %s and isDone = 0 order by date limit 1)" % id
        print(q)
        cursor.execute(q)
        data = cursor.fetchone()
        if data == None:
            print("no questions")
            return
        banswer = data['answer']
        qid = int(data['id'])
        bot.send_message(message.chat.id, "Ответ пользователя: " + uanswer + ", правильный овтет: " + banswer)
        cursor.execute("update riddle_answers set isDone = %s, date = NOW() where userid = %s and questionid = %s", (1, id, qid))
        connection.commit()
        if uanswer == banswer:
            cursor.execute("update riddle_users set points = points + 5 where id = %s", int(id))
            connection.commit()
            bot.send_message(id,"Вы угадали. Пять очнов грифиндору")
        else:
            cursor.execute("update riddle_users set points = points - 2 where id = %s", int(id))
            connection.commit()
            bot.send_message(id, "Вы не угадали. Минус два очка грифиндору")


def checktotal(id):
    with connection.cursor() as cursor:
        cursor.execute("select * from riddle_users where id = %s", int(id))
        data1 = cursor.fetchone()
        uname = data1['username']
        upoints = data1['points']
        print(upoints)
        bot.send_message(id, uname + ", ваш результат составляет " + str(upoints) + " очков")


connection = Connectionmodule.getConnection()
bot = telebot.TeleBot('975577758:AAF_WPl14UpqYYCZby7RFF_TZfp22Z3Yx_Y')
bot.delete_webhook()

@bot.message_handler(commands=['start'])
def start_message(message):
    print("start received")

    with connection.cursor() as cur:
        cur.execute("select * from riddle_users where id = %s", message.chat.id)
        #uuid = cur.rowcount
        userData = cur.fetchone()
        #print("Найдено строк в таблице: "+ str(uuid))
        if userData == None:
            cur.execute("insert into riddle_users (id, username, points) values (%s, %s, %s)", (message.chat.id, message.from_user.first_name, 0))
            connection.commit()
            print("Новый участник записан")
            bot.send_message(message.chat.id, 'Начинается игра в загадки.')
        Question(message.chat.id)

@bot.message_handler(commands=['reset'])
def reset_user(message):
    with connection.cursor() as cur:
        print("Вы уже пробовали играть. Начнем заново")
        # this action with command /reset
        cur.execute("delete from riddle_answers where userid = %s", message.chat.id)
        connection.commit()
        cur.execute("update riddle_users set points=0 where id=%d", message.chat.id)
        # cur.execute("delete from riddle_users where id = %s", message.chat.id)
        # connection.commit()
        # print("Старый профиль удалил")
        # cur.execute("insert into riddle_users (id, username, points) values (%s, %s, %s)", (message.chat.id, message.from_user.first_name, 0))
        # connection.commit()


bot.set_update_listener(listener)  # register listener
name = bot.get_me()
print(name.username + ". С подключением. Все в порядке")
bot.polling()

