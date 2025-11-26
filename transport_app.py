import tkinter as tk
from tkinter import messagebox
import sqlite3

class FreightTransport: #Класс для представления объекта грузового транспорта
    def __init__(self, id, name, payload_capacity, is_booked, length, width, height):
        self.id = id
        self.name = name
        self.payload_capacity = payload_capacity
        self.is_booked = is_booked
        self.length = length
        self.width = width
        self.height = height

class FreightTransportManager: #Класс для управления грузовым транспортом, включая взаимодействие с базой данных
    def __init__(self):
        self.connection = sqlite3.connect('transport.db')
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self): #Создание таблицы в базе данных
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS freight_transport
                            (id INTEGER PRIMARY KEY, name TEXT, payload_capacity REAL,
                            is_booked INTEGER, length REAL, width REAL, height REAL)''')
        self.connection.commit()

    def add_transport(self, name, payload_capacity, length, width, height): #Добавление нового транспорта в базу данных
        self.cursor.execute("INSERT INTO freight_transport (name, payload_capacity, is_booked, length, width, height) "
                            "VALUES (?, ?, 0, ?, ?, ?)",
                            (name, payload_capacity, length, width, height))
        self.connection.commit()
        messagebox.showinfo("Успешно", "Грузовой транспорт добавлен")

    def delete_transport(self, transport_id): #Удаление транспорта из базы данных по его идентификатору
        self.cursor.execute("DELETE FROM freight_transport WHERE id=?", (transport_id,))
        if self.cursor.rowcount == 0:
            return messagebox.showerror(title="Ошибка", message="Транспорт с указанным id не найден")
        else:
            self.connection.commit()
            messagebox.showinfo(title="Уведомление", message="Грузовой транспорт успешно удален")

    def view_all_transport(self):   #Отображение информации о всех транспортах из базы данных
        self.cursor.execute("SELECT * FROM freight_transport")
        transports = self.cursor.fetchall()
        if not transports:
            messagebox.showinfo("Грузовой транспорт", "Транспортные средства не добавлены")
            return
        transport_info =''
        for transport in transports:
            transport_info += f"ID: {transport[0]}, Название: {transport[1]}, " \
                              f"Грузоподъемность: {transport[2]}, " \
                              f"Длина: {transport[4]}, " \
                              f"Ширина: {transport[5]}, Высота: {transport[6]}," \
                              f"Забронирован: {'Да' if transport[3] else 'Нет'}\n"
        messagebox.showinfo("Грузовой транспорт", transport_info)

    def view_transport_by_capacity(self, payload_capacity): #Отображение информации о транспортах с грузоподъемностью больше или равной заданной
        self.cursor.execute("SELECT * FROM freight_transport WHERE payload_capacity >= ?", (payload_capacity,))
        transports = self.cursor.fetchall()
        if not transports:
            messagebox.showinfo("Грузовой транспорт", "Нет транспорта с подходящей грузоподъемностью")
            return
        transport_info = ""
        for transport in transports:
            transport_info += f"ID: {transport[0]}, Название: {transport[1]}, " \
                              f"Грузоподъемность: {transport[2]}, " \
                              f"Длина: {transport[4]}, Ширина: {transport[5]}, Высота: {transport[6]}," \
                              f"Забронирован: {'Да' if transport[3] else 'Нет'}\n"
        messagebox.showinfo("Грузовой транспорт", transport_info)

    def view_available_transport(self): #Отображение информации о свободных транспортах
        self.cursor.execute("SELECT * FROM freight_transport WHERE is_booked=0")
        transports = self.cursor.fetchall()
        if not transports:
            messagebox.showinfo("Свободный грузовой транспорт", "Нет свободного транспорта")
            return
        transport_info = ""
        for transport in transports:
            transport_info += f"ID: {transport[0]}, Название: {transport[1]}, " \
                              f"Грузоподъемность: {transport[2]}, " \
                              f"Длина: {transport[4]}, Ширина: {transport[5]}, Высота: {transport[6]}\n" 
        messagebox.showinfo("Свободный грузовой транспорт", transport_info)

    def view_transport_by_dimensions(self, length, width, height):  #Отображение информации о транспорте, удовлетворяющем указанным габаритам
        self.cursor.execute("SELECT * FROM freight_transport WHERE length >= ? AND width >= ? AND height >= ?",
                            (length, width, height))
        transports = self.cursor.fetchall()
        if not transports:
            messagebox.showinfo("Грузовой транспорт", "Нет подходящего транспорта по заданным габаритам.")
            return
        transport_info = ""
        for transport in transports:
            transport_info += f"ID: {transport[0]}, Название: {transport[1]}, Грузоподъемность: {transport[2]}, " \
                              f"Длина: {transport[4]}, Ширина: {transport[5]}, Высота: {transport[6]}, " \
                              f"Забронирован: {'Да' if transport[3] else 'Нет'}\n"
        messagebox.showinfo("Грузовой транспорт", transport_info)

    def make_booking(self, transport_id):   #Бронирование грузового транспорта по его идентификатору
        self.cursor.execute("SELECT * FROM freight_transport WHERE id=?", (transport_id,))
        t = self.cursor.fetchall()
        if len(t) > 0:
            if not t[0][3]:
                self.cursor.execute("UPDATE freight_transport SET is_booked=1 WHERE id=?", (transport_id,))
                self.connection.commit()
                messagebox.showinfo("Успешно", "Транспорт успешно забронирован.")
            else:
                messagebox.showerror("Ошибка", "Этот транспорт уже забронирован.")
        else:
            messagebox.showerror("Ошибка", "Транспорт с указанным id не найден.")

    
    def view_booked_transport(self):    #Отображение информации о забронированном транспорте
        self.cursor.execute("SELECT * FROM freight_transport WHERE is_booked=1")
        transports = self.cursor.fetchall()
        if not transports:
            messagebox.showinfo("Забронированный грузовой транспорт", "Нет забронированного транспорта.")
            return
        transport_info = ""
        for transport in transports:
            transport_info += f"ID: {transport[0]}, Название: {transport[1]}, " \
                              f"Грузоподъемность: {transport[2]}, " \
                              f"Длина: {transport[4]}, Ширина: {transport[5]}, Высота: {transport[6]}\n"
        messagebox.showinfo("Забронированный грузовой транспорт", transport_info)

    def cancel_booking(self, transport_id): #Отмена бронирования транспорта
        try:
            self.cursor.execute("SELECT is_booked FROM freight_transport WHERE id=?", (transport_id,))
            result = self.cursor.fetchone()
            if result and result[0] == 1:
                self.cursor.execute("UPDATE freight_transport SET is_booked=0 WHERE id=?", (transport_id,))
                self.connection.commit()
                messagebox.showinfo("Успешно", "Бронирование транспорта успешно отменено.")
            else:
                messagebox.showerror("Ошибка", "Этот транспорт не забронирован или не существует.")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))


    def close(self):    #Закрытие соединения с базой данных
        self.cursor.close()
        self.connection.close()

class GUI:  #Класс для создания графического интерфейса пользователя
    def __init__(self):
        self.manager = FreightTransportManager()  
        self.window = tk.Tk()  
        self.window.title("Учет грузового транспорта")  
        self.window.geometry("350x450")  
        self.window.resizable(False, False)  
        self.create_buttons()  

    def create_buttons(self):   #Создание кнопок главного меню
        self.clear_page()  # Очистка текущей страницы
        add_button = tk.Button(self.window, text="Добавить транспорт", command=self.add_transport_view)
        add_button.pack(pady=(20, 5))
        delete_button = tk.Button(self.window, text="Удалить транспорт", command=self.transport_delete)
        delete_button.pack(pady=5)
        view_all_button = tk.Button(self.window, text="Просмотреть весь транспорт", command=self.view_all_transport)
        view_all_button.pack(pady=5)
        view_capacity_button = tk.Button(self.window, text="Просмотреть транспорт по грузоподъемности", command=self.check_capacity)
        view_capacity_button.pack(pady=5)
        view_available_button = tk.Button(self.window, text="Просмотреть свободный транспорт", command=self.view_available_transport)
        view_available_button.pack(pady=5)
        view_dimensions_button = tk.Button(self.window, text="Подобрать транспорт по габаритам", command=self.view_transport_by_dimensions_view)
        view_dimensions_button.pack(pady=5)
        book_button = tk.Button(self.window, text="Забронировать транспорт", command=self.transport_booking)
        book_button.pack(pady=5)
        view_booked_button = tk.Button(self.window, text="Просмотреть забронированный транспорт", command=self.view_booked_transport)
        view_booked_button.pack(pady=5)
        cancel_booking_button = tk.Button(self.window, text="Отменить бронирование", command=self.cancel_booking_view)
        cancel_booking_button.pack(pady=5)
        exit_button = tk.Button(self.window, text="Выход", command=self.close)
        exit_button.pack(pady=5)
        self.window.protocol("WM_DELETE_WINDOW", self.close)  

    def clear_page(self):   #Очищение текущей страницы
        for widget in self.window.winfo_children():
            widget.destroy()

    def add_transport_view(self):    #Отображение вида для добавления нового транспорта
        self.clear_page()
        tk.Label(self.window, text="Название:").pack(pady=(20, 5))
        self.name_entry = tk.Entry(self.window)
        self.name_entry.pack(pady=5)
        tk.Label(self.window, text="Грузоподъемность:").pack(pady=5)
        self.capacity_entry = tk.Entry(self.window)
        self.capacity_entry.pack(pady=5)
        tk.Label(self.window, text="Длина:").pack(pady=5)
        self.length_entry = tk.Entry(self.window)
        self.length_entry.pack(pady=5)
        tk.Label(self.window, text="Ширина:").pack(pady=5)
        self.width_entry = tk.Entry(self.window)
        self.width_entry.pack(pady=5)
        tk.Label(self.window, text="Высота:").pack(pady=5)
        self.height_entry = tk.Entry(self.window)
        self.height_entry.pack(pady=5)
        add_button = tk.Button(self.window, text="Добавить", command=self.add_transport)
        add_button.pack(pady=5)
        add_button = tk.Button(self.window, text="Вернуться в меню", command=self.create_buttons)
        add_button.pack(pady=5)

    def add_transport(self):    #Добавление нового транспорта в базу данных
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Ошибка", "Поле 'Название' не может быть пустым")
            return
        try:
            capacity = float(self.capacity_entry.get())
            if capacity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректное значение в поле 'Грузоподъемность'. Должно быть положительное число.")
            return
        try:
            length = float(self.length_entry.get())
            if length <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректное значение в поле 'Длина'. Должно быть положительное число.")
            return
        try:
            width = float(self.width_entry.get())
            if width <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректное значение в поле 'Ширина'. Должно быть положительное число.")
            return
        try:
            height = float(self.height_entry.get())
            if height <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректное значение в поле 'Высота'. Должно быть положительное число.")
            return

        self.manager.add_transport(name, capacity, length, width, height)
        self.name_entry.delete(0, tk.END)
        self.capacity_entry.delete(0, tk.END)
        self.length_entry.delete(0, tk.END)
        self.width_entry.delete(0, tk.END)
        self.height_entry.delete(0, tk.END)

    def transport_delete(self): #Отображение вида для удаления транспорта
        self.clear_page()
        tk.Label(self.window, text="Введите ID транспорта:").pack(pady=(20, 5))
        self.delete_entry = tk.Entry(self.window)
        self.delete_entry.pack(pady=5)
        delete_button = tk.Button(self.window, text="Удалить", command=self.delete_transport)
        delete_button.pack(pady=5)
        add_button = tk.Button(self.window, text="Вернуться в меню", command=self.create_buttons)
        add_button.pack(pady=5)

    def delete_transport(self): #Удаление транспорта из базы данных по ID
        transport_id_str = self.delete_entry.get()
        if transport_id_str:
            try:
                transport_id = int(transport_id_str)
                self.manager.delete_transport(transport_id)
                self.delete_entry.delete(0, tk.END)
            except ValueError:
                messagebox.showerror(title="Ошибка", message="Некорректный идентификатор транспорта")
        else:
            messagebox.showerror(title="Ошибка", message="Введите идентификатор транспорта")

    def view_all_transport(self):   #Просмотр всех транспортных средств
        self.manager.view_all_transport()

    def check_capacity(self):   # Отображение формы для проверки грузоподъемности
        self.clear_page()
        tk.Label(self.window, text="Грузоподъемность:").pack(pady=(20,5))
        self.capacity_entry = tk.Entry(self.window)
        self.capacity_entry.pack(pady=5)
        view_capacity_button = tk.Button(self.window, text="Просмотреть", command=self.view_transport_by_capacity)
        view_capacity_button.pack(pady=5)
        add_button = tk.Button(self.window, text="Вернуться в меню", command=self.create_buttons)
        add_button.pack(pady=5)

    def view_transport_by_capacity(self):   # Просмотр транспортных средств по грузоподъемности с проверкой на положительные значения
        capacity_str = self.capacity_entry.get()
        if capacity_str:
            try:
                capacity = float(capacity_str)
                if capacity <= 0:
                    raise ValueError
                self.manager.view_transport_by_capacity(capacity)
            except ValueError:
                messagebox.showerror("Ошибка", "Некорректное значение грузоподъемности.")
        else:
            messagebox.showerror("Ошибка", "Введите значение грузоподъемности.")
        
    def view_available_transport(self):     #Просмотр всех свободных транспортных средств
        self.manager.view_available_transport()

    def view_transport_by_dimensions_view(self):    #Отображение вида для подбора транспорта по габаритам
        self.clear_page()
        tk.Label(self.window, text="Длина:").pack(pady=(20, 5))
        self.length_entry = tk.Entry(self.window)
        self.length_entry.pack(pady=5)
        tk.Label(self.window, text="Ширина:").pack(pady=5)
        self.width_entry = tk.Entry(self.window)
        self.width_entry.pack(pady=5)
        tk.Label(self.window, text="Высота:").pack(pady=5)
        self.height_entry = tk.Entry(self.window)
        self.height_entry.pack(pady=5)
        view_button = tk.Button(self.window, text="Подобрать транспорт", command=self.view_transport_by_dimensions)
        view_button.pack(pady=5)
        add_button = tk.Button(self.window, text="Вернуться в меню", command=self.create_buttons)
        add_button.pack(pady=5)

    def view_transport_by_dimensions(self): #Просмотр транспорт по опреденным габаритам
        try:
            length = float(self.length_entry.get())
            if length <= 0:
                raise ValueError
            width = float(self.width_entry.get())
            if width <= 0:
                raise ValueError
            height = float(self.height_entry.get())
            if height <= 0:
                raise ValueError
            self.manager.view_transport_by_dimensions(length, width, height)
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректные значения габаритов. Все значения должны быть положительными.")
              

    def transport_booking(self):    #Отображение вида для бронирования транспорта
        self.clear_page()
        tk.Label(self.window, text="Введите ID транспорта:").pack(pady=(20, 5))
        self.booking_entry = tk.Entry(self.window)
        self.booking_entry.pack(pady=5)
        book_button = tk.Button(self.window, text="Забронировать", command=self.make_booking)
        book_button.pack(pady=5)
        add_button = tk.Button(self.window, text="Вернуться в меню", command=self.create_buttons)
        add_button.pack(pady=5)

    def make_booking(self):     #Бронирование транспорта
        transport_id_str = self.booking_entry.get()
        if transport_id_str:
            try:
                transport_id = int(transport_id_str)
                self.manager.make_booking(transport_id)
                self.booking_entry.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Ошибка", "Некорректный идентификатор транспорта")
        else:
            messagebox.showerror("Ошибка", "Введите идентификатор транспорта")

    def view_booked_transport(self):    #Просмотр всех забронированных транспортных средств
        self.manager.view_booked_transport()

    def cancel_booking_view(self):  #Отображение вида для отмены бронирования транспорта
        self.clear_page()
        tk.Label(self.window, text="Введите ID транспорта для отмены брони:").pack(pady=(20,5))
        self.cancel_entry = tk.Entry(self.window)
        self.cancel_entry.pack(pady=5)
        cancel_button = tk.Button(self.window, text="Отменить бронь", command=self.perform_cancel_booking)
        cancel_button.pack(pady=5)
        back_button = tk.Button(self.window, text="Вернуться в меню", command=self.create_buttons)
        back_button.pack(pady=5)

    def perform_cancel_booking(self):   #Отмена бронирования транспорта
        transport_id_str = self.cancel_entry.get()
        try:
            transport_id = int(transport_id_str)
            self.manager.cancel_booking(transport_id)
            self.cancel_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный идентификатор транспорта.")

    def close(self):    #Закрытие приложения
        self.manager.close()
        self.window.destroy()


if __name__ == "__main__":
    gui = GUI()
    gui.create_buttons()
    tk.mainloop()


