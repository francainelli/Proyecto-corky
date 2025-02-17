import discord
from googletrans import Translator
from flask import Flask, send_from_directory
import threading
import os

# Configuración del bot de Discord
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = discord.Client(intents=intents)
translator = Translator()

# Canales permitidos (por ID de canal)
allowed_channels = [508291307060461571, 1179277831428116580]

# Configuración de Flask para mantener el bot activo
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.getcwd(), 'favicon.ico')

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    threading.Thread(target=run).start()

# Eventos del bot
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Verificar si el mensaje proviene de un canal permitido
    if message.channel.id not in allowed_channels:
        return

    # Traducción del mensaje
    try:
        detected_lang = translator.detect(message.content).lang

        if detected_lang == "es":
            translated_text = translator.translate(message.content, dest="en").text
            await message.channel.send(translated_text)
        elif detected_lang == "en":
            translated_text = translator.translate(message.content, dest="es").text
            await message.channel.send(translated_text)

    except Exception as e:
        print(f"Error al traducir: {e}")
        error_message = "Soy mogólico, no puedo traducir eso" if detected_lang == "es" else "I'm retarded, I can't translate that"
        await message.channel.send(error_message)

if __name__ == "__main__":
    keep_alive()
    bot.run(os.getenv("TOKEN"))