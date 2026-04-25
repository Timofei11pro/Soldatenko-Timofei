import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary")
        self.data_file = "weather_data.json"
        self.records = self.load_data()

        # Поля ввода
        tk.Label(root, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0)
        self.entry_date = tk.Entry(root)
        self.entry_date.grid(row=0, column=1)

        tk.Label(root, text="Температура (°C):").grid(row=1, column=0)
        self.entry_temp = tk.Entry(root)
        self.entry_temp.grid(row=1, column=1)

        tk.Label(root, text="Описание:").grid(row=2, column=0)
        self.entry_desc = tk.Entry(root)
        self.entry_desc.grid(row=2, column=1)

        self.var_precip = tk.BooleanVar()
        tk.Checkbutton(root, text="Осадки", variable=self.var_precip).grid(row=3, columnspan=2)

        # Кнопки
        tk.Button(root, text="Добавить запись", command=self.add_record).grid(row=4, columnspan=2, pady=5)
        tk.Button(root, text="Сбросить фильтр", command=self.update_table).grid(row=5, column=0)
        tk.Button(root, text="Фильтр > +10°C", command=self.filter_warm).grid(row=5, column=1)

        # Таблица
        self.tree = ttk.Treeview(root, columns=("Date", "Temp", "Desc", "Precip"), show='headings')
        self.tree.heading("Date", text="Дата")
        self.tree.heading("Temp", text="Темп.")
        self.tree.heading("Desc", text="Описание")
        self.tree.heading("Precip", text="Осадки")
        self.tree.grid(row=6, columnspan=2, padx=10, pady=10)

        self.update_table()

    def add_record(self):
        date = self.entry_date.get()
        temp = self.entry_temp.get()
        desc = self.entry_desc.get()
        precip = "Да" if self.var_precip.get() else "Нет"

        # Валидация
        if not date or not desc:
            messagebox.showerror("Ошибка", "Заполните все поля")
            return
        try:
            temp = float(temp)
        except ValueError:
            messagebox.showerror("Ошибка", "Температура должна быть числом")
            return

        self.records.append({"date": date, "temp": temp, "desc": desc, "precip": precip})
        self.save_data()
        self.update_table()
        
    def save_data(self):
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.records, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def update_table(self, data=None):
        for i in self.tree.get_children():
            self.tree.delete(i)
        display_data = data if data is not None else self.records
        for r in display_data:
            self.tree.insert("", "end", values=(r['date'], r['temp'], r['desc'], r['precip']))

    def filter_warm(self):
        filtered = [r for r in self.records if r['temp'] > 10]
        self.update_table(filtered)

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiary(root)
    root.mainloop()
