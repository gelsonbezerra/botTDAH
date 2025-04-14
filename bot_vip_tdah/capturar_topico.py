
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram import Update

BOT_TOKEN = "7922581689:AAH8Z7jxKueWm7VGVOjgUhUgUpqsp2s10ro"  # ⬅️ substitua pelo token real

async def capturar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.message_thread_id:
        thread_id = update.message.message_thread_id
        nome_usuario = update.effective_user.first_name
        print(f"👤 {nome_usuario} enviou no tópico ID: {thread_id}")
        await update.message.reply_text(f"✅ Este tópico tem ID: {thread_id}")
    else:
        print("⚠️ Mensagem sem thread_id")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, capturar))
app.run_polling()
