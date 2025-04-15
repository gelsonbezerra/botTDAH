import os
import shutil
import datetime
import asyncio
import json
import random
import pytz  # Suporte para fuso horário
from flask import Flask
from telegram import Bot, InputFile
from telegram.ext import ApplicationBuilder
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# 🕒 Ajustando corretamente para o fuso horário do Brasil
fuso_brasil = pytz.timezone("America/Sao_Paulo")
agora = datetime.datetime.now(datetime.timezone.utc).astimezone(fuso_brasil)
print(f"🕒 Horário ajustado para Brasil: {agora}")

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
    "motivacional": {
        "ativo": True,
        "id_topico": 4,
        "pasta": "motivacional",
        "padrao_nome": "mtv",
        "frequencia": "diario",
        "horarios": ["23:59", "21:59"],
    }
}

with open("mensagens.json", "r", encoding="utf-8") as f:
    MENSAGENS = json.load(f)

async def rotina_postagem():
    print("🚀 Entrando na rotina de postagem!")
    bot = Bot(BOT_TOKEN)
    agora = datetime.datetime.now(datetime.timezone.utc).astimezone(fuso_brasil).strftime("%H:%M")
    
    print(f"🕒 Horário atual: {agora}")

    for topico, config in TOPICOS.items():
        if config.get("ativo") and config.get("frequencia") == "diario" and agora in config["horarios"]:
            print(f"📌 Postando no tópico {topico}...")
            await bot.send_message(chat_id=GROUP_ID, message_thread_id=config["id_topico"], text="📌 Conteúdo VIP chegando!")
            await asyncio.sleep(5)

async def start_bot():
    print("🚀 Iniciando bot...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    scheduler = AsyncIOScheduler()

    # 🔄 Modificação: rodando a cada 30 segundos para testar agendamento
    scheduler.add_job(rotina_postagem, "cron", second="*/30")
    scheduler.start()

    await app.initialize()
    await app.start()

    webhook_url = "https://bottdah.onrender.com/webhook"
    print(f"🌐 Configurando Webhook: {webhook_url}")
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