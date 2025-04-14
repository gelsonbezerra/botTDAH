import os
import shutil
import datetime
import asyncio
import json
import random
from telegram import Bot, InputFile, Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from apscheduler.schedulers.asyncio import AsyncIOScheduler

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
        "teste": "testedd.pdf"
    },
    "dicaspraticas": {
        "ativo": True,
        "id_topico": 8,
        "pasta": "dicaspraticas",
        "padrao_nome": "dp",
        "frequencia": "semanal",
        "dias": ["terça", "quinta"],
        "horarios": ["10:00"],
        "teste": "testedp.pdf"
    },
    "insights": {
        "ativo": True,
        "id_topico": 169,
        "pasta": "insights",
        "padrao_nome": "in",
        "frequencia": "semanal",
        "dias": ["terça", "sexta"],
        "horarios": ["10:30"],
        "teste": "testein.pdf"
    },
    "motivacional": {
        "ativo": True,
        "id_topico": 4,
        "pasta": "motivacional",
        "padrao_nome": "mtv",
        "frequencia": "diario",
        "horarios": ["08:00", "19:00"],
        "teste": "testemtv.pdf"
    }
}

with open("mensagens.json", "r", encoding="utf-8") as f:
    MENSAGENS = json.load(f)

def mensagem_por_horario():
    hora = datetime.datetime.now().hour
    if hora < 12:
        return random.choice(MENSAGENS["manha"])
    elif 12 <= hora < 18:
        return random.choice(MENSAGENS["tarde"])
    else:
        return random.choice(MENSAGENS["noite"])

def proximo_arquivo(pasta, padrao_nome):
    arquivos = sorted([f for f in os.listdir(pasta) if f.endswith(f"{padrao_nome}.pdf")])
    return arquivos[0] if arquivos else None

def mover_para_postados(pasta, nome_arquivo):
    origem = os.path.join(pasta, nome_arquivo)
    destino_dir = os.path.join(pasta, "postados")
    os.makedirs(destino_dir, exist_ok=True)
    shutil.move(origem, os.path.join(destino_dir, nome_arquivo))

# --- Correção para evitar envio duplicado ---
arquivos_enviados = set()

async def postar_pdf(bot: Bot, pasta: str, nome_arquivo: str, id_topico: int, max_retentativas=3):
    caminho = os.path.join(pasta, nome_arquivo)

    if not os.path.exists(caminho):
        print(f"⚠️ Arquivo não encontrado: {caminho}")
        return

    if nome_arquivo in arquivos_enviados:
        print(f"🚫 Arquivo {nome_arquivo} já foi enviado anteriormente. Pulando...")
        return  

    # 🔥 Adiciona à lista de enviados antes da tentativa para evitar reenvio duplicado
    arquivos_enviados.add(nome_arquivo)

    tentativas = 0
    while tentativas < max_retentativas:
        print(f"🔄 Tentativa {tentativas + 1} de envio para {nome_arquivo}")  # Debug

        try:
            with open(caminho, "rb") as f:
                await bot.send_document(
                    chat_id=GROUP_ID,
                    message_thread_id=id_topico,
                    document=InputFile(f, filename=nome_arquivo),
                    caption="📌 Novo conteúdo do grupo VIP!"
                )

            mover_para_postados(pasta, nome_arquivo)
            print(f"✅ Enviado {nome_arquivo} para tópico {id_topico}")
            return  

        except Exception as e:
            print(f"❌ Erro ao enviar {nome_arquivo}: {e}")
            tentativas += 1
            await asyncio.sleep(10)  # Aumenta tempo entre tentativas

    print(f"🚫 Falha ao enviar {nome_arquivo} após {max_retentativas} tentativas.")

async def rotina_postagem():
    bot = Bot(BOT_TOKEN)
     # 🌎 Dicionário para traduzir os dias da semana
    DIAS_PT = {
        "monday": "segunda",
        "tuesday": "terça",
        "wednesday": "quarta",
        "thursday": "quinta",
        "friday": "sexta",
        "saturday": "sábado",
        "sunday": "domingo"
    }

    # Obtém o dia da semana em inglês e traduz para português
    hoje_ing = datetime.datetime.now().strftime("%A").lower()
    hoje = DIAS_PT.get(hoje_ing, hoje_ing)  # Faz a conversão automática

    agora = datetime.datetime.now().strftime("%H:%M")

                # 🔍 Adicionando prints para verificação
    print(f"Hoje em inglês: {hoje_ing}")  # Exibe o valor original
    print(f"Hoje traduzido: {hoje}")      # Exibe o valor traduzido corretamente
    print(f"Agora é: {agora}")

    agora = datetime.datetime.now().strftime("%H:%M")
    print(f"Hoje é: {hoje}")
    print(f"Agora é: {agora}")

    for topico, config in TOPICOS.items():
        if not config.get("ativo"):
            continue  
        if config.get("frequencia") == "diario" and agora in config["horarios"]:
            nome_arquivo = proximo_arquivo(config["pasta"], config["padrao_nome"])
            if nome_arquivo:
                await bot.send_message(chat_id=GROUP_ID, message_thread_id=config["id_topico"], text="📌 Conteúdo VIP chegando!")
                await asyncio.sleep(5)
                await postar_pdf(bot, config["pasta"], nome_arquivo, config["id_topico"])
        elif config.get("frequencia") == "semanal" and hoje in config.get("dias", []) and agora in config["horarios"]:
            print(f"🔍 Testando envio de {topico} - Hoje: {hoje}, Dias configurados: {config.get('dias')}, Agora: {agora}, Horários configurados: {config['horarios']}")
            if hoje in config.get("dias", []) and agora in config["horarios"]:
             print(f"✅ Deveria estar enviando {topico} agora!")

            nome_arquivo = proximo_arquivo(config["pasta"], config["padrao_nome"])
            if nome_arquivo:
                await bot.send_message(chat_id=GROUP_ID, message_thread_id=config["id_topico"], text="📌 Conteúdo VIP chegando!")
                await asyncio.sleep(5)
                await postar_pdf(bot, config["pasta"], nome_arquivo, config["id_topico"])

async def enviar_testes_iniciais():
    bot = Bot(BOT_TOKEN)
    for topico, config in TOPICOS.items():
        if config.get("ativo") and config.get("teste"):
            caminho = os.path.join(config["pasta"], config["teste"])
            if os.path.exists(caminho):
                try:
                    await bot.send_message(chat_id=GROUP_ID, message_thread_id=config["id_topico"], text="📌 Testando funcionamento!")
                    await asyncio.sleep(5)
                    with open(caminho, "rb") as f:
                        await bot.send_document(chat_id=GROUP_ID, message_thread_id=config["id_topico"], document=InputFile(f, filename=config["teste"]), caption="📌 Testando sistema pelo bot.")
                    print(f"✅ Teste enviado: {config['teste']} no tópico {topico}")
                except Exception as e:
                    print(f"❌ Erro ao enviar teste {config['teste']}: {e}")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(rotina_postagem, "cron", minute="*/1")
    scheduler.start()

    await enviar_testes_iniciais()
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    print("✅ Bot rodando localmente...")

    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
