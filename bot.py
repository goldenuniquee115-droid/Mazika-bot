import telebot
import json
import os
from threading import Thread
from flask import Flask
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8933277511:AAFEIb_lezIC7wS2aYjBl2cQyGQG70WtcS4"
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

ADMIN_USERNAME = "@Mazika8Bp"
ADMIN_IDS = [809475297]
VOUCHERS_FILE = "vouchers.json"
USERS_FILE = "users_balance.json"

IMAGES = {
    "main": "https://placehold.co/600x400/0d1b2a/00b4d8.png?text=Mazika8Bp+Panel",
    "deposit": "https://placehold.co/600x400/0d1b2a/00b4d8.png?text=Mazika8Bp+Deposit",
    "resellers": "https://placehold.co/600x400/0d1b2a/00b4d8.png?text=Mazika8Bp+Admin",
    "8bp_main": "https://placehold.co/600x400/0d1b2a/fca311.png?text=Mazika8Bp+8Ball+Pool",
    "8bp_hacks": "https://placehold.co/600x400/0d1b2a/e63946.png?text=Mazika8Bp+8BP+Hackers",
    "8bp_accounts": "https://placehold.co/600x400/0d1b2a/00b4d8.png?text=Clone+8Ball+Pool",
    "aim_king": "https://placehold.co/600x400/1d3557/fca311.png?text=AIM+KING+-+Mazika8Bp",
    "snake": "https://placehold.co/600x400/081c15/52b788.png?text=SNAKE+ENGINE+-+Mazika8Bp",
    "ninja": "https://placehold.co/600x400/240046/9d4edd.png?text=NINJA+ENGINE+-+Mazika8Bp",
    "fluorite": "https://placehold.co/600x400/03045e/00f5d4.png?text=FLUORITE+8BP+iOS",
    "ios_main": "https://placehold.co/600x400/0d1b2a/a8dadc.png?text=Mazika8Bp+iOS+Panel",
    "esign": "https://placehold.co/600x400/001219/00b4d8.png?text=Mazika8Bp+E-Sign"
}

user_states = {}

def load_data(filename):
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_data(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_balance(user_id):
    balances = load_data(USERS_FILE)
    return float(balances.get(str(user_id), 0.0))

def update_balance(user_id, amount):
    balances = load_data(USERS_FILE)
    current = float(balances.get(str(user_id), 0.0))
    balances[str(user_id)] = current + amount
    save_data(USERS_FILE, balances)

PRODUCTS = {
    "ak_3d_aq": {"name": "Aim King AQ ⚡\n3Day", "price": 8.0, "back": "menu_aim_king", "img": "aim_king"},
    "ak_3d_norm": {"name": "Aim King Normal 👑\n3Day", "price": 6.0, "back": "menu_aim_king", "img": "aim_king"},
    "ak_7d_aq": {"name": "Aim King AQ ⚡\n7Day", "price": 12.0, "back": "menu_aim_king", "img": "aim_king"},
    "ak_7d_norm": {"name": "Aim King Normal 👑\n7Day", "price": 10.0, "back": "menu_aim_king", "img": "aim_king"},
    "ak_30d_aq": {"name": "Aim King AQ ⚡\n30Day", "price": 27.0, "back": "menu_aim_king", "img": "aim_king"},
    "ak_30d_norm": {"name": "Aim King Normal 👑\n30Day", "price": 24.0, "back": "menu_aim_king", "img": "aim_king"},
    "ak_90d_aq": {"name": "Aim King AQ ⚡\n90Day", "price": 63.0, "back": "menu_aim_king", "img": "aim_king"},
    "ak_90d_norm": {"name": "Aim King Normal 👑\n90Day", "price": 51.0, "back": "menu_aim_king", "img": "aim_king"},
    "sn_3d": {"name": "Snake Engine 🐍\n3Day", "price": 5.0, "back": "menu_snake", "img": "snake"},
    "sn_10d": {"name": "Snake Engine 🐍\n10Day", "price": 9.0, "back": "menu_snake", "img": "snake"},
    "sn_30d": {"name": "Snake Engine 🐍\n30Day", "price": 18.0, "back": "menu_snake", "img": "snake"},
    "sn_90d": {"name": "Snake Engine 🐍\n90Day", "price": 42.0, "back": "menu_snake", "img": "snake"},
    "nj_3d": {"name": "Ninja Engine 🥷\n3Day", "price": 8.0, "back": "menu_ninja", "img": "ninja"},
    "nj_7d": {"name": "Ninja Engine 🥷\n7Day", "price": 16.0, "back": "menu_ninja", "img": "ninja"},
    "nj_30d": {"name": "Ninja Engine 🥷\n30Day", "price": 30.0, "back": "menu_ninja", "img": "ninja"},
    "fl_30d": {"name": "Fluorite 8BP iOS 💎\n30Day", "price": 30.0, "back": "menu_fluorite", "img": "fluorite"},
    "acc_500m": {"name": "Clone 8Ball Pool 🎱\n500M Coins", "price": 4.0, "back": "menu_8bp_accounts", "img": "8bp_accounts"},
    "acc_1b": {"name": "Clone 8Ball Pool 🎱\n1B Coins", "price": 6.0, "back": "menu_8bp_accounts", "img": "8bp_accounts"},
    "acc_2b": {"name": "Clone 8Ball Pool 🎱\n2B Coins", "price": 9.0, "back": "menu_8bp_accounts", "img": "8bp_accounts"},
    "acc_3b": {"name": "Clone 8Ball Pool 🎱\n3B Coins", "price": 14.0, "back": "menu_8bp_accounts", "img": "8bp_accounts"},
    "ios_1y": {"name": "iOS Cert 🌟\n1 Year (الشهادة مدتها سنة ومعاها ضمان شهر فقط)", "price": 15.0, "back": "menu_esign", "img": "esign"}
}

def edit_or_send(chat_id, message_id, photo_key, caption, markup):
    photo_url = IMAGES.get(photo_key, IMAGES["main"])
    try:
        media = telebot.types.InputMediaPhoto(media=photo_url, caption=caption, parse_mode="HTML")
        bot.edit_message_media(media=media, chat_id=chat_id, message_id=message_id, reply_markup=markup)
    except Exception:
        try:
            bot.delete_message(chat_id, message_id)
        except Exception:
            pass
        bot.send_photo(chat_id, photo=photo_url, caption=caption, reply_markup=markup)

def main_menu_data(user):
    balance = get_balance(user.id)
    first_name = user.first_name if user.first_name else "عزيزي"
    caption = (
        f"🔥 <b>مرحباً {first_name} في Mazika8Bp</b> 🔥\n"
        f"<blockquote>من فضلك أختر التطبيق المطلوب ❗️</blockquote>\n"
        f"💰 <b>رصيدك : ${balance:.1f}</b>"
    )
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("موزعين معتمدين 📌", callback_data="menu_resellers"),
        InlineKeyboardButton("إيداع 💵", callback_data="menu_deposit")
    )
    markup.add(InlineKeyboardButton("8Ball Pool 🎱", callback_data="menu_8bp"))
    markup.add(InlineKeyboardButton("شهادات ايفون ", callback_data="menu_ios"))
    if user.id in ADMIN_IDS:
        markup.add(InlineKeyboardButton("لوحة الأدمن ⚙️", callback_data="admin_panel"))
    markup.add(InlineKeyboardButton("الدعم الفني 💬", url=f"https://t.me/{ADMIN_USERNAME.replace('@', '')}"))
    return "main", caption, markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_states.pop(message.from_user.id, None)
    photo_key, caption, markup = main_menu_data(message.from_user)
    bot.send_photo(message.chat.id, photo=IMAGES[photo_key], caption=caption, reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def handle_text_messages(message):
    user_id = message.from_user.id
    state = user_states.get(user_id)

    if state == "waiting_for_voucher":
        user_states.pop(user_id, None)
        code = message.text.strip()
        vouchers = load_data(VOUCHERS_FILE)

        if code in vouchers:
            amount = float(vouchers.pop(code))
            save_data(VOUCHERS_FILE, vouchers)
            update_balance(user_id, amount)
            new_bal = get_balance(user_id)
            bot.reply_to(message, f"🎉 <b>تم إيداع مبلغ ${amount:.1f} بنجاح في رصيدك!</b>\n💰 رصيدك الحالي: ${new_bal:.1f}")
        else:
            bot.reply_to(message, "❌ <b>عذراً، هذا الكود غير صحيح أو تم استخدامه من قبل!</b>")
        return

    if user_id in ADMIN_IDS and state == "admin_create_voucher":
        user_states.pop(user_id, None)
        args = message.text.split()
        if len(args) != 2:
            bot.reply_to(message, "❌ الصيغة خطأ. أرسل هكذا:\n<code>[اسم_الكود] [المبلغ]</code>\nمثال: <code>mazika20 20</code>")
            return
        code, amount_str = args[0].strip(), args[1].strip()
        try:
            amount = float(amount_str)
            vouchers = load_data(VOUCHERS_FILE)
            vouchers[code] = amount
            save_data(VOUCHERS_FILE, vouchers)
            bot.reply_to(message, f"✅ <b>تم إنشاء كود الشحن بنجاح!</b>\n🎟 الكود: <code>{code}</code>\n💵 القيمة: ${amount:.1f}")
        except ValueError:
            bot.reply_to(message, "❌ تأكد من أن القيمة رقم صحيح.")
        return

@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    data = call.data
    balance = get_balance(user_id)
    user_states.pop(user_id, None)

    if data == "main_menu":
        photo_key, caption, markup = main_menu_data(call.from_user)
        edit_or_send(chat_id, msg_id, photo_key, caption, markup)

    elif data == "admin_panel":
        if user_id not in ADMIN_IDS: return
        caption = "⚙️ <b>لوحة التحكم الخاصة بالأدمن</b>\n\nاختر الإجراء المطلوب:"
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("إنشاء كود شحن جديد 🎟", callback_data="admin_new_voucher"),
            InlineKeyboardButton("رجوع 🔙", callback_data="main_menu")
        )
        edit_or_send(chat_id, msg_id, "resellers", caption, markup)

    elif data == "admin_new_voucher":
        if user_id not in ADMIN_IDS: return
        user_states[user_id] = "admin_create_voucher"
        caption = (
            "🎟 <b>إنشاء كود شحن جديد</b>\n\n"
            "أرسل الآن في الشات الكود والقيمة بهذا الشكل:\n"
            "<code>[اسم_الكود] [المبلغ]</code>\n\n"
            "<i>مثال:</i> <code>mazika20 20</code>"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("إلغاء 🔙", callback_data="admin_panel"))
        edit_or_send(chat_id, msg_id, "resellers", caption, markup)

    elif data == "menu_deposit":
        caption = (
            "💳 <b>اختر طريقة الإيداع المناسبة لك</b>\n\n"
            "يمكنك الشحن عبر طرق الدفع المتاحة أو تفعيل كود شحن فوري 🔻"
        )
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("Vodafone Cash 📱", callback_data="pay_vf"),
            InlineKeyboardButton("InstaPay ⚡", callback_data="pay_insta")
        )
        markup.add(
            InlineKeyboardButton("Binance 🔶", callback_data="pay_binance"),
            InlineKeyboardButton("شحن كود 🎟", callback_data="menu_redeem_code")
        )
        markup.add(InlineKeyboardButton("رجوع 🔙", callback_data="main_menu"))
        edit_or_send(chat_id, msg_id, "deposit", caption, markup)

    elif data == "menu_redeem_code":
        user_states[user_id] = "waiting_for_voucher"
        caption = (
            "🎟 <b>شحن كود رصيد</b>\n\n"
            "من فضلك، أرسل كود الشحن الآن في الشات لتتم إضافة الرصيد لحسابك فوراً:"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("رجوع 🔙", callback_data="menu_deposit"))
        edit_or_send(chat_id, msg_id, "deposit", caption, markup)

    elif data == "pay_vf":
        caption = (
            "💳 <b>تفاصيل الدفع - Vodafone Cash 📱</b>\n\n"
            "• <b>الرقم:</b> <code>01007639218</code>\n"
            "• <b>الاسم:</b> أحمد\n\n"
            f"<blockquote>بعد التحويل، أرسل صورة الإيصال للأدمن: {ADMIN_USERNAME}</blockquote>"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("مراسلة الأدمن لتأكيد الدفع 💬", url=f"https://t.me/{ADMIN_USERNAME.replace('@', '')}"))
        markup.add(InlineKeyboardButton("رجوع 🔙", callback_data="menu_deposit"))
        edit_or_send(chat_id, msg_id, "deposit", caption, markup)

    elif data == "pay_insta":
        caption = (
            "💳 <b>تفاصيل الدفع - InstaPay ⚡</b>\n\n"
            "• <b>رابط الدفع المباشر:</b>\n"
            "https://ipn.eg/S/ahmedahme/instapay/3SzOyV\n\n"
            f"<blockquote>بعد التحويل، أرسل صورة الإيصال للأدمن: {ADMIN_USERNAME}</blockquote>"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("اضغط هنا للدفع عبر InstaPay ⚡", url="https://ipn.eg/S/ahmedahme/instapay/3SzOyV"))
        markup.add(InlineKeyboardButton("مراسلة الأدمن لتأكيد الدفع 💬", url=f"https://t.me/{ADMIN_USERNAME.replace('@', '')}"))
        markup.add(InlineKeyboardButton("رجوع 🔙", callback_data="menu_deposit"))
        edit_or_send(chat_id, msg_id, "deposit", caption, markup)

    elif data == "pay_binance":
        caption = (
            "💳 <b>تفاصيل الدفع - Binance 🔶</b>\n\n"
            "• <b>اسم الحساب:</b> <code>Mazika 8Bp</code>\n"
            "• <b>ID:</b> <code>809475297</code>\n\n"
            f"<blockquote>بعد التحويل، أرسل صورة الإيصال للأدمن: {ADMIN_USERNAME}</blockquote>"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("مراسلة الأدمن لتأكيد الدفع 💬", url=f"https://t.me/{ADMIN_USERNAME.replace('@', '')}"))
        markup.add(InlineKeyboardButton("رجوع 🔙", callback_data="menu_deposit"))
        edit_or_send(chat_id, msg_id, "deposit", caption, markup)

    elif data == "menu_resellers":
        caption = f"• <b>Admin</b> 📌\n• {ADMIN_USERNAME} ⭐️"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("رجوع 🔙", callback_data="main_menu"))
        edit_or_send(chat_id, msg_id, "resellers", caption, markup)

    elif data == "menu_8bp":
        caption = (
            "<b>مرحباً بك في لوحة البلياردو 🎱</b>\n"
            "<blockquote>حدد ما تريد 🔻</blockquote>"
        )
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("حسابات 🎱", callback_data="menu_8bp_accounts"),
            InlineKeyboardButton("هكرات 🎗", callback_data="menu_8bp_hacks")
        )
        markup.add(InlineKeyboardButton("رجوع 🔙", callback_data="main_menu"))
        edit_or_send(chat_id, msg_id, "8bp_main", caption, markup)

    elif data == "menu_8bp_hacks":
        caption = (
            "<b>الهكرات 🎮</b>\n"
            "<blockquote>اختر المنتج المطلوب 🔻</blockquote>\n"
            f"💰 <b>رصيدك : ${balance:.1f}</b>"
        )
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(InlineKeyboardButton("Aim King 👑", callback_data="menu_aim_king"))
        markup.add(
            InlineKeyboardButton("Snake Engine 🐍", callback_data="menu_snake"),
            InlineKeyboardButton("Ninja Engine 🥷", callback_data="menu_ninja")
        )
        markup.add(InlineKeyboardButton("Fluorite 8BP iOS 💎", callback_data="menu_fluorite"))
        markup.add(InlineKeyboardButton("رجوع 🔙", callback_data="menu_8bp"))
        edit_or_send(chat_id, msg_id, "8bp_hacks", caption, markup)

    elif data == "menu_aim_king":
        caption = (
            "<b>من فضلك أختر الباقة والمدة 🎰</b>\n"
            f"💰 <b>رصيدك : ${balance:.1f}</b>"
        )
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("3Day AQ - 8.0$ 💰", callback_data="buy_ak_3d_aq"),
            InlineKeyboardButton("3Day Normal - 6.0$ 💰", callback_data="buy_ak_3d_norm")
        )
        markup.add(
            InlineKeyboardButton("7Day AQ - 12.0$ 💰", callback_data="buy_ak_7d_aq"),
            InlineKeyboardButton("7Day Normal - 10.0$ 💰", callback_data="buy_ak_7d_norm")
        )
        markup.add(
            InlineKeyboardButton("30Day AQ - 27.0$ 💰", callback_data="buy_ak_30d_aq"),
            InlineKeyboardButton("30Day Normal - 24.0$ 💰", callback_data="buy_ak_30d_norm")
        )
        markup.add(
            InlineKeyboardButton("90Day AQ - 63.0$ 💰", callback_data="buy_ak_90d_aq"),
            InlineKeyboardButton("90Day Normal - 51.0$ 💰", callback_data="buy_ak_90d_norm")
        )
        markup.add(InlineKeyboardButton("رجوع 🔙", callback_data="menu_8bp_hacks"))
        edit_or_send(chat_id, msg_id, "aim_king", caption, markup)

    elif data == "menu_snake":
        caption = (
            "<b>من فضلك أختر المدة 🎰</b>\n"
            f"💰 <b>رصيدك : ${balance:.1f}</b>"
        )
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("🐍 3Day - 5.0$", callback_data="buy_sn_3d"),
            InlineKeyboardButton("🐍 10Day - 9.0$", callback_data="buy_sn_10d"),
            InlineKeyboardButton("🐍 30Day - 18.0$", callback_data="buy_sn_30d"),
            InlineKeyboardButton("🐍 90Day - 42.0$", callback_data="buy_sn_90d"),
            InlineKeyboardButton("رجوع 🔙", callback_data="menu_8bp_hacks")
        )
        edit_or_send(chat_id, msg_id, "snake", caption, markup)

    elif data == "menu_ninja":
        caption = (
            "<b>من فضلك أختر المدة 🎰</b>\n"
            f"💰 <b>رصيدك : ${balance:.1f}</b>"
        )
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("3Day - 8.0$ 💰", callback_data="buy_nj_3d"),
            InlineKeyboardButton("7Day - 16.0$ 💰", callback_data="buy_nj_7d"),
            InlineKeyboardButton("30Day - 30.0$ 💰", callback_data="buy_nj_30d"),
            InlineKeyboardButton("رجوع 🔙", callback_data="menu_8bp_hacks")
        )
        edit_or_send(chat_id, msg_id, "ninja", caption, markup)

    elif data == "menu_fluorite":
        caption = (
            "<b>من فضلك أختر المدة 🎰</b>\n"
            f"💰 <b>رصيدك : ${balance:.1f}</b>"
        )
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("30Day - 30.0$ 💰", callback_data="buy_fl_30d"),
            InlineKeyboardButton("رجوع 🔙", callback_data="menu_8bp_hacks")
        )
        edit_or_send(chat_id, msg_id, "fluorite", caption, markup)

    elif data == "menu_8bp_accounts":
        caption = (
            "<b>من فضلك أختر الكمية 🎰</b>\n"
            f"💰 <b>رصيدك : ${balance:.1f}</b>"
        )
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("500M - 4.0$ 💰", callback_data="buy_acc_500m"),
            InlineKeyboardButton("1B - 6.0$ 💰", callback_data="buy_acc_1b"),
            InlineKeyboardButton("2B - 9.0$ 💰", callback_data="buy_acc_2b"),
            InlineKeyboardButton("3B - 14.0$ 💰", callback_data="buy_acc_3b"),
            InlineKeyboardButton("رجوع 🎱", callback_data="menu_8bp")
        )
        edit_or_send(chat_id, msg_id, "8bp_accounts", caption, markup)

    elif data == "menu_ios":
        caption = (
            "<b>قسم شهادات الايفون 🎮</b>\n"
            "<blockquote>اختر المنتج المطلوب 🔻</blockquote>\n"
            f"💰 <b>رصيدك : ${balance:.1f}</b>"
        )
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("شهادات ايفون 🌟", callback_data="menu_esign"),
            InlineKeyboardButton("رجوع 🔙", callback_data="main_menu")
        )
        edit_or_send(chat_id, msg_id, "ios_main", caption, markup)

    elif data == "menu_esign":
        caption = (
            "<b>من فضلك أختر مدة الضمان 🎰</b>\n"
            "<blockquote>الشهادة مدتها سنة ومعاها ضمان شهر فقط</blockquote>\n"
            f"💰 <b>رصيدك : ${balance:.1f}</b>"
        )
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("1 Year - 15.0$ 💰", callback_data="buy_ios_1y"),
            InlineKeyboardButton("رجوع ", callback_data="menu_ios")
        )
        edit_or_send(chat_id, msg_id, "esign", caption, markup)

    elif data.startswith("buy_"):
        prod_key = data.replace("buy_", "", 1)
        product = PRODUCTS.get(prod_key)
        if not product: return
        caption = (
            f"<blockquote><b>{product['name']}</b>\n\n"
            f"<b>الكمية: 1</b>\n"
            f"<b>السعر: ${product['price']:.1f}</b>\n"
            f"<b>رصيدك: ${balance:.1f}</b>\n\n"
            f"<b>هل أنت متأكد من الشراء؟</b></blockquote>"
        )
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("تأكيد ✔️", callback_data=f"confirm_{prod_key}"),
            InlineKeyboardButton("إلغاء ❌", callback_data=product["back"])
        )
        edit_or_send(chat_id, msg_id, product["img"], caption, markup)

    elif data.startswith("confirm_"):
        prod_key = data.replace("confirm_", "", 1)
        product = PRODUCTS.get(prod_key)
        if not product: return
        price = product["price"]
        if balance < price:
            needed 
