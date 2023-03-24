import asyncio
import locale

from aiogram import Bot, Dispatcher, executor
from config import Config
from news_parser import get_news


locale.setlocale(locale.LC_TIME, "Russian")

bot = Bot(token=Config.TELEGRAM_TOKEN)
dp = Dispatcher(bot)


async def check_news():
    last_news = None

    while True:
        await asyncio.sleep(60 * 5)

        news = (await get_news())[0]

        if last_news == news:
            continue

        last_news = news
        message_text = f"НОВАЯ НОВОСТЬ В WORLD OF TANKS\n" \
                       f"Заголовок: [{news.title}]({news.url})\n" \
                       f"Дата: {news.date.strftime('%Y, %d %B, %H:%M')}"

        await bot.send_message(Config.NEWS_CHAT_ID, message_text,
                               parse_mode="Markdown",
                               disable_web_page_preview=True)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(check_news())
    executor.start_polling(dp, loop=loop, skip_updates=True)
