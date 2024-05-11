import requests
from bs4 import BeautifulSoup
import telegram
import asyncio

from datetime import datetime, timedelta

# Current date
current_date = datetime.now().date()

# Telegram bot token
bot_token = '6558911734:AAF25728aE6uYFY5MGtBb3SlyP4ZYf6vRE4'
# Chat ID
chat_id = '5285233665'

# Initialize the Telegram bot
bot = telegram.Bot(token=bot_token)

async def send_message():
    while True:
        # URL of the website to scrape
        url = 'https://www.investing.com/economic-calendar/'

        print("Checking for events...")

        # Send a GET request to the URL
        response = requests.get(url)

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all tr elements with an id attribute starting with "eventRowId_"
        rows = soup.select('tr[id^="eventRowId_"]')

        american_rows = []

        for row in rows:
            td_elements = row.find_all('td')
            for td in td_elements:
                if 'CNY' in td.text:
                    american_rows.append(row)

        american_rows_with_3_star = []

        for row in american_rows:
            td_elements = row.find_all('td')
            for td in td_elements:
                if td.get('data-img_key') == 'bull2':
                    american_rows_with_3_star.append(row)

        for row in american_rows_with_3_star:
            td_elements = row.find_all('td')

            # Extract time from the td element
            time_str = td_elements[0].text
            # time_str = "17:56" # For testing purposes

            # Append current date to time string
            datetime_str = f"{current_date} {time_str}"

            # Convert datetime string to datetime object
            event_datetime = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
            current_datetime = datetime.now()

            # Calculate difference in time
            time_difference = event_datetime - current_datetime

            event_name = td_elements[3].text
            previous = td_elements[6].text
            forecast = td_elements[5].text
            current = td_elements[4].text

            # Calculate total minutes from time difference
            total_minutes = abs(time_difference.total_seconds()) // 60
            print("Left: ", total_minutes)

            if total_minutes == 30:
                message = event_name + " is coming out at " + td_elements[0].text + " Forecast: " + forecast + " " + "Previous: " + previous
                print("Event is coming out in 30 minutes")
                # Send the message to the bot
                await bot.send_message(chat_id=chat_id, text=message)

            if total_minutes == 0:
                print("Event is happening now")
                color = "🟩"
                message = event_name + " is happening now" + " Previous: " + previous + " " + "Forecast: " + forecast + " " + "Current: " + color + current
                await bot.send_message(chat_id=chat_id, text=message)

        # Pause execution for 60 seconds before checking again
        await asyncio.sleep(60)

# Start the event loop and run the function
loop = asyncio.get_event_loop()
loop.run_until_complete(send_message())