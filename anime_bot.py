import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

BOT_TOKEN ="8771143513:AAF8m7m2G--RIvgjwYZ5fdf6hwjf5tUv1BA

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def search_anime(query: str):
    url = f"https://api.jikan.moe/v4/anime?q={query}&limit=1"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                if data["data"]:
                    return data["data"][0]
    return None

def format_anime(anime: dict) -> str:
    title = anime.get("title", "Noma'lum")
    title_english = anime.get("title_english") or ""
    score = anime.get("score") or "—"
    episodes = anime.get("episodes") or "?"
    status = anime.get("status") or "Noma'lum"
    synopsis = anime.get("synopsis") or "Tavsif yo'q"
    genres = ", ".join([g["name"] for g in anime.get("genres", [])]) or "—"
    year = anime.get("year") or "?"
    anime_type = anime.get("type") or "?"
    url = anime.get("url", "")
    if len(synopsis) > 300:
        synopsis = synopsis[:300] + "..."
    text = f"🎌 <b>{title}</b>\n"
    if title_english and title_english != title:
        text += f"📝 <i>{title_english}</i>\n"
    text += (
        f"\n⭐ Reyting: <b>{score}</b>\n"
        f"📺 Turi: {anime_type}\n"
        f"🎬 Epizodlar: {episodes}\n"
        f"📅 Yil: {year}\n"
        f"📌 Holati: {status}\n"
        f"🏷 Janrlar: {genres}\n"
        f"\n📖 <b>Tavsif:</b>\n{synopsis}\n"
    )
    if url:
        text += f"\n🔗 <a href='{url}'>MyAnimeList da ko'rish</a>"
    return text

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "🎌 <b>Anime Qidiruv Botiga Xush Kelibsiz!</b>\n\n"
        "Anime nomini yozing, men uni topib beraman! 🔍",
        parse_mode="HTML"
    )

@dp.message()
async def find_anime(message: Message):
    query = message.text.strip()
    wait_msg = await message.answer("🔍 Qidiryapman...")
    anime = await search_anime(query)
    await wait_msg.delete()
    if not anime:
        await message.answer(
            f"❌ <b>'{query}'</b> topilmadi.",
            parse_mode="HTML"
        )
        return
    text = format_anime(anime)
    image_url = anime.get("images", {}).get("jpg", {}).get("large_image_url")
    try:
        if image_url:
            await message.answer_photo(
                photo=image_url,
                caption=text,
                parse_mode="HTML"
            )
        else:
            await message.answer(text, parse_mode="HTML")
    except Exception:
        await message.answer(text, parse_mode="HTML")

async def main():
    print("✅ Bot ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
