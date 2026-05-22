import asyncio
import random
import json
import os
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# ========== ТОКЕН (ВСТАВЬ СВОЙ) ==========
TOKEN = "8949697674:AAHAZywQYpmpYzx4BE2LJY1JiGC76WxWRx4"

# ========== АДМИНЫ ==========
MASTER_ADMIN_ID = 6900319945
POLINA_ID = 8428411159

# ========== ФАЙЛ ДЛЯ СОХРАНЕНИЯ ==========
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

# ========== ФУНКЦИЯ ПОЛУЧЕНИЯ ПОЛЬЗОВАТЕЛЯ ==========
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

# ========== ПРОФИЛЬ И ТОПЫ ==========
async def get_profile_text(user_id, target_id=None):
    if target_id is None:
        target_id = user_id
    target = get_user(target_id)
    try:
        chat = await bot.get_chat(target_id)
        name = chat.username or chat.first_name or str(target_id)
    except:
        name = str(target_id)
    pets_list = []
    for i, pet_id in enumerate(target["pets"][:10]):
        pet = PETS[pet_id]
        pet_name = target["pet_names"].get(pet_id, "")
        name_str = f" '{pet_name}'" if pet_name else ""
        pets_list.append(f"{i+1}. {pet['name']}{name_str}")
    pets_text = "\n".join(pets_list) if pets_list else "Нет питомцев"
    if len(target["pets"]) > 10:
        pets_text += f"\n... и ещё {len(target['pets']) - 10} питомцев"
    return (
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
        f"🐾 **Питомцы:**\n{pets_text}"
    )

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

# ========== КЛАВИАТУРЫ ==========
def main_kb():
    return ReplyKeyboardMarkup(
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

def games_kb():
    return ReplyKeyboardMarkup(
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

def admin_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💰 Выдать дубли"), KeyboardButton(text="🎁 Выдать питомца")],
            [KeyboardButton(text="📢 Объявление"), KeyboardButton(text="📊 Статистика")],
            [KeyboardButton(text="◀️ Назад")]
        ],
        resize_keyboard=True
    )

def chests_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📦 Обычный (100💎)")],
            [KeyboardButton(text="✨ Эпический (500💎)")],
            [KeyboardButton(text="🔥 Легендарный (2000💎)")],
            [KeyboardButton(text="◀️ Назад")]
        ],
        resize_keyboard=True
    )

def back_kb():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Назад")]], resize_keyboard=True)

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

# ========== ИГРЫ ==========
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
        return False, f"❌ Не хватает 30 дублей!\n💰 {user['dubli']}💎"
    slots = ["🍒", "🍋", "🍊", "🍉", "⭐", "💎", "7️⃣"]
    result = [random.choice(slots) for _ in range(3)]
    if result[0] == result[1] == result[2]:
        reward = 150
        user["dubli"] += reward
        msg = f"🎰 ДЖЕКПОТ! {result[0]}{result[1]}{result[2]} +150💎"
    elif result[0] == result[1] or result[1] == result[2]:
        reward = 60
        user["dubli"] += reward
        msg = f"🎰 Пара! {result[0]}{result[1]}{result[2]} +60💎"
    else:
        user["dubli"] -= 30
        msg = f"😔 {result[0]}{result[1]}{result[2]} -30💎"
    user["stats"]["games"] += 1
    save_data(users)
    return True, f"{msg}\n💰 {user['dubli']}💎"

async def game_blackjack(user_id):
    user = get_user(user_id)
    if user["dubli"] < 50:
        return False, f"❌ Не хватает 50 дублей!\n💰 {user['dubli']}💎"
    player = random.randint(10, 21)
    bot = random.randint(10, 21)
    if player > bot:
        reward = random.randint(50, 200)
        user["dubli"] += reward
        user["stats"]["wins"] += 1
        msg = f"🎉 {player} vs {bot} +{reward}💎"
    else:
        user["dubli"] -= 50
        user["stats"]["losses"] += 1
        msg = f"😔 {player} vs {bot} -50💎"
    user["stats"]["games"] += 1
    save_data(users)
    return True, f"{msg}\n💰 {user['dubli']}💎"

async def game_roulette(user_id):
    user = get_user(user_id)
    if user["dubli"] < 40:
        return False, f"❌ Не хватает 40 дублей!\n💰 {user['dubli']}💎"
    number = random.randint(0, 36)
    color = "красное" if number % 2 == 0 else "чёрное"
    win = random.choice([True, False])
    if win:
        reward = random.randint(40, 120)
        user["dubli"] += reward
        user["stats"]["wins"] += 1
        msg = f"🎡 Выпало {number} ({color})! +{reward}💎"
    else:
        user["dubli"] -= 40
        user["stats"]["losses"] += 1
        msg = f"😔 Выпало {number} ({color})! -40💎"
    user["stats"]["games"] += 1
    save_data(users)
    return win, f"{msg}\n💰 {user['dubli']}💎"

async def game_race(user_id):
    user = get_user(user_id)
    if user["dubli"] < 35:
        return False, f"❌ Не хватает 35 дублей!\n💰 {user['dubli']}💎"
    horses = ["🐎 Вороной", "🐎 Белый", "🐎 Рыжий", "🐎 Гнедой"]
    player = random.choice(horses)
    winner = random.choice(horses)
    if player == winner:
        reward = random.randint(35, 100)
        user["dubli"] += reward
        user["stats"]["wins"] += 1
        msg = f"🏆 Твоя лошадь {player} победила! +{reward}💎"
    else:
        user["dubli"] -= 35
        user["stats"]["losses"] += 1
        msg = f"😔 Победил {winner}, ты ставил на {player}. -35💎"
    user["stats"]["games"] += 1
    save_data(users)
    return True, f"{msg}\n💰 {user['dubli']}💎"

async def game_safe(user_id):
    user = get_user(user_id)
    if user["dubli"] < 45:
        return False, f"❌ Не хватает 45 дублей!\n💰 {user['dubli']}💎"
    code = random.randint(100, 999)
    guess = random.randint(100, 999)
    if abs(code - guess) < 50:
        reward = random.randint(45, 150)
        user["dubli"] += reward
        msg = f"🔐 Код {code}, ты ввёл {guess}! +{reward}💎"
    else:
        user["dubli"] -= 45
        msg = f"😔 Код {code}, ты ввёл {guess}! -45💎"
    user["stats"]["games"] += 1
    save_data(users)
    return True, f"{msg}\n💰 {user['dubli']}💎"

async def game_darts(user_id):
    user = get_user(user_id)
    if user["dubli"] < 25:
        return False, f"❌ Не хватает 25 дублей!\n💰 {user['dubli']}💎"
    score = random.randint(1, 10)
    if score >= 8:
        reward = random.randint(25, 80)
        user["dubli"] += reward
        msg = f"🎯 Ты попал в {score} очков! +{reward}💎"
    else:
        user["dubli"] -= 25
        msg = f"😔 Ты попал в {score} очков! -25💎"
    user["stats"]["games"] += 1
    save_data(users)
    return True, f"{msg}\n💰 {user['dubli']}💎"

async def game_duel(user_id):
    user = get_user(user_id)
    if user["dubli"] < 30:
        return False, f"❌ Не хватает 30 дублей!\n💰 {user['dubli']}💎"
    player = random.randint(1, 10)
    bot = random.randint(1, 10)
    if player > bot:
        reward = random.randint(30, 90)
        user["dubli"] += reward
        msg = f"⚔️ Ты нанёс {player} урона, враг {bot}. +{reward}💎"
    else:
        user["dubli"] -= 30
        msg = f"😔 Ты нанёс {player} урона, враг {bot}. -30💎"
    user["stats"]["games"] += 1
    save_data(users)
    return True, f"{msg}\n💰 {user['dubli']}💎"

async def game_fishing(user_id):
    user = get_user(user_id)
    if user["dubli"] < 20:
        return False, f"❌ Не хватает 20 дублей!\n💰 {user['dubli']}💎"
    fish = random.choice(["маленькую рыбку", "среднюю рыбку", "большую рыбу", "акулу", "золотую рыбку"])
    if fish == "акулу":
        reward = random.randint(20, 80)
        user["dubli"] += reward
        msg = f"🎣 Ты поймал {fish}! +{reward}💎"
    elif fish == "золотую рыбку":
        reward = random.randint(50, 150)
        user["dubli"] += reward
        msg = f"🎣 Ты поймал {fish}! Исполни желание? +{reward}💎"
    else:
        user["dubli"] -= 20
        msg = f"😔 Ты поймал {fish}. -20💎"
    user["stats"]["games"] += 1
    save_data(users)
    return True, f"{msg}\n💰 {user['dubli']}💎"

async def game_clover(user_id):
    user = get_user(user_id)
    if user["dubli"] < 15:
        return False, f"❌ Не хватает 15 дублей!\n💰 {user['dubli']}💎"
    luck = random.randint(1, 100)
    if luck > 70:
        reward = random.randint(15, 60)
        user["dubli"] += reward
        msg = f"🍀 Тебе повезло! +{reward}💎"
    else:
        user["dubli"] -= 15
        msg = f"😔 Сегодня не твой день... -15💎"
    user["stats"]["games"] += 1
    save_data(users)
    return True, f"{msg}\n💰 {user['dubli']}💎"

async def game_crystals(user_id):
    user = get_user(user_id)
    if user["dubli"] < 50:
        return False, f"❌ Не хватает 50 дублей!\n💰 {user['dubli']}💎"
    crystals = random.randint(1, 100)
    if crystals > 80:
        reward = random.randint(50, 200)
        user["dubli"] += reward
        msg = f"💎 Ты нашёл {crystals} кристаллов! +{reward}💎"
    else:
        user["dubli"] -= 50
        msg = f"😔 Ты нашёл {crystals} кристаллов... -50💎"
    user["stats"]["games"] += 1
    save_data(users)
    return True, f"{msg}\n💰 {user['dubli']}💎"

# ========== СУНДУКИ ==========
async def open_chest(user_id, chest_type):
    user = get_user(user_id)
    if chest_type == "common" and user["dubli"] < 100:
        return False, "❌ Не хватает 100 дублей!"
    elif chest_type == "epic" and user["dubli"] < 500:
        return False, "❌ Не хватает 500 дублей!"
    elif chest_type == "legendary" and user["dubli"] < 2000:
        return False, "❌ Не хватает 2000 дублей!"
    
    if chest_type == "common":
        user["dubli"] -= 100
        reward = random.randint(50, 200)
        user["dubli"] += reward
        if random.random() < 0.2:
            pet_id = random.choice(list(PETS.keys()))
            if pet_id not in user["pets"]:
                user["pets"].append(pet_id)
                user["stats"]["chests"] += 1
                save_data(users)
                return True, f"🎁 Ты открыл обычный сундук и получил {reward} дублей + нового питомца {PETS[pet_id]['name']}!"
        user["stats"]["chests"] += 1
        save_data(users)
        return True, f"🎁 Ты открыл обычный сундук и получил {reward} дублей!"
    elif chest_type == "epic":
        user["dubli"] -= 500
        reward = random.randint(200, 600)
        user["dubli"] += reward
        if random.random() < 0.4:
            pet_id = random.choice(list(PETS.keys()))
            if pet_id not in user["pets"]:
                user["pets"].append(pet_id)
                user["stats"]["chests"] += 1
                save_data(users)
                return True, f"✨ Ты открыл эпический сундук и получил {reward} дублей + нового питомца {PETS[pet_id]['name']}!"
        user["stats"]["chests"] += 1
        save_data(users)
        return True, f"✨ Ты открыл эпический сундук и получил {reward} дублей!"
    else:
        user["dubli"] -= 2000
        reward = random.randint(800, 2000)
        user["dubli"] += reward
        if random.random() < 0.6:
            pet_id = random.choice(list(PETS.keys()))
            if pet_id not in user["pets"]:
                user["pets"].append(pet_id)
                user["stats"]["chests"] += 1
                save_data(users)
                return True, f"🔥 Ты открыл легендарный сундук и получил {reward} дублей + нового питомца {PETS[pet_id]['name']}!"
        user["stats"]["chests"] += 1
        save_data(users)
        return True, f"🔥 Ты открыл легендарный сундук и получил {reward} дублей!"

# ========== ОХОТА ==========
async def hunt(user_id):
    user = get_user(user_id)
    if not user["pets"]:
        return False, "❌ У тебя нет питомцев для охоты!"
    pet_id = user["pets"][0]
    pet = PETS[pet_id]
    hunger = user["pet_hunger"].get(pet_id, 100)
    if hunger < 20:
        return False, "❌ Питомец голоден! Покорми его сначала."
    user["pet_hunger"][pet_id] = max(0, hunger - 20)
    user["stats"]["hunts"] += 1
    results = [
        {"type": "dubli", "amount": random.randint(20, 80), "chance": 40},
        {"type": "item", "item": "seed", "amount": random.randint(1, 3), "chance": 25},
        {"type": "item", "item": "meat", "amount": 1, "chance": 15},
        {"type": "nothing", "chance": 20}
    ]
    roll = random.randint(1, 100)
    cumulative = 0
    for res in results:
        cumulative += res["chance"]
        if roll <= cumulative:
            if res["type"] == "dubli":
                user["dubli"] += res["amount"]
                save_data(users)
                return True, f"🎯 {pet['name']} принёс {res['amount']} дублей!"
            elif res["type"] == "item":
                user["inventory"][res["item"]] = user["inventory"].get(res["item"], 0) + res["amount"]
                save_data(users)
                item_name = "🌽 Зерно" if res["item"] == "seed" else "🍖 Мясо"
                return True, f"🎯 {pet['name']} принёс {item_name} x{res['amount']}!"
            else:
                return True, f"😔 {pet['name']} ничего не нашёл..."
    return True, f"😔 {pet['name']} ничего не нашёл..."

# ========== PVP ==========
async def pvp(user_id, target_id):
    user = get_user(user_id)
    target = get_user(target_id)
    if not user["pets"] or not target["pets"]:
        return False, "❌ У одного из игроков нет питомцев!"
    user_power = sum(PETS[p]["power"] for p in user["pets"]) + user["rating"]
    target_power = sum(PETS[p]["power"] for p in target["pets"]) + target["rating"]
    user_chance = user_power / (user_power + target_power)
    if random.random() < user_chance:
        reward = random.randint(50, 200)
        user["dubli"] += reward
        user["rating"] += 10
        target["rating"] = max(0, target["rating"] - 5)
        save_data(users)
        return True, f"⚔️ Ты победил! +{reward} дублей, рейтинг +10!"
    else:
        user["dubli"] = max(0, user["dubli"] - 30)
        user["rating"] = max(0, user["rating"] - 5)
        target["rating"] += 10
        save_data(users)
        return False, f"💔 Ты проиграл! -30 дублей, рейтинг -5!"

# ========== КОМАНДЫ ==========
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: Message):
    user_id = message.from_user.id
    get_user(user_id)
    if user_id == POLINA_ID:
        await message.answer("🌸 **ПОЛЯШКА САМАЯ КРУТАЯ!** 🌸\n\n✨ Играй, покупай, сражайся!", reply_markup=main_kb())
    else:
        await message.answer("🎮 **Добро пожаловать в бот!** 🎮\n\nИграй, покупай питомцев, сражайся в PvP!", reply_markup=main_kb())

@dp.message(Command("profile"))
async def profile_cmd(message: Message):
    user_id = message.from_user.id
    args = message.text.split()
    if len(args) > 1:
        try:
            target_id = int(args[1])
            text = await get_profile_text(user_id, target_id)
            await message.answer(text, parse_mode="Markdown")
        except:
            await message.answer("❌ Неверный ID! Пример: /profile 6900319945")
    else:
        text = await get_profile_text(user_id)
        await message.answer(text, parse_mode="Markdown")

@dp.message(Command("top_rating"))
async def top_rating_cmd(message: Message):
    top = await get_top_rating()
    text = "🏆 **ТОП ПО РЕЙТИНГУ PVP** 🏆\n\n"
    for i, (name, rating, dubli, pets) in enumerate(top, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        text += f"{medal} {name[:20]} — {rating}⭐ ({dubli}💎, {pets} петов)\n"
    await message.answer(text)

@dp.message()
async def handle_message(message: Message):
    user_id = message.from_user.id
    user = get_user(user_id)
    text = message.text
    
    if text == "◀️ Назад":
        await message.answer("Главное меню:", reply_markup=main_kb())
        return
    
    if text == "👑 Админка" and user_id == MASTER_ADMIN_ID:
        await message.answer("👑 АДМИН-ПАНЕЛЬ", reply_markup=admin_kb())
        return
    
    if text == "💰 Выдать дубли" and user_id == MASTER_ADMIN_ID:
        await message.answer("Введи: /add ID КОЛИЧЕСТВО\nПример: /add 6900319945 500")
        return
    
    if text == "🎁 Выдать питомца" and user_id == MASTER_ADMIN_ID:
        await message.answer("Введи: /give ID НАЗВАНИЕ\nПример: /give 6900319945 Дракон")
        return
    
    if text == "📢 Объявление" and user_id == MASTER_ADMIN_ID:
        user["awaiting_broadcast"] = True
        await message.answer("📢 Введи текст объявления:")
        return
    
    if user.get("awaiting_broadcast"):
        count = 0
        for uid in users:
            try:
                await bot.send_message(int(uid), f"📢 **ОБЪЯВЛЕНИЕ** 📢\n\n{text}")
                count += 1
                await asyncio.sleep(0.05)
            except:
                pass
        user["awaiting_broadcast"] = False
        await message.answer(f"✅ Отправлено {count} игрокам!")
        return
    
    if text == "📊 Статистика" and user_id == MASTER_ADMIN_ID:
        await message.answer(
            f"📊 **СТАТИСТИКА** 📊\n\n"
            f"👥 Игроков: {len(users)}\n"
            f"💰 Дублей: {sum(u['dubli'] for u in users.values())}\n"
            f"🐾 Питомцев: {sum(len(u['pets']) for u in users.values())}\n"
            f"🎮 Игр: {sum(u['stats']['games'] for u in users.values())}\n"
            f"📦 Сундуков: {sum(u['stats']['chests'] for u in users.values())}",
            reply_markup=admin_kb()
        )
        return
    
    if text == "👤 Мой профиль":
        profile_text = await get_profile_text(user_id)
        await message.answer(profile_text, parse_mode="Markdown", reply_markup=main_kb())
        return
    
    if text == "🏆 Рейтинг":
        top = await get_top_rating()
        top_text = "🏆 **ТОП ПО РЕЙТИНГУ PVP** 🏆\n\n"
        for i, (name, rating, dubli, pets) in enumerate(top, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            top_text += f"{medal} {name[:20]} — {rating}⭐ ({dubli}💎, {pets} петов)\n"
        await message.answer(top_text, reply_markup=main_kb())
        return
    
    # Игры
    if text == "🎮 Игры":
        await message.answer("🎮 **Выбери игру:**", reply_markup=games_kb())
        return
    
    if text == "🎲 Орёл/Решка":
        kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Орел"), KeyboardButton(text="Решка")], [KeyboardButton(text="◀️ Назад")]], resize_keyboard=True)
        await message.answer("Выбери:", reply_markup=kb)
        return
    
    if text in ["Орел", "Решка"]:
        win, msg = await game_coin(user_id, text)
        await message.answer(msg, reply_markup=games_kb())
        return
    
    if text == "🔢 Угадай число":
        await message.answer("Введи число от 1 до 10:", reply_markup=back_kb())
        user["awaiting_number"] = True
        return
    
    if user.get("awaiting_number") and text.isdigit() and 1 <= int(text) <= 10:
        user["awaiting_number"] = False
        win, msg = await game_number(user_id, int(text))
        await message.answer(msg, reply_markup=games_kb())
        return
    
    if text == "🎲 Кости":
        win, msg = await game_dice(user_id)
        await message.answer(msg, reply_markup=games_kb())
        return
    
    if text == "✊ КНБ":
        kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="камень"), KeyboardButton(text="ножницы"), KeyboardButton(text="бумага")], [KeyboardButton(text="◀️ Назад")]], resize_keyboard=True)
        await message.answer("Выбери:", reply_markup=kb)
        return
    
    if text in ["камень", "ножницы", "бумага"]:
        win, msg = await game_rps(user_id, text)
        await message.answer(msg, reply_markup=games_kb())
        return
    
    if text == "⬆️ Выше-Ниже":
        kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="higher"), KeyboardButton(text="lower")], [KeyboardButton(text="◀️ Назад")]], resize_keyboard=True)
        await message.answer("Следующее число будет выше (higher) или ниже (lower)?", reply_markup=kb)
        return
    
    if text in ["higher", "lower"]:
        win, msg = await game_higher(user_id, text)
        await message.answer(msg, reply_markup=games_kb())
        return
    
    if text == "🎰 Слоты":
        win, msg = await game_slots(user_id)
        await message.answer(msg, reply_markup=games_kb())
        return
    
    if text == "🃏 Блэкджек":
        win, msg = await game_blackjack(user_id)
        await message.answer(msg, reply_markup=games_kb())
        return
    
    if text == "🎡 Рулетка":
        win, msg = await game_roulette(user_id)
        await message.answer(msg, reply_markup=games_kb())
        return
    
    if text == "🐎 Гонки":
        win, msg = await game_race(user_id)
        await message.answer(msg, reply_markup=games_kb())
        return
    
    if text == "🔐 Сейф":
        win, msg = await game_safe(user_id)
        await message.answer(msg, reply_markup=games_kb())
        return
    
    if text == "🎯 Дартс":
        win, msg = await game_darts(user_id)
        await message.answer(msg, reply_markup=games_kb())
        return
    
    if text == "⚔️ Дуэль":
        win, msg = await game_duel(user_id)
        await message.answer(msg, reply_markup=games_kb())
        return
    
    if text == "🎣 Рыбалка":
        win, msg = await game_fishing(user_id)
        await message.answer(msg, reply_markup=games_kb())
        return
    
    if text == "🍀 Клевер":
        win, msg = await game_clover(user_id)
        await message.answer(msg, reply_markup=games_kb())
        return
    
    if text == "💎 Кристаллы":
        win, msg = await game_crystals(user_id)
        await message.answer(msg, reply_markup=games_kb())
        return
    
    # Магазин
    if text == "🏪 Магазин":
        kb, total_pages, page = get_shop_keyboard(0)
        await message.answer(f"🏪 **Магазин** 🏪\nСтраница {page+1} из {total_pages}\nВсего: {len(PETS)} питомцев", reply_markup=kb)
        return
    
    # Питомцы
    if text == "🐾 Мои питомцы":
        if not user["pets"]:
            await message.answer("🐾 У тебя пока нет питомцев! Купи в магазине.", reply_markup=main_kb())
        else:
            pets_list = []
            for i, pet_id in enumerate(user["pets"][:30]):
                pet = PETS[pet_id]
                hunger = user["pet_hunger"].get(pet_id, 100)
                status = "😋" if hunger > 50 else "😔" if hunger > 20 else "💀"
                name = user["pet_names"].get(pet_id, "")
                name_str = f" '{name}'" if name else ""
                pets_list.append(f"{i+1}. {pet['name']}{name_str} {status} {hunger}%")
            text_msg = f"🐾 **Твои питомцы** ({len(user['pets'])}):\n\n" + "\n".join(pets_list)
            if len(user["pets"]) > 30:
                text_msg += f"\n... и ещё {len(user['pets']) - 30} питомцев!"
            await message.answer(text_msg, reply_markup=main_kb())
        return
    
    # Бонус
    if text == "🎁 Бонус":
        today = datetime.now().date().isoformat()
        if user.get("last_daily") == today:
            await message.answer("🎁 Ты уже получал бонус сегодня! Завтра приходи!", reply_markup=main_kb())
        else:
            bonus = random.randint(50, 200)
            user["dubli"] += bonus
            user["last_daily"] = today
            save_data(users)
            await message.answer(f"🎁 +{bonus} дублей!\n💰 {user['dubli']}💎", reply_markup=main_kb())
        return
    
    # Дубли
    if text == "💰 Дубли":
        await message.answer(
            f"💰 **{user['dubli']} дублей**\n\n"
            f"📊 Статистика:\n"
            f"🎮 Игр: {user['stats']['games']}\n"
            f"🏆 Побед: {user['stats']['wins']}\n"
            f"💔 Поражений: {user['stats']['losses']}\n"
            f"📦 Сундуков: {user['stats']['chests']}\n"
            f"🎯 Охот: {user['stats']['hunts']}\n"
            f"⭐ Рейтинг: {user['rating']}",
            reply_markup=main_kb()
        )
        return
    
    # Топ
    if text == "🏆 Топ":
        players = []
        for uid, data in users.items():
            try:
                chat = await bot.get_chat(int(uid))
                name = chat.username or chat.first_name or str(uid)
            except:
                name = str(uid)
            players.append((name, data["dubli"], len(data["pets"])))
        players.sort(key=lambda x: x[1], reverse=True)
        top_text = "🏆 **ТОП ИГРОКОВ** 🏆\n\n"
        for i, (name, dubli, pets) in enumerate(players[:15], 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            top_text += f"{medal} {name[:20]} — {dubli}💎 ({pets} петов)\n"
        await message.answer(top_text, reply_markup=main_kb())
        return
    
    # Сундуки
    if text == "🎁 Сундуки":
        await message.answer("🎁 **Сундуки** 🎁\n\n📦 Обычный (100💎) — дубли + шанс питомца\n✨ Эпический (500💎) — больше дублей + шанс питомца\n🔥 Легендарный (2000💎) — много дублей + шанс питомца", reply_markup=chests_kb())
        return
    
    if text == "📦 Обычный (100💎)":
        success, msg = await open_chest(user_id, "common")
        await message.answer(msg, reply_markup=chests_kb())
        return
    
    if text == "✨ Эпический (500💎)":
        success, msg = await open_chest(user_id, "epic")
        await message.answer(msg, reply_markup=chests_kb())
        return
    
    if text == "🔥 Легендарный (2000💎)":
        success, msg = await open_chest(user_id, "legendary")
        await message.answer(msg, reply_markup=chests_kb())
        return
    
    # Охота
    if text == "🎯 Охота":
        success, msg = await hunt(user_id)
        await message.answer(msg, reply_markup=main_kb())
        return
    
    # PvP
    if text == "⚔️ PvP":
        await message.answer("⚔️ Введи ID противника:\nПример: 6900319945", reply_markup=back_kb())
        user["awaiting_pvp"] = True
        return
    
    if user.get("awaiting_pvp"):
        try:
            target_id = int(text)
            if target_id == user_id:
                await message.answer("❌ Нельзя сражаться с самим собой!")
            else:
                win, msg = await pvp(user_id, target_id)
                await message.answer(msg, reply_markup=main_kb())
        except:
            await message.answer("❌ Неверный ID!")
        user["awaiting_pvp"] = False
        return
    
    # Дать имя
    if text == "✏️ Дать имя":
        if not user["pets"]:
            await message.answer("❌ У тебя нет питомцев!")
            return
        await message.answer("Введи номер питомца и имя:\nПример: `1 Буся`", parse_mode="Markdown")
        user["awaiting_name"] = True
        return
    
    if user.get("awaiting_name"):
        try:
            parts = text.split(maxsplit=1)
            pet_index = int(parts[0]) - 1
            name = parts[1]
            if 0 <= pet_index < len(user["pets"]):
                pet_id = user["pets"][pet_index]
                user["pet_names"][pet_id] = name
                save_data(users)
                await message.answer(f"✅ Питомец теперь носит имя **{name}**!")
            else:
                await message.answer("❌ Неправильный номер!")
        except:
            await message.answer("❌ Пример: `1 Буся`", parse_mode="Markdown")
        user["awaiting_name"] = False
        return

@dp.callback_query()
async def handle_callback(call: CallbackQuery):
    user_id = call.from_user.id
    user = get_user(user_id)
    data = call.data
    
    if data == "close_shop":
        await call.message.delete()
        return
    
    if data.startswith("shop_page_"):
        page = int(data.split("_")[2])
        kb, total_pages, page = get_shop_keyboard(page)
        await call.message.edit_text(f"🏪 **Магазин** 🏪\nСтраница {page+1} из {total_pages}\nВсего: {len(PETS)} питомцев", reply_markup=kb)
        return
    
    if data.startswith("buy_"):
        pet_id = data.replace("buy_", "")
        pet = PETS.get(pet_id)
        if not pet:
            await call.answer("❌ Питомец не найден!")
            return
        if user["dubli"] >= pet["price"]:
            user["dubli"] -= pet["price"]
            user["pets"].append(pet_id)
            user["pet_hunger"][pet_id] = 100
            user["pet_levels"][pet_id] = 1
            save_data(users)
            await call.message.edit_text(f"✅ Ты купил {pet['name']}!\nОсталось: {user['dubli']}💎")
            await call.answer(f"Куплен {pet['name']}!")
        else:
            await call.answer(f"❌ Нужно {pet['price']}💎", show_alert=True)

@dp.message(Command("add"))
async def add_dubli(message: Message):
    if message.from_user.id != MASTER_ADMIN_ID:
        await message.answer("❌ Нет доступа!")
        return
    args = message.text.split()
    if len(args) < 3:
        await message.answer("❌ /add ID КОЛИЧЕСТВО")
        return
    try:
        target_id = int(args[1])
        amount = int(args[2])
        if target_id not in users:
            users[target_id] = get_user(target_id)
        users[str(target_id)]["dubli"] += amount
        save_data(users)
        await message.answer(f"✅ Выдано {amount} дублей пользователю {target_id}")
    except:
        await message.answer("❌ Ошибка!")

@dp.message(Command("give"))
async def give_pet(message: Message):
    if message.from_user.id != MASTER_ADMIN_ID:
        await message.answer("❌ Нет доступа!")
        return
    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        await message.answer("❌ /give ID НАЗВАНИЕ")
        return
    try:
        target_id = int(args[1])
        pet_name = args[2].lower()
        for pet_id, pet in PETS.items():
            if pet_name in pet["name"].lower():
                if str(target_id) not in users:
                    users[str(target_id)] = get_user(target_id)
                users[str(target_id)]["pets"].append(pet_id)
                save_data(users)
                await message.answer(f"✅ Выдан питомец {pet['name']} пользователю {target_id}")
                return
        await message.answer("❌ Питомец не найден!")
    except:
        await message.answer("❌ Ошибка!")

# ========== ЗАПУСК ==========
async def main():
    print(f"✅ МЕГА-БОТ ЗАПУЩЕН!")
    print(f"🐾 ПИТОМЦЕВ: {len(PETS)}")
    print(f"🎮 ИГР: 15")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
