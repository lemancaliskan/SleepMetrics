import os
from PIL import Image
import customtkinter as ctk

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
png_path = os.path.join(ASSETS_DIR, "icon.png")
ico_path = os.path.join(ASSETS_DIR, "favicon.ico")

def initialize_assets():
    if os.path.exists(ico_path):
        return

    try:
        if not os.path.exists(ASSETS_DIR):
            os.makedirs(ASSETS_DIR)

        if os.path.exists(png_path):
            img = Image.open(png_path)
            icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
            img.save(ico_path, sizes=icon_sizes)
            print("Icon generated successfully.")
    except Exception as e:
        print(f"An error occurred while creating the icon: {e}")

class AppColors:
    PRIMARY = "#1C274C"
    SECONDARY = "#8d93a5"
    SUCCESS = "#4CAF50"
    WARNING = "#FFC107"
    DANGER = "#EF5350"
    TEXT_MAIN = "#FFFFFF"
    TEXT_MUTED = "#AAAAAA"

class AppImages:
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))
    ASSETS_PATH = os.path.join(BASE_PATH, "assets")

    LOGO_LIGHT_PATH = os.path.join(ASSETS_PATH, "logo.png")
    LOGO_DARK_PATH = os.path.join(ASSETS_PATH, "logo_dark.png")
    DAY_LIGHT_PATH = os.path.join(ASSETS_PATH, "day.png")
    DAY_DARK_PATH = os.path.join(ASSETS_PATH, "day_dark.png")
    NIGHT_LIGHT_PATH = os.path.join(ASSETS_PATH, "night.png")
    NIGHT_DARK_PATH = os.path.join(ASSETS_PATH, "night_dark.png")
    ICON_PATH = os.path.join(ASSETS_PATH, "icon.png")
    FAVICON_PATH = os.path.join(ASSETS_PATH, "favicon.ico")

    @classmethod
    def get_logo(cls, width=220, height=40):
        light_img = dark_img = None
        if os.path.exists(cls.LOGO_LIGHT_PATH):
            light_img = Image.open(cls.LOGO_LIGHT_PATH)
        if os.path.exists(cls.LOGO_DARK_PATH):
            dark_img = Image.open(cls.LOGO_DARK_PATH)
        else:
            dark_img = light_img

        if light_img:
            return ctk.CTkImage(light_image=light_img, dark_image=dark_img, size=(width, height))
        return None

    @classmethod
    def get_theme_icons(cls):
        day_img = night_img = None
        if os.path.exists(cls.DAY_ICON_PATH):
            img = Image.open(cls.DAY_ICON_PATH)
            day_img = ctk.CTkImage(light_image=img, dark_image=img, size=(20, 20))
        if os.path.exists(cls.NIGHT_ICON_PATH):
            img = Image.open(cls.NIGHT_ICON_PATH)
            night_img = ctk.CTkImage(light_image=img, dark_image=img, size=(20, 20))
        return day_img, night_img

    @classmethod
    def get_theme_icons(cls):
        day_img = night_img = None

        if os.path.exists(cls.DAY_LIGHT_PATH):
            l_day = Image.open(cls.DAY_LIGHT_PATH)
            d_day = Image.open(cls.DAY_DARK_PATH) if os.path.exists(cls.DAY_DARK_PATH) else l_day
            day_img = ctk.CTkImage(light_image=l_day, dark_image=d_day, size=(20, 20))

        if os.path.exists(cls.NIGHT_LIGHT_PATH):
            l_night = Image.open(cls.NIGHT_LIGHT_PATH)
            d_night = Image.open(cls.NIGHT_DARK_PATH) if os.path.exists(cls.NIGHT_DARK_PATH) else l_night
            night_img = ctk.CTkImage(light_image=l_night, dark_image=d_night, size=(20, 20))

        return day_img, night_img

class AppConfig:
    TITLE = "SleepMetrics"


