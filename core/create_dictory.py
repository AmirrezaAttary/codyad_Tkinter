import os

def create_dictory():
# لیست دایرکتوری‌هایی که باید بررسی و در صورت نیاز ساخته شوند
    directories = ['print','database', 'print_agin']

    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)

