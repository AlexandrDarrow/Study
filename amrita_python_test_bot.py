import telebot
import Connectionmodule

connection = Connectionmodule.getConnection()
bot = telebot.TeleBot('975577758:AAF_WPl14UpqYYCZby7RFF_TZfp22Z3Yx_Y')
bot.delete_webhook()


def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        chatid = m.chat.id
        if m.content_type == 'text':
            print(m.from_user.id)
            print(m.text)
            text = "Записал: " + m.from_user.username + " , " + m.text
            bot.send_message(chatid, text)
            with connection.cursor() as cursor:
                cursor.execute("select * from tgusers where usertgid = %s", m.from_user.id)
                already = cursor.rowcount
                print(already)
                if already == 0 :
                     with connection.cursor() as cursor:
                        affectedRows = cursor.execute("insert into tgusers values (NULL, %s, %s, NOW())", (m.from_user.id, m.text))
                        print("added rows: %d" % affectedRows)
                        cursor.execute("select * from tgusers where texttg = %s", m.text)
                        result = cursor.fetchall()
                        print(result)
                        connection.commit()
                else:
                    with connection.cursor() as cursor:
                        affectedRows = cursor.execute("update tgusers set texttg = %s, lasttime = NOW() where usertgid = %s", ( m.text, m.from_user.id))
                        print("updated rows: %d" % affectedRows)
                        cursor.execute("select * from tgusers where texttg = %s", m.text)
                        result = cursor.fetchall()
                        print(result)
                        bot.send_message(chatid, result[0])
                        connection.commit()
name = bot.get_me()
print("Bot auth ok! name: " + name.username)
bot.set_update_listener(listener) #register listener
bot.polling()




