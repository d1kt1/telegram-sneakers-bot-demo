import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)

# Загружаем переменные из .env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Главное меню внизу экрана
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👟 Каталог кроссовок")],
        [KeyboardButton(text="📦 Оформить заказ"), KeyboardButton(text="ℹ️ О магазине")],
    ],
    resize_keyboard=True,
)

# Инлайн-кнопки под карточкой товара
inline_buy_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔥 Купить за 9 990 ₽", callback_data="buy_sneakers")],
        [InlineKeyboardButton(text="↩️ Назад в меню", callback_data="back_to_menu")],
    ]
)


@dp.message(F.text == "/start")
async def start_command(message: Message):
    await message.answer(
        f"Добро пожаловать в Sneaker Store, {message.from_user.first_name}!\n"
        "Здесь ты можешь выбрать и купить лучшие кроссовки.",
        reply_markup=main_menu,
    )


@dp.message(F.text == "👟 Каталог кроссовок")
async def show_catalog(message: Message):
    await message.answer_photo(
        photo="https://images.unsplash.com/photo-1542291026-7eec264c27ff",
        caption=(
            "**Nike Air Max 90**\n\n"
            "Самая культовая модель в шикарном красном цвете.\n\n"
            "💰 **Цена:** 9 990 ₽\n"
            "📏 **Размеры в наличии:** 41, 42, 43, 44"
        ),
        reply_markup=inline_buy_menu,
        parse_mode="Markdown",
    )


@dp.callback_query(F.data == "buy_sneakers")
async def process_buy(callback: CallbackQuery):
    await callback.answer("Товар добавлен в корзину!")
    await callback.message.answer(
        "🎉 Отличный выбор! Для оформления заказа нажми кнопку "
        "'📦 Оформить заказ' в нижнем меню."
    )


@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("Главное меню:", reply_markup=main_menu)


@dp.message(F.text == "ℹ️ О магазине")
async def about_shop(message: Message):
    await message.answer(
        "Мы продаём только оригинальные кроссовки с быстрой доставкой! Работаем 24/7."
    )


# Кнопка для отправки телефона
request_phone_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📱 Поделиться номером телефона", request_contact=True)],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)


@dp.message(F.text == "📦 Оформить заказ")
async def start_order(message: Message):
    await message.answer(
        "Для оформления заказа нам понадобится твой номер телефона. "
        "Нажми на кнопку ниже, чтобы отправить его автоматически:",
        reply_markup=request_phone_menu,
    )


@dp.message(F.contact)
async def get_contact(message: Message):
    phone = message.contact.phone_number
    name = message.contact.first_name

    # Подтверждение клиенту
    await message.answer(
        f"Спасибо, {name}! Твой номер {phone} получен.\n"
        "Наш менеджер свяжется с тобой в течение 10 минут! 👟",
        reply_markup=main_menu,
    )

    # Уведомление админу (ID берётся из .env)
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            "🔔 **НОВЫЙ ЗАКАЗ!**\n\n"
            f"👤 Клиент: {name}\n"
            f"📱 Телефон: {phone}\n"
            "👟 Товар: Nike Air Max 90"
        ),
        parse_mode="Markdown",
    )


async def main():
    print("Бот-магазин кроссовок запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())