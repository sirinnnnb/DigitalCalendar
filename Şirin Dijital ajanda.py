import datetime
import tkinter as tk
from tkinter import messagebox
from datetime import date, timedelta
from tkinter import *
import json
from tkinter import simpledialog
import winsound



users = {
    "admin": "admin",
    "user1": "password1",
    "user2": "password2"
}

def login(self):
        
    
    username = self.username_entry.get()
    password = self.password_entry.get()

    if username in users and users[username] == password:
        self.root.destroy()
        login.destroy()
        CalendarApp()
        calendar_app = CalendarApp(self.root)
        self.root.mainloop()    
    else:
        messagebox.showerror("Hata", "Geçersiz Kullanıcı adı veya Şifre.")



root = tk.Tk()
root.title("Dijital Ajanda")


login_frame = tk.Frame(root)
login_frame.pack(pady=20)

username_label = tk.Label(login_frame, text="Kullanıcı Adı:")
username_label.grid(row=0, column=0, padx=10, pady=5)
username_entry = tk.Entry(login_frame)
username_entry.grid(row=0, column=1)

password_label = tk.Label(login_frame, text="Şifre:")
password_label.grid(row=1, column=0, padx=10, pady=5)
password_entry = tk.Entry(login_frame, show="*")
password_entry.grid(row=1, column=1)

login_button = tk.Button(root, text="Giriş Yap", command=login)
login_button.pack(pady=10)

def register():
    name = name_entry.get()
    surname = surname_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    tc = tc_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    address = address_entry.get()
    user_type = usertype_entry.get()
    
    users[username] = password
    with open ("users.json","w") as file :
        json.dump(users, file)
    


register_frame = tk.Frame(root)
register_frame.pack(pady=20)

name_label = tk.Label(register_frame, text="Ad:")
name_label.grid(row=0, column=0, padx=10, pady=5)
name_entry = tk.Entry(register_frame)
name_entry.grid(row=0, column=1)

surname_label = tk.Label(register_frame, text="Soyad:")
surname_label.grid(row=1, column=0, padx=10, pady=5)
surname_entry = tk.Entry(register_frame)
surname_entry.grid(row=1, column=1)

username_label = tk.Label(register_frame, text="Kullanıcı Adı:")
username_label.grid(row=2, column=0, padx=10, pady=5)
username_entry = tk.Entry(register_frame)
username_entry.grid(row=2, column=1)

password_label = tk.Label(register_frame, text="Şifre:")
password_label.grid(row=3, column=0, padx=10, pady=5)
password_entry = tk.Entry(register_frame, show="*")
password_entry.grid(row=3, column=1)

tc_label = tk.Label(register_frame, text="TC Kimlik No:")
tc_label.grid(row=4, column=0, padx=10, pady=5)
tc_entry = tk.Entry(register_frame)
tc_entry.grid(row=4, column=1)

phone_label = tk.Label(register_frame, text="Telefon:")
phone_label.grid(row=5, column=0, padx=10, pady=5)
phone_entry = tk.Entry(register_frame)
phone_entry.grid(row=5, column=1)

email_label = tk.Label(register_frame, text="Email:")
email_label.grid(row=6, column=0, padx=10, pady=5)
email_entry = tk.Entry(register_frame)
email_entry.grid(row=6, column=1)

address_label = tk.Label(register_frame, text="Adres:")
address_label.grid(row=7, column=0, padx=10, pady=5)
address_entry = tk.Entry(register_frame)
address_entry.grid(row=7, column=1)

usertype_label = tk.Label(register_frame, text="Kullanıcı Tipi:")
usertype_label.grid(row=8, column=0, padx=10, pady=5)
usertype_entry = tk.Entry(register_frame)
usertype_entry.grid(row=8, column=1)

register_button = tk.Button(register_frame, text="Kayıt Ol", command=register)
register_button.grid(row=9, columnspan=2, pady=10)


class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.events = {}
        self.root.title("Takvim Uygulaması")
        root.geometry("640x480")
        root.resizable(False, False)
        
        self.current_date = date.today()
        self.selected_date = self.current_date

        self.calendar_frame1 = tk.Frame(self.root)
        self.calendar_frame1.grid(pady=10)

        self.title_label = tk.Label(self.calendar_frame1, text="Takvim", font=("Helvetica", 20))
        self.title_label.grid(row=0, column=1, columnspan=10)

        self.previous_button = tk.Button(self.calendar_frame1, text="Önceki", command=self.previous_month)
        self.previous_button.grid(row=1, column=0)

        self.month_label = tk.Label(self.calendar_frame1, text="")
        self.month_label.grid(row=1, column=1, columnspan=5)

        self.next_button = tk.Button(self.calendar_frame1, text="Sonraki", command=self.next_month)
        self.next_button.grid(row=1, column=6)

        self.jump_button = tk.Button(self.calendar_frame1, text="Bugüne Git", command=self.go_to_today)
        self.load_events()
        self.event_entry = tk.Entry(root,width=50)
        
        self.frame2 = tk.Frame(self.root)
        self.frame2.grid(row=0, column=0, padx=10, pady=10)

    
        self.days_labels = []
        days = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]
        for i in range(7):
            label = tk.Label(self.calendar_frame1, text=days[i])
            label.grid(row=2, column=i)

        self.cells = []
        for i in range(6):
            row = []
            for j in range(7):
                cell = tk.Button(self.calendar_frame1, width=8, height=4, command=lambda i=i, j=j: self.select_date(i, j))
                cell.grid(row=i+3, column=j)
                row.append(cell)
            self.cells.append(row)

        
        # Create buttons
        self.view_events_button = tk.Button(self.frame2, text="Etkinlik Göster", command=self.view_events)
        self.update_event_button = tk.Button(self.frame2, text="Etkinlik Güncelle", command=self.update_event)
        self.delete_event_button = tk.Button(self.frame2, text="Etkinlik Sil", command=self.delete_event)
        self.set_reminder_button = tk.Button(self.frame2, text="Hatırlatıcı Ekle", command=self.set_reminder)

    # Align buttons to the right side
        self.view_events_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.update_event_button.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.delete_event_button.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.set_reminder_button.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        self.update_calendar()

    def update_calendar(self):
        month = self.current_date.month
        year = self.current_date.year
        self.month_label.config(text=f"{month} / {year}")

        first_day = date(year, month, 1).weekday()
        last_day = date(year, month+1, 1) - timedelta(days=1)
        last_day = last_day.day

        for i in range(6):
            for j in range(7):
                self.cells[i][j].config(text="")
        
        for day in range(1, last_day+1):
            row = (first_day + day - 1) // 7
            col = (first_day + day - 1) % 7
            self.cells[row][col].config(text=day)

    def previous_month(self):
        self.current_date = self.current_date.replace(day=1) - timedelta(days=1)
        self.update_calendar()

    def next_month(self):
        self.current_date = self.current_date.replace(day=28) + timedelta(days=4)
        self.update_calendar()

    def go_to_today(self):
        self.current_date = date.today()
        self.update_calendar()
        
    def select_date(self, row, col):
        day = self.cells[row][col].cget("text")
        if day != "":
            self.selected_date = date(self.current_date.year, self.current_date.month, int(day))
            messagebox.showinfo("Seçili Tarih", f"Seçili Tarih: {self.selected_date}")

            event = tk.Toplevel()
            event.title("Etkinlik Ekleme")

            event_label = tk.Label(event, text="Etkinlik:")
            event_label.pack()

            self.event_entry = tk.Entry(event)
            self.event_entry.pack()

            save_button = tk.Button(event, text="Kaydet", command=self.save_event)
            save_button.pack()
    
    def date_selected(self, date):
        self.selected_date = date
        self.add_event()

    def add_event(self):
        add_event_button = Button(self.calendar_frame, text="Etkinlik Ekle", command=self.save_event)
        if hasattr(self, "selected_date"):
            messagebox.showinfo("Etkinlik Ekle", f"Etkinlik Ekleme: {self.selected_date}")
            event = self.event_entry.get()
            calendar_app.save_event(event)
        else:
            messagebox.showerror("Hata", "Lütfen bir tarih seçin.")

    def save_event(self):
        event = self.event_entry.get()  
        self.events[str(self.selected_date)] = event  
        self.save_events_to_json()
        messagebox.showinfo("Etkinlik Eklendi", "Etkinlik başarıyla eklendi!")

        
    def save_events_to_json(self):
        with open("events.json", "w") as file:
            json.dump(self.events, file, default=str)


        
    def load_events(self):
        try:
           
            with open("events.json", "r") as file:
                self.events = json.load(file)
        except FileNotFoundError:
            self.events = []
            
            
    def view_events(self):
        event_list = ""
        if not self.events:
            event_list = "Takvimde hiç etkinlik yok."
        else:
            for date, event in self.events.items():
                event_list += f"{date}: {event}\n"

        event_window = tk.Toplevel(self.root)
        event_window.title("Takvimdeki Etkinlikler")
        
        messagebox.showinfo("Etkinlikler", event_list)
        event_label = tk.Label(event_window, text=event_list)
        event_label.pack(pady=10, padx=10)
        
        
    def update_event(self):
        if not self.events:
            messagebox.showinfo("Bilgi", "Takvimde hiç etkinlik yok.")
        else:
            selected_date = tk.simpledialog.askstring("Etkinlik Güncelle", "Güncellemek istediğiniz etkinliğin tarihini girin (YYYY-MM-DD):")
            if selected_date in self.events:
                new_event = tk.simpledialog.askstring("Etkinlik Güncelle", "Yeni etkinliği girin:")
                self.events[selected_date] = new_event  
                self.save_events_to_json()
                messagebox.showinfo("Bilgi", "Etkinlik güncellendi.")
            else:
                messagebox.showerror("Hata", "Belirtilen tarihe sahip bir etkinlik bulunamadı.")
    
    
    def delete_event(self):
        if not self.events:
            messagebox.showinfo("Bilgi", "Takvimde hiç etkinlik yok.")
        else:
            selected_date = simpledialog.askstring("Etkinlik Güncelle", "Güncellemek istediğiniz etkinliğin tarihini girin (YYYY-MM-DD):")
            if selected_date in self.events:
                del self.events[selected_date]
                self.save_events_to_json()
                messagebox.showinfo("Bilgi", "Etkinlik silindi.")
            else:
                messagebox.showerror("Hata", "Belirtilen tarihe sahip bir etkinlik bulunamadı.")
                
    def set_reminder(self):
        event = self.event_entry.get()
        if event:
            date_str = simpledialog.askstring("Hatırlatıcı Ekle", "Etkinlik Tarihini Girin (YYYY-MM-DD):")
            time_str = simpledialog.askstring("Hatırlatıcı Ekle", "Etkinlik Saatini Girin (HH:MM):")

            try:
                event_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                event_time = datetime.strptime(time_str, "%H:%M").time()

                reminder_datetime = datetime.combine(event_date, event_time)
                current_datetime = datetime.now()

                if reminder_datetime > current_datetime:
                    time_delta = reminder_datetime - current_datetime
                    seconds = time_delta.total_seconds()
                    self.root.after(int(seconds * 1000), self.show_reminder, event)
                    messagebox.showinfo("Hatırlatıcı Eklendi", "Hatırlatıcı başarıyla ayarlandı.")
                else:
                    messagebox.showerror("Hata", "Geçmiş bir tarih veya saat ayarlanamaz.")
            except ValueError:
                messagebox.showerror("Hata", "Geçersiz tarih veya saat formatı.")
        else:
            messagebox.showerror("Hata", "Etkinlik alanı boş olamaz.")

    def show_reminder(self, event):
        winsound.PlaySound("zil_sesi.wav", winsound.SND_FILENAME)
        messagebox.showinfo("Hatırlatıcı", f"{event}\n\nŞimdi zamanı geldi!")



if __name__ == "__main__":
    root = tk.Tk()
    calendar_app = CalendarApp(root)
    root.mainloop()
    
