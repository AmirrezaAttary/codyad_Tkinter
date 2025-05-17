import os
import win32api
import win32print

# مسیر فایل PDF که قبلاً توسط برنامه تولید شده
file_path = os.path.join(os.getcwd(), 'print_agin', 'paziresh_1591_mojadad.pdf')

# بررسی وجود فایل
if os.path.exists(file_path):
    try:
        # ارسال به پرینتر پیش‌فرض بدون باز کردن فایل
        win32api.ShellExecute(
            0,
            "print",
            file_path,
            None,
            ".",
            0
        )
        print("فایل ارسال شد به چاپگر")
    except Exception as e:
        print("خطا هنگام چاپ:", e)
else:
    print("فایل یافت نشد:", file_path)
