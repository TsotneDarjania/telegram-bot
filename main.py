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
chat_id = '-1002014070164'
# # for testing
# chat_id = '-1002130774666'
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
    "Initial Jobless Claims": "სამსახურის მაძიებელთა ინდექსი ზომავს იმ პირთა რაოდენობას, ვინც პირველად მოითხოვა უმუშევრობის დაზღვევა გასული კვირის განმავლობაში. ეს არის აშშ-ს ყველაზე ადრეული ეკონომიკური მონაცემები, მაგრამ ბაზრის გავლენა კვირიდან კვირამდე იცვლება.",
    "Existing Home Sales" : "არსებული სახლების გაყიდვები - არსებული სახლების გაყიდვები ზომავს ცვლილებას არსებული საცხოვრებელი კორპუსების წლიურ რაოდენობაში, რომლებიც გაიყიდა წინა თვეში. ეს ანგარიში ხელს უწყობს აშშ-ს საბინაო ბაზრის სიძლიერის შეფასებას და წარმოადგენს საერთო ეკონომიკური სიძლიერის ძირითად ინდიკატორს.",
    "Crude Oil Inventories" : "ენერგეტიკის ინფორმაციის ადმინისტრაციის (EIA) ნედლი ნავთობის მარაგები ზომავს ყოველკვირეულ ცვლილებას ბარელი კომერციული ნედლი ნავთობის რაოდენობაში, რომელსაც ფლობენ ამერიკული ფირმები. მარაგების დონე გავლენას ახდენს ნავთობპროდუქტების ფასზე, რამაც შეიძლება გავლენა მოახდინოს ინფლაციაზე.",
    "Federal Open Market Committee (FOMC) Meeting Minutes" : "ფედერალური ღია ბაზრის კომიტეტიs შეხვედრა - ფედერალური ღია ბაზრის კომიტეტის (FOMC) შეხვედრის ოქმი წარმოადგენს კომიტეტის პოლიტიკის შედგენის შეხვედრის დეტალურ ჩანაწერს, რომელიც იმართება დაახლოებით სამი კვირით ადრე. ოქმები დეტალურ ინფორმაციას გვთავაზობს FOMC-ის პოზიციას მონეტარული პოლიტიკის მიმართ, ამიტომ ვალუტზე მოვაჭრეები ყურადღებით ამოწმებენ მათ სამომავლო საპროცენტო განაკვეთის გადაწყვეტილების შედეგებთან დაკავშირებით.",
    "Initial Jobless Claims" : " სამსახურის მაძიებელთა ინდექსი ზომავს იმ პირთა რაოდენობას, ვინც პირველად მოითხოვა უმუშევრობის დაზღვევა გასული კვირის განმავლობაში. ეს არის აშშ-ს ყველაზე ადრეული ეკონომიკური მონაცემები, მაგრამ ბაზრის გავლენა კვირიდან კვირამდე იცვლება.",
    "S&P Global US Manufacturing PMI" : "ზომავს შესყიდვების მენეჯერების აქტივობის დონეს წარმოების სექტორში. 50-ზე მეტი მაჩვენებელი მიუთითებს სექტორის გაფართოებაზე; 50-ზე ქვემოთ მიუთითებს შესყიდვების შემცირებას.",
    "S&P Global Services PMI" : "სერვისის PMI გამოშვებას ყოველთვიურად ახდენს Markit Economics. მონაცემები ეფუძნება კერძო სექტორის მომსახურების კომპანიებში 400-ზე მეტ აღმასრულებელ გამოკითხვას. გამოკითხვები მოიცავს ტრანსპორტსა და კომუნიკაციებს, ფინანსურ შუამავლებს, ბიზნეს და პერსონალურ სერვისებს, გამოთვლებს და IT, სასტუმროებსა და რესტორნებს.",
    "New Home Sales" : "აშშ-ში ახალი სახლის გაყიდვები ზომავს ახალი კერძო სახლების წლიურ რაოდენობას, რომლებიც გაიყიდა წინა თვეში. ამ ანგარიშს უფრო მეტი გავლენა აქვს, როდესაც ის გამოქვეყნდება არსებული სახლის გაყიდვამდე, რადგან ანგარიშები მჭიდროდ არის დაკავშირებული.",
    "Durable Goods Orders (MoM)" : "გრძელვადიანი საქონლის შეკვეთები ზომავს გრძელვადიანი წარმოებული საქონლის ახალი შეკვეთების მთლიანი ღირებულების ცვლილებას, მათ შორის სატრანსპორტო ნივთებს.",
    "CB Consumer Confidence" : " მომხმარებელთა ნდობა ზომავს მომხმარებელთა ნდობის დონეს ეკონომიკური საქმიანობის მიმართ. ის წამყვანი ინდიკატორია, რადგან მას შეუძლია სამომხმარებლო ხარჯების პროგნოზირება, რაც დიდ როლს ასრულებს მთლიან ეკონომიკურ აქტივობაში.",
    "GDP (QoQ)" : "მთლიანი შიდა პროდუქტი (მშპ) ზომავს ეკონომიკის მიერ წარმოებული ყველა საქონლისა და მომსახურების ინფლაციით დარეგულირებული ღირებულების წლიურ ცვლილებას. ეს არის ეკონომიკური აქტივობის ყველაზე ფართო საზომი და ეკონომიკის სიჯანსაღის პირველადი მაჩვენებელი.",
    "Core PCE Price Index (MoM)" : "ძირითადი პირადი მოხმარების ხარჯების (PCE) ფასების ინდექსი ზომავს ცვლილებებს საქონლისა და მომსახურების ფასებში, რომლებიც შეძენილია მომხმარებლების მიერ მოხმარების მიზნით, საკვებისა და ენერგიის გამოკლებით. ფასები შეწონილია მთლიანი დანახარჯების მიხედვით ერთეულზე. ის ზომავს ფასების ცვლილებას მომხმარებლის პერსპექტივიდან. ეს არის მთავარი გზა შესყიდვის ტენდენციებისა და ინფლაციის ცვლილებების გასაზომად.",
    "Core PCE Price Index (YoY)" : "ძირითადი PCE ფასების ინდექსი არის PCE ფასების ინდექსის ნაკლებად არასტაბილური საზომი, რომელიც არ მოიცავს საკვებისა და ენერგიის უფრო არასტაბილურ და სეზონურ ფასებს. ვალუტაზე ზემოქმედება შეიძლება იყოს ორივე მიმართულებით, ინფლაციის ზრდამ შეიძლება გამოიწვიოს საპროცენტო განაკვეთების ზრდა და ადგილობრივი ვალუტის ზრდა, მეორე მხრივ, რეცესიის დროს ინფლაციის ზრდამ შეიძლება გამოიწვიოს რეცესიის გაღრმავება და, შესაბამისად, დაეცემა ადგილობრივ ვალუტაში.",
    "Chicago PMI" : "ჩიკაგოს შესყიდვების მენეჯერების ინდექსი (PMI) განსაზღვრავს წარმოების სექტორის ეკონომიკურ სიჯანსაღეს ჩიკაგოს რეგიონში. 50-ზე მეტი მაჩვენებელი მიუთითებს წარმოების სექტორის გაფართოებაზე; 50-ზე ნაკლები მიუთითებს შესყიდვების შემცირებას. ჩიკაგოს PMI შეიძლება დაგეხმაროთ ISM წარმოების PMI-ის პროგნოზირებაში.",
    "ISM Manufacturing PMI" : "მიწოდების მენეჯმენტის ინსტიტუტის (ISM) წარმოების შესყიდვების მენეჯერების ინდექსის (PMI) ანგარიში ბიზნესზე ეფუძნება მონაცემებს, რომლებიც შედგენილია ყოველთვიური პასუხებიდან 400-ზე მეტ ინდუსტრიულ კომპანიაში შესყიდვებისა და მიწოდების აღმასრულებლების მიერ დასმულ კითხვებზე. თითოეული გაზომილი ინდიკატორისთვის (ახალი შეკვეთები, შეკვეთების ჩამორჩენა, ახალი ექსპორტის შეკვეთები, იმპორტი, წარმოება, მარაგების მიწოდება, მარაგები, მომხმარებლების მარაგები, დასაქმება და ფასები), ეს ანგარიში აჩვენებს თითოეული პასუხის მოხსენების პროცენტს, წმინდა განსხვავებას შორის პასუხების რაოდენობა დადებითი ეკონომიკური მიმართულებით და უარყოფითი ეკონომიკური მიმართულებით და დიფუზიის ინდექსი. პასუხები არის დაუმუშავებელი მონაცემები და არასოდეს იცვლება.",
    "ISM Manufacturing Prices" : "მიწოდების მენეჯმენტის ინსტიტუტის (ISM) წარმოების შესყიდვების მენეჯერების ინდექსის (PMI) ანგარიში ბიზნესზე ეფუძნება მონაცემებს, რომლებიც შედგენილია ყოველთვიური პასუხებიდან 400-ზე მეტ ინდუსტრიულ კომპანიაში შესყიდვებისა და მიწოდების აღმასრულებლების მიერ დასმულ კითხვებზე. თითოეული გაზომილი ინდიკატორისთვის (ახალი შეკვეთები, შეკვეთების ჩამორჩენა, ახალი ექსპორტის შეკვეთები, იმპორტი, წარმოება, მარაგების მიწოდება, მარაგები, მომხმარებლების მარაგები, დასაქმება და ფასები), ეს ანგარიში აჩვენებს თითოეული პასუხის მოხსენების პროცენტს, წმინდა განსხვავებას შორის პასუხების რაოდენობა დადებითი ეკონომიკური მიმართულებით და უარყოფითი ეკონომიკური მიმართულებით და დიფუზიის ინდექსი. პასუხები არის დაუმუშავებელი მონაცემები და არასოდეს იცვლება",
    "JOLTs Job Openings" : "აშშ-ს შრომის სტატისტიკის ბიუროს მიერ ჩატარებული გამოკითხვა ვაკანსიების შესაფასებლად. ის აგროვებს მონაცემებს დამსაქმებლებისგან მათი ბიზნესის დასაქმების, სამუშაო ადგილების გახსნის, დაქირავების, დასაქმებისა და დათხოვის შესახებ."
}

images = {
    "PPI (MoM)": "https://tradershub.ge/wp-content/uploads/2023/03/Logo-site-1.png",
    "Fed Chair Powell": "https://tradershub.ge/wp-content/uploads/2023/03/Logo-site-1.png",
    "Core Retail Sales": "https://tradershub.ge/wp-content/uploads/2023/03/Logo-site-1.png",
    "Crude Oil Inventories": "https://tradershub.ge/wp-content/uploads/2023/03/Logo-site-1.pngე",
    "CPI (YoY)" : "https://tradershub.ge/wp-content/uploads/2023/03/Logo-site-1.png",
    "CPI (MoM)":  "https://tradershub.ge/wp-content/uploads/2023/03/Logo-site-1.png",
    "Initial Jobless Claims": "https://tradershub.ge/wp-content/uploads/2023/03/Logo-site-1.png",
    "Existing Home Sales" : "https://tradershub.ge/wp-content/uploads/2023/03/Logo-site-1.png",
    "Crude Oil Inventories" : "https://tradershub.ge/wp-content/uploads/2023/03/Logo-site-1.png",
    "Federal Open Market Committee (FOMC) Meeting Minutes" : "https://tradershub.ge/wp-content/uploads/2023/03/Logo-site-1.png",
    "Initial Jobless Claims" : "https://tradershub.ge/wp-content/uploads/2023/03/Logo-site-1.png",
    "S&P Global US Manufacturing PMI" : "https://tradershub.ge/wp-content/uploads/2023/03/Logo-site-1.png",
    "S&P Global Services PMI" : "https://tradershub.ge/wp-content/uploads/2023/03/Logo-site-1.png",
    "New Home Sales" : "https://tradershub.ge/wp-content/uploads/2023/03/Logo-site-1.png",
    "Durable Goods Orders (MoM)" : "https://tradershub.ge/wp-content/uploads/2023/03/Logo-site-1.png",
    "CB Consumer Confidence" : "https://tradershub.ge/wp-content/uploads/2023/03/Logo-site-1.png",
    "GDP (QoQ)" : "https://tradershub.ge/wp-content/uploads/2023/03/Logo-site-1.png",
    "Core PCE Price Index (MoM)" : "https://tradershub.ge/wp-content/uploads/2023/03/Logo-site-1.png",
    "Core PCE Price Index (YoY)" : "https://tradershub.ge/wp-content/uploads/2023/03/Logo-site-1.png",
    "Chicago PMI" : "https://tradershub.ge/wp-content/uploads/2023/03/Logo-site-1.png",
    "ISM Manufacturing PMI" : "https://tradershub.ge/wp-content/uploads/2023/03/Logo-site-1.png",
    "ISM Manufacturing Prices" : "https://tradershub.ge/wp-content/uploads/2023/03/Logo-site-1.png",
    "JOLTs Job Openings" : "https://tradershub.ge/wp-content/uploads/2023/03/Logo-site-1.png"
}

description_text = ""
event_time_text = ""

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

def get_image_url(event_name):
    for key in images.keys():
        if key in event_name:
            return images[key]
        else:
            return "https://tradershub.ge/wp-content/uploads/2023/03/Logo-site-1.png"

def get_rest_time(event_time_string):
    global event_time_text
    datetime_str = f"{datetime.now().date()} {event_time_string}"
    event_datetime = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
    event_datetime += timedelta(hours=hour_difference)
    current_datetime = datetime.now()
    current_datetime += timedelta(hours=4)
    # print("current_detatime ",current_datetime)
    event_time_text = event_datetime.strftime("%H:%M")

    # Calculate difference in time
    time_difference = event_datetime - current_datetime
    total_minutes = time_difference.total_seconds() // 60
    return total_minutes

async def send_message_before_event(event_name, time_difference, actual, forecast, previous):
    description_text = get_description_text(event_name)
    image_url = get_image_url(event_name)
    
    flag = "🇺🇸"
    current_value_str = re.sub(r'[^\d.]', '', actual) if actual else None
    forecast_value_str = re.sub(r'[^\d.]', '', forecast) if forecast else None

    if(current_value_str == "" or forecast_value_str == ""):
         message = f"{flag}<b>{event_name}</b>\n🕒 დაიწყება {time_difference} წუთში\n\n"
    else:
        message = f"{flag}<b>{event_name}</b>\n🕒 დაიწყება {time_difference} წუთში\n\n<b>აღწერა</b>: {description_text}\n\n<b>ფაქტობრივი:</b> {actual}\n<b>პროგნოზი:</b> {forecast}\n<b>წინა:</b> {previous}"

    # Send a message with the image to the chat
    await bot.sendPhoto(chat_id=chat_id,parse_mode=ParseMode.HTML, photo=image_url, caption=message)

async def send_message_start_event(event_name,event_time, actual, forecast, previous):
    description_text = get_description_text(event_name)
    image_url = get_image_url(event_name)
    
    current_value_str = re.sub(r'[^\d.]', '', actual) if actual else None
    forecast_value_str = re.sub(r'[^\d.]', '', forecast) if forecast else None

    extraText = ""
    flag = "🇺🇸"
    smallIcon = ""

    if current_value_str == "" or forecast_value_str == "":
        message = f"<b>{flag}{event_name}</b>\n🕒 მიმდინარეობს ამჟამად\nთარიღი:{event_time_text}\n\n{flag} <b>აღწერა:</b> {description_text}"         
    else:
        message = f"<b>{flag}{event_name}</b>\n🕒 მიმდინარეობს ამჟამად\nთარიღი:{event_time_text}\n\n{flag} <b>აღწერა:</b> {description_text}\n\n{flag}<b>ფაქტობრივი:</b> {actual}\n{flag}<b>პროგნოზი:</b> {forecast}\n{flag}<b>წინა:</b> {previous}\n\n{smallIcon}  {extraText}"

        if float(current_value_str) > float(forecast_value_str):
            smallIcon = "🐂"
            extraText = "<b>ხარისებრი პოზიცია </b> მოსალოდნელზე მაღალი მაჩვენებელი უნდა იქნას მიღებული, როგორც დადებითი/ აშშ დოლარისთვის."
        else:
            smallIcon = "🐻"
            extraText = "<b>დათვისებრი პოზიცია </b> მოსალოდნელზე დაბალი მაჩვენებელი უნდა იქნას მიღებული, როგორც აშშ დოლარის უარყოფითი/პოზიცია"
    
    
    # Send a message with the image to the chat
    await bot.sendPhoto(chat_id=chat_id, parse_mode=ParseMode.HTML, photo=image_url, caption=message)


async def main():
    print("start working... at ", datetime.now())
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
        # print("Start Checking..................")
        td_elements = row.find_all('td')

        event_datetime_string = td_elements[0].text

        event_name = td_elements[3].text
        actual = td_elements[4].text
        forecast = td_elements[5].text
        previous = td_elements[6].text


        # calculate rest time
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

asyncio.run(run_main_periodically())


