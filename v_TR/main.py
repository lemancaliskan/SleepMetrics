import customtkinter as ctk
from ui_components import *
import os
import sys
import ctypes
import warnings

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if base_path not in sys.path:
    sys.path.append(base_path)

from assets_manager import AppImages, initialize_assets, AppColors, AppConfig
from engine import SleepEngine

warnings.filterwarnings("ignore", category=UserWarning)

try:
    myappid = 'sleepmetrics'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except:
    pass

def resource_path(relative_path):
    import sys, os
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    return os.path.join(base_path, relative_path)

os.chdir(base_path)
initialize_assets()

class SleepApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.engine = SleepEngine()

        ctk.set_appearance_mode("light")
        self.title(AppConfig.TITLE)

        try:
            self.iconbitmap("assets/favicon.ico")
        except Exception as e:
            try:
                import os
                abs_path = os.path.abspath("assets/favicon.ico")
                self.iconbitmap(abs_path)
            except:
                print(f"İkon yüklenemedi: {e}")

        self.app_w = 980
        self.app_h = 666
        self.set_top_center()

        self.after(100, self.lift)
        self.setup_ui()

    def set_top_center(self):
        screen_width = self.winfo_screenwidth()
        x = (screen_width // 2) - (self.app_w // 2)
        y = 20
        self.geometry(f"{self.app_w}x{self.app_h}+{int(x)}+{int(y)}")

    def setup_ui(self):
        self.sidebar = ctk.CTkFrame(self, width=400, corner_radius=0, fg_color=("#f2f2f2", "#1e1e1e"))
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        logo_img = AppImages.get_logo(width=300, height=36)
        if logo_img:
            ctk.CTkLabel(self.sidebar, text="", image=logo_img).pack(pady=(25, 15))
        else:
            ctk.CTkLabel(self.sidebar, text="🌙 SLEEPMETRICS AI",
                         font=ctk.CTkFont(size=22, weight="bold"),
                         text_color=AppColors.PRIMARY).pack(pady=(25, 15))

        self.form_container = ctk.CTkScrollableFrame(self.sidebar, fg_color="transparent")
        self.form_container.pack(fill="both", expand=True, padx=15, pady=5)
        self.form_container.grid_columnconfigure((0, 1), weight=1)

        self.inputs = {}
        self.setup_form()

        self.bottom_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.bottom_frame.pack(side="bottom", fill="x", pady=20, padx=25)

        self.btn_analyze = ctk.CTkButton(self.bottom_frame, text="UYKU ANALİZİNİ BAŞLAT",
                                         command=self.run_analysis,
                                         fg_color=AppColors.PRIMARY, hover_color=AppColors.SECONDARY,
                                         height=50, font=ctk.CTkFont(size=14, weight="bold"),
                                         corner_radius=12)
        self.btn_analyze.pack(fill="x")

        self.theme_frame = ctk.CTkFrame(self.bottom_frame, fg_color="transparent")
        self.theme_frame.pack(fill="x", pady=(15, 0))
        day_icon, night_icon = AppImages.get_theme_icons()

        if night_icon and day_icon:
            ctk.CTkButton(self.theme_frame, text="", image=night_icon, width=35, fg_color="transparent",
                          command=lambda: [ctk.set_appearance_mode("dark"),
                                           self.gauge.draw_gauge(self.gauge.current_value)]).pack(side="right")
            ctk.CTkButton(self.theme_frame, text="", image=day_icon, width=35, fg_color="transparent",
                          command=lambda: [ctk.set_appearance_mode("light"),
                                           self.gauge.draw_gauge(self.gauge.current_value)]).pack(side="right")

        self.dashboard = ctk.CTkFrame(self, fg_color="transparent")
        self.dashboard.pack(side="right", fill="both", expand=True, padx=25, pady=20)

        self.res_frame = ctk.CTkFrame(self.dashboard, fg_color=("white", "#2b2b2b"), corner_radius=15)
        self.res_frame.pack(fill="x", pady=10)

        self.gauge = SemiCircleGauge(self.res_frame)
        self.gauge.pack(pady=20)

        self.info_card = ctk.CTkFrame(self.dashboard, fg_color=("white", "#2b2b2b"), corner_radius=15)
        self.info_card.pack(fill="both", expand=True, pady=10)

        self.prediction_label = ctk.CTkLabel(self.info_card, text="Analiz İçin Verileri Girin...",
                                             font=ctk.CTkFont(size=18, weight="bold"),
                                             text_color=(AppColors.PRIMARY, AppColors.SECONDARY))
        self.prediction_label.pack(expand=True)

        self.rec_ui = RecommendationBox(self.dashboard)
        self.rec_ui.pack(fill="both", expand=True, pady=5)

        MedicalDisclaimer(self.dashboard).pack(side="bottom", fill="x", pady=10)

    def setup_form(self):
        fields = [
            ("Cinsiyet", "Erkek", "Gender", ["Kadın", "Erkek"]),
            ("Yaş", 30, "Age", None),
            ("Boy (cm)", 175, "Height", None),
            ("Kilo (kg)", 75, "Weight", None),
            ("Uyku Süresi", 7.5, "Duration", None),
            ("Fiziksel Aktivite (dk)", 60, "Activity", None),
            ("Sistolik Kan Basıncı", 120, "Systolic", None),
            ("Diastolik Kan Basıncı", 80, "Diastolic", None),
            ("Kalp Atış Hızı", 70, "HR", None),
            ("Stres Seviyesi (1-10)", 5, "Stress", None),
            ("Günlük Adım Sayısı", 8000, "Steps", None)
        ]

        for i, (label, default, key, options) in enumerate(fields):
            row, col = i // 2, i % 2
            inp = StyledInput(self.form_container, label, default, options)
            inp.grid(row=row, column=col, padx=8, pady=10, sticky="ew")
            self.inputs[key] = inp

    def calculate_bmi_category(self, height_cm, weight_kg):
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)

        return round(bmi, 2)

    def run_analysis(self):
        try:
            def get_safe_val(key, default_type, default_val):
                val = self.inputs[key].input_field.get().strip()
                if not val:
                    return default_type(default_val)
                return default_type(val)

            gender_val = 0 if "Kadın" in self.inputs["Gender"].input_field.get() else 1

            age = get_safe_val("Age", int, 30)
            duration = get_safe_val("Duration", float, 7.5)
            activity = get_safe_val("Activity", int, 60)
            stress = get_safe_val("Stress", int, 5)
            sys_bp = get_safe_val("Systolic", int, 120)
            dia_bp = get_safe_val("Diastolic", int, 80)
            hr = get_safe_val("HR", int, 70)
            steps = get_safe_val("Steps", int, 8000)
            h = get_safe_val("Height", float, 175)
            w = get_safe_val("Weight", float, 75)

            bmi_val = self.calculate_bmi_category(h, w)
            input_features = [gender_val, age, duration, activity, stress, bmi_val, sys_bp, dia_bp, hr, steps]

            quality, disorder = self.engine.predict(input_features, lang="tr")

            self.gauge.draw_gauge(quality)
            is_healthy = "Sağlıklı" in disorder

            self.prediction_label.configure(
                text=f"Tahmini Uyku Kalitesi: {quality}\n {disorder.upper()}",
                text_color=AppColors.SUCCESS if is_healthy else AppColors.DANGER
            )
            self.rec_ui.update_recommendations(quality, disorder, stress, activity, duration, hr, sys_bp, steps)

        except Exception as e:
            print(f"Hata: {e}")
            self.prediction_label.configure(text=f"Lütfen değerleri kontrol edin!\n({e})", text_color=AppColors.DANGER)

if __name__ == "__main__":
    app = SleepApp()
    app.mainloop()