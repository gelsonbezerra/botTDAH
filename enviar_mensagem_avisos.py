
import asyncio
from telegram import Bot

BOT_TOKEN = "7922581689:AAH8Z7jxKueWm7VGVOjgUhUgUpqsp2s10ro"  # ⬅️ Substitua pelo seu token real
GROUP_ID = -1002655972228     # ID do seu grupo

mensagem = """👋 *Seja bem-vindo(a) ao nosso Grupo VIP TDAH!*

Este é o seu espaço exclusivo para acesso a conteúdos que vão te ajudar com foco, organização e equilíbrio no dia a dia com TDAH. Aqui você encontrará apoio, direcionamento e motivação constantes!

📚 *Organização do grupo por tópicos:*

✅ Dicas Diárias – Dica nova todos os dias em PDF  
✅ Motivacional – 2x por dia (08h e 20h) pra manter sua energia alta  
✅ Insights – Reflexões profundas 2x por semana  
✅ Dicas Práticas – Segunda e quinta com estratégias aplicáveis

🚧 Em breve: Atividades guiadas e dicas extras

⏰ *Horários automáticos:*  
- Dicas Diárias → 09h  
- Motivacional → 08h e 20h  
- Dicas Práticas → segunda e quinta às 10h  
- Insights → terça e sexta às 10h30

🧑‍💼 *Suporte:* Fale com @thalitamag  
🚫 Evite mensagens fora do tema  
💬 Interaja com os membros se quiser

💙 Esse espaço foi criado com carinho pra você viver com mais leveza, foco e clareza — mesmo com o TDAH!
"""

async def enviar():
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(chat_id=GROUP_ID, text=mensagem, parse_mode="Markdown")
    print("✅ Mensagem enviada com sucesso no tópico Geral!")

asyncio.run(enviar())
