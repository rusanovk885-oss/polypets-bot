import asyncio
import random
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# ========== ТОКЕН (ВСТАВЛЕН ТВОЙ) ==========
TOKEN = "8949697674:AAHAZywQYpmpYzx4BE2LJY1JiGC76WxWRx4"

# ========== ID ==========
MASTER_ADMIN_ID = 6900319945
POLINA_ID = 8428411159

# ========== ПИТОМЦЫ ==========
PETS = {
    "kurochka": {"name": "🐔 Курица", "price": 50, "income": 2, "emoji": "🐔"},
    "krokodil": {"name": "🐊 Крокодил", "price": 120, "income": 5, "emoji": "🐊"},
    "hamster": {"name": "🐹 Хомяк", "price": 80, "income": 3, "emoji": "🐹"},
    "drakosha": {"name": "🐉 Дракон", "price": 200, "income": 10, "emoji": "🐉"},
    "cat": {"name": "🐱 Кот", "price": 150, "income": 7, "emoji": "🐱"}
}

FOOD = {
    "seed": {"name": "🌽 Зерно", "price": 5, "restore": 15, "emoji": "🌽"},
    "meat": {"name": "🍖 Мясо", "price": 15, "restore": 35, "emoji": "🍖"},
    "candy": {"name": "🍭 Конфета", "price": 8, "restore": 20, "emoji": "🍭"},
    "cake": {"name": "🍰 Торт", "price": 25, "restore": 50, "emoji": "🍰"}
}

users = {}

def get_user(user_id):
    if user_id not in users:
        users[user_id] = {
            "dubli": 150,
            "pets": ["kurochka"],
            "active_pet": "kurochka",
            "inventory": {"seed": 3, "meat": 1},
            "last_daily": None
        }
    return users[user_id]

def main_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🐾 Мои питомцы", callback_data="my_pets")],
        [InlineKeyboardButton(text="🏪 Магазин", callback_data="shop_menu")],
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

def food_shop_kb(user):
    kb = InlineKeyboardMarkup(inline_keyboard=[])
    for food_id, food in FOOD.items():
        count = user["inventory"].get(food_id, 0)
        kb.inline_keyboard.append([InlineKeyboardButton(text=f"{food['emoji']} {food['name']} — {food['price']}💎 ({count}шт)", callback_data=f"buy_food_{food_id}")])
    kb.inline_keyboard.append([InlineKeyboardButton(text="◀️ Назад", callback_data="shop_menu")])
    return kb

def games_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎲 Орёл/Решка (10💎)", callback_data="game_coin")],
        [InlineKeyboardButton(text="🔢 Угадай число (5-25💎)", callback_data="game_number")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_main")]
    ])

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: Message):
    user = get_user(message.from_user.id)
    await message.answer(f"🎮 Бот для Поляшки\n\n💰 Дублей: {user['dubli']}\n🐾 Питомцев: {len(user['pets'])}", reply_markup=main_kb())

@dp.message(Command("id"))
async def show_id(message: Message):
    await message.answer(f"Твой ID: {message.from_user.id}")

@dp.callback_query()
async def handle_callback(call: CallbackQuery):
    user = get_user(call.from_user.id)
    data = call.data

    if data == "back_main":
        await call.message.edit_text(f"💰 Дублей: {user['dubli']}", reply_markup=main_kb())
    
    elif data == "my_dublis":
        await call.answer(f"{user['dubli']} дублей")
    
    elif data == "my_pets":
        text = "🐾 Твои питомцы:\n"
        for pet_id in user["pets"]:
            text += f"{PETS[pet_id]['emoji']} {PETS[pet_id]['name']}\n"
        await call.message.edit_text(text, reply_markup=main_kb())
    
    elif data == "shop_menu":
        await call.message.edit_text("🏪 Магазин", reply_markup=shop_menu_kb())
    
    elif data == "pet_shop":
        await call.message.edit_text("🐾 Купить питомца:", reply_markup=pet_shop_kb())
    
    elif data == "food_shop":
        await call.message.edit_text("🍗 Купить еду:", reply_markup=food_shop_kb(user))
    
    elif data.startswith("buy_pet_"):
        pet_id = data.split("_")[2]
        pet = PETS[pet_id]
        if pet_id in user["pets"]:
            await call.answer("Уже есть")
        elif user["dubli"] >= pet["price"]:
            user["dubli"] -= pet["price"]
            user["pets"].append(pet_id)
            await call.answer(f"Куплен {pet['name']}")
            await call.message.edit_text(f"✅ {pet['name']} куплен!", reply_markup=main_kb())
        else:
            await call.answer(f"Нужно {pet['price']}💎")
    
    elif data.startswith("buy_food_"):
        food_id = data.split("_")[2]
        food = FOOD[food_id]
        if user["dubli"] >= food["price"]:
            user["dubli"] -= food["price"]
            user["inventory"][food_id] = user["inventory"].get(food_id, 0) + 1
            await call.answer(f"Куплен {food['name']}")
            await call.message.edit_text(f"✅ {food['name']} в инвентаре", reply_markup=food_shop_kb(user))
        else:
            await call.answer("Не хватает дублей")
    
    elif data == "games_menu":
        await call.message.edit_text("🎮 Выбери игру:", reply_markup=games_menu_kb())
    
    elif data == "game_coin":
        if user["dubli"] < 10:
            await call.answer("Не хватает 10 дублей")
            return
        result = random.choice(["орел", "решка"])
        user_choice = random.choice(["орел", "решка"])
        if result == user_choice:
            user["dubli"] += 10
            msg = f"🎉 {result}! Выиграл +10 дублей"
        else:
            user["dubli"] -= 10
            msg = f"😔 {result}! Проиграл -10 дублей"
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
            msg = f"🔢 Число {number}! Угадал! +{reward} дублей"
        else:
            user["dubli"] -= 5
            msg = f"🔢 Число {number}, ты назвал {user_num}. -5 дублей"
        await call.answer(msg)
        await call.message.edit_text(f"{msg}\n💰 {user['dubli']}💎", reply_markup=games_menu_kb())
    
    elif data == "daily":
        today = datetime.now().date().isoformat()
        if user.get("last_daily") == today:
            await call.answer("Бонус уже получен")
        else:
            bonus = random.randint(30, 80)
            user["dubli"] += bonus
            user["last_daily"] = today
            await call.answer(f"+{bonus} дублей!")
            await call.message.edit_text(f"🎁 +{bonus} дублей!\n💰 {user['dubli']}💎", reply_markup=main_kb())
    
    await call.answer()

async def main():
    print("✅ Бот для Поляшки запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
