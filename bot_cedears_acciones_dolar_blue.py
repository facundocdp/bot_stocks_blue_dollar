from telegram import Bot
import yfinance as yf
import asyncio
import schedule
import time
import requests

# Telegram bot configuration
TELEGRAM_TOKEN = '<YOUR_TELEGRAM_TOKEN' # Replace with your token
CHAT_ID = '<YOUR_CHAT_ID>' # Replace with your chat id

# Cedear list
cedears = ['AAPL.BA', 'AMD.BA', 'AMZN.BA', 'AVGO.BA', 'CSCO.BA', 'INTC.BA'] 

# Stocks list
stocks = ['BMA', 'GCAL', 'SUPV'] 

# Get stocks closing prices
def get_stocks():
    message = "📈 **RESUMEN DE ACCIONES AL CIERRE** \n\n"
    for ticker in stocks:
        data = yf.Ticker(ticker).history(period="1d")
        if not data.empty:
            closing = data['Close'].iloc[-1]
            opening = data['Open'].iloc[-1]
            change = (closing - opening) / opening * 100
            if change > 0:
                message += f"✅ {ticker}: subió {change:.2f}%\n"
            elif change == 0:
                message += f"⏸️ {ticker}: sin cambios\n"   
            else:
                message += f"🔻 {ticker}: bajó {change:.2f}%\n"             
        else:
            message += f"⚠️ No se encontraron datos para {ticker}.\n"
    return message    

# Get cedears closing prices
def get_cedears():
    message = "📉 **RESUMEN DE CEDEARS AL CIERRE** \n\n"
    for ticker in cedears:
        data = yf.Ticker(ticker).history(period="1d")
        if not data.empty:
            closing = data['Close'].iloc[-1]
            opening = data['Open'].iloc[-1]
            change = (closing - opening) / opening * 100
            if change > 0:
                message += f"✅ {ticker}: subió {change:.2f}%\n"
            elif change == 0:
                message += f"⏸️ {ticker}: sin cambios\n"   
            else:
                message += f"🔻 {ticker}: bajó {change:.2f}%\n"             
        else:
            message += f"⚠️ No se encontraron datos para {ticker}.\n"
    return message

# Get 'blue dollar' price
def get_blue_dollar_price():
    try:
        response = requests.get('https://api.bluelytics.com.ar/v2/latest')
        if response.status_code == 200:
            data = response.json()
            dolar_blue = data['blue']
            buy = int(dolar_blue['value_buy'])
            sell = int(dolar_blue['value_sell'])
            return f"💵 **DÓLAR BLUE** \nCompra: ${buy}\nVenta: ${sell}\n"
        else:
            return "⚠️ No se pudo obtener el precio del dólar blue.\n"
    except Exception as e:
        return f"⚠️ Error al obtener el precio del dólar blue: {e}\n"    

# Send message function
async def send_message():
    bot = Bot(token=TELEGRAM_TOKEN)
    message_cedears = get_cedears()
    message_stocks = get_stocks()
    message_dolar = get_blue_dollar_price()
    separator = "\n" + "-" * 35 + "\n\n"
    message = message_stocks + separator + message_cedears + separator + message_dolar
    await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='Markdown')

# Asynchronous function to execute scheduled tasks
async def run_schedule():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

# Schedule for message
schedule.every().day.at("18:00").do(lambda: asyncio.create_task(send_message()))

# Main program
async def main():
    print("Bot is running...")
    await run_schedule()

# Execute script
if __name__ == '__main__':
    asyncio.run(main())
