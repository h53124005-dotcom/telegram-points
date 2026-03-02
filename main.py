import json
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")
DATA = "points.json"


# ======================
# 📦 تحميل البيانات
# ======================
def load_data():
    if os.path.exists(DATA):
        try:
            with open(DATA, "r") as f:
                return json.load(f)
        except:
            pass
    return {}


def save_data(data):
    with open(DATA, "w") as f:
        json.dump(data, f, indent=4)


data = load_data()


# ======================
# ➕ إضافة نقاط
# ======================
async def add_points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 2:
        return await update.message.reply_text("استخدم: /dxp اسم عدد")

    name = context.args[0]

    try:
        amount = int(context.args[1])
    except ValueError:
        return await update.message.reply_text("❌ لازم الرقم يكون عدد صحيح")

    data[name] = data.get(name, 0) + amount
    save_data(data)

    await update.message.reply_text(f"✅ تمت إضافة {amount} نقطة لـ {name}")


# ======================
# ➖ خصم نقاط
# ======================
async def remove_points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 2:
        return await update.message.reply_text("استخدم: /rep اسم عدد")

    name = context.args[0]

    try:
        amount = int(context.args[1])
    except ValueError:
        return await update.message.reply_text("❌ لازم الرقم يكون عدد صحيح")

    data[name] = data.get(name, 0) - amount
    save_data(data)

    await update.message.reply_text(f"❌ تم خصم {amount} نقطة من {name}")


# ======================
# 🏆 عرض أفضل 10
# ======================
async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not data:
        return await update.message.reply_text("❌ لا توجد نقاط حالياً")

    sorted_users = sorted(data.items(), key=lambda x: x[1], reverse=True)[:10]

    text = "🏆 أفضل 10:\n\n"
    for i, (name, points) in enumerate(sorted_users, 1):
        text += f"{i}- {name} | {points}\n"

    await update.message.reply_text(text)


# ======================
# 🚀 تشغيل البوت
# ======================
def main():
    if not TOKEN:
        raise ValueError("TOKEN غير موجود في Environment Variables")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("dxp", add_points))
    app.add_handler(CommandHandler("rep", remove_points))
    app.add_handler(CommandHandler("top", top))

    print("🚀 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
