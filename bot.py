import asyncio
import random
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# ========== ТОКЕН ==========
TOKEN = "8949697674:AAHAZywQYpmpYzx4BE2LJY1JiGC76WxWRx4"

# ========== АДМИНЫ ==========
ADMIN_IDS = [6900319945]  # Твой ID
POLINA_ID = 8428411159

# ========== ГЕНЕРАЦИЯ 100+ ПИТОМЦЕВ ==========
PET_NAMES = [
    "Курица", "Крокодил", "Хомяк", "Дракон", "Кот", "Пёс", "Лиса", "Волк", "Медведь", "Панда",
    "Тигр", "Лев", "Слон", "Жираф", "Зебра", "Обезьяна", "Кенгуру", "Коала", "Пингвин", "Фламинго",
    "Сова", "Орёл", "Сокол", "Попугай", "Воробей", "Голубь", "Лебедь", "Утка", "Гусь", "Цыплёнок",
    "Ёж", "Белка", "Заяц", "Лось", "Олень", "Кабан", "Бобр", "Выдра", "Норка", "Соболь",
    "Дельфин", "Кит", "Акула", "Осьминог", "Медуза", "Краб", "Лобстер", "Креветка", "Рыба-клоун", "Скат",
    "Хамелеон", "Ящерица", "Змея", "Черепаха", "Лягушка", "Жаба", "Тритон", "Саламандра", "Геккон", "Игуана",
    "Единорог", "Феникс", "Грифон", "Цербер", "Пегас", "Кракен", "Василиск", "Химера", "Сфинкс", "Циклоп"
]

PRICES = [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 220, 240, 260, 280, 300, 350, 400, 450, 500]
emoji_list = ["🐔", "🐊", "🐹", "🐉", "🐱", "🐶", "🦊", "🐺", "🐻", "🐼", "🐯", "🦁", "🐘", "🦒", "🦓", "🐒", "🦘", "🐨", "🐧", "🦩", "🦉", "🦅", "🦜", "🐦", "🕊️", "🦢", "🦆", "🐥", "🦔", "🐿️", "🐇", "🦌", "🐗", "🦫", "🐬", "🐋", "🦈", "🐙", "🦀", "🦞", "🦐", "🐠", "🦑", "🦎", "🐍", "🐢", "🦄", "🔥", "🦅", "🔱", "🐴", "🐙"]

PETS = {}
for i, name in enumerate(PET_NAMES):
    emoji = emoji_list[i % len(emoji_list)]
    if i < 40:
        rarity = "⚪ common"
    elif i < 70:
        rarity = "🔵 rare"
    elif i < 90:
        rarity = "🟣 epic"
    else:
        rarity = "🟠 legendary"
    price = PRICES[i % len(PRICES)]
    PETS[f"pet_{i}"] = {
        "name": f"{emoji} {name}",
        "price": price,
        "emoji": emoji,
        "rarity": rarity
    }

# ========== ИГРЫ (15 ШТУК) ==========
async def game_coin(user_id, choice):
    user = get_user(user_id)
    if user["dubli"] < 10:
        return False, "❌ Не хватает 10 дублей!"
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
    return win, f"{msg}\n💰 {user['dubli']}💎"

async def game_number(user_id, number):
    user = get_user(user_id)
    if user["dubli"] < 5:
        return False, "❌ Не хватает 5 дублей!"
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
        return False, "❌ Не хватает 20 дублей!"
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
        return False, "❌ Не хватает 15 дублей!"
    choices = ["камень", "ножницы", "бумага"]
    bot = random.choice(choices)
    if choice == bot:
        msg = f"🤝 Ничья! {choice} - {bot}"
        return True, msg
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
        return False, "❌ Не хватает 25 дублей!"
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
        return False, "❌ Не хватает 30 дублей!"
    slots = ["🍒", "🍋", "🍊", "🍉", "⭐", "💎"]
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
    return True, f"{msg}\n💰 {user['dubli']}💎"

async def game_blackjack(user_id):
    user = get_user(user_id)
    if user["dubli"] < 50:
        return False, "❌ Не хватает 50 дублей!"
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
        return False, "❌ Не хватает 40 дублей!"
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
        return False, "❌ Не хватает 35 дублей!"
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
        msg = f"😔 Победил {winner}, а ты ставил на {player}. -35💎"
    user["stats"]["games"] += 1
    return True, f"{msg}\n💰 {user['dubli']}💎"

async def game_safe(user_id):
    user = get_user(user_id)
    if user["dubli"] < 45:
        return False, "❌ Не хватает 45 дублей!"
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
        return False, "❌ Не хватает 25 дублей!"
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
        return False, "❌ Не хватает 30 дублей!"
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
        return False, "❌ Не хватает 20 дублей!"
    fish = random.choice(["🐟 маленькую", "🐠 среднюю", "🐡 большую", "🦈 акулу!"])
    if fish == "🦈 акулу!":
        reward = random.randint(20, 80)
        user["dubli"] += reward
        msg = f"🎣 Ты поймал {fish} +{reward}💎"
    else:
        user["dubli"] -= 20
        msg = f"😔 Ты поймал {fish} -20💎"
    user["stats"]["games"] += 1
    return True, f"{msg}\n💰 {user['dubli']}💎"

async def game_clover(user_id):
    user = get_user(user_id)
    if user["dubli"] < 15:
        return False, "❌ Не хватает 15 дублей!"
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
        return False, "❌ Не хватает 50 дублей!"
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

# ========== БАЗА ДАННЫХ ==========
users = {}

def get_user(user_id):
    if user_id not in users:
        users[user_id] = {
            "dubli": 500,
            "pets": ["kurochka"],
            "last_daily": None,
            "stats": {"games": 0, "wins": 0, "losses": 0}
        }
    return users[user_id]

# ========== КЛАВИАТУРЫ ==========
def main_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🐾 Мои питомцы"), KeyboardButton(text="🏪 Магазин")],
            [KeyboardButton(text="🎮 Игры"), KeyboardButton(text="🎁 Бонус")],
            [KeyboardButton(text="💰 Дубли"), KeyboardButton(text="🏆 Топ")],
            [KeyboardButton(text="👑 Админка")]
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
            [KeyboardButton(text="💰 Выдать дубли"), KeyboardButton(text="📢 Объявление")],
            [KeyboardButton(text="📊 Статистика"), KeyboardButton(text="◀️ Назад")]
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
        await message.answer("🌸 **ПОЛЯШКА САМАЯ КРУТАЯ!** 🌸\n\n✨ Ты зашла в свой личный бот! ✨", reply_markup=main_kb())
    else:
        await message.answer("🎮 **Добро пожаловать в бот!** 🎮\n\nИграй, покупай питомцев, становись лучшим!", reply_markup=main_kb())

@dp.message()
async def handle_message(message: Message):
    user_id = message.from_user.id
    user = get_user(user_id)
    text = message.text
    
    # ========== НАЗАД ==========
    if text == "◀️ Назад":
        await message.answer("Главное меню:", reply_markup=main_kb())
        return
    
    # ========== АДМИНКА ==========
    if text == "👑 Админка" and user_id in ADMIN_IDS:
        await message.answer("👑 **АДМИН-ПАНЕЛЬ** 👑", reply_markup=admin_kb())
        return
    
    # ========== ИГРЫ ==========
    if text == "🎮 Игры":
        await message.answer("🎮 **Выбери игру:**\n\nСтавки от 5 до 50💎\nУдачи! 🍀", reply_markup=games_kb())
        return
    
    # Обработка игр
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
    
    # ========== МАГАЗИН ==========
    if text == "🏪 Магазин":
        # Создаём клавиатуру с питомцами
        kb = InlineKeyboardMarkup(inline_keyboard=[])
        count = 0
        for pet_id, pet in PETS.items():
            if count >= 24:
                break
            kb.inline_keyboard.append([InlineKeyboardButton(text=f"{pet['name']} — {pet['price']}💎", callback_data=f"buy_{pet_id}")])
            count += 1
        kb.inline_keyboard.append([InlineKeyboardButton(text="❌ Закрыть", callback_data="close")])
        
        await message.answer(f"🏪 **Магазин питомцев** 🏪\n\nВсего питомцев: {len(PETS)}\n\nВыбери питомца кнопкой:", reply_markup=kb)
        return
    
    if text == "🐾 Мои питомцы":
        if len(user["pets"]) == 0:
            await message.answer("🐾 У тебя пока нет питомцев! Купи в магазине /shop", reply_markup=main_kb())
        else:
            pets_list = "\n".join([f"{i+1}. {PETS[p]['name']}" for i, p in enumerate(user["pets"][:30])])
            await message.answer(f"🐾 **Твои питомцы** ({len(user['pets'])}):\n\n{pets_list}", reply_markup=main_kb())
        return
    
    # ========== БОНУС ==========
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
    
    # ========== ДУБЛИ ==========
    if text == "💰 Дубли":
        await message.answer(f"💰 **Твой баланс:** {user['dubli']} дублей!\n\n📊 **Статистика:**\n🎮 Игр: {user['stats']['games']}\n🏆 Побед: {user['stats']['wins']}\n💔 Поражений: {user['stats']['losses']}", reply_markup=main_kb())
        return
    
    # ========== ТОП ==========
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
    
    # ========== АДМИН-КОМАНДЫ ==========
    if text == "💰 Выдать дубли" and user_id in ADMIN_IDS:
        await message.answer("Введи: `/add ID КОЛИЧЕСТВО`\nПример: /add 6900319945 500", parse_mode="Markdown", reply_markup=admin_kb())
        return
    
    if text == "📢 Объявление" and user_id in ADMIN_IDS:
        await message.answer("Введи текст объявления:", reply_markup=admin_kb())
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
    
    if data.startswith("buy_"):
        pet_id = data.replace("buy_", "")
        pet = PETS.get(pet_id)
        
        if not pet:
            await call.answer("❌ Питомец не найден!")
            return
        
        if user["dubli"] >= pet["price"]:
            user["dubli"] -= pet["price"]
            user["pets"].append(pet_id)
            await call.message.edit_text(f"✅ Ты купил {pet['name']}! 💖\nОсталось: {user['dubli']}💎")
            await call.answer(f"Куплен {pet['name']}!")
        else:
            await call.answer(f"❌ Не хватает! Нужно {pet['price']}💎", show_alert=True)
    
    elif data == "close":
        await call.message.delete()

@dp.message(Command("add"))
async def add_dubli(message: Message):
    user_id = message.from_user.id
    if user_id not in ADMIN_IDS:
        await message.answer("❌ Нет доступа!")
        return
    
    args = message.text.split()
    if len(args) < 3:
        await message.answer("❌ Использование: /add ID КОЛИЧЕСТВО# ========== БАЗА ДАННЫХ ==========
users = {}

def get_user(user_id):
    if user_id not in users:
        users[user_id] = {
            "dubli": 500,
            "pets": [],
            "pet_counter": 0,
            "last_daily": None,
            "clan": None,
            "stats": {"games": 0, "wins": 0, "losses": 0}
        }
    return users[user_id]

# ========== КЛАВИАТУРЫ ==========
def main_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🐾 Мои питомцы"), KeyboardButton(text="🏪 Магазин")],
            [KeyboardButton(text="🎮 Игры"), KeyboardButton(text="🎁 Бонус")],
            [KeyboardButton(text="💰 Дубли"), KeyboardButton(text="🏆 Топ")],
            [KeyboardButton(text="👥 Кланы"), KeyboardButton(text="⚔️ Арена")],
            [KeyboardButton(text="👑 Админка")]
        ],
        resize_keyboard=True
    )
    return kb

def games_menu_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎲 Орёл/Решка"), KeyboardButton(text="🔢 Угадай число")],
            [KeyboardButton(text="🎲 Кости"), KeyboardButton(text="✊ КНБ")],
            [KeyboardButton(text="⬆️ Выше-Ниже"), KeyboardButton(text="🎰 Слоты")],
            [KeyboardButton(text="🃏 Блэкджек"), KeyboardButton(text="◀️ Назад")]
        ],
        resize_keyboard=True
    )
    return kb

def clan_menu_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Мои кланы"), KeyboardButton(text="➕ Создать клан")],
            [KeyboardButton(text="🔍 Найти клан"), KeyboardButton(text="🚪 Выйти из клана")],
            [KeyboardButton(text="💰 Внести в казну"), KeyboardButton(text="◀️ Назад")]
        ],
        resize_keyboard=True
    )
    return kb

def admin_panel_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💰 Выдать дубли"), KeyboardButton(text="🎁 Выдать питомца")],
            [KeyboardButton(text="📢 Объявление"), KeyboardButton(text="📊 Статистика")],
            [KeyboardButton(text="⏰ Бонус всем"), KeyboardButton(text="◀️ Назад")]
        ],
        resize_keyboard=True
    )
    return kb

def back_kb():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Назад")]], resize_keyboard=True)

# ========== ИГРЫ ==========
async def play_coin(user_id, choice):
    user = get_user(user_id)
    if user["dubli"] < 10:
        return False, "❌ Не хватает 10 дублей!"
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
    return win, f"{msg}\n💰 Теперь {user['dubli']}💎"

async def play_number(user_id, number):
    user = get_user(user_id)
    if user["dubli"] < 5:
        return False, "❌ Не хватает 5 дублей!"
    secret = random.randint(1, 10)
    win = number == secret
    if win:
        reward = random.randint(5, 25)
        user["dubli"] += reward
        user["stats"]["wins"] += 1
        msg = f"🎉 Число {secret}! Ты угадал! +{reward} дублей!"
    else:
        user["dubli"] -= 5
        user["stats"]["losses"] += 1
        msg = f"😔 Число {secret}, ты назвал {number}. -5 дублей!"
    user["stats"]["games"] += 1
    return win, f"{msg}\n💰 Теперь {user['dubli']}💎"

async def play_dice(user_id):
    user = get_user(user_id)
    if user["dubli"] < 20:
        return False, "❌ Не хватает 20 дублей!"
    player = random.randint(1, 6)
    bot = random.randint(1, 6)
    win = player > bot
    if win:
        reward = random.randint(20, 60)
        user["dubli"] += reward
        user["stats"]["wins"] += 1
        msg = f"🎉 Ты выбросил {player}, бот {bot}. +{reward} дублей!"
    elif player < bot:
        user["dubli"] -= 20
        user["stats"]["losses"] += 1
        msg = f"😔 Ты выбросил {player}, бот {bot}. -20 дублей!"
    else:
        msg = f"🤝 Ничья! {player} - {bot}. Дубли возвращены."
    user["stats"]["games"] += 1
    return win, f"{msg}\n💰 Теперь {user['dubli']}💎"

async def play_rps(user_id, choice):
    user = get_user(user_id)
    if user["dubli"] < 15:
        return False, "❌ Не хватает 15 дублей!"
    choices = ["камень", "ножницы", "бумага"]
    bot = random.choice(choices)
    if choice == bot:
        msg = f"🤝 Ничья! {choice} - {bot}. Дубли возвращены."
        return True, msg
    elif (choice == "камень" and bot == "ножницы") or (choice == "ножницы" and bot == "бумага") or (choice == "бумага" and bot == "камень"):
        user["dubli"] += 15
        user["stats"]["wins"] += 1
        msg = f"🎉 {choice} vs {bot}! Ты победил! +15 дублей!"
    else:
        user["dubli"] -= 15
        user["stats"]["losses"] += 1
        msg = f"😔 {choice} vs {bot}! Ты проиграл! -15 дублей!"
    user["stats"]["games"] += 1
    return True, f"{msg}\n💰 Теперь {user['dubli']}💎"

async def play_higher(user_id, guess):
    user = get_user(user_id)
    if user["dubli"] < 25:
        return False, "❌ Не хватает 25 дублей!"
    num = random.randint(1, 100)
    next_num = random.randint(1, 100)
    win = (guess == "higher" and next_num > num) or (guess == "lower" and next_num < num)
    if win:
        reward = random.randint(25, 75)
        user["dubli"] += reward
        user["stats"]["wins"] += 1
        msg = f"🎉 Было {num}, стало {next_num}. +{reward} дублей!"
    else:
        user["dubli"] -= 25
        user["stats"]["losses"] += 1
        msg = f"😔 Было {num}, стало {next_num}. -25 дублей!"
    user["stats"]["games"] += 1
    return win, f"{msg}\n💰 Теперь {user['dubli']}💎"

async def play_slots(user_id):
    user = get_user(user_id)
    if user["dubli"] < 30:
        return False, "❌ Не хватает 30 дублей!"
    slots = ["🍒", "🍋", "🍊", "🍉", "⭐", "💎", "7️⃣"]
    result = [random.choice(slots) for _ in range(3)]
    if result[0] == result[1] == result[2]:
        reward = 150
        user["dubli"] += reward
        msg = f"🎰 ДЖЕКПОТ! {result[0]} {result[1]} {result[2]} +{reward} дублей!"
    elif result[0] == result[1] or result[1] == result[2] or result[0] == result[2]:
        reward = 60
        user["dubli"] += reward
        msg = f"🎰 Пара! {result[0]} {result[1]} {result[2]} +{reward} дублей!"
    else:
        user["dubli"] -= 30
        msg = f"😔 {result[0]} {result[1]} {result[2]} -30 дублей!"
    user["stats"]["games"] += 1
    return True, f"{msg}\n💰 Теперь {user['dubli']}💎"

async def play_blackjack(user_id):
    user = get_user(user_id)
    if user["dubli"] < 50:
        return False, "❌ Не хватает 50 дублей!"
    player = random.randint(10, 21)
    bot = random.randint(10, 21)
    win = player > bot
    if win:
        reward = random.randint(50, 200)
        user["dubli"] += reward
        user["stats"]["wins"] += 1
        msg = f"🎉 У тебя {player}, у бота {bot}. +{reward} дублей!"
    else:
        user["dubli"] -= 50
        user["stats"]["losses"] += 1
        msg = f"😔 У тебя {player}, у бота {bot}. -50 дублей!"
    user["stats"]["games"] += 1
    return win, f"{msg}\n💰 Теперь {user['dubli']}💎"

# ========== БОТ ==========
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: Message):
    user_id = message.from_user.id
    get_user(user_id)
    
    # Приветствие "Поляшка самая крутая!"
    if user_id == POLINA_ID:
        await message.answer("🌸 **ПОЛЯШКА САМАЯ КРУТАЯ!** 🌸\n\n✨ Ты зашла в свой личный бот! ✨")
    else:
        await message.answer("🎮 **Добро пожаловать в бот!** 🎮\n\nИграй, покупай питомцев, создавай кланы!", reply_markup=main_kb())

@dp.message(Command("id"))
async def show_id(message: Message):
    await message.answer(f"🆔 Твой ID: `{message.from_user.id}`", parse_mode="Markdown")

@dp.message()
async def handle_message(message: Message):
    user_id = message.from_user.id
    user = get_user(user_id)
    text = message.text
    
    # ========== НАЗАД ==========
    if text == "◀️ Назад":
        await message.answer("Главное меню:", reply_markup=main_kb())
        return
    
    # ========== АДМИНКА ==========
    if text == "👑 Админка" and user_id in ADMIN_IDS:
        await message.answer("👑 **АДМИН-ПАНЕЛЬ** 👑", reply_markup=admin_panel_kb())
        return
    
    # ========== КЛАВИАТУРЫ ==========
    if text == "🎮 Игры":
        await message.answer("🎮 **Выбери игру:**", reply_markup=games_menu_kb())
        return
    
    if text == "👥 Кланы":
        await message.answer("👥 **Кланы и гильдии** 👥\n\nСоздавай клан, приглашай друзей, пополняй казну!", reply_markup=clan_menu_kb())
        return
    
    # ========== ИГРЫ ==========
    if text == "🎲 Орёл/Решка":
        kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Орел"), KeyboardButton(text="Решка")], [KeyboardButton(text="◀️ Назад")]], resize_keyboard=True)
        await message.answer("Выбери:", reply_markup=kb)
        return
    
    if text in ["Орел", "Решка"]:
        win, msg = await play_coin(user_id, text)
        await message.answer(msg, reply_markup=games_menu_kb())
        return
    
    if text == "🔢 Угадай число":
        await message.answer("Введи число от 1 до 10:", reply_markup=back_kb())
        user["awaiting_number"] = True
        return
    
    if user.get("awaiting_number") and text.isdigit() and 1 <= int(text) <= 10:
        user["awaiting_number"] = False
        win, msg = await play_number(user_id, int(text))
        await message.answer(msg, reply_markup=games_menu_kb())
        return
    
    if text == "🎲 Кости":
        win, msg = await play_dice(user_id)
        await message.answer(msg, reply_markup=games_menu_kb())
        return
    
    if text == "✊ КНБ":
        kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="камень"), KeyboardButton(text="ножницы"), KeyboardButton(text="бумага")], [KeyboardButton(text="◀️ Назад")]], resize_keyboard=True)
        await message.answer("Выбери:", reply_markup=kb)
        return
    
    if text in ["камень", "ножницы", "бумага"]:
        win, msg = await play_rps(user_id, text)
        await message.answer(msg, reply_markup=games_menu_kb())
        return
    
    if text == "⬆️ Выше-Ниже":
        kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="higher"), KeyboardButton(text="lower")], [KeyboardButton(text="◀️ Назад")]], resize_keyboard=True)
        await message.answer("Следующее число будет выше (higher) или ниже (lower)?", reply_markup=kb)
        return
    
    if text in ["higher", "lower"]:
        win, msg = await play_higher(user_id, text)
        await message.answer(msg, reply_markup=games_menu_kb())
        return
    
    if text == "🎰 Слоты":
        win, msg = await play_slots(user_id)
        await message.answer(msg, reply_markup=games_menu_kb())
        return
    
    if text == "🃏 Блэкджек":
        win, msg = await play_blackjack(user_id)
        await message.answer(msg, reply_markup=games_menu_kb())
        return
    
    # ========== КЛАНЫ ==========
    if text == "➕ Создать клан":
        await message.answer("Введи название клана:", reply_markup=back_kb())
        user["awaiting_clan_name"] = True
        return
    
    if user.get("awaiting_clan_name"):
        if text in clans:
            await message.answer("❌ Клан с таким названием уже существует!", reply_markup=clan_menu_kb())
        else:
            create_clan(user_id, text)
            user["clan"] = text
            await message.answer(f"✅ Клан **{text}** создан! Ты стал его лидером.", reply_markup=clan_menu_kb())
        user["awaiting_clan_name"] = False
        return
    
    if text == "📋 Мои кланы":
        if user["clan"] and user["clan"] in clans:
            clan = clans[user["clan"]]
            await message.answer(
                f"👥 **Клан {user['clan']}**\n"
                f"👑 Лидер: {clan['owner']}\n"
                f"📊 Уровень: {clan['level']}\n"
                f"💰 В казне: {clan['balance']}💎\n"
                f"👥 Участников: {len(clan['members'])}"
            )
        else:
            await message.answer("❌ Ты не состоишь в клане!", reply_markup=clan_menu_kb())
        return
    
    # ========== МАГАЗИН ==========
    if text == "🏪 Магазин":
        pet_list = "\n".join([f"{p['name']} — {p['price']}💎 [{p['rarity']}]" for p in list(PETS.values())[:20]])
        await message.answer(f"🏪 **Магазин питомцев** 🏪\n\n{pet_list}\n\n...и ещё {len(PETS)-20} питомцев!\n\nКупить: напиши **/buy [название питомца]**", reply_markup=main_kb())
        return
    
    # ========== ПОКУПКА ==========
    if text.startswith("/buy"):
        args = text.split(maxsplit=1)
        if len(args) < 2:
            await message.answer("❌ Напиши: /buy Курица")
            return
        
        for pet_id, pet in PETS.items():
            if pet["name"].lower() in args[1].lower():
                if user["dubli"] >= pet["price"]:
                    user["dubli"] -= pet["price"]
                    pet_copy = pet.copy()
                    pet_copy["custom_name"] = None
                    pet_copy["pet_id"] = len(user["pets"])
                    user["pets"].append(pet_copy)
                    await message.answer(f"✅ Ты купил {pet['name']}! 💖\nОсталось: {user['dubli']}💎")
                else:
                    await message.answer(f"❌ Не хватает! Нужно {pet['price']}💎")
                return
        await message.answer("❌ Питомец не найден! Доступны: /shop для списка")
        return
    
    # ========== ПИТОМЦЫ ==========
    if text == "🐾 Мои питомцы":
        if not user["pets"]:
            await message.answer("🐾 У тебя пока нет питомцев! Купи в магазине /shop")
        else:
            pets_list = "\n".join([f"{i+1}. {p['name']}" for i, p in enumerate(user["pets"][:30])])
            await message.answer(f"🐾 **Твои питомцы** ({len(user['pets'])}):\n\n{pets_list}" + ("\n...и ещё!" if len(user["pets"]) > 30 else ""))
        return
    
    # ========== ДУБЛИ ==========
    if text == "💰 Дубли":
        await message.answer(f"💰 **Твой баланс:** {user['dubli']} дублей!\n🎮 Игр сыграно: {user['stats']['games']}\n🏆 Побед: {user['stats']['wins']}\n💔 Поражений: {user['stats']['losses']}", reply_markup=main_kb())
        return
    
    # ========== БОНУС ==========
    if text == "🎁 Бонус":
        today = datetime.now().date().isoformat()
        if user.get("last_daily") == today:
            await message.answer("🎁 Ты уже получал бонус сегодня! Завтра приходи!")
        else:
            bonus = random.randint(50, 200)
            user["dubli"] += bonus
            user["last_daily"] = today
            await message.answer(f"🎁 **Ежедневный бонус!** +{bonus} дублей! 💰\nТеперь у тебя {user['dubli']}💎")
        return
    
    # ========== ТОП ==========
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
        await message.answer(top_text)
        return
    
    # ========== АДМИН-КОМАНДЫ ==========
    if text == "💰 Выдать дубли" and user_id in ADMIN_IDS:
        await message.answer("Введи: /add ID КОЛИЧЕСТВО\nПример: /add 6900319945 500", reply_markup=admin_panel_kb())
        return
    
    if text == "🎁 Выдать питомца" and user_id in ADMIN_IDS:
        await message.answer("Введи: /give ID НАЗВАНИЕ\nПример: /give 6900319945 Дракон", reply_markup=admin_panel_kb())
        return
    
    if text == "📢 Объявление" and user_id in ADMIN_IDS:
        await message.answer("Введи текст объявления:", reply_markup=admin_panel_kb())
        user["awaiting_broadcast"] = True
        return
    
    if user.get("awaiting_broadcast"):
        for uid in users:
            try:
                await bot.send_message(uid, f"📢 **ОБЪЯВЛЕНИЕ ОТ АДМИНА** 📢\n\n{text}")
                await asyncio.sleep(0.05)
            except:
                pass
        user["awaiting_broadcast"] = False
        await message.answer(f"✅ Объявление отправлено {len(users)} игрокам!", reply_markup=admin_panel_kb())
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
            reply_markup=admin_panel_kb()
        )
        return

# ========== АДМИН-КОМАНДЫ ==========
@dp.message(Command("add"))
async def add_dubli(message: Message):
    user_id = message.from_user.id
    if user_id not in ADMIN_IDS:
        await message.answer("❌ Нет доступа!")
        return
    
    args = message.text.split()
    if len(args) < 3:
        await message.answer("❌ Использование: /add ID КОЛИЧЕСТВО")
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
                pet_copy = pet.copy()
                pet_copy["custom_name"] = None
                pet_copy["pet_id"] = len(users[target_id]["pets"])
                users[target_id]["pets"].append(pet_copy)
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
    print(f"👑 АДМИНЫ: {ADMIN_IDS}")
    print(f"🎮 ИГР: {len(GAMES)}")
    print(f"🐾 ПИТОМЦЕВ: {len(PETS)}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())            "last_daily": None,
            "daily_quests": {},
            "achievements": [],
            "stats": {"games_played": 0, "chests_opened": 0, "pets_bought": 1, "dubli_earned": 200}
        }
        for quest in DAILY_QUESTS:
            users[user_id]["daily_quests"][quest["id"]] = 0
    return users[user_id]

def check_achievements(user_id):
    user = get_user(user_id)
    new_achievements = []
    
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

def check_daily_quests(user_id):
    user = get_user(user_id)
    completed = []
    
    for quest in DAILY_QUESTS:
        progress = user["daily_quests"].get(quest["id"], 0)
        if progress >= quest["target"]:
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
            [KeyboardButton(text="🏆 Топ игроков"), KeyboardButton(text="📋 Квесты")],
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
            [KeyboardButton(text="🏆 Топ игроков"), KeyboardButton(text="📋 Квесты")],
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
            [KeyboardButton(text="🏆 Топ игроков"), KeyboardButton(text="📋 Квесты")],
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
    user["daily_quests"]["open_chests"] = user["daily_quests"].get("open_chests", 0) + 1
    
    reward = random.randint(chest["price"] // 2, chest["price"] * 2)
    user["dubli"] += reward
    
    pet_reward = ""
    pet_chance = random.randint(1, 100)
    if chest_type == "common" and pet_chance <= 20:
        available = [p for p in PETS if PETS[p]["rarity"] == "common" and p not in user["pets"]]
        if available:
            pet_id = random.choice(available)
            user["pets"].append(pet_id)
            pet_reward = f"\n🐾 + {PETS[pet_id]['name']} (новый питомец!)"
    elif chest_type == "epic" and pet_chance <= 30:
        available = [p for p in PETS if PETS[p]["rarity"] in ["common", "rare"] and p not in user["pets"]]
        if available:
            pet_id = random.choice(available)
            user["pets"].append(pet_id)
            pet_reward = f"\n🐾 + {PETS[pet_id]['name']} (новый питомец!)"
    elif chest_type == "legendary" and pet_chance <= 50:
        available = [p for p in PETS if PETS[p]["rarity"] in ["rare", "epic"] and p not in user["pets"]]
        if available:
            pet_id = random.choice(available)
            user["pets"].append(pet_id)
            pet_reward = f"\n🐾 + {PETS[pet_id]['name']} (новый питомец!)"
    
    check_achievements(user_id)
    check_daily_quests(user_id)
    
    return True, f"🎁 Ты открыл {chest['name']} сундук и получил {reward} дублей!{pet_reward}\n💰 Осталось: {user['dubli']}💎"

# ========== БОТ ==========
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: Message):
    user_id = message.from_user.id
    get_user(user_id)
    
    if user_id == MASTER_ADMIN_ID:
        await message.answer("👑 Добро пожаловать, ГЛАВНЫЙ АДМИН! 👑", reply_markup=master_admin_kb())
    elif user_id == NUTRIKA_ADMIN_ID:
        await message.answer("🔧 Добро пожаловать, АДМИН НАКРУТКИ! 🔧", reply_markup=nutrika_admin_kb())
    else:
        await message.answer("🎮 Бот для Поляшки 🎮\n\nВыполняй квесты, открывай сундуки, собирай питомцев!", reply_markup=main_kb())

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
        await message.answer("👑 АДМИН-ПАНЕЛЬ 👑", reply_markup=admin_panel_kb())
        return
    
    # ========== КВЕСТЫ ==========
    if text == "📋 Квесты":
        check_daily_quests(user_id)
        today = datetime.now().strftime("%d.%m.%Y")
        quests_text = f"📋 ЕЖЕДНЕВНЫЕ КВЕСТЫ ({today}) 📋\n\n"
        
        for quest in DAILY_QUESTS:
            progress = user["daily_quests"].get(quest["id"], 0)
            status = "✅" if progress >= quest["target"] else "⏳"
            quests_text += f"{status} {quest['name']} — {progress}/{quest['target']}\n   {quest['desc']} | Награда: +{quest['reward']}💎\n\n"
        
        await message.answer(quests_text, reply_markup=main_kb())
        return
    
    # ========== ДОСТИЖЕНИЯ ==========
    if text == "🏅 Достижения":
        check_achievements(user_id)
        achievements_text = "🏅 ДОСТИЖЕНИЯ 🏅\n\n"
        
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
        await message.answer("🎁 Выбери сундук:", reply_markup=chests_menu_kb())
        return
    
    if text == "📦 Обычный (100💎)":
        success, msg = await open_chest(user_id, "common")
        await message.answer(msg, reply_markup=chests_menu_kb() if success else main_kb())
        return
    
    if text == "✨ Эпический (500💎)":
        success, msg = await open_chest(user_id, "epic")
        await message.answer(msg, reply_markup=chests_menu_kb() if success else main_kb())
        return
    
    if text == "🔥 Легендарный (2000💎)":
        success, msg = await open_chest(user_id, "legendary")
        await message.answer(msg, reply_markup=chests_menu_kb() if success else main_kb())
        return
    
    # ========== МАГАЗИН ==========
    if text == "🏪 Магазин":
        await message.answer("🏪 Добро пожаловать в магазин!", reply_markup=shop_menu_kb())
        return
    
    if text == "🐾 Купить питомца":
        pets_list = "\n".join([f"{p['emoji']} {p['name']} [{p['rarity']}] — {p['price']}💎" for p in PETS.values()])
        await message.answer(f"🐾 Питомцы в магазине:\n\n{pets_list}\n\nНапиши Купить [название]\nПример: Купить Курица", reply_markup=shop_menu_kb())
        return
    
    if text == "🍗 Купить еду":
        food_list = "\n".join([f"{f['emoji']} {f['name']} — {f['price']}💎" for f in FOOD.values()])
        await message.answer(f"🍗 Еда в магазине:\n\n{food_list}\n\nНапиши Купить [название]\nПример: Купить Зерно", reply_markup=shop_menu_kb())
        return
    
    # ========== ПОКУПКА ==========
    if text.startswith("Купить "):
        item = text.replace("Купить ", "").strip().lower()
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
                    check_achievements(user_id)
                    check_daily_quests(user_id)
                    await message.answer(f"✅ Ты купил {pet['name']}! 💖\nОсталось дублей: {user['dubli']}", reply_markup=shop_menu_kb())
                else:
                    await message.answer(f"❌ Не хватает дублей! Нужно {pet['price']}💎")
                found = True
                break
        
        if not found:
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
            await message.answer("❌ Такой товар не найден!\n\n📝 Правильное написание:\nКупить Курица\nКупить Крокодил\nКупить Хомяк\nКупить Дракон\nКупить Кот\n\n🍗 Или еду:\nКупить Зерно\nКупить Мясо\nКупить Конфета\nКупить Торт")
        return
    
    # ========== ИГРЫ ==========
    if text == "🎮 Игры":
        await message.answer("🎮 Выбери игру:", reply_markup=games_menu_kb())
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
        user["daily_quests"]["earn_dubli"] = user["daily_quests"].get("earn_dubli", 0) + (10 if text == result else 0)
        check_achievements(user_id)
        check_daily_quests(user_id)
        await message.answer(f"{msg}\n💰 Теперь {user['dubli']}💎", reply_markup=games_menu_kb())
        return
    
    if text == "🔢 Угадай число":
        await message.answer("Введи число от 1 до 10:", reply_markup=back_kb())
        return
    
    if text.isdigit() and 1 <= int(text) <= 10:
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
    
    # ========== БОНУС ==========
    if text == "🎁 Бонус":
        today = datetime.now().date().isoformat()
        if user.get("last_daily") == today:
            await message.answer("🎁 Ты уже получал бонус сегодня! Завтра приходи!", reply_markup=main_kb())
        else:
            bonus = random.randint(50, 150)
            user["dubli"] += bonus
            user["last_daily"] = today
            await message.answer(f"🎁 Ежедневный бонус! Ты получил {bonus} дублей! 💰\nТеперь у тебя {user['dubli']} дублей.", reply_markup=main_kb())
        return
    
    # ========== ПИТОМЦЫ ==========
    if text == "🐾 Мои питомцы":
        pets_list = "\n".join([f"{PETS[p]['emoji']} {PETS[p]['name']} [{PETS[p]['rarity']}]" for p in user["pets"]])
        await message.answer(f"🐾 Твои питомцы ({len(user['pets'])}):\n\n{pets_list}", reply_markup=main_kb())
        return
    
    # ========== ДУБЛИ ==========
    if text == "💎 Дубли":
        await message.answer(f"💰 Твой баланс: {user['dubli']} дублей!", reply_markup=main_kb())
        return
    
    # ========== ТОП ИГРОКОВ ==========
    if text == "🏆 Топ игроков":
        players = []
        for uid, data in users.items():
            try:
                chat = await bot.get_chat(uid)
                name = chat.username or chat.first_name or str(uid)
            except:
                name = str(uid)
            players.append((name, data["dubli"], len(data["pets"])))
        players.sort(key=lambda x: x[1], reverse=True)
        
        if not players:
            await message.answer("Пока нет игроков в топе! Будь первым! 🏆", reply_markup=main_kb())
            return
        
        top_text = "🏆 ТОП ИГРОКОВ 🏆\n\n"
        for i, (name, dubli, pets_count) in enumerate(players[:15], 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            if len(name) > 20:
                name = name[:17] + "..."
            top_text += f"{medal} {name} — {dubli}💎 ({pets_count} петов)\n"
        
        await message.answer(top_text, reply_markup=main_kb())
        return
    
    # ========== АДМИН-КОМАНДЫ ==========
    if text == "💰 Накрутить Поляшке" and user_id in [MASTER_ADMIN_ID, NUTRIKA_ADMIN_ID]:
        user["awaiting_polina"] = True
        await message.answer("💰 Введи количество дублей для Поляшки:", reply_markup=back_kb())
        return
    
    if user.get("awaiting_polina") and text.isdigit():
        amount = int(text)
        if POLINA_ID not in users:
            users[POLINA_ID] = get_user(POLINA_ID)
        users[POLINA_ID]["dubli"] += amount
        user["awaiting_polina"] = False
        await message.answer(f"✅ Поляшке накручено {amount} дублей!")
        await bot.send_message(POLINA_ID, f"👑 Тебе начислено {amount} дублей! 💰")
        return
    
    if text == "🎁 Выдать питомца" and user_id == MASTER_ADMIN_ID:
        pets_list = "\n".join([f"{p['emoji']} {p['name']}" for p in PETS.values()])
        user["awaiting_pet"] = True
        await message.answer(f"🎁 Введи ID пользователя и название питомца:\nПример: 6900319945 Курица\n\nДоступные питомцы:\n{pets_list}", reply_markup=back_kb())
        return
    
    if user.get("awaiting_pet") and user_id == MASTER_ADMIN_ID:
        parts = text.split()
        if len(parts) == 2:
            target_id = int(parts[0])
            pet_name = parts[1].lower()
            for pet_id, pet in PETS.items():
                if pet["name"].lower() == pet_name or pet["name"].lower().replace("🐔", "").replace("🐊", "").replace("🐹", "").replace("🐉", "").replace("🐱", "").strip() == pet_name:
                    if target_id not in users:
                        users[target_id] = get_user(target_id)
                    if pet_id not in users[target_id]["pets"]:
                        users[target_id]["pets"].append(pet_id)
                        user["awaiting_pet"] = False
                        await message.answer(f"✅ Выдан питомец {pet['name']} пользователю {target_id}")
                        await bot.send_message(target_id, f"👑 Админ выдал тебе питомца {pet['name']}! 🎉")
                    else:
                        await message.answer("❌ У пользователя уже есть этот питомец!")
                    return
        await message.answer("❌ Неверный формат! Пример: 6900319945 Курица")
        return
    
    if text == "📢 Объявление" and user_id == MASTER_ADMIN_ID:
        user["awaiting_broadcast"] = True
        await message.answer("📢 Введи текст объявления для всех игроков:", reply_markup=back_kb())
        return
    
    if user.get("awaiting_broadcast"):
        count = 0
        for uid in users:
            if uid not in [MASTER_ADMIN_ID, NUTRIKA_ADMIN_ID]:
                try:
                    await bot.send_message(uid, f"📢 ОБЪЯВЛЕНИЕ ОТ АДМИНА 📢\n\n{text}")
                    count += 1
                    await asyncio.sleep(0.05)
                except:
                    pass
        user["awaiting_broadcast"] = False
        await message.answer(f"✅ Объявление отправлено {count} игрокам!")
        return
    
    if text == "📊 Статистика" and user_id == MASTER_ADMIN_ID:
        total_players = len(users)
        total_dubli = sum(u["dubli"] for u in users.values())
        total_pets = sum(len(u["pets"]) for u in users.values())
        total_games = sum(u["stats"]["games_played"] for u in users.values())
        total_chests = sum(u["stats"]["chests_opened"] for u in users.values())
        await message.answer(
            f"📊 СТАТИСТИКА БОТА 📊\n\n"
            f"👥 Игроков: {total_players}\n"
            f"💰 Дублей в обороте: {total_dubli}\n"
            f"🐾 Всего питомцев: {total_pets}\n"
            f"🎮 Сыграно игр: {total_games}\n"
            f"🎁 Открыто сундуков: {total_chests}",
            reply_markup=admin_panel_kb()
        )
        return

# ========== ЗАПУСК ==========
async def main():
    print("✅ МЕГА-БОТ ДЛЯ ПОЛЯШКИ ЗАПУЩЕН!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
