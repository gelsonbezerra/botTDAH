import os
import shutil
import datetime
import asyncio
import json
import random
from flask import Flask
from telegram import Bot, InputFile
from telegram.ext import ApplicationBuilder
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# 🕒 Verificando o horário do servidor na Render
agora = datetime.datetime.now()
print(f"🕒 Horário do servidor: {agora}")

BOT_TOKEN = "7922581689:AAH8Z7jxKueWm7VGVOjgUhUgUpqsp2s10ro"
GROUP_ID = -1002655972228

TOPICOS = {
    "dicasdiarias": {
        "ativo": True,
        "id_topico": 6,
        "pasta": "dicasdiarias",
        "padrao_nome": "dd",
        "frequencia": "diario",
        "horarios": ["09:00"],
    },
    "dicaspraticas": {
        "ativo": True,
        "id_topico": 8,
        "pasta": "dicaspraticas",
        "padrao_nome": "dp",
        "frequencia": "semanal",
        "dias": ["terça", "quinta"],
        "horarios": ["10:00"],
    },
    "insights": {
        "ativo": True,
        "id_topico": 169,
        "pasta": "insights",
        "padrao_nome": "in",
        "frequencia": "semanal",
        "dias": ["terça", "sexta"],
        "horarios": ["10:30"],
    },
    "motivacional": {
        "ativo": True,
        "id_topico": 4,
        "pasta": "motivacional",
        "padrao_nome": "mtv",
        "frequencia": "diario",
<<<<<<< HEAD
        "horarios": ["22:56", "22:58"],
        #"teste": "testemtv.pdf"
=======
        "horarios": ["21:57", "21:59"],
>>>>>>> 5f56b89 (Adicionando verificação do horário do servidor)
    }
}

with open("mensagens.json", "r", encoding="utf-8") as f:
    MENSAGENS = json.load(f)

async def rotina_postagem():
    bot = Bot(BOT_TOKEN)
    agora = datetime.datetime.now().strftime("%H:%M")
    hoje = datetime.datetime.now().strftime("%A").lower()

    for topico, config in TOPICOS.items():
        if config.get("ativo") and config.get("frequencia") == "diario" and agora in config["horarios"]:
            await bot.send_message(chat_id=GROUP_ID, message_thread_id=config["id_topico"], text="📌 Conteúdo VIP chegando!")
            await asyncio.sleep(5)

async def enviar_testes_iniciais():
    bot = Bot(BOT_TOKEN)
    for topico, config in TOPICOS.items():
        if config.get("ativo") and config.get("teste"):
            await bot.send_message(chat_id=GROUP_ID, message_thread_id=config["id_topico"], text="📌 Testando funcionamento!")
            await asyncio.sleep(5)

async def start_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(rotina_postagem, "cron", minute="*/1")
    scheduler.start()

    await enviar_testes_iniciais()
    await app.initialize()
    await app.start()

    webhook_url = "https://bottdah.onrender.com/webhook"
    await app.bot.set_webhook(webhook_url)

    print("✅ Bot rodando com Webhooks na Render!")
    await asyncio.Event().wait()

# 🚀 Configurar um servidor Flask para Render
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot rodando!"

PORT = int(os.environ.get("PORT", 5000))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(start_bot())
    app.run(host="0.0.0.0", port=PORT)
