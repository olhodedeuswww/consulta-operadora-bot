```python
import os
import re
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
DIRECTCALL_TOKEN = os.environ["DIRECTCALL_TOKEN"]

URL = "https://api.directcallsoft.com/portabilidade/consultar"
ALGAR_URL = "https://apialgarzinha.shardweb.app/apialgar"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📱 CONSULTA DE OPERADORA\n\n"
        "Envie o número assim:\n"
        "/consulta 21999999999\n\n"
        "Para consultar Algar:\n"
        "/algar 21850371881"
    )


async def consulta(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text(
            "❌ Informe o número.\n\n"
            "Exemplo:\n"
            "/consulta 21999999999"
        )
        return

    numero = re.sub(r"\D", "", context.args[0])

    if len(numero) not in (10, 11):
        await update.message.reply_text(
            "❌ Número inválido.\n"
            "Use DDD + número."
        )
        return

    await update.message.reply_text("🔎 Consultando...")

    dados = {
        "access_token": DIRECTCALL_TOKEN,
        "numero": numero,
        "formato": "json"
    }

    try:
        resposta = requests.post(
            URL,
            data=dados,
            timeout=20
        )

        resultado = resposta.json()

    except Exception:
        await update.message.reply_text(
            "❌ Erro ao consultar a DirectCall."
        )
        return

    if not isinstance(resultado, dict):
        await update.message.reply_text(
            "❌ A DirectCall retornou uma resposta inesperada."
        )
        return

    numero_api = resultado.get("NUMERO", numero)
    origem = resultado.get("OPERADORA_ORIGEM", "Não informado")
    atual = resultado.get("OPERADORA_ATUAL", "Não informado")
    migracao = resultado.get("DATA_MIGRACAO", "Não informado")

    mensagem = (
        "📱 *RESULTADO DA CONSULTA*\n\n"
        f"📞 Número: `{numero_api}`\n"
        f"📡 Operadora de origem: *{origem}*\n"
        f"📡 Operadora atual: *{atual}*\n"
        f"🔄 Data de migração: `{migracao or 'Não informado'}`"
    )

    await update.message.reply_text(
        mensagem,
        parse_mode="Markdown"
    )


async def plano(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text(
            "❌ Informe o número.\n\n"
            "Exemplo:\n"
            "/plano 21999999999"
        )
        return

    numero = re.sub(r"\D", "", context.args[0])

    if len(numero) not in (10, 11):
        await update.message.reply_text(
            "❌ Número inválido.\n"
            "Use DDD + número."
        )
        return

    await update.message.reply_text(
        "📦 *CONSULTA DE PLANO*\n\n"
        f"📞 Número: `{numero}`\n\n"
        "ℹ️ A consulta do plano comercial "
        "depende de uma API autorizada da operadora."
    )


async def algar(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text(
            "❌ Informe o documento.\n\n"
            "Exemplo:\n"
            "/algar 21850371881"
        )
        return

    documento = re.sub(r"\D", "", context.args[0])

    if not documento:
        await update.message.reply_text(
            "❌ Documento inválido."
        )
        return

    await update.message.reply_text(
        "🔎 Consultando Algar..."
    )

    try:
        resposta = requests.get(
            ALGAR_URL,
            params={"documento": documento},
            timeout=20
        )

        resultado = resposta.json()

    except Exception:
        await update.message.reply_text(
            "❌ Erro ao consultar a API Algar."
        )
        return

    if not isinstance(resultado, dict):
        await update.message.reply_text(
            "❌ A API Algar retornou uma resposta inesperada."
        )
        return

    resultados = resultado.get("results", [])

    if not resultados:
        await update.message.reply_text(
            "❌ Nenhum resultado encontrado."
        )
        return

    linhas = []

    for item in resultados:
        tipo = item.get("type", "Não informado")
        valor = item.get("value", "Não informado")
        method_id = item.get("method_id", "Não informado")

        linhas.append(
            f"📌 Tipo: `{tipo}`\n"
            f"📄 Valor: `{valor}`\n"
            f"🔑 Method ID: `{method_id}`"
        )

    mensagem = (
        "📱 *CONSULTA ALGAR*\n\n"
        + "\n\n".join(linhas)
    )

    await update.message.reply_text(
        mensagem,
        parse_mode="Markdown"
    )


def main():

    bot = Application.builder().token(TELEGRAM_TOKEN).build()

    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(CommandHandler("consulta", consulta))
    bot.add_handler(CommandHandler("plano", plano))
    bot.add_handler(CommandHandler("algar", algar))

    print("🤖 Bot iniciado!")

    bot.run_polling()


if __name__ == "__main__":
    main()
```
