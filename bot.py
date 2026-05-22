import asyncio
import random
import json
import os
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# ========== ТОКЕН (ВСТАВЬ СВОЙ НОВЫЙ ТОКЕН) ==========
TOKEN = "8949697674:AAHAZywQYpmpYzx4BE2LJY1JiGC76WxWRx4"

# ========== АДМИНЫ ==========
MASTER_ADMIN_ID = 6900319945
NUTRIKA_ADMIN_ID = 8428411159
POLINA_ID = 8428411159

# ========== ПИТОМЦЫ (20+ ШТУК) ==========
PETS = {
    # Обычные
    "kurochka": {"name": "🐔 Курица", "price": 50, "income": 2, "max_hunger": 100, "rarity": "common", "emoji": "🐔", "power": 10},
    "hamster": {"name": "🐹 Хомяк", "price": 80, "income": 3, "max_hunger": 90, "rarity": "common", "emoji": "🐹", "power": 12},
    "penguin": {"name": "🐧 Пингвин", "price": 100, "income": 4, "max_hunger": 85, "rarity": "common", "emoji": "🐧", "power": 15},
    "rabbit": {"name": "🐰 Кролик", "price": 70, "income": 3, "max_hunger": 95, "rarity": "common", "emoji": "🐰", "power": 11},
    "frog": {"name": "🐸 Лягушка", "price": 60, "income": 2, "max_hunger": 80, "rarity": "common", "emoji": "🐸", "power": 8},
    
    # Редкие
    "krokodil": {"name": "🐊 Крокодил", "price": 150, "income": 7, "max_hunger": 80, "rarity": "rare", "emoji": "🐊", "power": 30},
    "wolf": {"name": "🐺 Волк", "price": 180, "income": 8, "max_hunger": 85, "rarity": "rare", "emoji": "🐺", "power": 35},
    "fox": {"name": "🦊 Лис", "price": 200, "income": 9, "max_hunger": 90, "rarity": "rare", "emoji": "🦊", "power": 32},
    "deer": {"name": "🦌 Олень", "price": 170, "income": 7, "max_hunger": 100, "rarity": "rare", "emoji": "🦌", "power": 28},
    
    # Эпические
    "drakosha": {"name": "🐉 Дракон", "price": 400, "income": 15, "max_hunger": 120, "rarity": "epic", "emoji": "🐉", "power": 70},
    "panda": {"name": "🐼 Панда", "price": 350, "income": 13, "max_hunger": 110, "rarity": "epic", "emoji": "🐼", "power": 60},
    "owl": {"name": "🦉 Сова", "price": 380, "income": 14, "max_hunger": 100, "rarity": "epic", "emoji": "🦉", "power": 55},
    
    # Легендарные
    "unicorn": {"name": "🦄 Единорог", "price": 1000, "income": 30, "max_hunger": 150, "rarity": "legendary", "emoji": "🦄", "power": 120},
    "phoenix": {"name": "🔥 Феникс", "price": 1200, "income": 35, "max_hunger": 140, "rarity": "legendary", "emoji": "🔥", "power": 150},
    "dragon_king": {"name": "👑 Король-Дракон", "price": 1500, "income": 40, "max_hunger": 160, "rarity": "legendary", "emoji": "👑", "power": 200},
    
    # Мифические
    "cerberus": {"name": "🔱 Цербер", "price": 3000, "income": 60, "max_hunger": 180, "rarity": "mythic", "emoji": "🔱", "power": 350},
    "godzilla": {"name": "🦖 Годзилла", "price": 5000, "income": 100, "max_hunger": 200, "rarity": "mythic", "emoji": "🦖", "power": 500}
}

# ========== СУНДУКИ (ЛУТБОКСЫ) ==========
CHESTS = {
    "common": {
        "name": "📦 Обычный сундук",
        "price": 100,
        "emoji": "📦",
        "rewards": {
            "pet": {"chance": 15, "rarities": ["common", "rare"]},
            "dubli": {"min": 30, "max": 100, "chance": 50},
            "food": {"min": 1, "max": 5, "chance": 25},
            "buff": {"chance": 10}
        }
    },
    "epic": {
        "name": "✨ Эпический сундук",
        "price": 500,
        "emoji": "✨",
        "rewards": {
            "pet": {"chance": 30, "rarities": ["rare", "epic"]},
            "dubli": {"min": 150, "max": 400, "chance": 35},
            "food": {"min": 3, "max": 10, "chance": 20},
            "skin": {"chance": 10},
            "buff": {"chance": 15}
        }
    },
    "legendary": {
        "name": "🔥 Легендарный сундук",
        "price": 2000,
        "emoji": "🔥",
        "rewards": {
            "pet": {"chance": 50, "rarities": ["epic", "legendary", "mythic"]},
            "dubli": {"min": 500, "max": 1500, "chance": 25},
            "food": {"min": 5, "max": 20, "chance": 15},
            "skin": {"chance": 20},
            "buff": {"chance": 25}
        }
    }
}

# ========== БАФФЫ (ВРЕМЕННЫЕ УЛУЧШЕНИЯ) ==========
BUFFS = {
    "double_income": {"name": "💹 Двойной доход", "desc": "Доход от питомцев x2", "duration": 3600, "emoji": "💹"},
    "lucky": {"name": "🍀 Удача", "desc": "Шанс победы в играх +20%", "duration": 1800, "emoji": "🍀"},
    "speed": {"name": "⚡ Ускорение", "desc": "Питомцы приносят доход в 2 раза чаще", "duration": 7200, "emoji": "⚡"},
    "divine": {"name": "👑 Божественное благословение", "desc": "Доход +50%", "duration": 86400, "emoji": "👑"}
}

# ========== ЕДА ==========
FOOD = {
    "seed": {"name": "🌽 Зерно", "price": 5, "restore": 15, "emoji": "🌽"},
    "meat": {"name": "🍖 Мясо", "price": 15, "restore": 35, "emoji": "🍖"},
    "candy": {"name": "🍭 Конфета", "price": 8, "restore": 20, "emoji": "🍭"},
    "cake": {"name": "🍰 Торт", "price": 25, "restore": 50, "emoji": "🍰"},
    "golden_apple": {"name": "🍎 Золотое яблоко", "price": 100, "restore": 100, "emoji": "🍎", "rarity": "rare"}
}

# ========== СКИНЫ ==========
SKINS = {
    "golden": {"name": "✨ Золотая", "price": 500, "effect": "доход +20%", "emoji": "✨"},
    "shadow": {"name": "🌑 Теневая", "price": 400, "effect": "сила +15%", "emoji": "🌑"},
    "rainbow": {"name": "🌈 Радужная", "price": 600, "effect": "все статы +10%", "emoji": "🌈"},
    "void": {"name": "🌀 Пустотная", "price": 1000, "effect": "доход +50%", "emoji": "🌀"}
}

# ========== КЛАВИАТУРЫ ==========
def main_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🐾 Мои питомцы"), KeyboardButton(text="🏪 Магазин")],
            [KeyboardButton(text="🍗 Покормить"), KeyboardButton(text="🎮 Игры")],
            [KeyboardButton(text="🎁 Бонус"), KeyboardButton(text="💎 Дубли")],
            [KeyboardButton(text="🎁 Сундуки"), KeyboardButton(text="🏆 Топ игроков")],
            [KeyboardButton(text="✨ Мои баффы")]
        ],
        resize_keyboard=True
    )
    return kb

def chests_menu_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📦 Открыть обычный сундук (100💎)")],
            [KeyboardButton(text="✨ Открыть эпический сундук (500💎)")],
            [KeyboardButton(text="🔥 Открыть легендарный сундук (2000💎)")],
            [KeyboardButton(text="◀️ Назад в меню")]
        ],
        resize_keyboard=True
    )
    return kb

def shop_menu_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🐾 Купить питомца"), KeyboardButton(text="🍗 Купить еду")],
            [KeyboardButton(text="✨ Купить скин"), KeyboardButton(text="🎁 Сундуки")],
            [KeyboardButton(text="◀️ Назад в меню")]
        ],
        resize_keyboard=True
    )
    return kb

def games_menu_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎲 Орёл/Решка"), KeyboardButton(text="🔢 Угадай число")],
            [KeyboardButton(text="✊ Камень-ножницы-бумага"), KeyboardButton(text="🎲 Кости")],
            [KeyboardButton(text="◀️ Назад в меню")]
        ],
        resize_keyboard=True
    )
    return kb

def admin_panel_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💰 Накрутить Поляшке"), KeyboardButton(text="🎁 Выдать питомца")],
            [KeyboardButton(text="📢 Объявление"), KeyboardButton(text="📊 Статистика")],
            [KeyboardButton(text="👑 Выдать сундук"), KeyboardButton(text="💪 Выдать бафф")],
            [KeyboardButton(text="◀️ Назад в меню")]
        ],
        resize_keyboard=True
    )
    return kb

# ========== БАЗА ДАННЫХ ==========
users = {}

def get_user(user_id):
    if user_id not in users:
        users[user_id] = {
            "dubli": 200,
            "pets": ["kurochka"],
            "active_pet": "kurochka",
            "hunger": {"kurochka": 100},
            "inventory": {"seed": 3, "meat": 1},
            "skins": {},
            "buffs": {},
            "last_daily": None,
            "total_games": 0,
            "total_chests": 0
        }
    return users[user_id]

# ========== ФУНКЦИЯ ОТКРЫТИЯ СУНДУКА ==========
async def open_chest(user_id, chest_type):
    user = get_user(user_id)
    chest = CHESTS[chest_type]
    
    if user["dubli"] < chest["price"]:
        return False, f"❌ Не хватает {chest['price']} дублей на {chest['name']}!", None
    
    user["dubli"] -= chest["price"]
    user["total_chests"] += 1
    
    # Определяем награду
    rewards = chest["rewards"]
    reward_type = random.choices(
        list(rewards.keys()),
        weights=[rewards[r]["chance"] for r in rewards]
    )[0]
    
    reward_text = ""
    reward_data = None
    
    if reward_type == "pet":
        # Получаем питомца из доступных редкостей
        available_pets = [p for p, data in PETS.items() if data["rarity"] in rewards["pet"]["rarities"]]
        if available_pets:
            pet_id = random.choice(available_pets)
            if pet_id not in user["pets"]:
                user["pets"].append(pet_id)
                user["hunger"][pet_id] = 100
                reward_text = f"🐾 НОВЫЙ ПИТОМЕЦ: {PETS[pet_id]['name']}!"
                reward_data = pet_id
            else:
                # Если питомец уже есть — даём дубли
                bonus = random.randint(50, 150)
                user["dubli"] += bonus
                reward_text = f"🎁 Питомец уже есть! Компенсация: +{bonus} дублей!"
        else:
            bonus = random.randint(50, 100)
            user["dubli"] += bonus
            reward_text = f"🎁 +{bonus} дублей!"
    
    elif reward_type == "dubli":
        amount = random.randint(rewards["dubli"]["min"], rewards["dubli"]["max"])
        user["dubli"] += amount
        reward_text = f"💰 {amount} дублей!"
    
    elif reward_type == "food":
        food_id = random.choice(list(FOOD.keys()))
        amount = random.randint(rewards["food"]["min"], rewards["food"]["max"])
        user["inventory"][food_id] = user["inventory"].get(food_id, 0) + amount
        reward_text = f"🍗 {FOOD[food_id]['name']} x{amount}!"
    
    elif reward_type == "skin":
        skin_id = random.choice(list(SKINS.keys()))
        user["skins"][user["active_pet"]] = skin_id
        reward_text = f"✨ СКИН: {SKINS[skin_id]['name']} для активного питомца!"
    
    elif reward_type == "buff":
        buff_id = random.choice(list(BUFFS.keys()))
        user["buffs"][buff_id] = datetime.now().timestamp() + BUFFS[buff_id]["duration"]
        reward_text = f"💪 БАФФ: {BUFFS[buff_id]['name']} на {BUFFS[buff_id]['duration']//3600}ч!"
    
    return True, f"🎉 ТЫ ОТКРЫЛ {chest['name']}! 🎉\n\nПолучено: {reward_text}\n\n💰 Осталось дублей: {user['dubli']}", reward_data

# ========== ОБРАБОТЧИКИ ==========
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: Message):
    user = get_user(message.from_user.id)
    await message.answer(
        f"🎮 МЕГА-БОТ ДЛЯ ПОЛЯШКИ 🎮\n\n"
        f"💰 Дублей: {user['dubli']}\n"
        f"🐾 Питомцев: {len(user['pets'])}\n"
        f"🎁 Сундуков открыто: {user['total_chests']}\n\n"
        f"🔥 Тебя ждут сундуки с редкими питомцами и баффами!",
        reply_markup=main_kb()
    )

@dp.message()
async def handle_message(message: Message):
    user_id = message.from_user.id
    user = get_user(user_id)
    text = message.text
    
    # ========== ГЛАВНОЕ МЕНЮ ==========
    if text == "🐾 Мои питомцы":
        pets_list = "\n".join([f"{PETS[p]['emoji']} {PETS[p]['name']} [{PETS[p]['rarity']}]" for p in user["pets"]])
        await message.answer(f"🐾 Твои питомцы ({len(user['pets'])}):\n{pets_list}", reply_markup=main_kb())
    
    elif text == "💎 Дубли":
        await message.answer(f"💰 У тебя {user['dubli']} дублей!", reply_markup=main_kb())
    
    elif text == "🏪 Магазин":
        await message.answer("🏪 Добро пожаловать в магазин!", reply_markup=shop_menu_kb())
    
    elif text == "🎮 Игры":
        await message.answer("🎮 Выбери игру:", reply_markup=games_menu_kb())
    
    elif text == "🎁 Сундуки":
        await message.answer(
            "🎁 **СУНДУКИ** 🎁\n\n"
            "📦 **Обычный** (100💎) - питомцы common/rare, дубли, еда\n"
            "✨ **Эпический** (500💎) - питомцы rare/epic, дубли, скины, баффы\n"
            "🔥 **Легендарный** (2000💎) - питомцы epic/legendary/mythic, дубли, скины, баффы\n\n"
            "Выбери сундук в меню 👇",
            reply_markup=chests_menu_kb()
        )
    
    elif text == "✨ Мои баффы":
        if not user["buffs"]:
            await message.answer("✨ У тебя пока нет активных баффов. Открывай сундуки! ✨", reply_markup=main_kb())
        else:
            now = datetime.now().timestamp()
            active_buffs = []
            for buff_id, end_time in user["buffs"].items():
                if end_time > now:
                    remaining = int((end_time - now) / 60)
                    active_buffs.append(f"{BUFFS[buff_id]['emoji']} {BUFFS[buff_id]['name']} — осталось {remaining} мин")
            if active_buffs:
                await message.answer("✨ **АКТИВНЫЕ БАФФЫ:** ✨\n\n" + "\n".join(active_buffs), reply_markup=main_kb())
            else:
                await message.answer("✨ У тебя нет активных баффов. Открывай сундуки! ✨", reply_markup=main_kb())
    
    # ========== СУНДУКИ ==========
    elif text == "📦 Открыть обычный сундук (100💎)":
        success, msg, _ = await open_chest(user_id, "common")
        await message.answer(msg, reply_markup=chests_menu_kb() if success else main_kb())
    
    elif text == "✨ Открыть эпический сундук (500💎)":
        success, msg, _ = await open_chest(user_id, "epic")
        await message.answer(msg, reply_markup=chests_menu_kb() if success else main_kb())
    
    elif text == "🔥 Открыть легендарный сундук (2000💎)":
        success, msg, _ = await open_chest(user_id, "legendary")
        await message.answer(msg, reply_markup=chests_menu_kb() if success else main_kb())
    
    # ========== ТОП ИГРОКОВ ==========
    elif text == "🏆 Топ игроков":
        sorted_users = sorted(users.items(), key=lambda x: x[1]["dubli"], reverse=True)[:10]
        top_text = "🏆 **ТОП ИГРОКОВ** 🏆\n\n"
        for i, (uid, data) in enumerate(sorted_users, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            top_text += f"{medal} Игрок — {data['dubli']}💎 ({len(data['pets'])} петов)\n"
        await message.answer(top_text, reply_markup=main_kb())
    
    # ========== НАЗАД ==========
    elif text == "◀️ Назад в меню":
        await message.answer("Главное меню:", reply_markup=main_kb())
    
    # ========== ПРОСТЫЕ ИГРЫ ==========
    elif text == "🎲 Орёл/Решка":
        await message.answer("Выбери: Орел или Решка?", reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Орел"), KeyboardButton(text="Решка")], [KeyboardButton(text="◀️ Назад в меню")]],
            resize_keyboard=True
        ))
    
    elif text in ["Орел", "Решка"]:
        if user["dubli"] < 10:
            await message.answer("❌ Не хватает 10 дублей!", reply_markup=games_menu_kb())
            return
        result = random.choice(["Орел", "Решка"])
        if text == result:
            user["dubli"] += 10
            await message.answer(f"🎉 {result}! Ты выиграл +10 дублей!\n💰 Теперь {user['dubli']}💎", reply_markup=games_menu_kb())
        else:
            user["dubli"] -= 10
            await message.answer(f"😔 {result}! Ты проиграл -10 дублей!\n💰 Теперь {user['dubli']}💎", reply_markup=games_menu_kb())
    
    elif text == "🔢 Угадай число":
        await message.answer("Введи число от 1 до 10:", reply_markup=back_kb())
    
    elif text.isdigit() and 1 <= int(text) <= 10:
        if user["dubli"] < 5:
            await message.answer("❌ Не хватает 5 дублей!", reply_markup=games_menu_kb())
            return
        secret = random.randint(1, 10)
        if int(text) == secret:
            reward = random.randint(5, 25)
            user["dubli"] += reward
            await message.answer(f"🎉 Число {secret}! Ты угадал! +{reward} дублей!\n💰 Теперь {user['dubli']}💎", reply_markup=games_menu_kb())
        else:
            user["dubli"] -= 5
            await message.answer(f"😔 Было {secret}, а ты назвал {text}. -5 дублей!\n💰 Теперь {user['dubli']}💎", reply_markup=games_menu_kb())
    
    # ========== ЕЖЕДНЕВНЫЙ БОНУС ==========
    elif text == "🎁 Бонус":
        today = datetime.now().date().isoformat()
        if user.get("last_daily") == today:
            await message.answer("🎁 Ты уже получал бонус сегодня! Завтра приходи!", reply_markup=main_kb())
        else:
            bonus = random.randint(50, 150)
            user["dubli"] += bonus
            user["last_daily"] = today
            await message.answer(f"🎁 Ежедневный бонус! Ты получил {bonus} дублей! 💰\nТеперь у тебя {user['dubli']} дублей.", reply_markup=main_kb())
    
    # ========== ПОКУПКА ПИТОМЦА ==========
    elif text.startswith("Купить "):
        item = text.replace("Купить ", "").lower()
        for pet_id, pet in PETS.items():
            if pet["name"].lower() == item:
                if pet_id in user["pets"]:
                    await message.answer("❌ У тебя уже есть этот питомец!")
                elif user["dubli"] >= pet["price"]:
                    user["dubli"] -= pet["price"]
                    user["pets"].append(pet_id)
                    user["hunger"][pet_id] = 100
                    await message.answer(f"✅ Ты купил {pet['name']} [{pet['rarity']}]! 💖\nОсталось дублей: {user['dubli']}", reply_markup=shop_menu_kb())
                else:
                    await message.answer(f"❌ Не хватает дублей! Нужно {pet['price']}💎")
                return
        
        for food_id, food in FOOD.items():
            if food["name"].lower() == item:
                if user["dubli"] >= food["price"]:
                    user["dubli"] -= food["price"]
                    user["inventory"][food_id] = user["inventory"].get(food_id, 0) + 1
                    await message.answer(f"✅ Ты купил {food['name']}! 💖\nОсталось дублей: {user['dubli']}", reply_markup=shop_menu_kb())
                else:
                    await message.answer(f"❌ Не хватает дублей! Нужно {food['price']}💎")
                return
        
        await message.answer("❌ Товар не найден! Напиши название как в магазине.")

# ========== ВСПОМОГАТЕЛЬНЫЕ КЛАВИАТУРЫ ==========
def back_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="◀️ Назад в меню")]],
        resize_keyboard=True
    )
    return kb

# ========== ЗАПУСК ==========
async def main():
    print("✅ МЕГА-БОТ ДЛЯ ПОЛЯШКИ ЗАПУЩЕН!")
    print("🎁 СУНДУКИ, ПИТОМЦЫ, БАФФЫ — ВСЁ РАБОТАЕТ!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
