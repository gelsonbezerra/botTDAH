
import asyncio
from telegram import Bot, InputFile

BOT_TOKEN = "7922581689:AAH8Z7jxKueWm7VGVOjgUhUgUpqsp2s10ro"
GROUP_ID = -1002655972228
TOPICO_ID = 4  # Motivacional
CAMINHO_PDF = r"C:\Users\Dell\Documents\bot_vip_tdah\motivacional\testemtv.pdf.pdf"
NOME_PDF = "testemtv.pdf"

async def enviar_pdf_teste():
    bot = Bot(BOT_TOKEN)
    try:
        with open(CAMINHO_PDF, "rb") as f:
            await bot.send_document(
                chat_id=GROUP_ID,
                message_thread_id=TOPICO_ID,
                document=InputFile(f, filename=NOME_PDF),
                caption="📄 Teste de envio de PDF com InputFile e filename"
            )
        print("✅ PDF enviado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao enviar o PDF: {e}")

asyncio.run(enviar_pdf_teste())
