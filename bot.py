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

# ========== 112 ПИТОМЦЕВ ==========
PET_NAMES = [
    "Курица", "Петух", "Цыплёнок", "Крокодил", "Хомяк", "Крыса", "Морская свинка", "Попугай", "Канарейка", "Черепаха",
    "Кот", "Кошка", "Котёнок", "Лев", "Тигр", "Леопард", "Гепард", "Пума", "Рысь", "Ягуар",
    "Пёс", "Щенок", "Волк", "Лиса", "Шакал", "Койот", "Хаски", "Овчарка", "Такса", "Бульдог",
    "Медведь", "Белый медведь", "Панда", "Барибал", "Гризли", "Лошадь", "Осёл", "Зебра", "Жираф", "Слон",
    "Носорог", "Бегемот", "Олень", "Лось", "Кабан", "Обезьяна", "Шимпанзе", "Горилла", "Орангутанг", "Лемур",
    "Кенгуру", "Коала", "Вомбат", "Опоссум", "Квокка", "Орёл", "Сокол", "Ястреб", "Сова", "Филин",
    "Пингвин", "Фламинго", "Лебедь", "Павлин", "Страус", "Дельфин", "Кит", "Касатка", "Акула", "Скат",
    "Осьминог", "Кальмар", "Медуза", "Краб", "Лобстер", "Змея", "Гадюка", "Кобра", "Питон", "Удав",
    "Ящерица", "Варан", "Игуана", "Хамелеон", "Геккон", "Паук", "Скорпион", "Пчела", "Бабочка", "Божья коровка",
    "Кузнечик", "Стрекоза", "Муравей", "Жук", "Богомол", "Лягушка", "Жаба", "Тритон", "Саламандра", "Квакша",
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

print(f"✅ Загружено {len(PETS)} питомцев")

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

# ... (остальные игры такие же, не менялись)

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

# ========== МАГАЗИН С ПАГИНАЦИЕЙ ==========
shop_pages = {}

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
        nav_buttons.append(InlineKeyboardButton(text="◀️ Назад", callback_data=f"shop_page_{page-1}"))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton(text="Вперёд ▶️", callback_data=f"shop_page_{page+1}"))
    if nav_buttons:
        kb.inline_keyboard.append(nav_buttons)
    
    kb.inline_keyboard.append([InlineKeyboardButton(text="❌ Закрыть", callback_data="close_shop")])
    return kb, total_pages, page

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
            f"🐾 Питомцев: {len(users[user_id]['pets'])}\n"
            f"📊 Всего питомцев в игре: {len(PETS)}",
            reply_markup=main_kb()
        )
    else:
        await message.answer(
            "🎮 **Добро пожаловать в бот!** 🎮\n\n"
            f"💰 У тебя {users[user_id]['dubli']} дублей\n"
            f"📊 Всего питомцев в игре: {len(PETS)}",
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
    
    # ========== АДМИНКА ==========
    if text == "👑 Админка" and user_id in ADMIN_IDS:
        await message.answer("👑 **АДМИН-ПАНЕЛЬ** 👑", reply_markup=admin_kb())
        return
    
    # ========== НАКРУТКА (РАБОТАЕТ!) ==========
    if text == "💰 Выдать дубли" and user_id in ADMIN_IDS:
        await message.answer("💰 Введи ID пользователя и количество дублей.\n\nПример: `6900319945 500`", parse_mode="Markdown")
        user["awaiting_admin_add"] = True
        return
    
    if user.get("awaiting_admin_add"):
        try:
            parts = text.split()
            target_id = int(parts[0])
            amount = int(parts[1])
            if target_id not in users:
                users[target_id] = get_user(target_id)
            users[target_id]["dubli"] += amount
            await message.answer(f"✅ Выдано {amount} дублей пользователю {target_id}")
            try:
                await bot.send_message(target_id, f"👑 Админ выдал тебе {amount} дублей! 💰")
            except:
                pass
        except:
            await message.answer("❌ Ошибка! Пример: `6900319945 500`", parse_mode="Markdown")
        user["awaiting_admin_add"] = False
        return
    
    if text == "🎁 Выдать питомца" and user_id in ADMIN_IDS:
        await message.answer("🎁 Введи ID пользователя и название питомца.\n\nПример: `6900319945 Дракон`", parse_mode="Markdown")
        user["awaiting_admin_give"] = True
        return
    
    if user.get("awaiting_admin_give"):
        try:
            parts = text.split(maxsplit=1)
            target_id = int(parts[0])
            pet_name = parts[1].lower()
            found = False
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
                    found = True
                    break
            if not found:
                await message.answer("❌ Питомец не найден!")
        except:
            await message.answer("❌ Ошибка! Пример: `6900319945 Дракон`", parse_mode="Markdown")
        user["awaiting_admin_give"] = False
        return
    
    if text == "📢 Объявление" and user_id in ADMIN_IDS:
        await message.answer("📢 Введи текст объявления для всех игроков:")
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
            f"🎮 Сыграно игр: {total_games}\n"
            f"📋 Всего питомцев в игре: {len(PETS)}",
            reply_markup=admin_kb()
        )
        return
    
    # ========== МАГАЗИН ==========
    if text == "🏪 Магазин":
        kb, total_pages, current_page = get_shop_keyboard(0)
        shop_pages[user_id] = current_page
        await message.answer(f"🏪 **Магазин питомцев** 🏪\n\nСтраница {current_page + 1} из {total_pages}\nВсего питомцев: {len(PETS)}", reply_markup=kb)
        return
    
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
            # Показываем первых 30 питомцев
            display_pets = pets_list[:30]
            text = f"🐾 **Твои питомцы** ({len(user['pets'])}):\n\n" + "\n".join(display_pets)
            if len(pets_list) > 30:
                text += f"\n\n... и ещё {len(pets_list) - 30} питомцев!"
            await message.answer(text, reply_markup=main_kb())
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
        await message.answer(
            f"💰 **Твой баланс:** {user['dubli']} дублей!\n\n"
            f"📊 **Статистика:**\n"
            f"🎮 Игр сыграно: {user['stats']['games']}\n"
            f"🏆 Побед: {user['stats']['wins']}\n"
            f"💔 Поражений: {user['stats']['losses']}",
            reply_markup=main_kb()
        )
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
            players.append((name, data["dubli"], len(data["pets"])))
        
        players.sort(key=lambda x: x[1], reverse=True)
        top_text = "🏆 **ТОП ИГРОКОВ** 🏆\n\n"
        for i, (name, dubli, pets) in enumerate(players[:15], 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            top_text += f"{medal} {name[:20]} — {dubli}💎 ({pets} петов)\n"
        await message.answer(top_text, reply_markup=main_kb())
        return
    
    # ========== ИГРЫ (кратко) ==========
    if text == "🎮 Игры":
        await message.answer("🎮 **Выбери игру:**\n\nСтавки от 5 до 50💎", reply_markup=games_kb())
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
                f"🐾 **Выбери питомца по номеру и напиши имя:**\n\n" + "\n".join(pets_list[:20]) + "\n\nПример: `1 Буся`",
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

@dp.callback_query()
async def handle_callback(call: CallbackQuery):
    user_id = call.from_user.id
    user = get_user(user_id)
    data = call.data
    
    if data == "close_shop":
        await call.message.delete()
        await call.answer()
        return
    
    if data.startswith("shop_page_"):
        page = int(data.split("_")[2])
        kb, total_pages, current_page = get_shop_keyboard(page)
        await call.message.edit_text(f"🏪 **Магазин питомцев** 🏪\n\nСтраница {current_page + 1} из {total_pages}\nВсего питомцев: {len(PETS)}", reply_markup=kb)
        await call.answer()
        return
    
    if data.startswith("buy_"):
        pet_id = data.replace("buy_", "")
        pet = PETS.get(pet_id)
        
        if pet is None:
            await call.answer("❌ Питомец не найден!")
            return
        
        if user["dubli"] >= pet["price"]:
            user["dubli"] -= pet["price"]
            user["pets"].append(pet_id)
            await call.message.edit_text(f"✅ Ты купил {pet['name']}! 💖\nОсталось: {user['dubli']}💎")
            await call.answer(f"Куплен {pet['name']}!")
        else:
            await call.answer(f"❌ Не хватает! Нужно {pet['price']}💎", show_alert=True)

# ========== ЗАПУСК ==========
async def main():
    print("✅ МЕГА-БОТ ЗАПУЩЕН!")
    print(f"🐾 ПИТОМЦЕВ: {len(PETS)}")
    print(f"👑 АДМИНЫ: {ADMIN_IDS}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
