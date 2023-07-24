import logging
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler

def strongCheck(titles):
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
    count = 0
    profession = update.message.text
    response_array = ""     
    await context.bot.send_message(chat_id=update.effective_chat.id, text="минуточку...")
    for i in range(1,10):

      url = f"https://belmeta.com/vacansii?l=Брест&sort=date&page={i}"
      response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

      soup = BeautifulSoup(response.content, "html.parser")

      titles = soup.select(".title a")
      company = soup.select(".company")
      print(profession)
      # strongCheck(titles)

      for j in range(len(titles)):
        if (titles[j].text.lower().__contains__(profession.lower())):
            count+=1
            response_array += f"{count} - {titles[j].text}\n{company[j].text}\nhttps://belmeta.com{titles[j]['href']}\n\n"
    if response_array == "":
        response_array = "Ничего не найдено"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response_array)

if __name__ == '__main__':
    application = ApplicationBuilder().token(token).build()
    
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    
    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.run_polling()



