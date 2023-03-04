import logging

from asgiref.sync import sync_to_async, async_to_sync
from telegrambot.models import Category_group,Category,Service,ServiceReport
from django.core.management.base import BaseCommand
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler,MessageHandler,filters


# Название класса обязательно - "Command"
class Command(BaseCommand):
    # Используется как описание команды обычно
    help = 'Implemented to Django application telegram bot setup command'

    def handle(self, *args, **kwargs):
        application = ApplicationBuilder().token('6034356544:AAHBY7V4l2JnE1njaUF1aWyZUq_hxuM0y_4').build()

        service_not_work_hendler = MessageHandler(filters.Regex("^/service_not_work_\d$"), service_not_work)

        echo_handler = MessageHandler(filters.COMMAND, echo)

        start_handler = CommandHandler('start', start)
        application.add_handler(start_handler)
        application.add_handler(service_not_work_hendler)
        application.add_handler(echo_handler)


        application.run_polling()


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

@sync_to_async
def crate_service_report(service_id,user_id):

    service_report = ServiceReport()
    service_report.service_id = service_id
    service_report.userId = user_id
    service_report.save()

@sync_to_async
def service_report_exist(service_id, user_id):
    serviceReport = ServiceReport.objects.filter(userId=user_id, service_id=service_id).first()
    if not serviceReport:
        return False
    return True

async def service_not_work(update: Update, context: ContextTypes.DEFAULT_TYPE):

    service_id = int(update.message.text.replace('/service_not_work_', ''))
    service_rep_exist = await service_report_exist(service_id, update.message.from_user.id)
    if service_rep_exist:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Ваш запит вже прийнято')
        return

    await crate_service_report(service_id, update.message.from_user.id)
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Дякую за інформацію')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    command = update.message.text.replace('/', '')
    services = Service.objects.filter(category__slug=command)
    async for service in services:
         text_message = service.name
         text_message += '\n'+service.description
         text_message += '\n➖➖➖➖➖➖➖➖'
         text_message += '\nПовідомити про неактуальний номер:'
         text_message += '\n/service_not_work_'+str(service.id)


         await context.bot.send_message(chat_id=update.effective_chat.id, text=text_message)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    Category_groups = Category_group.objects.all();
    text_message='Привіт. На даний момент мені відомо про такі послуги:'
    async for Category_groups_item in Category_groups:
         text_message+="\n <b>"+Category_groups_item.name+"</b>"
         async for Category_item in Category_groups_item.category_set.all():
             text_message += '\n /' + Category_item.slug + ' ' + Category_item.name
             text_message += '\n' + '➖➖➖➖➖➖➖➖'
    text_message += '\n\n /addservice - ✅ додати свою послугу в каталог'

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_message, parse_mode="HTML")
