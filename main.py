import telebot 
from config import token
from logic import Pokemon
import threading
import time

bot = telebot.TeleBot(token) 

# увеличения голода 
def increase_hunger_periodically():
    while True:
        time.sleep(300)  # Каждые 5 минут
        for pokemon in Pokemon.pokemons.values():
            pokemon.increase_hunger()

# фоновый процесс
hunger_thread = threading.Thread(target=increase_hunger_periodically)
hunger_thread.daemon = True
hunger_thread.start()

@bot.message_handler(commands=['go'])
def go(message):
    if message.from_user.username not in Pokemon.pokemons.keys():
        pokemon = Pokemon(message.from_user.username)
        bot.send_message(message.chat.id, pokemon.info())
        bot.send_photo(message.chat.id, pokemon.show_img())
        
        # Если покемон редкий 
        if pokemon.is_rare:
            bot.send_message(message.chat.id, "🎉 Вам выпал РЕДКИЙ покемон! Используйте /bonus чтобы получить супер-бонус!")
    else:
        bot.reply_to(message, "Ты уже создал себе покемона")

@bot.message_handler(commands=['feed'])
def feed_pokemon(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        pokemon = Pokemon.pokemons[message.from_user.username]
        result = pokemon.feed()
        
        # повышение уровня
        level_up = pokemon.check_level_up()
        
        response = result
        if level_up:
            response += f"\n\n{level_up}"
            
        bot.send_message(message.chat.id, response)
    else:
        bot.reply_to(message, "Сначала создайте покемона командой /go")

@bot.message_handler(commands=['info'])
def pokemon_info(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        pokemon = Pokemon.pokemons[message.from_user.username]
        bot.send_message(message.chat.id, pokemon.info())
        bot.send_photo(message.chat.id, pokemon.show_img())
    else:
        bot.reply_to(message, "Сначала создайте покемона командой /go")

@bot.message_handler(commands=['bonus'])
def super_bonus(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        pokemon = Pokemon.pokemons[message.from_user.username]
        result = pokemon.get_super_bonus()
        bot.send_message(message.chat.id, result)
        bot.send_message(message.chat.id, pokemon.info())
    else:
        bot.reply_to(message, "Сначала создайте покемона командой /go")

@bot.message_handler(commands=['achievements'])
def show_achievements(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        pokemon = Pokemon.pokemons[message.from_user.username]
        if pokemon.achievements:
            achievements_text = "🏆 Ваши достижения:\n• " + "\n• ".join(pokemon.achievements)
        else:
            achievements_text = "У вас пока нет достижений. Кормите покемона и повышайте уровень!"
        bot.send_message(message.chat.id, achievements_text)
    else:
        bot.reply_to(message, "Сначала создайте покемона командой /go")

bot.infinity_polling(none_stop=True)