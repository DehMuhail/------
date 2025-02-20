import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import yt_dlp

# Настройки
ffmpeg_path = r'C:\Program Files\ffmpeg\ffmpeg-7.1-full_build\bin\ffmpeg.exe'
download_path = r'C:\Users\Фыва\Desktop\фильмЫ\фильмы'

ydl_opts = {
    'format': 'best',
    'outtmpl': os.path.join(download_path, '%(playlist_title)s/%(title)s.%(ext)s'),
    'ffmpeg_location': ffmpeg_path,
}

# Функция для скачивания видео или плейлиста
def download_content(url, save_path, is_playlist):
    try:
        opts = ydl_opts.copy()
        opts['outtmpl'] = os.path.join(save_path, '%(playlist_title)s/%(title)s.%(ext)s') if is_playlist else os.path.join(save_path, '%(title)s.%(ext)s')
        opts['noplaylist'] = not is_playlist
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Успех", f"Контент по адресу {url} успешно скачан в {save_path}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при скачивании {url}: {e}")

# Класс интерфейса
class VideoDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Скачиватель видео и плейлистов")
        
        # Поле для ввода ссылки
        self.url_label = tk.Label(root, text="Ссылка на видео/плейлист:")
        self.url_label.grid(row=0, column=0, padx=5, pady=5)
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.grid(row=0, column=1, padx=5, pady=5)
        self.add_button = tk.Button(root, text="Добавить в очередь", command=self.add_to_queue)
        self.add_button.grid(row=0, column=2, padx=5, pady=5)
        
        # Поле для выбора пути
        self.path_label = tk.Label(root, text="Путь для сохранения:")
        self.path_label.grid(row=1, column=0, padx=5, pady=5)
        self.path_entry = tk.Entry(root, width=50)
        self.path_entry.insert(0, download_path)
        self.path_entry.grid(row=1, column=1, padx=5, pady=5)
        self.browse_button = tk.Button(root, text="Выбрать...", command=self.browse_path)
        self.browse_button.grid(row=1, column=2, padx=5, pady=5)
        
        # Чекбокс для выбора типа скачивания
        self.playlist_var = tk.BooleanVar()
        self.playlist_checkbox = tk.Checkbutton(root, text="Скачать как плейлист", variable=self.playlist_var)
        self.playlist_checkbox.grid(row=2, column=1, pady=5)
        
        # Очередь
        self.queue_label = tk.Label(root, text="Очередь:")
        self.queue_label.grid(row=3, column=0, padx=5, pady=5)
        self.queue_list = tk.Listbox(root, selectmode=tk.SINGLE, width=50, height=10)
        self.queue_list.grid(row=3, column=1, padx=5, pady=5)
        self.remove_button = tk.Button(root, text="Удалить", command=self.remove_from_queue)
        self.remove_button.grid(row=3, column=2, padx=5, pady=5)
        
        # Кнопка запуска
        self.download_button = tk.Button(root, text="Начать скачивание", command=self.start_download)
        self.download_button.grid(row=4, column=1, pady=10)
    
    def add_to_queue(self):
        url = self.url_entry.get().strip()
        if url:
            self.queue_list.insert(tk.END, url)
            self.url_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Внимание", "Введите ссылку!")
    
    def remove_from_queue(self):
        selected = self.queue_list.curselection()
        if selected:
            self.queue_list.delete(selected)
        else:
            messagebox.showwarning("Внимание", "Выберите элемент для удаления!")
    
    def browse_path(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder)
    
    def start_download(self):
        urls = self.queue_list.get(0, tk.END)
        save_path = self.path_entry.get()
        is_playlist = self.playlist_var.get()
        if not urls:
            messagebox.showwarning("Внимание", "Очередь пуста!")
            return
        for url in urls:
            download_content(url, save_path, is_playlist)

# Основной запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = VideoDownloaderApp(root)
    root.mainloop()
