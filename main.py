import os
import logging
import requests
from bs4 import BeautifulSoup
from telegram import Update
from dotenv import load_dotenv
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler

load_dotenv()
token = os.getenv("BELMETA_TOKEN")


def strong_check(titles):
    for strongList in titles:
        if strongList.find("strong") is not None:
            title = strongList.find("strong")
            print(type(title.text))
            # return title.text


# profession = str(input("Какую вакансию будем искать?\n"))
# pg_count = int(input("Сколько страниц надо обработать?\n"))

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите название вакансии, которую ищете...")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    profession = update.message.text
    response_array_belmeta = ""
    response_array_hh = ""
    count = 0

    await context.bot.send_message(chat_id=update.effective_chat.id, text="минуточку...")
    for i in range(0, 20):

        url_belmeta = f'https://belmeta.com/vacansii?l=Брест&sort=date&page={i}'
        url_hh = f"https://hh.ru/search/vacancy?area=1007&order_by=publication_time&page={i}"

        response_belmeta = requests.get(url_belmeta, headers={'User-Agent': 'Mozilla/5.0'})
        response_hh = requests.get(url_hh, headers={'User-Agent': 'Mozilla/5.0'})

        soup_belmeta = BeautifulSoup(response_belmeta.content, "html.parser")
        soup_hh = BeautifulSoup(response_hh.content, "html.parser")

        titles_belmeta = soup_belmeta.select(".title a")
        titles_hh = soup_hh.select(".serp-item__title-link")

        company_belmeta = soup_belmeta.select(".company")
        company_hh = soup_hh.select(".vacancy-serp-item__meta-info-company")

        link_hh = soup_hh.select(".serp-item__title-link-wrapper")
        print(profession)
        # strongCheck(titles)

        for j in range(len(titles_belmeta)):
            if titles_belmeta[j].text.lower().__contains__(profession.lower()):
                count += 1
                response_array_belmeta += \
                    (f"{count} - {titles_belmeta[j].text}\n{company_belmeta[j].text}\n"
                     f"https://belmeta.com{titles_belmeta[j]['href']}\n\n")

        for k in range(len(titles_hh)):
            if titles_hh[k].text.lower().__contains__(profession.lower()):
                count += 1
                response_array_hh += f"{count} - {titles_hh[k].text}\n{company_hh[k].contents[0].text}\n{link_hh[k].contents[0]['href'].split('?')[0]}\n\n"

    if response_array_belmeta == "":
        response_array_belmeta = "На Белмете ничего не найдено"

    if response_array_hh == "":
        response_array_hh = "На Хедхантере ничего не найдено"

    await context.bot.send_message(chat_id=update.effective_chat.id, text=response_array_hh)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response_array_belmeta)


if __name__ == '__main__':
    application = ApplicationBuilder().token(token).build()

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.run_polling()
