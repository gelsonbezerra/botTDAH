import asyncio
from telegram import Bot, InputFile
import os

BOT_TOKEN = "7922581689:AAH8Z7jxKueWm7VGVOjgUhUgUpqsp2s10ro"
GROUP_ID = -1002655972228
TOPICO_ID = 13  # ID do tópico 'dicas_extras'

# ⬇️ Altere aqui com o nome do PDF que você quer enviar (dentro da pasta dicas_extras)
nome_arquivo = "meu.pdf"
caminho_arquivo = os.path.join("dicasextras", nome_arquivo)

async def enviar_pdf():
    bot = Bot(token=BOT_TOKEN)
    if os.path.exists(caminho_arquivo):
        try:
            with open(caminho_arquivo, "rb") as f:
                await bot.send_document(
                    chat_id=GROUP_ID,
                    message_thread_id=TOPICO_ID,
                    document=InputFile(f, filename=nome_arquivo),
                    caption="📎 Conteúdo extra enviado pelo administrador."
                )
            print(f"✅ '{nome_arquivo}' enviado com sucesso para o tópico extras!")
        except Exception as e:
            print(f"❌ Erro ao enviar o PDF: {e}")
    else:
        print(f"⚠️ Arquivo não encontrado: {caminho_arquivo}")

asyncio.run(enviar_pdf())
