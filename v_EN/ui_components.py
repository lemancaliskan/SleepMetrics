import customtkinter as ctk
from assets_manager import AppColors

class StyledInput(ctk.CTkFrame):
    def __init__(self, master, label_text, default_value=None, options=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.label = ctk.CTkLabel(self, text=label_text, font=ctk.CTkFont(size=11, weight="bold"))
        self.label.pack(anchor="w", padx=2)

        if options:
            self.input_field = ctk.CTkComboBox(self, values=options, height=32,
                                               border_color=AppColors.PRIMARY,
                                               fg_color=("white", "#2b2b2b"))
            self.input_field.set(options[0])
        else:
            self.input_field = ctk.CTkEntry(self, height=32,
                                            border_color=AppColors.PRIMARY,
                                            placeholder_text=str(default_value),
                                            fg_color=("white", "#2b2b2b"))

        self.input_field.pack(pady=(2, 0), fill="x")

    def get_value(self):
        val = self.input_field.get().strip()

        if not val and hasattr(self.input_field, "_placeholder_text"):
            return self.input_field._placeholder_text

        return val.split(":")[0].strip() if ":" in val else val

class SemiCircleGauge(ctk.CTkCanvas):
    def __init__(self, master, width=200, height=120, **kwargs):
        is_dark = ctk.get_appearance_mode() == "Dark"
        bg_color = "#2b2b2b" if is_dark else "white"

        super().__init__(master, width=width, height=height,
                         highlightthickness=0, bg=bg_color, **kwargs)

        self.width, self.height = width, height
        self.thickness = 20
        self.current_value = 0
        self.draw_gauge(0)

    def draw_gauge(self, value):
        self.current_value = value
        self.delete("all")

        is_dark = ctk.get_appearance_mode() == "Dark"
        bg_color = "#2b2b2b" if is_dark else "white"
        base_circle_color = "#3d3d3d" if is_dark else "#e0e0e0"
        text_primary = "white" if is_dark else "black"

        self.configure(bg=bg_color)

        cx, cy, r = self.width / 2, self.height - 15, (self.width / 2) - self.thickness

        self.create_arc(cx - r, cy - r, cx + r, cy + r, start=0, extent=180,
                        style="arc", width=self.thickness, outline=base_circle_color)

        gauge_color = AppColors.SUCCESS if value >= 8 else (AppColors.WARNING if value >= 5 else AppColors.DANGER)

        if value > 0:
            self.create_arc(cx - r, cy - r, cx + r, cy + r, start=180,
                            extent=-(value / 10 * 180), style="arc",
                            width=self.thickness, outline=gauge_color)

        self.create_text(cx, cy - r / 2.2, text=f"{value}",
                         font=("Arial", 32, "bold"), fill=text_primary)

        self.create_text(cx, cy - 8, text="Sleep Quality (0/10)",
                         font=("Arial", 10, "bold"), fill="#888888")

    def _set_appearance_mode(self, mode_string):
        super()._set_appearance_mode(mode_string)
        self.after(200, lambda: self.draw_gauge(self.current_value))

class RecommendationCard(ctk.CTkFrame):
    def __init__(self, master, title, text, icon, color, **kwargs):
        super().__init__(master, corner_radius=8, border_width=1, border_color=color, fg_color="transparent", **kwargs)
        ctk.CTkLabel(self, text=icon, font=ctk.CTkFont(size=18), text_color=color).pack(side="left", padx=10)
        f = ctk.CTkFrame(self, fg_color="transparent")
        f.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        ctk.CTkLabel(f, text=title, font=ctk.CTkFont(size=11, weight="bold"), text_color=color).pack(anchor="w")
        ctk.CTkLabel(f, text=text, font=ctk.CTkFont(size=10), wraplength=200, justify="left").pack(anchor="w")

class RecommendationBox(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=("white", "#2b2b2b"), corner_radius=15, **kwargs)

        ctk.CTkLabel(self, text="✨ Personalized Health Recommendations",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=(AppColors.PRIMARY, AppColors.SECONDARY)).pack(pady=(12, 8), padx=15, anchor="w")

        self.container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)

    def update_recommendations(self, quality, disorder, stress, activity, duration, hr, sys, steps):
        for widget in self.container.winfo_children():
            widget.destroy()

        recs = []

        if "Apnea" in disorder:
            recs.append(("Sleep Apnea", "Consult an ENT specialist.", "🌬️", "#ff4b4b"))
        elif "İnsomnia" in disorder:
            recs.append(("İnsomnia", "Avoid blue light exposure 2 hours before sleep.", "📱", "#3498db"))

        if stress > 7:
            recs.append(("High Stress", "Practice breathing exercises before sleep.", "🧘", "#9b59b6"))

        if duration < 6:
            recs.append(("Low Duration", "Aim for 7+ hours for body recovery.", "⏰", "#e67e22"))

        if activity < 30:
            recs.append(("Inactivity", "A daily 20-30 min walk increases deep sleep by 30%.", "👟", "#2ecc71"))

        if not recs:
            recs.append(("Excellent!", "Your sleep data looks quite healthy.", "✅", AppColors.SUCCESS))

        if hr > 100:
            recs.append(
                ("High Heart Rate", "Reduce caffeine intake and drink plenty of water.", "❤️", "#e74c3c"))

        if sys > 140:
            recs.append(("High Blood Pressure", "Limit salt intake and monitor more frequently.", "⚠️", "#ff4b4b"))

        if steps < 5000:
            recs.append(("Low Step Count", "7,500 steps a day reduces sleep onset latency by 15%.", "👣", "#3498db"))
        elif steps < 8000:
            recs.append(("Activity Goal", "Increase your goal to 10,000 steps for full recovery during sleep.", "🏃", "#f39c12"))

        for i, (title, text, icon, color) in enumerate(recs):
            row = i // 2
            col = i % 2

            card = ctk.CTkFrame(self.container,
                                fg_color=("#f8f9fa", "#343434"),
                                corner_radius=10,
                                border_width=1,
                                border_color=color,
                                height=70)
            card.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")
            card.grid_propagate(False)

            lbl_title = ctk.CTkLabel(card, text=f"{icon} {title}",
                                     font=ctk.CTkFont(size=11, weight="bold"),
                                     text_color=color)
            lbl_title.pack(anchor="w", padx=8, pady=(5, 0))

            lbl_text = ctk.CTkLabel(card, text=text,
                                    font=ctk.CTkFont(size=10),
                                    wraplength=200,
                                    justify="left")
            lbl_text.pack(anchor="w", padx=10, pady=(0, 5))

class MedicalDisclaimer(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        text_box = ctk.CTkFrame(self, fg_color=("#fff5f5", "#2d1f1f"), corner_radius=8, border_width=1,
                                border_color="#ffcccc")
        text_box.pack(fill="x", padx=10, pady=5)
        disclaimer = ("⚠️ SleepMetrics Core - Sleep Health & Risk Assessment Tool:"
                      "\nThis calculation tool is for informational purposes only and is not a substitute"
                      " for professional medical advice, diagnosis, or treatment."
                      "\nIf you have any concerns regarding your health, please consult a healthcare professional.")

        self.label = ctk.CTkLabel(text_box, text=disclaimer, font=ctk.CTkFont(size=10, slant="italic"),
                                  text_color=("#d9534f", "#ff8080"), justify="center")
        self.label.pack(pady=8, padx=12)