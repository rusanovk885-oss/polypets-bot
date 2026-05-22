import asyncio
import random
import json
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

TOKEN = "8085068905:AAE1ceefPTGc94jEaFgUVP7tUO9famyzKZ4"
MASTER_ADMIN_ID = 6900319945
POLINA_ID = 8428411159
DATA_FILE = "poly_bot_data.json"

PETS = {
    "kurochka": {"name": "🐔 Курица", "price": 50, "income": 2, "max_hunger": 100, "emoji": "🐔"},
    "krokodil": {"name": "🐊 Крокодил", "price": 120, "income": 5, "max_hunger": 80, "emoji": "🐊"},
    "hamster": {"name": "🐹 Хомяк", "price": 80, "income": 3, "max_hunger": 90, "emoji": "🐹"},
    "drakosha": {"name": "🐉 Дракон", "price": 200, "income": 10, "max_hunger": 120, "emoji": "🐉"},
    "cat": {"name": "🐱 Кот", "price": 150, "income": 7, "max_hunger": 85, "emoji": "🐱"}
}

FOOD = {
    "seed": {"name": "🌽 Зерно", "price": 5, "restore": 15, "emoji": "🌽"},
    "meat": {"name": "🍖 Мясо", "price": 15, "restore": 35, "emoji": "🍖"},
    "candy": {"name": "🍭 Конфета", "price": 8, "restore": 20, "emoji": "🍭"},
    "cake": {"name": "🍰 Торт", "price": 25, "restore": 50, "emoji": "🍰"}
}

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

users_db = load_data()

def get_user(user_id):
    uid = str(user_id)
    if uid not in users_db:
        users_db[uid] = {
            "dubli": 150,
            "pets": ["kurochka"],
            "active_pet": "kurochka",
            "hunger": {"kurochka": 100},
            "inventory": {"seed": 3, "meat": 1},
            "last_daily": None,
            "username": None
        }
        save_data(users_db)
    return users_db[uid]

def save_user(user_id, data):
    users_db[str(user_id)] = data
    save_data(users_db)

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: Message):
    user_id = message.from_user.id
    user = get_user(user_id)
    text = f"🎮 Бот для Поляшки\n\n💰 Дублей: {user['dubli']}\n🐾 Питомцев: {len(user['pets'])}"
    await message.answer(text, reply_markup=main_kb())

@dp.message(Command("id"))
async def show_id(message: Message):
    await message.answer(f"ID: {message.from_user.id}")

def main_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🐾 Мои питомцы", callback_data="my_pets")],
        [InlineKeyboardButton(text="🏪 Магазин", callback_data="shop_menu")],
        [InlineKeyboardButton(text="🍗 Покормить", callback_data="feed_menu")],
        [InlineKeyboardButton(text="🎮 Игры", callback_data="games_menu")],
        [InlineKeyboardButton(text="🎁 Бонус", callback_data="daily")],
        [InlineKeyboardButton(text="💎 Дубли", callback_data="my_dublis")]
    ])

def shop_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🐾 Купить питомца", callback_data="pet_shop")],
        [InlineKeyboardButton(text="🍗 Купить еду", callback_data="food_shop")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_main")]
    ])

def pet_shop_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[])
    for pet_id, pet in PETS.items():
        kb.inline_keyboard.append([InlineKeyboardButton(text=f"{pet['emoji']} {pet['name']} — {pet['price']}💎", callback_data=f"buy_pet_{pet_id}")])
    kb.inline_keyboard.append([InlineKeyboardButton(text="◀️ Назад", callback_data="shop_menu")])
    return kb

def games_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎲 Орёл/Решка (10💎)", callback_data="game_coin")],
        [InlineKeyboardButton(text="🔢 Угадай число (5💎)", callback_data="game_number")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_main")]
    ])

@dp.callback_query()
async def handle_callback(call: CallbackQuery):
    user_id = call.from_user.id
    user = get_user(user_id)
    data = call.data

    if data == "back_main":
        await call.message.edit_text(f"💰 Дублей: {user['dubli']}", reply_markup=main_kb())
    
    elif data == "my_dublis":
        await call.answer(f"{user['dubli']} дублей")
    
    elif data == "my_pets":
        text = "🐾 Твои питомцы:\n"
        for pet_id in user["pets"]:
            pet = PETS[pet_id]
            text += f"{pet['emoji']} {pet['name']}\n"
        await call.message.edit_text(text, reply_markup=main_kb())
    
    elif data == "shop_menu":
        await call.message.edit_text("🏪 Магазин", reply_markup=shop_menu_kb())
    
    elif data == "pet_shop":
        await call.message.edit_text("🐾 Купить питомца:", reply_markup=pet_shop_kb())
    
    elif data.startswith("buy_pet_"):
        pet_id = data.split("_")[2]
        pet = PETS[pet_id]
        if pet_id in user["pets"]:
            await call.answer("Уже есть")
        elif user["dubli"] >= pet["price"]:
            user["dubli"] -= pet["price"]
            user["pets"].append(pet_id)
            user["hunger"][pet_id] = 100
            save_user(user_id, user)
            await call.answer(f"Куплен {pet['name']}")
            await call.message.edit_text(f"✅ {pet['name']} куплен!", reply_markup=main_kb())
        else:
            await call.answer(f"Нужно {pet['price']}💎")
    
    elif data == "games_menu":
        await call.message.edit_text("🎮 Игры:", reply_markup=games_menu_kb())
    
    elif data == "game_coin":
        if user["dubli"] < 10:
            await call.answer("Не хватает 10 дублей")
            return
        result = random.choice(["орел", "решка"])
        user_choice = random.choice(["орел", "решка"])
        if result == user_choice:
            user["dubli"] += 10
            msg = f"🎉 {result}! +10 дублей"
        else:
            user["dubli"] -= 10
            msg = f"😔 {result}! -10 дублей"
        save_user(user_id, user)
        await call.answer(msg)
        await call.message.edit_text(f"{msg}\n💰 {user['dubli']}💎", reply_markup=games_menu_kb())
    
    elif data == "game_number":
        if user["dubli"] < 5:
            await call.answer("Не хватает 5 дублей")
            return
        number = random.randint(1, 10)
        user_num = random.randint(1, 10)
        if number == user_num:
            reward = random.randint(5, 25)
            user["dubli"] += reward
            msg = f"🔢 Число {number}! +{reward} дублей"
        else:
            user["dubli"] -= 5
            msg = f"🔢 Число {number}, ты {user_num}. -5 дублей"
        save_user(user_id, user)
        await call.answer(msg)
        await call.message.edit_text(f"{msg}\n💰 {user['dubli']}💎", reply_markup=games_menu_kb())
    
    elif data == "daily":
        last = user.get("last_daily")
        today = datetime.now().date().isoformat()
        if last == today:
            await call.answer("Бонус уже получен")
        else:
            bonus = random.randint(30, 80)
            user["dubli"] += bonus
            user["last_daily"] = today
            save_user(user_id, user)
            await call.answer(f"+{bonus} дублей!")

async def main():
    print("✅ Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
