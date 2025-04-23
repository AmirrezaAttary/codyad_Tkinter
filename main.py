def divide(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print("خطا: تقسیم بر صفر امکان‌پذیر نیست.")
        return None

while True:
    try:
        num1 = int(input("Enter first number: "))
        num2 = int(input("Enter second number: "))
        result = divide(num1, num2)
        if result is not None:
            print("Result:", result)
            break  # اگر همه چیز درست بود، از حلقه خارج شویم
    except ValueError:
        print("خطا: لطفاً فقط عدد وارد کنید.")
    finally:
        print("برنامه با موفقیت اجرا شد!\n")
