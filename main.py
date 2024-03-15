import csv
import threading
import telebot
from telebot import types  
from Response import RunBot

BOT_TOKEN = "YOUR_BOT_TOKEN"
bot = telebot.TeleBot(BOT_TOKEN)
user_instances = {}
lock = threading.Lock()

# Open CSV file in write mode
csv_file = open("user_details.csv", "w", newline="", encoding="utf-8")
csv_writer = csv.writer(csv_file)
# Write headers to the CSV file
csv_writer.writerow(["Username", "First Name", "Message with Command", "Bot's Reply"])
csv_file.flush()  # Flush the buffer to ensure data is written to file


def handle_user(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    username = message.from_user.username

    if user_id not in user_instances:
        user_instances[user_id] = RunBot(first_name)

    command = message.text
    print(f"{username}: {command} \n")

    try:
        reply_message = user_instances[user_id].bot_output(command)
    except Exception as e:
        print(e)
        reply_message = "Sorry, I encountered an error. Please try again later."

    if reply_message.strip():  # Check if a reply message is not empty
        bot.reply_to(message, reply_message)
        print("\nBOTS_REPLY:" + reply_message)

        # Write user details and conversation to CSV file
        with lock:
            csv_writer.writerow([username, first_name, command, reply_message])
            csv_file.flush()  # Flush the buffer to ensure data is written to file
    else:
        # Creating inline keyboard
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row(types.InlineKeyboardButton("Hi kalai!", callback_data="hi_kalai"),
                     types.InlineKeyboardButton("Tell me about our college", callback_data="college_info"))

        bot.reply_to(message, "Hi, I am kalai, do you have any questions regarding Dr.NGP iTECH?",
                     reply_markup=keyboard)


@bot.message_handler(commands=['start'])
def handle_start(message):
    # Creating inline keyboard
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(types.InlineKeyboardButton("Hi kalai!", callback_data="hi_kalai"),
                 types.InlineKeyboardButton("Tell me about our college", callback_data="college_info"))

    bot.reply_to(message, "Welcome! Please choose an option:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "hi_kalai":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, f"Hi! {call.message.chat.first_name}, nice to meet you, ask me any questions about out college!")
    elif call.data == "college_info":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "Dr.NGP iTECH is an amazing institution!, there are a lot of thinks to discuss about it, ask me specific questions!")


def process_message(message):
    handle_user(message)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    t = threading.Thread(target=process_message, args=(message,))
    t.start()


bot.polling()
