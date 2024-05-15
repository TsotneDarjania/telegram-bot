import requests
from bs4 import BeautifulSoup
import telegram
import asyncio
import re;
from datetime import datetime, timedelta
from telegram.constants import ParseMode

# Telegram bot token
bot_token = '6558911734:AAF25728aE6uYFY5MGtBb3SlyP4ZYf6vRE4'
# Chat ID
chat_id = '-1002130774666'
# hour Difference
hour_difference = 8
# currenct
currency = "USD"
# stars can be "bull1", "bull2", "bull3"
stars = "bull3"
# Create a bot
bot = telegram.Bot(token=bot_token)

texts = {
    "PPI (MoM)": "მწარმოებელთა ფასების ინდექსი, თვიდან თვემდე - მწარმოებლის ფასების ინდექსი (PPI) ზომავს მწარმოებლების მიერ გაყიდული საქონლის ფასის ცვლილებას. ეს არის სამომხმარებლო ფასების ინფლაციის წამყვანი მაჩვენებელი, რომელიც მთლიან ინფლაციის უდიდეს ნაწილს შეადგენს",
    "Fed Chair Powell": "ამერიკის ფედერალური სამსახურის თავჯდომარე (პაუელის) მოხსენება - ფედერალური სარეზერვო ფონდის თავმჯდომარე (ჯერომ პაუელი) (თებერვალი 2018 - თებერვალი 2022) უნდა წარმოადგინოს ეკონომიკური პერსპექტივების და ბოლოდროინდელი მონეტარული პოლიტიკის ქმედებების შესახებ ერთობლივი ეკონომიკური კომიტეტის წინაშე, ვაშინგტონში. ჩვენება ორ ნაწილადაა; პირველი არის მომზადებული განცხადება, შემდეგ კომიტეტი ატარებს კითხვა-პასუხის სხდომას. ჩვენების კითხვა-პასუხის ნაწილმა შეიძლება დაინახოს ბაზრის მძიმე ცვალებადობა მთელი პერიოდის განმავლობაში",
    "Core Retail Sales": "ძირითადი საცალო გაყიდვები, თვიდან თვემდე - ძირითადი საცალო გაყიდვები ზომავს გაყიდვების მთლიანი ღირებულების ცვლილებას საცალო ვაჭრობის დონეზე აშშ-ში, ავტომობილების გამოკლებით. ეს არის სამომხმარებლო ხარჯების მნიშვნელოვანი მაჩვენებელი და ასევე განიხილება, როგორც ტემპის მაჩვენებელი აშშ-ს ეკონომიკისთვის.",
    "Crude Oil Inventories": "ენერგეტიკის ინფორმაციის ადმინისტრაციის (EIA) ნედლი ნავთობის მარაგები ზომავს ყოველკვირეულ ცვლილებას ბარელი კომერციული ნედლი ნავთობის რაოდენობაში, რომელსაც ფლობენ ამერიკული ფირმები. მარაგების დონე გავლენას ახდენს ნავთობპროდუქტების ფასზე, რამაც შეიძლება გავლენა მოახდინოს ინფლაციაზე",
    "CPI (YoY)" : "სამომხმარებლო ფასების ინდექსი, წლიდან წლამდე - სამომხმარებლო ფასების ინდექსი (CPI) ზომავს საქონლისა და მომსახურების ფასის ცვლილებას მომხმარებლის პერსპექტივიდან. ეს არის მთავარი გზა შესყიდვის ტენდენციებისა და ინფლაციის ცვლილებების გასაზომად",
    "CPI (MoM)":  "სამომხმარებლო ფასების ინდექსი, თვიდან თვემდე - სამომხმარებლო ფასების ინდექსი (CPI) ზომავს საქონლისა და მომსახურების ფასის ცვლილებას მომხმარებლის პერსპექტივიდან. ეს არის მთავარი გზა შესყიდვის ტენდენციებისა და ინფლაციის ცვლილებების გასაზომად.",
    "Initial Jobless Claims": "სამსახურის მაძიებელთა ინდექსი ზომავს იმ პირთა რაოდენობას, ვინც პირველად მოითხოვა უმუშევრობის დაზღვევა გასული კვირის განმავლობაში. ეს არის აშშ-ს ყველაზე ადრეული ეკონომიკური მონაცემები, მაგრამ ბაზრის გავლენა კვირიდან კვირამდე იცვლება."
}

description_text = ""

class WebScraper:
    def __init__(self, url,currency):
        self.url = url
        self.webContent = None
        # Init Functions
        self.getContent()
        
    def getContent(self):
        # Send a GET request to the URL
        response = requests.get(self.url)
        # Parse the HTML content of the page
        self.webContent = BeautifulSoup(response.text, 'html.parser')

def get_description_text(event_name):
    for key in texts.keys():
        if key in event_name:
            return texts[key]
        else:
            print("Unknown text key")

def get_rest_time(event_time_string):
    datetime_str = f"{datetime.now().date()} {event_time_string}"
    event_datetime = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
    event_datetime += timedelta(hours=hour_difference)
    current_datetime = datetime.now()
    # Calculate difference in time
    time_difference = event_datetime - current_datetime
    total_minutes = time_difference.total_seconds() // 60
    return total_minutes

async def send_message_before_event(event_name, time_difference, actual, forecast, previous):
    description_text = get_description_text(event_name)
    flag = "🇺🇸"
    current_value_str = re.sub(r'[^\d.]', '', actual) if actual else None
    forecast_value_str = re.sub(r'[^\d.]', '', forecast) if forecast else None

    if(current_value_str == "" or forecast_value_str == ""):
         message = f"{flag}{event_name}დაიწყება {time_difference} წუთში\n\n<b>აღწერა</b>: {description_text}"
    else:
        message = f"{flag}{event_name}დაიწყება {time_difference} წუთში\n\n<b>აღწერა</b>: {description_text}\n\n<b>ფაქტობრივი:</b> {actual}\n<b>პროგნოზი:</b> {forecast}\n<b>წინა:</b> {previous}"

    # Send a message with the image to the chat
    await bot.sendPhoto(chat_id=chat_id,parse_mode=ParseMode.HTML, photo="https://tradershub.ge/wp-content/uploads/2023/03/Logo-site-1.png", caption=message)

async def send_message_start_event(event_name,event_time, actual, forecast, previous):
    description_text = get_description_text(event_name)
    
    current_value_str = re.sub(r'[^\d.]', '', actual) if actual else None
    forecast_value_str = re.sub(r'[^\d.]', '', forecast) if forecast else None

    extraText = ""
    flag = "🇺🇸"
    smallIcon = ""

    if current_value_str == "" or forecast_value_str == "":
        message = f"<b>{flag}{event_name}</b>მიმდინარეობს ამჟამად\nთარიღი:{event_time}\n\n<b>აღწერა:</b> {description_text}"         
    else:
        message = f"<b>{flag}{event_name}</b>მიმდინარეობს ამჟამად\nთარიღი:{event_time}\n\n<b>აღწერა:</b> {description_text}\n\n{flag}<b>ფაქტობრივი:</b> {actual}\n{flag}<b>პროგნოზი:</b> {forecast}\n{flag}<b>წინა:</b> {previous}\n\n{smallIcon}  {extraText}"

        if float(current_value_str) > float(forecast_value_str):
            smallIcon = "🐂"
            extraText = "<b>ხარისებრი პოზიცია </b> მოსალოდნელზე მაღალი მაჩვენებელი უნდა იქნას მიღებული, როგორც დადებითი/ აშშ დოლარისთვის."
        else:
            smallIcon = "🐻"
            extraText = "<b>დათვისებრი პოზიცია </b> მოსალოდნელზე დაბალი მაჩვენებელი უნდა იქნას მიღებული, როგორც აშშ დოლარის უარყოფითი/პოზიცია"
    
    
    # Send a message with the image to the chat
    await bot.sendPhoto(chat_id=chat_id, parse_mode=ParseMode.HTML, photo="https://ibb.co/ngHd385", caption=message)


async def main():
    scraber = WebScraper('https://www.investing.com/economic-calendar/', currency)

    allRows = scraber.webContent.select('tr[id^="eventRowId_"]')

    currency_rows = []
    # choose Currency rows from Web Content
    for row in allRows:
        td_elements = row.find_all('td')
        for td in td_elements[1]:
            if currency in td.text:
                currency_rows.append(row)

    target_rows = []
    # target rows with 3 stars
    for row in currency_rows:
        td_elements = row.find_all('td')
        for td in td_elements:
            if td.get('data-img_key') == stars:
                target_rows.append(row)

    for row in target_rows:
        print("Start Checking..................")

        td_elements = row.find_all('td')

        event_datetime_string = td_elements[0].text

        event_name = td_elements[3].text
        actual = td_elements[4].text
        forecast = td_elements[5].text
        previous = td_elements[6].text


        # Calculate the time difference
        rest_time = get_rest_time(event_datetime_string)
        print(f"Rest time: {rest_time} minutes for {event_name} event")

        rest_time = 30


        if rest_time == 30:
            await send_message_before_event(event_name, rest_time, actual, forecast, previous)

        
        if rest_time == 0:
            await send_message_start_event(event_name, datetime.now().strftime("%H:%M"), actual, forecast, previous)


async def run_main_periodically():
    while True:
        await main()
        await asyncio.sleep(60)

# Run the main function infinitely every 60 seconds
asyncio.run(run_main_periodically())
    
   
 


