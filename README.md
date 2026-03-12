# 🌙 SleepMetrics - Sleep Health & Lifestyle Analysis Tool

SleepMetrics is a modern desktop application designed to analyze sleep quality and predict potential sleep disorders using advanced machine learning algorithms. By processing lifestyle and clinical data through a sleek, high-DPI interface, it provides users with data-driven insights into their sleep health.

---
📺 Demo
---
### 🎨 Visual Experience
*The application features a dedicated toggle for seamless switching between light and dark modes.*
<br>*Features integrated real-time gauges for the live visualization of sleep quality scores.*

### 🔍 Desktop Application (EN/TR)
*Optimized for a 980x666 centered window layout, this standalone application delivers a precision-focused, localized experience through a theme-aware ``CustomTkinter`` UI designed for both global and local users.*

**TURKISH UI:**
<br><img width="670" height="687" alt="image" src="https://github.com/user-attachments/assets/b4598d99-01c8-4dd0-b83a-772d1a9f524a" />

**ENGLISH UI:**
<br><img width="670" alt="image" src="https://github.com/user-attachments/assets/19fbcc9b-2320-410a-8f60-b262fd0cdcd9" />


### 🌐 Web Application (Streamlit):
*A responsive and lightweight web version for instant access from any device.*
<img width="670" alt="image" src="https://github.com/user-attachments/assets/75d2692a-30ef-4331-b27b-ff47140b947d" />


---
✨ Features
---
- ***Dual Language Support:*** Optimized interfaces for both English (EN) and Turkish (TR).

- ***Modern GUI:*** A sleek design powered by ``CustomTkinter`` with native Dark and Light mode support.

- ***Smart Analysis:*** Real-time risk estimation using scikit-learn models (``Gradient Boosting`` / ``Random Forest``).

- ***Data-Driven Insights***: Analyzes metrics such as heart rate, physical activity, stress levels, and BMI to provide a holistic view.
  
- ***Medical Disclaimer System***: Dynamic recommendation engine and mandatory legal disclaimer components.

---
🧬 Technical Architecture
---
*The application is structured into three main layers:*

- **UI Components:** Custom-styled input fields, combo boxes, and dashboard elements.

- **Sleep Engine:** The core logic where ``RandomForest`` and ``Gradient Boosting`` models are managed via ``joblib``

- **Assets Manager:** Handles dynamic asset loading (icons, logos) for a consistent UI experience.

---
📊 Data Foundation
---
*The intelligence of SleepMetrics is built upon a synthesis of high-quality health and productivity data:*

- **[Sleep Health and Lifestyle Dataset](https://www.kaggle.com/datasets/uom190346a/sleep-health-and-lifestyle-dataset)** : Provides the core clinical metrics including sleep duration, quality, and disorder labels.

- **[Sleep Health and Lifestyle](https://www.kaggle.com/datasets/adilshamim8/sleep-cycle-and-productivity)** : Provides the core clinical metrics including sleep duration, quality, and disorder labels.

<br>*The data was pre-processed through a custom pipeline to normalize biometric features and handle categorical variables, ensuring the models remain robust across diverse user profiles.*

---
⚙️ Backend Engine
---
The analytical core utilizes two specialized machine learning models trained on the "Sleep Health and Lifestyle" dataset:

<img width="410" height="110" alt="image" src="https://github.com/user-attachments/assets/ef153bc0-0191-4765-ae42-9bb2e1aa5e46" />


- **Quality Model:** ``RandomForestRegressor`` (150 estimators) for precise quality scoring.

- **Diagnosis Model:** ``GradientBoostingClassifier`` (150 estimators) for categorical disorder identification.

- **Performance**: The models have been rigorously validated through the ``SleepEngine`` training pipeline:

  - Sleep Quality Prediction Accuracy (R2): **99.08%**

  - Sleep Disorder Diagnosis Accuracy: **88.00%**

---
🚀 Live Demo (Web Version)
---
You can now try the application directly in your browser without any installation:
Go to the **[SleepMetrics Streamlit App](https://sleepmetrics.streamlit.app)**

---
🛠️ Installation & Usage
---

- ***Cloud Version (Recommended for quick use)***
  <br>Access the web application instantly: **[SleepMetrics Streamlit App](https://sleepmetrics.streamlit.app)**
  
- ***Standalone Executable***
<br>To run the app without installing Python:

    - Go to the **[Releases Page](https://github.com/lemancaliskan/SleepMetrics/releases/tag/v1.0)**
    - Download the .exe file for your preferred language (SleepMetrics_EN.exe or SleepMetrics_TR.exe)
    - Ensure the ``data/`` folder containing the ``.csv`` files is in the same directory.
    - Double-click to run

- ***For Developers (Source Code)***
<br>If you want to run the project locally or contribute:

```bash
# Clone the repository
git clone https://github.com/lemancaliskan/SleepMetrics.git

# --- For Desktop (CustomTkinter) ---
pip install -r requirements-wapp.txt

# To run the Turkish version:
cd v_TR
python main.py

# To run the English version:
cd v_EN
python main.py

# --- For Web (Streamlit) ---
# (Back to root directory)
pip install -r requirements.txt
streamlit run web_app.py
```

---
Project Structure
---

```bash
SleepMetrics/
├── assets/             # App icons and logos
├── data/               # CSV datasets
├── model/              # Trained .pkl files
├── v_EN/               # English Version
│   ├── main.py
│   └── ui_components.py
├── v_TR/               # Turkish Version
│   ├── main.py
│   └── ui_components.py
├── engine.py           # Core ML Logic
└── assets_manager.py   # Asset & Color Management
├── requirements.txt      # Web/General requirements
└── requirements-wapp.txt # Desktop App specific requirements
```

---
🤝 Contributing
---
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

```bash
# Fork the Project

# Create your Feature Branch 
(git checkout -b feature/AmazingFeature)

# Commit your Changes 
(git commit -m 'Add some AmazingFeature')

# Push to the Branch 
(git push origin feature/AmazingFeature)

# Open a Pull Request
```

---
