import requests
from bs4 import BeautifulSoup
import telegram
import asyncio
import re;
from datetime import datetime, timedelta

# Current date
current_date = datetime.now().date()

# Telegram bot token
bot_token = '6558911734:AAF25728aE6uYFY5MGtBb3SlyP4ZYf6vRE4'
# Chat ID
chat_id = '5285233665'

hour_defference_canada = 8

# Initialize the Telegram bot
bot = telegram.Bot(token=bot_token)

currency = "USD"

stars = "bull2"

async def send_message():
    while True:
        # URL of the website to scrape
        url = 'https://www.investing.com/economic-calendar/'

        print("Checking for events.....................")

        # Send a GET request to the URL
        response = requests.get(url)

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all tr elements with an id attribute starting with "eventRowId_"
        rows = soup.select('tr[id^="eventRowId_"]')

        currency_rows = []

        for row in rows:
            td_elements = row.find_all('td')
            for td in td_elements[1]:
                if currency in td.text:
                    currency_rows.append(row)

        # only 3 star events
        target_rows = []

        for row in currency_rows:
            td_elements = row.find_all('td')
            for td in td_elements:
                if td.get('data-img_key') == stars:
                    target_rows.append(row)

        for row in target_rows:
            td_elements = row.find_all('td')

            # Extract time from the td element
            time_str = td_elements[0].text
            # time_str = "9:41" # For testing purposes

            # Append current date to time string
            datetime_str = f"{current_date} {time_str}"

            # Convert datetime string to datetime object
            event_datetime = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
            # Add 8 hours becouse of canadian time
            event_datetime += timedelta(hours=hour_defference_canada)
          
            current_datetime = datetime.now()

            # Calculate difference in time
            time_difference = event_datetime - current_datetime

            event_name = td_elements[3].text
            previous = td_elements[6].text
            forecast = td_elements[5].text
            current = td_elements[4].text
  

            # Calculate total minutes from time difference
            total_minutes = time_difference.total_seconds() // 60
            print("Left: ", total_minutes , " event name: ", event_name)
            

            if(total_minutes >= 0):
                if total_minutes == 30:
                    # Convert string to datetime object
                    time_obj = datetime.strptime(td_elements[0].text, "%H:%M")

                    # Add 8 hours
                    new_time_obj = time_obj + timedelta(hours=hour_defference_canada)

                    # Convert back to string
                    new_time_str = new_time_obj.strftime("%H:%M")

                    message = event_name + " is coming out at " + new_time_str + " Forecast: " + forecast + " " + "Previous: " + previous
                    print("Event is coming out in 30 minutes")
                    # Send the message to the bot
                    await bot.send_message(chat_id=chat_id, text=message)

                if total_minutes == 0:
                    print("Event is happening now")
                    color = ""
                    extraText = ""

                   # Handle empty strings
                    current_value_str = re.sub(r'[^\d.]', '', current) if current else None
                    forecast_value_str = re.sub(r'[^\d.]', '', forecast) if forecast else None

                    print("Current: ", current_value_str)
                    print("Forecast: ", forecast_value_str)

                    if current_value_str == "" or forecast_value_str == "":
                        print("Current or forecast value is empty")
                        # previous = "Uknown"
                        # forecast = "Uknown"
                    else:
                        if float(current_value_str) > float(forecast_value_str):
                            color = "🟩"
                            extraText = "Better than expected"
                        else:
                            color = "🟥"
                            extraText = "Worse than expected"
                    
                
                    message = event_name + " is happening now" + " Previous: " + previous + " " + "Forecast: " + forecast + " " + "Current: " + current + " " + color + " " + extraText
                    await bot.send_message(chat_id=chat_id, text=message)

        # Pause execution for 60 seconds before checking again
        await asyncio.sleep(60)

# Start the event loop and run the function
loop = asyncio.get_event_loop()
loop.run_until_complete(send_message())