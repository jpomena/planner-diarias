from src import MainController

if __name__ == "__main__":
    app = MainController()
    app.main_window.iconbitmap('icon.ico')
    app.main_window.mainloop()
