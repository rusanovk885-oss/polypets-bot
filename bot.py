import asyncio
import random
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# ========== ТОКЕН ==========
TOKEN = "8949697674:AAHAZywQYpmpYzx4BE2LJY1JiGC76WxWRx4"

# ========== АДМИНЫ ==========
ADMIN_IDS = [6900319945]
POLINA_ID = 8428411159

# ========== 100+ ПИТОМЦЕВ ==========
PET_NAMES = [
    "Курица", "Петух", "Цыплёнок", "Крокодил", "Хомяк", "Крыса", "Морская свинка", "Попугай", "Канарейка", "Черепаха",
    "Кот", "Кошка", "Котёнок", "Лев", "Тигр", "Леопард", "Гепард", "Пума", "Рысь", "Ягуар",
    "Пёс", "Щенок", "Волк", "Лиса", "Шакал", "Койот", "Хаски", "Овчарка", "Такса", "Бульдог",
    "Медведь", "Белый медведь", "Панда", "Барибал", "Гризли",
    "Лошадь", "Осёл", "Зебра", "Жираф", "Слон", "Носорог", "Бегемот", "Олень", "Лось", "Кабан",
    "Обезьяна", "Шимпанзе", "Горилла", "Орангутанг", "Лемур",
    "Кенгуру", "Коала", "Вомбат", "Опоссум", "Квокка",
    "Орёл", "Сокол", "Ястреб", "Сова", "Филин", "Пингвин", "Фламинго", "Лебедь", "Павлин", "Страус",
    "Дельфин", "Кит", "Касатка", "Акула", "Скат", "Осьминог", "Кальмар", "Медуза", "Краб", "Лобстер",
    "Змея", "Гадюка", "Кобра", "Питон", "Удав", "Ящерица", "Варан", "Игуана", "Хамелеон", "Геккон",
    "Паук", "Скорпион", "Пчела", "Бабочка", "Божья коровка", "Кузнечик", "Стрекоза", "Муравей", "Жук", "Богомол",
    "Лягушка", "Жаба", "Тритон", "Саламандра", "Квакша",
    "Дракон", "Единорог", "Феникс", "Грифон", "Цербер", "Пегас", "Циклоп", "Минотавр", "Кракен", "Василиск", "Химера", "Сфинкс"
]

PRICES = [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 220, 240, 260, 280, 300, 350, 400, 450, 500]
emoji_list = ["🐔", "🐓", "🐥", "🐊", "🐹", "🐀", "🐭", "🦜", "🐦", "🐢", "🐱", "🐈", "🐈⬛", "🦁", "🐯", "🐆", "🐅", "🐻", "🐈", "🐆", "🐕", "🐶", "🐺", "🦊", "🐕", "🐺", "🐕‍🦺", "🐕", "🐩", "🐕", "🐻", "🐻‍❄️", "🐼", "🐻", "🐻", "🐎", "🫏", "🦓", "🦒", "🐘", "🦏", "🦛", "🦌", "🦌", "🐗", "🐒", "🦍", "🦧", "🦝", "🐨", "🦘", "🦥", "🦔", "🐁", "🦅", "🦅", "🦅", "🦉", "🦉", "🐧", "🦩", "🦢", "🦚", "🐦‍⬛", "🐬", "🐋", "🐋", "🦈", "🐟", "🐙", "🦑", "🪼", "🦀", "🦞", "🐍", "🐍", "🐍", "🐍", "🐍", "🦎", "🦎", "🦎", "🦎", "🦎", "🕷️", "🦂", "🐝", "🦋", "🐞", "🦗", "🦟", "🐜", "🪲", "🦗", "🐸", "🐸", "🦎", "🦎", "🐸", "🐉", "🦄", "🔥", "🦅", "🔱", "🐴", "🔱", "🐂", "🐙", "🐉", "🦄"]

PETS = {}
for i, name in enumerate(PET_NAMES):
    emoji = emoji_list[i % len(emoji_list)]
    if i < 40:
        rarity = "⚪ Обычный"
    elif i < 70:
        rarity = "🔵 Редкий"
    elif i < 90:
        rarity = "🟣 Эпический"
    else:
        rarity = "🟠 Легендарный"
    price = PRICES[i % len(PRICES)]
    PETS[f"pet_{i}"] = {"name": f"{emoji} {name}", "price": price, "emoji": emoji, "rarity": rarity}

# ========== БАЗА ДАННЫХ ==========
users = {}

def get_user(user_id):
    if user_id not in users:
        users[user_id] = {
            "dubli": 500,
            "pets": [],
            "pet_names": {},
            "last_daily": None,
            "stats": {"games": 0, "wins": 0, "losses": 0}
        }
    return users[user_id]

# ========== 15 ИГР ==========
async def game_coin(user_id, choice):
    user = get_user(user_id)
    if user["dubli"] < 10:
        return False, f"❌ Не хватает 10 дублей!\n💰 У тебя {user['dubli']}💎"
    result = random.choice(["Орел", "Решка"])
    win = choice == result
    if win:
        user["dubli"] += 10
        user["stats"]["wins"] += 1
        msg = f"🎉 {result}! Ты выиграл +10 дублей!"
    else:
        user["dubli"] -= 10
        user["stats"]["losses"] += 1
        msg = f"😔 {result}! Ты проиграл -10 дублей!"
    user["stats"]["games"] += 1
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
    elif result[0] == result[1] or result[1] == result[2] or result[0] == result[2]:
        reward = 60
        user["dubli"] += reward
        msg = f"🎰 Пара! {result[0]}{result[1]}{result[2]} +60💎"
    else:
        user["dubli"] -= 30
        msg = f"😔 {result[0]}{result[1]}{result[2]} -30💎"
    user["stats"]["games"] += 1
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
    return True, f"{msg}\n💰 {user['dubli']}💎"

async def game_fishing(user_id):
    user = get_user(user_id)
    if user["dubli"] < 20:
        return False, f"❌ Не хватает 20 дублей!\n💰 {user['dubli']}💎"
    fish = random.choice(["🐟 маленькую рыбку", "🐠 среднюю рыбку", "🐡 большую рыбу", "🦈 акулу"])
    if fish == "🦈 акулу":
        reward = random.randint(20, 80)
        user["dubli"] += reward
        msg = f"🎣 Ты поймал {fish}! +{reward}💎"
    else:
        user["dubli"] -= 20
        msg = f"😔 Ты поймал {fish}. -20💎"
    user["stats"]["games"] += 1
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
    return True, f"{msg}\n💰 {user['dubli']}💎"

# ========== КЛАВИАТУРЫ ==========
def main_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🐾 Мои питомцы"), KeyboardButton(text="🏪 Магазин")],
            [KeyboardButton(text="🎮 Игры"), KeyboardButton(text="🎁 Бонус")],
            [KeyboardButton(text="💰 Дубли"), KeyboardButton(text="🏆 Топ")],
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

def back_kb():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Назад")]], resize_keyboard=True)

# ========== БОТ ==========
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: Message):
    user_id = message.from_user.id
    get_user(user_id)
    
    if user_id == POLINA_ID:
        await message.answer(
            "🌸 **ПОЛЯШКА САМАЯ КРУТАЯ!** 🌸\n\n"
            "✨ Ты зашла в свой личный бот! ✨\n\n"
            f"💰 У тебя {users[user_id]['dubli']} дублей\n"
            f"🐾 Питомцев: {len(users[user_id]['pets'])}",
            reply_markup=main_kb()
        )
    else:
        await message.answer(
            "🎮 **Добро пожаловать в бот!** 🎮\n\n"
            "Играй, покупай питомцев, давай им имена!\n\n"
            f"💰 У тебя {users[user_id]['dubli']} дублей",
            reply_markup=main_kb()
        )

@dp.message(Command("id"))
async def show_id(message: Message):
    await message.answer(f"🆔 Твой ID: `{message.from_user.id}`", parse_mode="Markdown")

@dp.message()
async def handle_message(message: Message):
    user_id = message.from_user.id
    user = get_user(user_id)
    text = message.text
    
    if text == "◀️ Назад":
        await message.answer("Главное меню:", reply_markup=main_kb())
        return
    
    if text == "👑 Админка" and user_id in ADMIN_IDS:
        await message.answer("👑 **АДМИН-ПАНЕЛЬ** 👑", reply_markup=admin_kb())
        return
    
    if text == "🎮 Игры":
        await message.answer("🎮 **Выбери игру:**\n\nСтавки от 5 до 50💎\nУдачи! 🍀", reply_markup=games_kb())
        return
    
    # Игры
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
        kb = InlineKeyboardMarkup(inline_keyboard=[])
        for i, (pet_id, pet) in enumerate(PETS.items()):
            if i >= 20:
                break
            kb.inline_keyboard.append([InlineKeyboardButton(text=f"{pet['name']} — {pet['price']}💎", callback_data=f"buy_{pet_id}")])
        kb.inline_keyboard.append([InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_menu")])
        await message.answer(f"🏪 **Магазин питомцев** 🏪\n\nВсего питомцев: {len(PETS)}\n\nВыбери питомца:", reply_markup=kb)
        return
    
    # Дать имя
    if text == "✏️ Дать имя":
        if len(user["pets"]) == 0:
            await message.answer("🐾 У тебя пока нет питомцев! Купи сначала в магазине.", reply_markup=main_kb())
        else:
            pets_list = []
            for i, pet_id in enumerate(user["pets"]):
                pet = PETS[pet_id]
                current_name = user["pet_names"].get(pet_id, "")
                name_str = f" (имя: {current_name})" if current_name else ""
                pets_list.append(f"{i+1}. {pet['name']}{name_str}")
            await message.answer(
                f"🐾 **Выбери питомца по номеру и напиши имя:**\n\n" + "\n".join(pets_list) + "\n\nПример: `1 Буся`",
                reply_markup=back_kb()
            )
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
                user["awaiting_name"] = False
                await message.answer(f"✅ Питомец {PETS[pet_id]['name']} теперь носит имя **{name}**!", reply_markup=main_kb())
            else:
                await message.answer("❌ Неправильный номер питомца!")
        except:
            await message.answer("❌ Напиши в формате: `номер имя`\nПример: `1 Буся`", reply_markup=back_kb())
        return
    
    # Мои питомцы
    if text == "🐾 Мои питомцы":
        if len(user["pets"]) == 0:
            await message.answer("🐾 У тебя пока нет питомцев! Купи в магазине.", reply_markup=main_kb())
        else:
            pets_list = []
            for i, pet_id in enumerate(user["pets"]):
                pet = PETS[pet_id]
                name = user["pet_names"].get(pet_id, "")
                name_str = f" (имя: {name})" if name else ""
                pets_list.append(f"{i+1}. {pet['name']}{name_str} [{pet['rarity']}]")
            await message.answer(f"🐾 **Твои питомцы** ({len(user['pets'])}):\n\n" + "\n".join(pets_list), reply_markup=main_kb())
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
            await message.answer(f"🎁 **Ежедневный бонус!** +{bonus} дублей! 💰\nТеперь у тебя {user['dubli']}💎", reply_markup=main_kb())
        return
    
    # Дубли
    if text == "💰 Дубли":
        await message.answer(
            f"💰 **Твой баланс:** {user['dubli']} дублей!\n\n"
            f"📊 **Статистика:**\n"
            f"🎮 Игр сыграно: {user['stats']['games']}\n"
            f"🏆 Побед: {user['stats']['wins']}\n"
            f"💔 Поражений: {user['stats']['losses']}",
            reply_markup=main_kb()
        )
        return
    
    # Топ
    if text == "🏆 Топ":
        players = []
        for uid, data in users.items():
            try:
                chat = await bot.get_chat(uid)
                name = chat.username or chat.first_name or str(uid)
            except:
                name = str(uid)
            players.append((name, data["dubli"], len(data["pets"]), data["stats"]["games"]))
        
        players.sort(key=lambda x: x[1], reverse=True)
        top_text = "🏆 **ТОП ИГРОКОВ** 🏆\n\n"
        for i, (name, dubli, pets, games) in enumerate(players[:15], 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            top_text += f"{medal} {name[:20]} — {dubli}💎 ({pets} петов)\n"
        await message.answer(top_text, reply_markup=main_kb())
        return
    
    # Админ команды
    if text == "💰 Выдать дубли" and user_id in ADMIN_IDS:
        await message.answer("Введи: `/add ID КОЛИЧЕСТВО`\nПример: /add 6900319945 500", parse_mode="Markdown")
        return
    
    if text == "🎁 Выдать питомца" and user_id in ADMIN_IDS:
        await message.answer("Введи: `/give ID НАЗВАНИЕ`\nПример: /give 6900319945 Дракон", parse_mode="Markdown")
        return
    
    if text == "📢 Объявление" and user_id in ADMIN_IDS:
        await message.answer("Введи текст объявления:", reply_markup=back_kb())
        user["awaiting_broadcast"] = True
        return
    
    if user.get("awaiting_broadcast"):
        count = 0
        for uid in users:
            try:
                await bot.send_message(uid, f"📢 **ОБЪЯВЛЕНИЕ ОТ АДМИНА** 📢\n\n{text}")
                count += 1
                await asyncio.sleep(0.05)
            except:
                pass
        user["awaiting_broadcast"] = False
        await message.answer(f"✅ Объявление отправлено {count} игрокам!", reply_markup=admin_kb())
        return
    
    if text == "📊 Статистика" and user_id in ADMIN_IDS:
        total_players = len(users)
        total_dubli = sum(u["dubli"] for u in users.values())
        total_pets = sum(len(u["pets"]) for u in users.values())
        total_games = sum(u["stats"]["games"] for u in users.values())
        await message.answer(
            f"📊 **СТАТИСТИКА БОТА** 📊\n\n"
            f"👥 Игроков: {total_players}\n"
            f"💰 Дублей в обороте: {total_dubli}\n"
            f"🐾 Всего питомцев: {total_pets}\n"
            f"🎮 Сыграно игр: {total_games}",
            reply_markup=admin_kb()
        )
        return

@dp.callback_query()
async def handle_callback(call: CallbackQuery):
    user_id = call.from_user.id
    user = get_user(user_id)
    data = call.data
    
    if data == "back_to_menu":
        await call.message.edit_text("Главное меню:", reply_markup=main_kb())
        await call.answer()
        return
    
    if data.startswith("buy_"):
        pet_id = data.replace("buy_", "")
        pet = PETS.get(pet_id)
        
        if user["dubli"] >= pet["price"]:
            user["dubli"] -= pet["price"]
            user["pets"].append(pet_id)
            await call.message.edit_text(f"✅ Ты купил {pet['name']}! 💖\nОсталось: {user['dubli']}💎")
            await call.answer(f"Куплен {pet['name']}!")
        else:
            await call.answer(f"❌ Не хватает! Нужно {pet['price']}💎", show_alert=True)

@dp.message(Command("add"))
async def add_dubli(message: Message):
    user_id = message.from_user.id
    if user_id not in ADMIN_IDS:
        await message.answer("❌ Нет доступа!")
        return
    
    args = message.text.split()
    if len(args) < 3:
        await message.answer("❌ Использование: /add ID КОЛИЧЕСТВО\nПример: /add 6900319945 500")
        return
    
    try:
        target_id = int(args[1])
        amount = int(args[2])
        if target_id not in users:
            users[target_id] = get_user(target_id)
        users[target_id]["dubli"] += amount
        await message.answer(f"✅ Выдано {amount} дублей пользователю {target_id}")
        try:
            await bot.send_message(target_id, f"👑 Админ выдал тебе {amount} дублей! 💰")
        except:
            pass
    except:
        await message.answer("❌ Ошибка! Пример: /add 6900319945 500")

@dp.message(Command("give"))
async def give_pet(message: Message):
    user_id = message.from_user.id
    if user_id not in ADMIN_IDS:
        await message.answer("❌ Нет доступа!")
        return
    
    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        await message.answer("❌ Использование: /give ID НАЗВАНИЕ\nПример: /give 6900319945 Дракон")
        return
    
    try:
        target_id = int(args[1])
        pet_name = args[2].lower()
        
        for pet_id, pet in PETS.items():
            if pet_name in pet["name"].lower():
                if target_id not in users:
                    users[target_id] = get_user(target_id)
                users[target_id]["pets"].append(pet_id)
                await message.answer(f"✅ Выдан питомец {pet['name']} пользователю {target_id}")
                try:
                    await bot.send_message(target_id, f"👑 Админ выдал тебе питомца {pet['name']}! 🎉")
                except:
                    pass
                return
        await message.answer("❌ Питомец не найден!")
    except:
        await message.answer("❌ Ошибка! Пример: /give 6900319945 Дракон")

# ========== ЗАПУСК ==========
async def main():
    print("✅ МЕГА-БОТ ЗАПУЩЕН!")
    print(f"🐾 ПИТОМЦЕВ: {len(PETS)}")
    print(f"🎮 ИГР: 15")
    print(f"👑 АДМИНЫ: {ADMIN_IDS}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
