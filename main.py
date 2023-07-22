import requests
from bs4 import BeautifulSoup

def strongCheck(titles):
  for strongList in titles:
    if strongList.find("strong") is not None:
      title = strongList.find("strong")
      print(type(title.text))
      # return title.text

profession = str(input("Какую вакансию будем искать?\n"))
pg_count = int(input("Сколько страниц надо обработать?\n"))

count = 0
for i in range(1,pg_count):
    
    url = f"https://belmeta.com/vacansii?l=Брест&sort=date&page={i}"
    # url = f"https://belmeta.com/vacansii?q=front&l=Минск" 
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    soup = BeautifulSoup(response.content, "html.parser")

    titles = soup.select(".title a")
    company = soup.select(".company")
    # strongCheck(titles)

    for j in range(len(titles)):
        if (titles[j].text.lower().__contains__(f"{profession}")):
            count+=1
            print(f"{count}-{titles[j].text}\n{company[j].text}\nhttps://belmeta.com{titles[j]['href']}\n")

