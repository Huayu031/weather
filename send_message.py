import os
import requests
import random
from datetime import datetime

# 获取环境变量
app_id = os.getenv("APP_ID")
app_secret = os.getenv("APP_SECRET")
openid = os.getenv("OPENID")
hefeng_api_key = os.getenv("HEFENG_API_KEY")

# 恋爱开始的日期
love_start_date = datetime(2023, 1, 1)

# 两个人的生日
my_birthday = datetime(datetime.today().year, 12, 10)  # 我的生日
girlfriend_birthday = datetime(datetime.today().year, 6, 15)  # 女友的生日

# 获取今天的日期
today = datetime.today()

# 计算恋爱的第几天
days_in_love = (today - love_start_date).days

# 计算下一个生日
def days_until_next_birthday(birthday):
    if today > birthday:
        birthday = datetime(today.year + 1, birthday.month, birthday.day)
    return (birthday - today).days

# 计算距离下一个生日的天数
my_birthday_days_left = days_until_next_birthday(my_birthday)
girlfriend_birthday_days_left = days_until_next_birthday(girlfriend_birthday)

# 每日寄语
daily_quotes = [
    "每天都是新的开始，珍惜每一刻。",
    "爱是一种温暖的陪伴。",
    "无论何时，只要你需要，我都会在你身边。",
    "爱情不仅是甜蜜的承诺，更是彼此的支持。",
    "每天都是爱的延续，感谢有你。",
    "遇到你，是我一生最美好的事。"
]

# 随机选择一条每日寄语
daily_quote = random.choice(daily_quotes)

def get_weather(city):
    url = f"https://devapi.qweather.com/v7/weather/now?location={city}&key={hefeng_api_key}"
    response = requests.get(url)
    return response.json()

def send_message():
    # 获取天气信息
    weather = get_weather("your_city")  # 替换为你所在城市的代码
    message_data = {
        "touser": openid,
        "template_id": "your_template_id",  # 替换为你在公众号后台申请的模板 ID
        "data": {
            "date": {"value": str(today.date()), "color": "#173177"},
            "weather": {"value": weather['now']['text'], "color": "#173177"},
            "temp": {"value": f"{weather['now']['temp']}℃", "color": "#173177"},
            "days_in_love": {"value": f"恋爱的第 {days_in_love} 天", "color": "#FF69B4"},
            "my_birthday_days_left": {"value": f"距离我的生日还有 {my_birthday_days_left} 天", "color": "#FF6347"},
            "girlfriend_birthday_days_left": {"value": f"距离女友的生日还有 {girlfriend_birthday_days_left} 天", "color": "#FF1493"},
            "daily_quote": {"value": daily_quote, "color": "#FF4500"}
        }
    }

    # 发送消息的请求
    url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}"
    response = requests.post(url, json=message_data)
    print(response.json())

if __name__ == "__main__":
    send_message()
