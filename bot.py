import asyncio
import random
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

# ========== ТОКЕН (ВСТАВЬ СВОЙ) ==========
TOKEN = "8949697674:AAHAZywQYpmpYzx4BE2LJY1JiGC76WxWRx4"

# ========== АДМИНЫ ==========
MASTER_ADMIN_ID = 6900319945
NUTRIKA_ADMIN_ID = 8428411159
POLINA_ID = 8428411159

# ========== ПИТОМЦЫ ==========
PETS = {
    "kurochka": {"name": "🐔 Курица", "price": 50, "income": 2, "emoji": "🐔", "rarity": "common"},
    "krokodil": {"name": "🐊 Крокодил", "price": 120, "income": 5, "emoji": "🐊", "rarity": "rare"},
    "hamster": {"name": "🐹 Хомяк", "price": 80, "income": 3, "emoji": "🐹", "rarity": "common"},
    "drakosha": {"name": "🐉 Дракон", "price": 200, "income": 10, "emoji": "🐉", "rarity": "epic"},
    "cat": {"name": "🐱 Кот", "price": 150, "income": 7, "emoji": "🐱", "rarity": "rare"}
}

# ========== ЕДА ==========
FOOD = {
    "seed": {"name": "🌽 Зерно", "price": 5, "restore": 15, "emoji": "🌽"},
    "meat": {"name": "🍖 Мясо", "price": 15, "restore": 35, "emoji": "🍖"},
    "candy": {"name": "🍭 Конфета", "price": 8, "restore": 20, "emoji": "🍭"},
    "cake": {"name": "🍰 Торт", "price": 25, "restore": 50, "emoji": "🍰"}
}

# ========== СУНДУКИ ==========
CHESTS = {
    "common": {"name": "📦 Обычный", "price": 100},
    "epic": {"name": "✨ Эпический", "price": 500},
    "legendary": {"name": "🔥 Легендарный", "price": 2000}
}

# ========== КВЕСТЫ И ДОСТИЖЕНИЯ ==========
DAILY_QUESTS = [
    {"id": "play_games", "name": "🎮 Игроман", "desc": "Сыграй в 3 игры", "target": 3, "reward": 50},
    {"id": "open_chests", "name": "🎁 Везунчик", "desc": "Открой 2 сундука", "target": 2, "reward": 100},
    {"id": "earn_dubli", "name": "💰 Богач", "desc": "Заработай 200 дублей", "target": 200, "reward": 75},
    {"id": "buy_pet", "name": "🐾 Коллекционер", "desc": "Купи питомца", "target": 1, "reward": 80}
]

ACHIEVEMENTS = [
    {"id": "pet_5", "name": "🐾 Начинающий коллекционер", "desc": "Собрать 5 питомцев", "reward": 200},
    {"id": "pet_10", "name": "🌟 Мастер-коллекционер", "desc": "Собрать 10 питомцев", "reward": 500},
    {"id": "dubli_1000", "name": "💰 Банкир", "desc": "Накопить 1000 дублей", "reward": 300},
    {"id": "games_50", "name": "🎮 Заядлый игрок", "desc": "Сыграть 50 игр", "reward": 400},
    {"id": "chests_20", "name": "🎁 Сундучник", "desc": "Открыть 20 сундуков", "reward": 600}
]

# ========== БАЗА ДАННЫХ ==========
users = {}

def get_user(user_id):
    if user_id not in users:
        users[user_id] = {
            "dubli": 200,
            "pets": ["kurochka"],
            "inventory": {"seed": 3, "meat": 1},
            "last_daily": None,
            "daily_quests": {},
            "achievements": [],
            "stats": {"games_played": 0, "chests_opened": 0, "pets_bought": 1, "dubli_earned": 200}
        }
        # Инициализация квестов
        for quest in DAILY_QUESTS:
            users[user_id]["daily_quests"][quest["id"]] = 0
    return users[user_id]

# ========== ПРОВЕРКА ДОСТИЖЕНИЙ ==========
def check_achievements(user_id):
    user = get_user(user_id)
    new_achievements = []
    
    # Проверяем каждое достижение
    for ach in ACHIEVEMENTS:
        if ach["id"] in user["achievements"]:
            continue
        
        achieved = False
        if ach["id"] == "pet_5" and len(user["pets"]) >= 5:
            achieved = True
        elif ach["id"] == "pet_10" and len(user["pets"]) >= 10:
            achieved = True
        elif ach["id"] == "dubli_1000" and user["dubli"] >= 1000:
            achieved = True
        elif ach["id"] == "games_50" and user["stats"]["games_played"] >= 50:
            achieved = True
        elif ach["id"] == "chests_20" and user["stats"]["chests_opened"] >= 20:
            achieved = True
        
        if achieved:
            user["achievements"].append(ach["id"])
            user["dubli"] += ach["reward"]
            new_achievements.append(ach)
    
    return new_achievements

# ========== ПРОВЕРКА КВЕСТОВ ==========
def check_daily_quests(user_id):
    user = get_user(user_id)
    completed = []
    
    for quest in DAILY_QUESTS:
        progress = user["daily_quests"].get(quest["id"], 0)
        if progress >= quest["target"]:
            # Проверяем, не получена ли уже награда
            if f"{quest['id']}_claimed" not in user:
                user[f"{quest['id']}_claimed"] = True
                user["dubli"] += quest["reward"]
                completed.append(quest)
    
    return completed

# ========== КЛАВИАТУРЫ ==========
def main_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🐾 Мои питомцы"), KeyboardButton(text="🏪 Магазин")],
            [KeyboardButton(text="🎮 Игры"), KeyboardButton(text="🎁 Бонус")],
            [KeyboardButton(text="💎 Дубли"), KeyboardButton(text="🎁 Сундуки")],
            [KeyboardButton(text="🏆 Топ"), KeyboardButton(text="📋 Квесты")],
            [KeyboardButton(text="🏅 Достижения")]
        ],
        resize_keyboard=True
    )
    return kb

def shop_menu_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🐾 Купить питомца"), KeyboardButton(text="🍗 Купить еду")],
            [KeyboardButton(text="🎁 Сундуки"), KeyboardButton(text="◀️ Назад")]
        ],
        resize_keyboard=True
    )
    return kb

def games_menu_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎲 Орёл/Решка"), KeyboardButton(text="🔢 Угадай число")],
            [KeyboardButton(text="◀️ Назад")]
        ],
        resize_keyboard=True
    )
    return kb

def chests_menu_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📦 Обычный (100💎)")],
            [KeyboardButton(text="✨ Эпический (500💎)")],
            [KeyboardButton(text="🔥 Легендарный (2000💎)")],
            [KeyboardButton(text="◀️ Назад")]
        ],
        resize_keyboard=True
    )
    return kb

def master_admin_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👑 АДМИНКА")],
            [KeyboardButton(text="🐾 Мои питомцы"), KeyboardButton(text="🏪 Магазин")],
            [KeyboardButton(text="🎮 Игры"), KeyboardButton(text="🎁 Бонус")],
            [KeyboardButton(text="💎 Дубли"), KeyboardButton(text="🎁 Сундуки")],
            [KeyboardButton(text="🏆 Топ"), KeyboardButton(text="📋 Квесты")],
            [KeyboardButton(text="🏅 Достижения")]
        ],
        resize_keyboard=True
    )
    return kb

def admin_panel_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💰 Накрутить Поляшке"), KeyboardButton(text="🎁 Выдать питомца")],
            [KeyboardButton(text="📢 Объявление"), KeyboardButton(text="📊 Статистика")],
            [KeyboardButton(text="◀️ Назад")]
        ],
        resize_keyboard=True
    )
    return kb

def nutrika_admin_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💰 Накрутить Поляшке")],
            [KeyboardButton(text="🐾 Мои питомцы"), KeyboardButton(text="🏪 Магазин")],
            [KeyboardButton(text="🎮 Игры"), KeyboardButton(text="🎁 Бонус")],
            [KeyboardButton(text="💎 Дубли"), KeyboardButton(text="🎁 Сундуки")],
            [KeyboardButton(text="🏆 Топ"), KeyboardButton(text="📋 Квесты")],
            [KeyboardButton(text="🏅 Достижения")]
        ],
        resize_keyboard=True
    )
    return kb

def back_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="◀️ Назад")]],
        resize_keyboard=True
    )
    return kb

# ========== ФУНКЦИИ ==========
async def open_chest(user_id, chest_type):
    user = get_user(user_id)
    chest = CHESTS[chest_type]
    
    if user["dubli"] < chest["price"]:
        return False, f"❌ Не хватает {chest['price']} дублей на {chest['name']} сундук!"
    
    user["dubli"] -= chest["price"]
    user["stats"]["chests_opened"] += 1
    
    # Обновляем квест
    user["daily_quests"]["open_chests"] = user["daily_quests"].get("open_chests", 0) + 1
    
    # Награда
    reward = random.randint(chest["price"] // 2, chest["price"] * 2)
    user["dubli"] += reward
    
    # Шанс получить питомца
    pet_chance = random.randint(1, 100)
    pet_reward = ""
    if chest_type == "common" and pet_chance <= 20:
        pet_id = random.choice([p for p in PETS if PETS[p]["rarity"] == "common"])
        if pet_id not in user["pets"]:
            user["pets"].append(pet_id)
            pet_reward = f"\n🐾 + {PETS[pet_id]['name']} (новый питомец!)"
    elif chest_type == "epic" and pet_chance <= 30:
        pet_id = random.choice([p for p in PETS if PETS[p]["rarity"] in ["common", "rare"]])
        if pet_id not in user["pets"]:
            user["pets"].append(pet_id)
            pet_reward = f"\n🐾 + {PETS[pet_id]['name']} (новый питомец!)"
    elif chest_type == "legendary" and pet_chance <= 50:
        pet_id = random.choice([p for p in PETS if PETS[p]["rarity"] in ["rare", "epic"]])
        if pet_id not in user["pets"]:
            user["pets"].append(pet_id)
            pet_reward = f"\n🐾 + {PETS[pet_id]['name']} (новый питомец!)"
    
    # Проверяем достижения и квесты
    check_achievements(user_id)
    check_daily_quests(user_id)
    
    return True, f"🎁 Ты открыл {chest['name']} сундук и получил {reward} дублей!{pet_reward}\n💰 Осталось: {user['dubli']}💎"

async def get_top_text():
    players = []
    for uid, data in users.items():
        try:
            chat = await bot.get_chat(uid)
            name = chat.username or chat.first_name or str(uid)
        except:
            name = str(uid)
        players.append((name, data["dubli"], len(data["pets"])))
    players.sort(key=lambda x: x[1], reverse=True)
    
    top_text = "🏆 **ТОП ИГРОКОВ** 🏆\n\n"
    for i, (name, dubli, pets_count) in enumerate(players[:15], 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        if len(name) > 20:
            name = name[:17] + "..."
        top_text += f"{medal} {name} — {dubli}💎 ({pets_count} петов)\n"
    return top_text

# ========== БОТ ==========
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: Message):
    user_id = message.from_user.id
    get_user(user_id)
    
    if user_id == MASTER_ADMIN_ID:
        await message.answer("👑 **Добро пожаловать, ГЛАВНЫЙ АДМИН!** 👑", reply_markup=master_admin_kb())
    elif user_id == NUTRIKA_ADMIN_ID:
        await message.answer("🔧 **Добро пожаловать, АДМИН НАКРУТКИ!** 🔧", reply_markup=nutrika_admin_kb())
    else:
        await message.answer("🎮 **Бот для Поляшки** 🎮\n\nВыполняй квесты, открывай сундуки, собирай питомцев и получай достижения!", reply_markup=main_kb())

@dp.message()
async def handle_message(message: Message):
    user_id = message.from_user.id
    user = get_user(user_id)
    text = message.text
    
    # ========== НАЗАД ==========
    if text == "◀️ Назад":
        if user_id == MASTER_ADMIN_ID:
            await message.answer("Главное меню:", reply_markup=master_admin_kb())
        elif user_id == NUTRIKA_ADMIN_ID:
            await message.answer("Главное меню:", reply_markup=nutrika_admin_kb())
        else:
            await message.answer("Главное меню:", reply_markup=main_kb())
        return
    
    # ========== АДМИНКА ==========
    if text == "👑 АДМИНКА" and user_id == MASTER_ADMIN_ID:
        await message.answer("👑 **АДМИН-ПАНЕЛЬ** 👑", reply_markup=admin_panel_kb())
        return
    
    # ========== КВЕСТЫ ==========
    if text == "📋 Квесты":
        check_daily_quests(user_id)
        today = datetime.now().strftime("%d.%m.%Y")
        quests_text = f"📋 **ЕЖЕДНЕВНЫЕ КВЕСТЫ** ({today}) 📋\n\n"
        
        for quest in DAILY_QUESTS:
            progress = user["daily_quests"].get(quest["id"], 0)
            status = "✅" if progress >= quest["target"] else "⏳"
            quests_text += f"{status} {quest['name']} — {progress}/{quest['target']}\n   {quest['desc']} | Награда: +{quest['reward']}💎\n\n"
        
        await message.answer(quests_text, reply_markup=main_kb())
        return
    
    # ========== ДОСТИЖЕНИЯ ==========
    if text == "🏅 Достижения":
        check_achievements(user_id)
        achievements_text = "🏅 **ДОСТИЖЕНИЯ** 🏅\n\n"
        
        for ach in ACHIEVEMENTS:
            if ach["id"] in user["achievements"]:
                status = "✅"
            else:
                status = "🔒"
            achievements_text += f"{status} {ach['name']}\n   {ach['desc']} | Награда: {ach['reward']}💎\n\n"
        
        await message.answer(achievements_text, reply_markup=main_kb())
        return
    
    # ========== СУНДУКИ ==========
    if text == "🎁 Сундуки":
        await message.answer("🎁 **Выбери сундук:**\n\n📦 Обычный (100💎) — дубли + шанс 20% на обычного питомца\n✨ Эпический (500💎) — дубли + шанс 30% на редкого питомца\n🔥 Легендарный (2000💎) — дубли + шанс 50% на эпического питомца", reply_markup=chests_menu_kb())
        return
    
    if text.startswith("📦 Обычный"):
        success, msg = await open_chest(user_id, "common")
        await message.answer(msg, reply_markup=chests_menu_kb() if success else main_kb())
        return
    
    if text.startswith("✨ Эпический"):
        success, msg = await open_chest(user_id, "epic")
        await message.answer(msg, reply_markup=chests_menu_kb() if success else main_kb())
        return
    
    if text.startswith("🔥 Легендарный"):
        success, msg = await open_chest(user_id, "legendary")
        await message.answer(msg, reply_markup=chests_menu_kb() if success else main_kb())
        return
    
    # ========== МАГАЗИН ==========
    if text == "🏪 Магазин":
        await message.answer("🏪 **Добро пожаловать в магазин!**", reply_markup=shop_menu_kb())
        return
    
    if text == "🐾 Купить питомца":
        pets_list = "\n".join([f"{p['emoji']} {p['name']} [{p['rarity']}] — {p['price']}💎" for p in PETS.values()])
        await message.answer(f"🐾 **Питомцы в магазине:**\n\n{pets_list}\n\nНапиши **Купить [название]**\nПример: Купить Курица", reply_markup=shop_menu_kb())
        return
    
    if text == "🍗 Купить еду":
        food_list = "\n".join([f"{f['emoji']} {f['name']} — {f['price']}💎" for f in FOOD.values()])
        await message.answer(f"🍗 **Еда в магазине:**\n\n{food_list}\n\nНапиши **Купить [название]**\nПример: Купить Зерно", reply_markup=shop_menu_kb())
        return
    
    # ========== ПОКУПКА ==========
    if text.startswith("Купить "):
        item = text.replace("Купить ", "").strip().lower()
        
        # Поиск питомца
        found = False
        for pet_id, pet in PETS.items():
            pet_name_lower = pet["name"].lower().replace("🐔", "").replace("🐊", "").replace("🐹", "").replace("🐉", "").replace("🐱", "").strip()
            item_clean = item.replace("🐔", "").replace("🐊", "").replace("🐹", "").replace("🐉", "").replace("🐱", "").strip()
            
            if pet_name_lower == item_clean or pet["name"].lower() == item_clean:
                if pet_id in user["pets"]:
                    await message.answer(f"❌ У тебя уже есть {pet['name']}!")
                elif user["dubli"] >= pet["price"]:
                    user["dubli"] -= pet["price"]
                    user["pets"].append(pet_id)
                    user["stats"]["pets_bought"] = user["stats"].get("pets_bought", 0) + 1
                    user["daily_quests"]["buy_pet"] = user["daily_quests"].get("buy_pet", 0) + 1
                    await message.answer(f"✅ Ты купил {pet['name']}! 💖\nОсталось дублей: {user['dubli']}", reply_markup=shop_menu_kb())
                else:
                    await message.answer(f"❌ Не хватает дублей! Нужно {pet['price']}💎")
                found = True
                break
        
        if not found:
            # Поиск еды
            for food_id, food in FOOD.items():
                food_name_lower = food["name"].lower().replace("🌽", "").replace("🍖", "").replace("🍭", "").replace("🍰", "").strip()
                item_clean = item.replace("🌽", "").replace("🍖", "").replace("🍭", "").replace("🍰", "").strip()
                
                if food_name_lower == item_clean or food["name"].lower() == item_clean:
                    if user["dubli"] >= food["price"]:
                        user["dubli"] -= food["price"]
                        user["inventory"][food_id] = user["inventory"].get(food_id, 0) + 1
                        await message.answer(f"✅ Ты купил {food['name']}! 💖\nОсталось дублей: {user['dubli']}", reply_markup=shop_menu_kb())
                    else:
                        await message.answer(f"❌ Не хватает дублей! Нужно {food['price']}💎")
                    found = True
                    break
        
        if not found:
            await message.answer("❌ Такой товар не найден!\n\n📝 **Правильное написание:**\nКупить Курица\nКупить Крокодил\nКупить Хомяк\nКупить Дракон\nКупить Кот\n\n🍗 **Или еду:**\nКупить Зерно\nКупить Мясо\nКупить Конфета\nКупить Торт")
        return
        # Поиск еды
        for food_id, food in FOOD.items():
            food_name_lower = food["name"].lower().replace("🌽", "").replace("🍖", "").replace("🍭", "").replace("🍰", "").strip()
            item_clean = item.replace("🌽", "").replace("🍖", "").replace("🍭", "").replace("🍰", "").strip()
            
            if food_name_lower == item_clean or food["name"].lower() == item_clean:
                if user["dubli"] >= food["price"]:
                    user["dubli"] -= food["price"]
                    user["inventory"][food_id] = user["inventory"].get(food_id, 0) + 1
                    await message.answer(f"✅ Ты купил {food['name']}! 💖\nОсталось дублей: {user['dubli']}", reply_markup=shop_menu_kb())
                else:
                    await message.answer(f"❌ Не хватает дублей! Нужно {food['price']}💎")
                found = True
                break
    
    if not found:
        await message.answer("❌ Такой товар не найден!\n\n📝 **Правильное написание:**\nКупить Курица\nКупить Крокодил\nКупить Хомяк\nКупить Дракон\nКупить Кот\n\n🍗 **Или еду:**\nКупить Зерно\nКупить Мясо\nКупить Конфета\nКупить Торт")
    return
        
        # Поиск еды
        for food_id, food in FOOD.items():
            if food["name"].lower() == item:
                if user["dubli"] >= food["price"]:
                    user["dubli"] -= food["price"]
                    user["inventory"][food_id] = user["inventory"].get(food_id, 0) + 1
                    await message.answer(f"✅ Ты купил {food['name']}! 💖\nОсталось дублей: {user['dubli']}", reply_markup=shop_menu_kb())
                else:
                    await message.answer(f"❌ Не хватает дублей! Нужно {food['price']}💎")
                return
        
        await message.answer("❌ Такой товар не найден!\nНапиши: Купить Курица или Купить Зерно")
        return
    
    # ========== ИГРЫ ==========
    if text == "🎮 Игры":
        await message.answer("🎮 **Выбери игру:**", reply_markup=games_menu_kb())
        return
    
    if text == "🎲 Орёл/Решка":
        await message.answer("Выбери: Орел или Решка?", reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Орел"), KeyboardButton(text="Решка")], [KeyboardButton(text="◀️ Назад")]],
            resize_keyboard=True
        ))
        return
    
    if text in ["Орел", "Решка"]:
        if user["dubli"] < 10:
            await message.answer("❌ Не хватает 10 дублей!", reply_markup=games_menu_kb())
            return
        result = random.choice(["Орел", "Решка"])
        if text == result:
            user["dubli"] += 10
            user["stats"]["dubli_earned"] += 10
            msg = f"🎉 {result}! Ты выиграл +10 дублей!"
        else:
            user["dubli"] -= 10
            msg = f"😔 {result}! Ты проиграл -10 дублей!"
        user["stats"]["games_played"] += 1
        user["daily_quests"]["play_games"] = user["daily_quests"].get("play_games", 0) + 1
        user["daily_quests"]["earn_dubli"] = user["daily_quests"].get("earn_dubli", 0) + 10
        check_achievements(user_id)
        check_daily_quests(user_id)
        await message.answer(f"{msg}\n💰 Теперь {user['dubli']}💎", reply_markup=games_menu_kb())
        return
    
    if text == "🔢 Угадай число":
        await message.answer("Введи число от 1 до 10:", reply_markup=back_kb())
        return
    
    if text.isdigit() and 1 <= int(text) <= 10 and user.get("waiting_number"):
        user["waiting_number"] = False
        if user["dubli"] < 5:
            await message.answer("❌ Не хватает 5 дублей!", reply_markup=games_menu_kb())
            return
        secret = random.randint(1, 10)
        if int(text) == secret:
            reward = random.randint(5, 25)
            user["dubli"] += reward
            user["stats"]["dubli_earned"] += reward
            msg = f"🎉 Число {secret}! Ты угадал! +{reward} дублей!"
        else:
            user["dubli"] -= 5
            msg = f"😔 Было {secret}, а ты назвал {text}. -5 дублей!"
        user["stats"]["games_played"] += 1
        user["daily_quests"]["play_games"] = user["daily_quests"].get("play_games", 0) + 1
        check_achievements(user_id)
        check_daily_quests(user_id)
        await message.answer(f"{msg}\n💰 Теперь {user['dubli']}💎", reply_markup=games_menu_kb())
        return
    
    if text.isdigit() and 1 <= int(text) <= 10:
        user["waiting_number"] = True
        await message.answer(f"Ты выбрал число {text}. Ставка 5💎\nРезультат через секунду...")
        await asyncio.sleep(1)
        await handle_message(message)
        return
    
    # ========== БОНУС ==========
    if text == "🎁 Бонус":
        today = datetime.now().date().isoformat()
        if user.get("last_daily") == today:
            await message.answer("🎁 Ты уже получал бонус сегодня! Возвращайся завтра!", reply_markup=main_kb())
        else:
            bonus = random.randint(50, 150)
            user["dubli"] += bonus
            user["last_daily"] = today
            await message.answer(f"🎁 Ежедневный бонус! Ты получил {bonus} дублей! 💰\nТеперь у тебя {user['dubli']} дублей.", reply_markup=main_kb())
        return
    
    # ========== ПИТОМЦЫ ==========
    if text == "🐾 Мои питомцы":
        pets_list = "\n".join([f"{PETS[p]['emoji']} {PETS[p]['name']} [{PETS[p]['rarity']}]" for p in user["pets"]])
        await message.answer(f"🐾 **Твои питомцы** ({len(user['pets'])}):\n\n{pets_list}", reply_markup=main_kb())
        return
    
    # ========== ДУБЛИ ==========
    if text == "💎 Дубли":
        await message.answer(f"💰 **Твой баланс:** {user['dubli']} дублей!", reply_markup=main_kb())
        return
    
    # ========== ТОП ==========
    if text == "🏆 Топ":
        top_text = await get_top_text()
        await message.answer(top_text, reply_markup=main_kb())
        return
    
    # ========== АДМИН-КОМАНДЫ (НАКРУТКА) ==========
    if text == "💰 Накрутить Поляшке" and user_id in [MASTER_ADMIN_ID, NUTRIKA_ADMIN_ID]:
        await message.answer("💎 Введи количество дублей для Поляшки:", reply_markup=admin_panel_kb() if user_id == MASTER_ADMIN_ID else nutrika_admin_kb())
        user["awaiting_polina_dubli"] = True
        return
    
    if user.get("awaiting_polina_dubli"):
        try:
            amount = int(text)
            if POLINA_ID not in users:
                users[POLINA_ID] = get_user(POLINA_ID)
            users[POLINA_ID]["dubli"] += amount
            await message.answer(f"✅ Поляшке накручено {amount} дублей!")
            await bot.send_message(POLINA_ID, f"👑 Тебе начислено {amount} дублей! 💰")
        except:
            await message.answer("❌ Введи число!")
        user["awaiting_polina_dubli"] = False
        return
    
    # ========== СТАТИСТИКА ДЛЯ АДМИНА ==========
    if text == "📊 Статистика" and user_id == MASTER_ADMIN_ID:
        total_players = len(users)
        total_dubli = sum(u["dubli"] for u in users.values())
        total_pets = sum(len(u["pets"]) for u in users.values())
        total_games = sum(u["stats"]["games_played"] for u in users.values())
        total_chests = sum(u["stats"]["chests_opened"] for u in users.values())
        await message.answer(
            f"📊 **СТАТИСТИКА БОТА** 📊\n\n"
            f"👥 Игроков: {total_players}\n"
            f"💰 Дублей в обороте: {total_dubli}\n"
            f"🐾 Всего питомцев: {total_pets}\n"
            f"🎮 Сыграно игр: {total_games}\n"
            f"🎁 Открыто сундуков: {total_chests}",
            reply_markup=admin_panel_kb()
        )
        return
    
    # ========== ОБЪЯВЛЕНИЕ (только админ) ==========
    if text == "📢 Объявление" and user_id == MASTER_ADMIN_ID:
        await message.answer("📢 Введи текст объявления для всех игроков:", reply_markup=admin_panel_kb())
        user["awaiting_broadcast"] = True
        return
    
    if user.get("awaiting_broadcast"):
        for uid in users:
            if uid not in [MASTER_ADMIN_ID, NUTRIKA_ADMIN_ID]:
                try:
                    await bot.send_message(uid, f"📢 **ОБЪЯВЛЕНИЕ ОТ АДМИНА** 📢\n\n{text}")
                    await asyncio.sleep(0.05)
                except:
                    pass
        await message.answer(f"✅ Объявление отправлено всем игрокам!")
        user["awaiting_broadcast"] = False
        return

# ========== ЗАПУСК ==========
async def main():
    print("✅ МЕГА-БОТ ДЛЯ ПОЛЯШКИ ЗАПУЩЕН!")
    print("🎯 КВЕСТЫ, ДОСТИЖЕНИЯ, СУНДУКИ — ВСЁ РАБОТАЕТ!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
