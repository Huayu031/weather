import os
import requests
import random
from datetime import datetime

# 获取环境变量
app_id = "wx9c17d2ffce0e489e"  # 替换成你的公众号的 AppID
app_secret = "08104cab40adb2bde4476069e4bab08b"  # 替换成你的公众号的 AppSecret
openid = "o603S6X7MkTBvEzPpWm-gDZQn-V8"  # 替换成实际用户的 openid
hefeng_api_key = "df95c9c800344ed39ec2b4bc31f531b3"  # 替换成你的和风天气 API 密钥

# 恋爱开始的日期
love_start_date = datetime(2024, 11, 22)

# 两个人的生日
my_birthday = datetime(datetime.today().year, 3, 1)  # 我的生日
girlfriend_birthday = datetime(datetime.today().year, 1, 12)  # 女友的生日

# 获取今天的日期
today = datetime.today()

# 计算恋爱的第几天
days_in_love = (today - love_start_date).days +1


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


def get_weather(city_code, api_key):
    url = f"https://devapi.qweather.com/v7/weather/now?location={city_code}&key={api_key}"
    response = requests.get(url)
    data = response.json()

    # 打印整个响应数据，确保我们能看到温度信息
    print("Weather API Response:", data)

    if data['code'] == '200':  # 确保请求成功
        current_temp = data['now'].get('temp', 'N/A')  # 当前温度
        weather_text = data['now'].get('text', '未知')  # 天气描述

        # 可选：其他天气信息
        feels_like = data['now'].get('feelsLike', 'N/A')  # 体感温度
        wind_dir = data['now'].get('windDir', '未知')  # 风向
        wind_speed = data['now'].get('windSpeed', 'N/A')  # 风速

        # 打印当前温度，确保数据正确
        print(f"Current temperature: {current_temp}°C")

        return current_temp, feels_like, weather_text, wind_dir, wind_speed
    else:
        print(f"Error: Unable to fetch weather data. Code: {data.get('code')}")
        return None, None, None, None, None


def get_access_token(app_id, app_secret):
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
    response = requests.get(url)
    print(f"Access Token 请求响应: {response.text}")  # 打印响应内容
    data = response.json()

    if 'access_token' in data:
        return data['access_token']
    else:
        print(f"Error: {data.get('errmsg', 'Unable to fetch access_token')}")
        return None


def send_message():
    access_token = get_access_token(app_id, app_secret)

    if not access_token:
        print("无法获取 Access Token，退出程序。")
        return  # 退出程序

    # 获取天气信息
    current_temp, feels_like, weather_text, wind_dir, wind_speed = get_weather("101230107", hefeng_api_key)

    if current_temp is None:
        print("Weather data is unavailable.")
        return  # 如果天气信息获取失败，则不发送消息

    # 生成模板消息数据
    message_data = {
        "touser": openid,
        "template_id": "FpaxwnbsnOS94aDCHngi4Y0B2tAFXw1skE3ml_BM2jQ",
        "data": {
            "first": {"value": "你好！", "color": "#173177"},
            "date": {"value": str(today.date()), "color": "#173177"},
            "weather": {"value": weather_text, "color": "#173177"},
            "current_temp": {"value": f"{current_temp}°C", "color": "#173177"},
            "feels_like": {"value": f"{feels_like}°C", "color": "#FF6347"},
            "wind_speed": {"value": f"{wind_speed} km/h", "color": "#FF1493"},
            "days_in_love": {"value": f"{days_in_love}", "color": "#FF69B4"},
            "my_birthday_days_left": {"value": f"{my_birthday_days_left}", "color": "#FF6347"},
            "girlfriend_birthday_days_left": {"value": f"{girlfriend_birthday_days_left}",
                                              "color": "#FF1493"},
            "daily_quote": {"value": daily_quote, "color": "#FF4500"}
        }
    }

    # 发送模板消息
    url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}"
    response = requests.post(url, json=message_data)
    print("API 请求响应:", response.text)  # 打印返回的响应内容



# 调用函数发送消息
send_message()
