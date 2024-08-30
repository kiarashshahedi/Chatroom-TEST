import requests

# تعریف URL API
url = "http://api.iransmsservice.com/v2/sms/send/simple"

# تعریف پارامترهای payload
payload = {
    "message": "کد OTP شما: 123456",  # این را با پیام واقعی خود جایگزین کنید
    "sender": "03000260026",  # این را با شماره فرستنده واقعی خود جایگزین کنید
    "receptor": "09056860284",  # شماره گیرنده
}

# تعریف هدرها با کلید API
headers = {
    "apikey": "4nH28xq0uiwHbzLrSOxewVxuFOkfmwT1SvLEbkIl7HA"
}

# ارسال درخواست POST
try:
    response = requests.post(url, data=payload, headers=headers)
    response.raise_for_status()  # برای خطاهای HTTP استثنا ایجاد می‌کند
    print("کد وضعیت پاسخ:", response.status_code)
    print("متن پاسخ:", response.text)
except requests.exceptions.RequestException as e:
    print("یک خطا رخ داده است:", e)
