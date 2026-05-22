import asyncio
import logging
import random
import json
import os
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# ========== НАСТРОЙКИ ==========
# ⚠️ ТОКЕН ВСТАВЬ СЮДА (НЕ ПУБЛИКУЙ НИГДЕ!)
TOKEN = "8085068905:AAE1CeeFPTGc94jEaFgUVP7tUO9famyzKZ4"

# 👑 ТВОЙ ID (самый главный админ) - ВСЁ МОЖЕТ
MASTER_ADMIN_ID = 6900319945

# 🤝 АДМИН ДЛЯ НАКРУТКИ (только накрутка Полине)
NUTRIKA_ADMIN_ID = 8428411159

# 💖 ПОЛЯШКА (её ID, для удобства)
POLINA_ID = 8428411159  # если это её ID, или поменяй

DATA_FILE = "poly_bot_data.json"

# Питомцы
PETS = {
    "kurochka":   {"name": "🐔 Курица", "price": 50,  "income": 2,  "max_hunger": 100, "emoji": "🐔"},
    "krokodil":   {"name": "🐊 Крокодил", "price": 120, "income": 5,  "max_hunger": 80, "emoji": "🐊"},
    "hamster":    {"name": "🐹 Хомяк", "price": 80,  "income": 3,  "max_hunger": 90, "emoji": "🐹"},
    "drakosha":   {"name": "🐉 Дракон", "price": 200, "income": 10, "max_hunger": 120, "emoji": "🐉"},
    "cat":        {"name": "🐱 Кот", "price": 150, "income": 7,  "max_hunger": 85, "emoji": "🐱"}
}

# Еда
FOOD = {
    "seed":   {"name": "🌽 Зерно", "price": 5,  "restore": 15, "emoji": "🌽"},
    "meat":   {"name": "🍖 Мясо", "price": 15, "restore": 35, "emoji": "🍖"},
    "candy":  {"name": "🍭 Конфета", "price": 8,  "restore": 20, "emoji": "🍭"},
    "cake":   {"name": "🍰 Торт", "price": 25, "restore": 50, "emoji": "🍰"}
}

# ========== ЗАГРУЗКА / СОХРАНЕНИЕ ==========
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
            "last_income_time": datetime.now().isoformat(),
            "username": None,
            "total_games": 0,
            "total_feeds": 0
        }
        save_data(users_db)
    return users_db[uid]

def save_user(user_id, data):
    users_db[str(user_id)] = data
    save_data(users_db)

async def update_username(user_id):
    user = get_user(user_id)
    try:
        chat = await bot.get_chat(user_id)
        username = chat.username or chat.first_name
        user["username"] = username
        save_user(user_id, user)
    except:
        user["username"] = str(user_id)
        save_user(user_id, user)

# ========== ДОХОД ОТ ПИТОМЦЕВ ==========
async def update_income(user_id):
    user = get_user(user_id)
    last = datetime.fromisoformat(user["last_income_time"])
    now = datetime.now()
    diff_hours = (now - last).total_seconds() / 3600
    if diff_hours < 0.1:
        return
    total_income = 0
    for pet_id in user["pets"]:
        hunger = user["hunger"].get(pet_id, 100)
        if hunger > 20:
            total_income += PETS[pet_id]["income"] * diff_hours * (min(hunger, 100)/100)
    if total_income > 0:
        user["dubli"] += int(total_income)
        user["last_income_time"] = now.isoformat()
        for pet_id in user["pets"]:
            old = user["hunger"].get(pet_id, 100)
            new = max(0, old - diff_hours * 3)
            user["hunger"][pet_id] = new
        save_user(user_id, user)

# ========== ТОПЫ ==========
def get_top_by_dubli():
    players = []
    for uid, data in users_db.items():
        players.append((data.get("username", uid), data.get("dubli", 0), len(data.get("pets", []))))
    players.sort(key=lambda x: x[1], reverse=True)
    return players[:15]

def get_top_by_pets():
    players = []
    for uid, data in users_db.items():
        players.append((data.get("username", uid), len(data.get("pets", [])), data.get("dubli", 0)))
    players.sort(key=lambda x: x[1], reverse=True)
    return players[:15]

# ========== КЛАВИАТУРЫ ==========
def main_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🐾 Мои питомцы", callback_data="my_pets")],
        [InlineKeyboardButton(text="🏪 Магазин", callback_data="shop_menu")],
        [InlineKeyboardButton(text="🍗 Покормить", callback_data="feed_menu")],
        [InlineKeyboardButton(text="🎮 Игры", callback_data="games_menu")],
        [InlineKeyboardButton(text="🎁 Бонус", callback_data="daily")],
        [InlineKeyboardButton(text="🏆 Топы", callback_data="top_menu")],
        [InlineKeyboardButton(text="💎 Дубли", callback_data="my_dublis")]
    ])
    return kb

def games_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎲 Орёл/Решка (10💎)", callback_data="game_coin")],
        [InlineKeyboardButton(text="🔢 Угадай число (5-25💎)", callback_data="game_number")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_main")]
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
        kb.inline_keyboard.append([InlineKeyboardButton(text=f"{food['emoji']} {food['name']} (+{food['restore']}) {count}шт — {food['price']}💎", callback_data=f"buy_food_{food_id}")])
    kb.inline_keyboard.append([InlineKeyboardButton(text="◀️ Назад", callback_data="shop_menu")])
    return kb

def feed_menu_kb(user):
    kb = InlineKeyboardMarkup(inline_keyboard=[])
    active = user["active_pet"]
    for pet_id in user["pets"]:
        pet = PETS[pet_id]
        marker = "✅" if pet_id == user["active_pet"] else "🔘"
        kb.inline_keyboard.append([InlineKeyboardButton(text=f"{marker} {pet['emoji']} {pet['name']}", callback_data=f"switch_pet_{pet_id}")])
    kb.inline_keyboard.append([InlineKeyboardButton(text=f"🍽️ Покормить {PETS[active]['emoji']} {PETS[active]['name']}", callback_data="do_feed")])
    kb.inline_keyboard.append([InlineKeyboardButton(text="◀️ Назад", callback_data="back_main")])
    return kb

def top_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏆 По дублям", callback_data="top_dubli")],
        [InlineKeyboardButton(text="🐾 По питомцам", callback_data="top_pets")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_main")]
    ])

# ========== АДМИН-КЛАВИАТУРЫ (ТОЛЬКО ДЛЯ ТЕБЯ) ==========
def master_admin_kb():
    """Кнопки для главного админа (ты) - всё может"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👑 ПОЛНАЯ АДМИНКА", callback_data="full_admin_panel")],
        [InlineKeyboardButton(text="🔄 Переключиться в обычное меню", callback_data="back_main")]
    ])

def full_admin_panel_kb():
    """Полная админ-панель только для главного админа"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Накрутить дубли ПОЛЯШКЕ", callback_data="admin_add_polina")],
        [InlineKeyboardButton(text="🎁 Выдать питомца ПОЛЯШКЕ", callback_data="admin_give_pet_polina")],
        [InlineKeyboardButton(text="➕ Выдать дубли ЛЮБОМУ", callback_data="admin_add_dubli")],
        [InlineKeyboardButton(text="➖ Забрать дубли", callback_data="admin_remove_dubli")],
        [InlineKeyboardButton(text="🎁 Выдать питомца ЛЮБОМУ", callback_data="admin_give_pet")],
        [InlineKeyboardButton(text="📢 Объявление всем", callback_data="admin_broadcast")],
        [InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats")],
        [InlineKeyboardButton(text="👥 Список игроков", callback_data="admin_players")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_main")]
    ])

def nutrika_admin_kb():
    """Кнопки для админа накрутки (только накрутка Полине)"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Накрутить дубли ПОЛЯШКЕ", callback_data="admin_add_polina")],
        [InlineKeyboardButton(text="🎁 Выдать питомца ПОЛЯШКЕ", callback_data="admin_give_pet_polina")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_main")]
    ])

# ========== ИГРЫ ==========
async def play_coin(user_id):
    user = get_user(user_id)
    if user["dubli"] < 10:
        return False, "Не хватает 10 дублей"
    result = random.choice(["орел", "решка"])
    user_choice = random.choice(["орел", "решка"])
    if result == user_choice:
        user["dubli"] += 10
        save_user(user_id, user)
        return True, f"🎲 {result}! Выиграл +10 дублей"
    else:
        user["dubli"] -= 10
        save_user(user_id, user)
        return False, f"🎲 {result}. Проиграл -10 дублей"

async def play_number(user_id):
    user = get_user(user_id)
    if user["dubli"] < 5:
        return False, "Не хватает 5 дублей"
    number = random.randint(1, 10)
    user_num = random.randint(1, 10)
    if number == user_num:
        reward = random.randint(5, 25)
        user["dubli"] += reward
        save_user(user_id, user)
        return True, f"🔢 Число {number}! Угадал! +{reward} дублей"
    else:
        user["dubli"] -= 5
        save_user(user_id, user)
        return False, f"🔢 Число {number}, ты назвал {user_num}. -5 дублей"

# ========== АДМИН-ФУНКЦИИ ==========
async def add_dubli_to_user(target_id, amount, admin_id):
    """Добавить дубли пользователю"""
    target_user = get_user(target_id)
    target_user["dubli"] += amount
    save_user(target_id, target_user)
    await bot.send_message(target_id, f"👑 Админ выдал тебе {amount} дублей! 💰")
    if admin_id == MASTER_ADMIN_ID:
        await bot.send_message(admin_id, f"✅ Выдано {amount} дублей пользователю {target_id}")
    return True

async def give_pet_to_user(target_id, pet_id, admin_id):
    """Выдать питомца пользователю"""
    if pet_id not in PETS:
        return False, f"Питомец {pet_id} не найден"
    target_user = get_user(target_id)
    if pet_id in target_user["pets"]:
        return False, "У пользователя уже есть этот питомец"
    target_user["pets"].append(pet_id)
    target_user["hunger"][pet_id] = 100
    save_user(target_id, target_user)
    await bot.send_message(target_id, f"👑 Админ выдал тебе питомца {PETS[pet_id]['name']}! 🎉")
    return True, "✅ Питомец выдан"

# ========== КОМАНДЫ ==========
@dp.message(Command("start"))
async def start_cmd(message: Message):
    user_id = message.from_user.id
    await update_income(user_id)
    await update_username(user_id)
    user = get_user(user_id)
    
    text = f"🎮 Бот для Поляшки\n\n💰 Дублей: {user['dubli']}\n🐾 Питомцев: {len(user['pets'])}\n💪 Активный: {PETS[user['active_pet']]['name']}"
    
    if user_id == MASTER_ADMIN_ID:
        await message.answer(text, reply_markup=master_admin_kb())
    elif user_id == NUTRIKA_ADMIN_ID:
        await message.answer(text, reply_markup=nutrika_admin_kb())
    else:
        await message.answer(text, reply_markup=main_kb())

@dp.message(Command("id"))
async def show_id(message: Message):
    await message.answer(f"Твой ID: {message.from_user.id}")

@dp.callback_query()
async def handle_callback(call: CallbackQuery):
    user_id = call.from_user.id
    await update_income(user_id)
    await update_username(user_id)
    user = get_user(user_id)
    data = call.data
    
    # Навигация
    if data == "back_main":
        text = f"💰 Дублей: {user['dubli']}\n🐾 Питомцев: {len(user['pets'])}"
        if user_id == MASTER_ADMIN_ID:
            await call.message.edit_text(text, reply_markup=master_admin_kb())
        elif user_id == NUTRIKA_ADMIN_ID:
            await call.message.edit_text(text, reply_markup=nutrika_admin_kb())
        else:
            await call.message.edit_text(text, reply_markup=main_kb())
    
    elif data == "full_admin_panel" and user_id == MASTER_ADMIN_ID:
        await call.message.edit_text("👑 ПОЛНАЯ АДМИН-ПАНЕЛЬ 👑\n\nТы главный, можешь всё!", reply_markup=full_admin_panel_kb())
    
    # ----- ОБЫЧНЫЕ ФУНКЦИИ -----
    elif data == "my_dublis":
        await call.answer(f"{user['dubli']} дублей", show_alert=True)
    
    elif data == "my_pets":
        text = "🐾 Твои питомцы:\n"
        for pet_id in user["pets"]:
            pet = PETS[pet_id]
            hunger = user["hunger"].get(pet_id, 100)
            status = "сыт" if hunger > 50 else "голоден"
            active_mark = "⭐ " if pet_id == user["active_pet"] else "   "
            text += f"{active_mark}{pet['emoji']} {pet['name']} — {status} ({int(hunger)}/{pet['max_hunger']})\n"
        await call.message.edit_text(text, reply_markup=main_kb())
    
    elif data.startswith("switch_pet_"):
        pet_id = data.split("_")[2]
        if pet_id in user["pets"]:
            user["active_pet"] = pet_id
            save_user(user_id, user)
            await call.answer(f"Активен: {PETS[pet_id]['name']}")
            await call.message.edit_text("✅ Питомец выбран", reply_markup=feed_menu_kb(user))
    
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
            user["hunger"][pet_id] = 100
            save_user(user_id, user)
            await call.answer(f"Куплен {pet['name']}")
            await call.message.edit_text(f"✅ {pet['name']} куплен!\nОсталось: {user['dubli']}💎", reply_markup=main_kb())
        else:
            await call.answer(f"Нужно {pet['price']}💎")
    
    elif data.startswith("buy_food_"):
        food_id = data.split("_")[2]
        food = FOOD[food_id]
        if user["dubli"] >= food["price"]:
            user["dubli"] -= food["price"]
            user["inventory"][food_id] = user["inventory"].get(food_id, 0) + 1
            save_user(user_id, user)
            await call.answer(f"Куплен {food['name']}")
            await call.message.edit_text(f"✅ {food['name']} в инвентаре", reply_markup=food_shop_kb(user))
        else:
            await call.answer("Не хватает дублей")
    
    elif data == "feed_menu":
        await call.message.edit_text("🍗 Выбери питомца:", reply_markup=feed_menu_kb(user))
    
    elif data == "do_feed":
        active = user["active_pet"]
        for food_id, count in user["inventory"].items():
            if count > 0:
                food = FOOD[food_id]
                user["inventory"][food_id] -= 1
                old_hunger = user["hunger"][active]
                new_hunger = min(PETS[active]["max_hunger"], old_hunger + food["restore"])
                user["hunger"][active] = new_hunger
                save_user(user_id, user)
                await call.answer(f"{PETS[active]['name']} накормлен! +{food['restore']}")
                await call.message.edit_text(f"✅ {PETS[active]['name']} сыт\nГолод: {int(new_hunger)}/{PETS[active]['max_hunger']}", reply_markup=main_kb())
                return
        await call.answer("Нет еды! Купи в магазине")
    
    elif data == "games_menu":
        await call.message.edit_text("🎮 Выбери игру:", reply_markup=games_menu_kb())
    
    elif data == "game_coin":
        win, msg = await play_coin(user_id)
        user = get_user(user_id)
        await call.answer(msg)
        await call.message.edit_text(f"{msg}\n💰 {user['dubli']}💎", reply_markup=games_menu_kb())
    
    elif data == "game_number":
        win, msg = await play_number(user_id)
        user = get_user(user_id)
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
            await call.message.edit_text(f"🎁 +{bonus} дублей!\n💰 {user['dubli']}💎", reply_markup=main_kb())
    
    elif data == "top_menu":
        await call.message.edit_text("🏆 Топы:", reply_markup=top_menu_kb())
    
    elif data == "top_dubli":
        top = get_top_by_dubli()
        text = "🏆 ТОП ПО ДУБЛЯМ 🏆\n"
        for i, (name, dubli, _) in enumerate(top, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            text += f"{medal} {name} — {dubli}💎\n"
        await call.message.edit_text(text, reply_markup=top_menu_kb())
    
    elif data == "top_pets":
        top = get_top_by_pets()
        text = "🏆 ТОП ПО ПИТОМЦАМ 🏆\n"
        for i, (name, pets_count, _) in enumerate(top, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            text += f"{medal} {name} — {pets_count} питомцев\n"
        await call.message.edit_text(text, reply_markup=top_menu_kb())
    
    # ----- АДМИН-ФУНКЦИИ НАКРУТКИ ПОЛЯШКЕ (доступно тебе и админу накрутки)-----
    elif data == "admin_add_polina":
        if user_id not in [MASTER_ADMIN_ID, NUTRIKA_ADMIN_ID]:
            await call.answer("❌ Нет доступа!")
            return
        await call.message.edit_text("💰 Введи количество дублей для ПОЛЯШКИ\n\nПример: `1000`", reply_markup=main_kb())
        await call.message.answer("Напиши число дублей:")
        # Сохраняем состояние
        user["admin_action"] = "add_polina"
        save_user(user_id, user)
    
    elif data == "admin_give_pet_polina":
        if user_id not in [MASTER_ADMIN_ID, NUTRIKA_ADMIN_ID]:
            await call.answer("❌ Нет доступа!")
            return
        pets_list = "\n".join([f"{pid} — {p['name']}" for pid, p in PETS.items()])
        await call.message.edit_text(f"🎁 Введи ID питомца для ПОЛЯШКИ\n\nДоступно:\n{pets_list}\n\nПример: `drakosha`", reply_markup=main_kb())
        user["admin_action"] = "give_pet_polina"
        save_user(user_id, user)
    
    # ----- ПОЛНАЯ АДМИНКА (только для тебя) -----
    elif data == "admin_add_dubli" and user_id == MASTER_ADMIN_ID:
        await call.message.edit_text("💰 Введи ID пользователя и количество дублей\n\nПример: `6900319945 1000`", reply_markup=full_admin_panel_kb())
    
    elif data == "admin_remove_dubli" and user_id == MASTER_ADMIN_ID:
        await call.message.edit_text("➖ Введи ID пользователя и количество дублей для списания\n\nПример: `6900319945 50`", reply_markup=full_admin_panel_kb())
    
    elif data == "admin_give_pet" and user_id == MASTER_ADMIN_ID:
        pets_list = "\n".join([f"{pid} — {p['name']}" for pid, p in PETS.items()])
        await call.message.edit_text(f"🎁 Введи ID пользователя и ID питомца\n\nДоступно:\n{pets_list}\n\nПример: `6900319945 drakosha`", reply_markup=full_admin_panel_kb())
    
    elif data == "admin_broadcast" and user_id == MASTER_ADMIN_ID:
        await call.message.edit_text("📢 Введи текст объявления для ВСЕХ игроков:", reply_markup=full_admin_panel_kb())
    
    elif data == "admin_stats" and user_id == MASTER_ADMIN_ID:
        total_players = len(users_db)
        total_dubli = sum(data.get("dubli", 0) for data in users_db.values())
        total_pets = sum(len(data.get("pets", [])) for data in users_db.values())
        await call.answer(f"📊 Игроков: {total_players}\n💰 Дублей: {total_dubli}\n🐾 Питомцев: {total_pets}", show_alert=True)
        await call.message.edit_text("Статистика показана", reply_markup=full_admin_panel_kb())
    
    elif data == "admin_players" and user_id == MASTER_ADMIN_ID:
        players_list = ""
        for uid, data in users_db.items():
            players_list += f"ID: {uid} | {data.get('username', 'Нет имени')} | 💰{data.get('dubli', 0)}\n"
        if len(players_list) > 4000:
            players_list = players_list[:4000] + "\n...и другие"
        await call.message.edit_text(f"👥 СПИСОК ИГРОКОВ:\n\n{players_list}", reply_markup=full_admin_panel_kb())
    
    await call.answer()

# ========== ОБРАБОТКА ТЕКСТОВЫХ КОМАНД ==========
@dp.message()
async def text_commands(message: Message):
    user_id = message.from_user.id
    user = get_user(user_id)
    text = message.text.strip()
    
    # Обработка накрутки для Поляшки (доступно тебе и админу)
    if user.get("admin_action") == "add_polina" and user_id in [MASTER_ADMIN_ID, NUTRIKA_ADMIN_ID]:
        try:
            amount = int(text)
            await add_dubli_to_user(POLINA_ID, amount, user_id)
            user["admin_action"] = None
            save_user(user_id, user)
            await message.answer(f"✅ Поляшке накручено {amount} дублей! 💰")
        except:
            await message.answer("❌ Введи число!")
        return
    
    if user.get("admin_action") == "give_pet_polina" and user_id in [MASTER_ADMIN_ID, NUTRIKA_ADMIN_ID]:
        pet_id = text.strip()
        success, msg = await give_pet_to_user(POLINA_ID, pet_id, user_id)
        await message.answer(msg)
        user["admin_action"] = None
        save_user(user_id, user)
        return
    
    # ПОЛНАЯ АДМИНКА (только для тебя)
    if user_id != MASTER_ADMIN_ID:
        return
    
    # Выдача дублей
    if text.startswith("add "):
        try:
            parts = text.split()
            target_id = int(parts[1])
            amount = int(parts[2])
            await add_dubli_to_user(target_id, amount, user_id)
        except:
            await message.answer("❌ Формат: add ID КОЛИЧЕСТВО")
    
    # Забрать дубли
    elif text.startswith("remove "):
        try:
            parts = text.split()
            target_id = int(parts[1])
            amount = int(parts[2])
            target_user = get_user(target_id)
            target_user["dubli"] = max(0, target_user["dubli"] - amount)
            save_user(target_id, target_user)
            await message.answer(f"✅ Забрано {amount} дублей у {target_id}")
        except:
            await message.answer("❌ Формат: remove ID КОЛИЧЕСТВО")
    
    # Выдать питомца
    elif text.startswith("givepet "):
        try:
            parts = text.split()
            target_id = int(parts[1])
            pet_id = parts[2]
            success, msg = await give_pet_to_user(target_id, pet_id, user_id)
            await message.answer(msg)
        except:
            await message.answer("❌ Формат: givepet ID ПИТОМЕЦ")
    
    # Рассылка
    elif text.startswith("broadcast "):
        broadcast_text = text[10:]
        count = 0
        for uid in users_db:
            try:
                await bot.send_message(int(uid), f"📢 ОБЪЯВЛЕНИЕ ОТ АДМИНА 📢\n\n{broadcast_text}")
                count += 1
                await asyncio.sleep(0.05)
            except:
                pass
        await message.answer(f"✅ Отправлено {count} игрокам")

# ========== ЗАПУСК ==========
bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    logging.basicConfig(level=logging.INFO)
    print("✅ Бот запущен!")
    print(f"👑 Главный админ: {MASTER_ADMIN_ID}")
    print(f"🔧 Админ накрутки: {NUTRIKA_ADMIN_ID}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())