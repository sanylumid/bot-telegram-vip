from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import datetime

TOKEN = "8654898833:AAFrYaWMf1mOf9GAhGT0Uk6APlSGo9TGkRc"

CANAL_ID = -1001234567890
GRUPO_ID = -1001234567890

usuarios = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bienvenido VIP 🔥\nUsa /pagar")

async def pagar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Paga aquí:\nhttps://tulinkdepago.com\nLuego usa /verificar")

async def verificar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    fecha_exp = datetime.datetime.now() + datetime.timedelta(days=30)
    usuarios[user_id] = fecha_exp
    
    canal_link = await context.bot.create_chat_invite_link(CANAL_ID, member_limit=1)
    grupo_link = await context.bot.create_chat_invite_link(GRUPO_ID, member_limit=1)
    
    await update.message.reply_text(
        f"Acceso:\nCanal: {canal_link.invite_link}\nGrupo: {grupo_link.invite_link}"
    )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("pagar", pagar))
app.add_handler(CommandHandler("verificar", verificar))

app.run_polling()

async def revisar_vencimientos(context: ContextTypes.DEFAULT_TYPE):
    ahora = datetime.datetime.now()
    
    for user_id, fecha in list(usuarios.items()):
        if ahora > fecha:
            try:
                await context.bot.ban_chat_member(CANAL_ID, user_id)
                await context.bot.ban_chat_member(GRUPO_ID, user_id)
                del usuarios[user_id]
            except:
                pass

from telegram.ext import JobQueue

job_queue = app.job_queue
job_queue.run_repeating(revisar_vencimientos, interval=86400, first=10)