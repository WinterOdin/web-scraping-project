import requests
from bs4 import BeautifulSoup 
import pandas as pd
baseUrl = ' https://www.autoscout24.pl'
headers = { 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36' }

carDetailLinks = []
carInfoData    = []

for x in range(1,8):#getting first 10 pages of cars because we can't access the pagination it's probably generated with js thats why we cant see them
    r       = requests.get(f'https://www.autoscout24.pl/lst/bmw/635?sort=standard&desc=0&ustate=N%2CU&size=20&page={x}&fregto=1990&atype=C&')
    soup    = BeautifulSoup(r.content, 'lxml')
    carList = soup.find_all('div', class_='cl-list-element cl-list-element-gap')


    #loking in every item for main link to acces detail page and get the info about equipment that car has 
    for item in carList:
        for link in item.find_all('a', href=True, attrs={'data-item-name':True}):
            carDetailLinks.append(baseUrl+link['href'])


for xd in carDetailLinks:  
    r              = requests.get(xd, headers=headers)
    soup           = BeautifulSoup(r.content, 'lxml')
    carPrice       = soup.find('div',  class_="cldt-price").text.strip()
    carInfo        = str(soup.find('div',  class_="cldt-stage-basic-data").text).split() # we can't group this data in static way because car listings have diffrent quantity of info
    try:
        carName    = soup.find('span', class_="cldt-detail-version").text.strip()
    except: 
        carName    = "no detail name"
    context    = {

        'name' : carName,
        'price': carPrice,
        'info' : carInfo,

    }

    carInfoData.append(context)
    print("Saving" ,context['name'])

df  =   pd.DataFrame(carInfoData)
