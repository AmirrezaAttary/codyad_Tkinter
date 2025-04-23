class Library:
    def __init__(self):
        self.books = []  # لیست کتاب‌ها

    def add_book(self, title, author):
        self.books.append({"title": title, "author": author})
        print(f"کتاب '{title}' به کتابخانه اضافه شد.")

    def remove_book(self, title):
        for book in self.books:
            if book['title'] == title:
                self.books.remove(book)
                print(f"کتاب '{title}' از کتابخانه حذف شد.")
                return
        print(f"کتاب '{title}' پیدا نشد.")

    def search_book(self, title):
        for book in self.books:
            if book['title'] == title:
                print(f"کتاب پیدا شد: {book['title']} نوشته {book['author']}")
                return
        print(f"کتاب '{title}' پیدا نشد.")

    def show_books(self):
        if not self.books:
            print("کتابخانه خالی است.")
        else:
            print("کتاب‌های موجود در کتابخانه:")
            for book in self.books:
                print(f"عنوان: {book['title']}, نویسنده: {book['author']}")
