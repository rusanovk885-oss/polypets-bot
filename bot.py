import asyncio
import random
import json
import os
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# ========== ТОКЕН ==========
TOKEN = "8949697674:AAHAZywQYpmpYzx4BE2LJY1JiGC76WxWRx4"

# ========== АДМИНЫ ==========
MASTER_ADMIN_ID = 6900319945
POLINA_ID = 8428411159

# ========== ФАЙЛ ДЛЯ СОХРАНЕНИЯ ДАННЫХ ==========
DATA_FILE = "polypets_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ========== ЗАГРУЖАЕМ ДАННЫЕ ==========
users = load_data()
clans = {}

# ========== 670+ ПИТОМЦЕВ ==========
PET_BASES = [
    "Курица", "Петух", "Цыплёнок", "Крокодил", "Хомяк", "Крыса", "Попугай", "Черепаха",
    "Кот", "Кошка", "Лев", "Тигр", "Леопард", "Гепард", "Пума", "Рысь", "Ягуар", "Львёнок", "Тигрёнок",
    "Пёс", "Щенок", "Волк", "Волчонок", "Лиса", "Лисёнок", "Шакал", "Койот", "Хаски", "Овчарка",
    "Такса", "Бульдог", "Доберман", "Ротвейлер", "Спаниель", "Лайка", "Мопс", "Чихуахуа", "Дворняга",
    "Медведь", "Медвежонок", "Белый медведь", "Панда", "Малая панда", "Барибал", "Гризли", "Коала", "Вомбат",
    "Лошадь", "Жеребёнок", "Осёл", "Зебра", "Жираф", "Слон", "Слонёнок", "Носорог", "Бегемот", "Олень",
    "Оленёнок", "Лось", "Лосёнок", "Кабан", "Кабанчик", "Косуля", "Зубр", "Бизон", "Як", "Буйвол",
    "Обезьяна", "Мартышка", "Шимпанзе", "Горилла", "Орангутанг", "Лемур", "Макака", "Павиан", "Гиббон", "Капуцин",
    "Кенгуру", "Кенгурёнок", "Коала", "Вомбат", "Опоссум", "Квокка", "Тасманийский дьявол", "Ехидна", "Утконос",
    "Орёл", "Орлёнок", "Сокол", "Соколёнок", "Ястреб", "Ястребёнок", "Сова", "Совёнок", "Филин", "Пингвин",
    "Пингвинёнок", "Фламинго", "Лебедь", "Лебедёнок", "Павлин", "Страус", "Страусёнок", "Пеликан", "Аист", "Цапля",
    "Дельфин", "Дельфинёнок", "Кит", "Китёнок", "Касатка", "Касаточка", "Акула", "Скат", "Осьминог", "Кальмар",
    "Медуза", "Краб", "Лобстер", "Креветка", "Омар", "Мидия", "Устрица", "Морской конёк", "Морская звезда", "Морской ёж",
    "Змея", "Гадюка", "Кобра", "Питон", "Удав", "Ящерица", "Варан", "Игуана", "Хамелеон", "Геккон",
    "Паук", "Скорпион", "Пчела", "Шмель", "Бабочка", "Божья коровка", "Кузнечик", "Стрекоза", "Муравей", "Жук",
    "Лягушка", "Жаба", "Тритон", "Саламандра", "Квакша", "Древолаз", "Аксолотль", "Жерлянка", "Чесночница", "Уж",
    "Дракон", "Дракончик", "Единорог", "Феникс", "Грифон", "Цербер", "Пегас", "Кентавр", "Василиск", "Химера",
    "Сфинкс", "Циклоп", "Минотавр", "Кракен", "Гидра", "Левиафан", "Бегемот", "Мантикора", "Вампир", "Оборотень"
]

COLORS = ["Красный", "Синий", "Зелёный", "Жёлтый", "Фиолетовый", "Оранжевый", "Розовый", "Чёрный", "Белый", "Золотой", "Серебряный", "Бронзовый"]
TYPES = ["Огненный", "Водный", "Земляной", "Воздушный", "Ледяной", "Электрический", "Тёмный", "Светлый", "Призрачный", "Драконний"]

PRICES = [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 220, 240, 260, 280, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000]
emoji_list = ["🐔", "🐓", "🐥", "🐊", "🐹", "🐀", "🦜", "🐢", "🐱", "🐈", "🦁", "🐯", "🐆", "🐅", "🐻", "🐈", "🐆", "🦁", "🐅", "🐕", "🐶", "🐺", "🐕‍🦺", "🦊", "🦊", "🐺", "🐕", "🐩", "🐕", "🐻", "🐻‍❄️", "🐼", "🐨", "🐻", "🐎", "🫏", "🦓", "🦒", "🐘", "🦏", "🦛", "🦌", "🦌", "🐗", "🐒", "🦍", "🦧", "🦝", "🐨", "🦘", "🦥", "🦔", "🐁", "🦅", "🦅", "🦅", "🦉", "🦉", "🐧", "🦩", "🦢", "🦚", "🐦‍⬛", "🐬", "🐋", "🐋", "🦈", "🐟", "🐙", "🦑", "🪼", "🦀", "🦞", "🐍", "🐍", "🐍", "🐍", "🦎", "🕷️", "🦂", "🐝", "🦋", "🐞", "🦗", "🦟", "🐜", "🪲", "🦗", "🐸", "🐸", "🦎", "🦎", "🐸", "🐉", "🦄", "🔥", "🦅", "🔱", "🐴", "🔱", "🐂", "🐙", "🐉", "🦄"]

PETS = {}
pet_counter = 0
for base in PET_BASES:
    for color in COLORS[:3]:
        for pet_type in TYPES[:2]:
            if pet_counter >= 670:
                break
            name = f"{color} {pet_type} {base}"
            emoji = emoji_list[pet_counter % len(emoji_list)]
            if pet_counter < 300:
                rarity = "⚪ Обычный"
            elif pet_counter < 500:
                rarity = "🔵 Редкий"
            elif pet_counter < 600:
                rarity = "🟣 Эпический"
            else:
                rarity = "🟠 Легендарный"
            price = PRICES[pet_counter % len(PRICES)]
            PETS[f"pet_{pet_counter}"] = {
                "name": f"{emoji} {name}",
                "price": price,
                "emoji": emoji,
                "rarity": rarity,
                "power": random.randint(10, 200)
            }
            pet_counter += 1
            if pet_counter >= 670:
                break
        if pet_counter >= 670:
            break
    if pet_counter >= 670:
        break

print(f"✅ ЗАГРУЖЕНО {len(PETS)} ПИТОМЦЕВ")

# ========== ФУНКЦИЯ ПОЛУЧЕНИЯ ПОЛЬЗОВАТЕЛЯ С АВТОСОХРАНЕНИЕМ ==========
def get_user(user_id):
    uid = str(user_id)
    if uid not in users:
        users[uid] = {
            "dubli": 500,
            "pets": [],
            "pet_names": {},
            "pet_hunger": {},
            "pet_levels": {},
            "inventory": {"seed": 3, "meat": 1},
            "last_daily": None,
            "last_hourly": None,
            "clan": None,
            "rating": 1000,
            "investments": 0,
            "investment_time": None,
            "stats": {"games": 0, "wins": 0, "losses": 0, "chests": 0, "hunts": 0},
            "achievements": []
        }
        save_data(users)
    return users[uid]

# ========== КЛАВИАТУРЫ ==========
def main_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🐾 Мои питомцы"), KeyboardButton(text="🏪 Магазин")],
            [KeyboardButton(text="🎮 Игры"), KeyboardButton(text="🎁 Бонус")],
            [KeyboardButton(text="💰 Дубли"), KeyboardButton(text="🏆 Топ")],
            [KeyboardButton(text="🍽️ Покормить"), KeyboardButton(text="🎯 Охота")],
            [KeyboardButton(text="🎁 Сундуки"), KeyboardButton(text="🔨 Крафт")],
            [KeyboardButton(text="⚔️ PvP"), KeyboardButton(text="💎 Инвестиции")],
            [KeyboardButton(text="👥 Кланы"), KeyboardButton(text="🏅 Достижения")],
            [KeyboardButton(text="✏️ Дать имя"), KeyboardButton(text="👑 Админка")]
        ],
        resize_keyboard=True
    )
    return kb

def games_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎲 Орёл/Решка"), KeyboardButton(text="🔢 Угадай число")],
            [KeyboardButton(text="🎲 Кости"), KeyboardButton(text="✊ КНБ")],
            [KeyboardButton(text="⬆️ Выше-Ниже"), KeyboardButton(text="🎰 Слоты")],
            [KeyboardButton(text="🃏 Блэкджек"), KeyboardButton(text="🎡 Рулетка")],
            [KeyboardButton(text="🐎 Гонки"), KeyboardButton(text="🔐 Сейф")],
            [KeyboardButton(text="🎯 Дартс"), KeyboardButton(text="⚔️ Дуэль")],
            [KeyboardButton(text="🎣 Рыбалка"), KeyboardButton(text="🍀 Клевер")],
            [KeyboardButton(text="💎 Кристаллы"), KeyboardButton(text="◀️ Назад")]
        ],
        resize_keyboard=True
    )
    return kb

def admin_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💰 Выдать дубли"), KeyboardButton(text="🎁 Выдать питомца")],
            [KeyboardButton(text="📢 Объявление"), KeyboardButton(text="📊 Статистика")],
            [KeyboardButton(text="◀️ Назад")]
        ],
        resize_keyboard=True
    )
    return kb

def chests_kb():
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

def back_kb():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Назад")]], resize_keyboard=True)

# ========== МАГАЗИН С ПАГИНАЦИЕЙ ==========
def get_shop_keyboard(page=0):
    items_per_page = 10
    pet_list = list(PETS.items())
    total_pages = (len(pet_list) + items_per_page - 1) // items_per_page
    start = page * items_per_page
    end = min(start + items_per_page, len(pet_list))
    
    kb = InlineKeyboardMarkup(inline_keyboard=[])
    for pet_id, pet in pet_list[start:end]:
        kb.inline_keyboard.append([InlineKeyboardButton(text=f"{pet['name']} — {pet['price']}💎", callback_data=f"buy_{pet_id}")])
    
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="◀️", callback_data=f"shop_page_{page-1}"))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton(text="▶️", callback_data=f"shop_page_{page+1}"))
    if nav_buttons:
        kb.inline_keyboard.append(nav_buttons)
    kb.inline_keyboard.append([InlineKeyboardButton(text="❌ Закрыть", callback_data="close_shop")])
    return kb, total_pages, page

# ========== ИГРЫ (С СОХРАНЕНИЕМ) ==========
async def game_coin(user_id, choice):
    user = get_user(user_id)
    if user["dubli"] < 10:
        return False, f"❌ Не хватает 10 дублей!\n💰 {user['dubli']}💎"
    result = random.choice(["Орел", "Решка"])
    win = choice == result
    if win:
        user["dubli"] += 10
        user["stats"]["wins"] += 1
        msg = f"🎉 {result}! +10 дублей!"
    else:
        user["dubli"] -= 10
        user["stats"]["losses"] += 1
        msg = f"😔 {result}! -10 дублей!"
    user["stats"]["games"] += 1
    save_data(users)
    return win, f"{msg}\n💰 {user['dubli']}💎"

async def game_number(user_id, number):
    user = get_user(user_id)
    if user["dubli"] < 5:
        return False, f"❌ Не хватает 5 дублей!\n💰 {user['dubli']}💎"
    secret = random.randint(1, 10)
    win = number == secret
    if win:
        reward = random.randint(5, 25)
        user["dubli"] += reward
        user["stats"]["wins"] += 1
        msg = f"🎉 Число {secret}! +{reward} дублей!"
    else:
        user["dubli"] -= 5
        user["stats"]["losses"] += 1
        msg = f"😔 Число {secret}, ты назвал {number}. -5 дублей!"
    user["stats"]["games"] += 1
    save_data(users)
    return win, f"{msg}\n💰 {user['dubli']}💎"

async def game_dice(user_id):
    user = get_user(user_id)
    if user["dubli"] < 20:
        return False, f"❌ Не хватает 20 дублей!\n💰 {user['dubli']}💎"
    player = random.randint(1, 6)
    bot = random.randint(1, 6)
    if player > bot:
        reward = random.randint(20, 60)
        user["dubli"] += reward
        user["stats"]["wins"] += 1
        msg = f"🎉 {player} vs {bot} +{reward}💎"
    elif player < bot:
        user["dubli"] -= 20
        user["stats"]["losses"] += 1
        msg = f"😔 {player} vs {bot} -20💎"
    else:
        msg = f"🤝 Ничья! {player}-{bot}"
    user["stats"]["games"] += 1
    save_data(users)
    return True, f"{msg}\n💰 {user['dubli']}💎"

async def game_rps(user_id, choice):
    user = get_user(user_id)
    if user["dubli"] < 15:
        return False, f"❌ Не хватает 15 дублей!\n💰 {user['dubli']}💎"
    choices = ["камень", "ножницы", "бумага"]
    bot = random.choice(choices)
    if choice == bot:
        msg = f"🤝 Ничья! {choice} - {bot}"
        return True, f"{msg}\n💰 {user['dubli']}💎"
    elif (choice == "камень" and bot == "ножницы") or (choice == "ножницы" and bot == "бумага") or (choice == "бумага" and bot == "камень"):
        user["dubli"] += 15
        user["stats"]["wins"] += 1
        msg = f"🎉 {choice} vs {bot} +15💎"
    else:
        user["dubli"] -= 15
        user["stats"]["losses"] += 1
        msg = f"😔 {choice} vs {bot} -15💎"
    user["stats"]["games"] += 1
    save_data(users)
    return True, f"{msg}\n💰 {user['dubli']}💎"

async def game_higher(user_id, guess):
    user = get_user(user_id)
    if user["dubli"] < 25:
        return False, f"❌ Не хватает 25 дублей!\n💰 {user['dubli']}💎"
    num = random.randint(1, 100)
    next_num = random.randint(1, 100)
    win = (guess == "higher" and next_num > num) or (guess == "lower" and next_num < num)
    if win:
        reward = random.randint(25, 75)
        user["dubli"] += reward
        user["stats"]["wins"] += 1
        msg = f"🎉 {num} → {next_num} +{reward}💎"
    else:
        user["dubli"] -= 25
        user["stats"]["losses"] += 1
        msg = f"😔 {num} → {next_num} -25💎"
    user["stats"]["games"] += 1
    save_data(users)
    return win, f"{msg}\n💰 {user['dubli']}💎"

async def game_slots(user_id):
    user = get_user(user_id)
    if user["dubli"] < 30:
        return False,
        # ========== ПРОФИЛЬ ИГРОКА ==========
async def get_profile_text(user_id, target_id=None):
    """Возвращает текст профиля пользователя"""
    if target_id is None:
        target_id = user_id
    
    target = get_user(target_id)
    
    try:
        chat = await bot.get_chat(target_id)
        name = chat.username or chat.first_name or str(target_id)
    except:
        name = str(target_id)
    
    # Формируем список питомцев с именами
    pets_list = []
    for i, pet_id in enumerate(target["pets"][:10]):  # Показываем первых 10 питомцев
        pet = PETS[pet_id]
        pet_name = target["pet_names"].get(pet_id, "")
        name_str = f" '{pet_name}'" if pet_name else ""
        pets_list.append(f"{i+1}. {pet['name']}{name_str}")
    
    pets_text = "\n".join(pets_list) if pets_list else "Нет питомцев"
    if len(target["pets"]) > 10:
        pets_text += f"\n... и ещё {len(target['pets']) - 10} питомцев"
    
    last_seen = "Сейчас в игре"
    
    text = (
        f"👤 **ПРОФИЛЬ ИГРОКА** 👤\n\n"
        f"⭐ **{name}**\n"
        f"🆔 ID: `{target_id}`\n\n"
        f"💰 Дублей: {target['dubli']}\n"
        f"🐾 Питомцев: {len(target['pets'])}\n"
        f"⭐ Рейтинг PvP: {target['rating']}\n\n"
        f"📊 **Статистика:**\n"
        f"🎮 Игр: {target['stats']['games']}\n"
        f"🏆 Побед: {target['stats']['wins']}\n"
        f"💔 Поражений: {target['stats']['losses']}\n"
        f"📦 Сундуков: {target['stats']['chests']}\n"
        f"🎯 Охот: {target['stats']['hunts']}\n\n"
        f"🐾 **Питомцы:**\n{pets_text}\n\n"
        f"🕐 Последняя активность: {last_seen}"
    )
    
    return text

# ========== ТОП ПО РЕЙТИНГУ ==========
async def get_top_rating():
    players = []
    for uid, data in users.items():
        try:
            chat = await bot.get_chat(int(uid))
            name = chat.username or chat.first_name or str(uid)
        except:
            name = str(uid)
        players.append((name, data["rating"], data["dubli"], len(data["pets"])))
    players.sort(key=lambda x: x[1], reverse=True)
    return players[:15]

# ========== ТОП ПО ПИТОМЦАМ ==========
async def get_top_pets():
    players = []
    for uid, data in users.items():
        try:
            chat = await bot.get_chat(int(uid))
            name = chat.username or chat.first_name or str(uid)
        except:
            name = str(uid)
        players.append((name, len(data["pets"]), data["dubli"], data["rating"]))
    players.sort(key=lambda x: x[1], reverse=True)
    return players[:15]

# ========== ДОБАВЛЯЕМ НОВЫЕ КНОПКИ В КЛАВИАТУРЫ ==========
def main_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🐾 Мои питомцы"), KeyboardButton(text="🏪 Магазин")],
            [KeyboardButton(text="🎮 Игры"), KeyboardButton(text="🎁 Бонус")],
            [KeyboardButton(text="💰 Дубли"), KeyboardButton(text="🏆 Топ")],
            [KeyboardButton(text="👤 Мой профиль"), KeyboardButton(text="🏆 Рейтинг")],
            [KeyboardButton(text="🍽️ Покормить"), KeyboardButton(text="🎯 Охота")],
            [KeyboardButton(text="🎁 Сундуки"), KeyboardButton(text="🔨 Крафт")],
            [KeyboardButton(text="⚔️ PvP"), KeyboardButton(text="💎 Инвестиции")],
            [KeyboardButton(text="👥 Кланы"), KeyboardButton(text="✏️ Дать имя")],
            [KeyboardButton(text="👑 Админка")]
        ],
        resize_keyboard=True
    )
    return kb

# ========== ДОБАВЛЯЕМ ОБРАБОТЧИКИ В handle_message ==========
# Добавь эти строки в функцию handle_message (внутрь @dp.message()):

    # Профиль
    if text == "👤 Мой профиль":
        profile_text = await get_profile_text(user_id)
        await message.answer(profile_text, parse_mode="Markdown", reply_markup=main_kb())
        return
    
    # Топ по рейтингу
    if text == "🏆 Рейтинг":
        top = await get_top_rating()
        top_text = "🏆 **ТОП ПО РЕЙТИНГУ PVP** 🏆\n\n"
        for i, (name, rating, dubli, pets) in enumerate(top, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            top_text += f"{medal} {name[:20]} — {rating}⭐ ({dubli}💎, {pets} петов)\n"
        await message.answer(top_text, reply_markup=main_kb())
        return

# ========== ДОБАВЛЯЕМ КОМАНДЫ ==========

@dp.message(Command("profile"))
async def profile_cmd(message: Message):
    user_id = message.from_user.id
    args = message.text.split()
    
    if len(args) > 1:
        try:
            target_id = int(args[1])
            profile_text = await get_profile_text(user_id, target_id)
            await message.answer(profile_text, parse_mode="Markdown", reply_markup=main_kb())
        except:
            await message.answer("❌ Неверный ID! Пример: /profile 6900319945")
    else:
        profile_text = await get_profile_text(user_id)
        await message.answer(profile_text, parse_mode="Markdown", reply_markup=main_kb())

@dp.message(Command("top_pets"))
async def top_pets_cmd(message: Message):
    top = await get_top_pets()
    top_text = "🏆 **ТОП ПО КОЛИЧЕСТВУ ПИТОМЦЕВ** 🏆\n\n"
    for i, (name, pets, dubli, rating) in enumerate(top, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        top_text += f"{medal} {name[:20]} — {pets} 🐾 ({dubli}💎, {rating}⭐)\n"
    await message.answer(top_text, reply_markup=main_kb())

@dp.message(Command("top_rating"))
async def top_rating_cmd(message: Message):
    top = await get_top_rating()
    top_text = "🏆 **ТОП ПО РЕЙТИНГУ PVP** 🏆\n\n"
    for i, (name, rating, dubli, pets) in enumerate(top, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        top_text += f"{medal} {name[:20]} — {rating}⭐ ({dubli}💎, {pets} петов)\n"
    await message.answer(top_text, reply_markup=main_kb())
