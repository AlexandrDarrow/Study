import telebot
import Connectionmodule
import random

connection = Connectionmodule.getConnection()
bot = telebot.TeleBot('975577758:AAF_WPl14UpqYYCZby7RFF_TZfp22Z3Yx_Y')
bot.delete_webhook()


def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """

    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, 'Начинается игра в загадки.')
        nextQuestion(message.chat.id)

    @bot.message_handler(content_types=['text'])
    def answering(m):
        useranswer = m.text
        print("ответ пользователя: " + useranswer)
        with connection.cursor() as cur:
            cur.execute("select * from riddle_questions where id in (select questionid from riddle_answers where isdone = 0 )")
            data = cur.fetchone()
            qanswear = data["answer"]
            idqanswear = data["question"]
            uid = ["userid"]
            print("правильный ответ: " + qanswear)

        if useranswer == qanswear:
            cur.execute("update riddle_answers set date NOW(), isDone = 1 where userid = %s and questionid = %s", ())
            print('Угадал БЛЯЯЯЯ')
            nextQuestion(m.chat.id)
        else:
            print('Не угадал)))')

    def nextQuestion(id):
        with connection.cursor() as cursor:
            cursor.execute("select * from riddle_questions where id NOT IN (select questionId from riddle_answers where userId= %s) order by rand() limit 1", id)
            data = cursor.fetchone() #check data for none
            if data == None:
                print("poshel von!")
                return
            qid = data["id"]
            qtx = data["question"]
            uid = id
            cursor.execute("insert into riddle_answers (userid, questionid, isdone) values (%s, %s, %s)", (uid, qid, 0))
            connection.commit()
            bot.send_message(id, "Загадка: " + qtx)
            print("Загадка: " + qtx)


bot.set_update_listener(listener)  # register listener
name = bot.get_me()
print("С подключением к боту " + name.username + " все в порядке!")
bot.polling()
