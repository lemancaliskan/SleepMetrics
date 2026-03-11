import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier
import joblib
import os

class SleepEngine:
    def __init__(self):
        self.data_dir = "data"
        self.model_dir = "model"

        if not os.path.exists(self.model_dir): os.makedirs(self.model_dir)

        self.quality_model_path = os.path.join(self.model_dir, "sleep_quality_model.pkl")
        self.disorder_model_path = os.path.join(self.model_dir, "sleep_disorder_model.pkl")

        self.quality_model = RandomForestRegressor(n_estimators=150, random_state=42)
        self.disorder_model = GradientBoostingClassifier(n_estimators=150, random_state=42)

        self.is_trained = False

        if os.path.exists(self.quality_model_path) and os.path.exists(self.disorder_model_path):
            self._load_models()
        else:
            print("Models not found or retrain requested. Initiating training process...")
            self.train_from_data_folder()

    def _load_models(self):
        try:
            self.quality_model = joblib.load(self.quality_model_path)
            self.disorder_model = joblib.load(self.disorder_model_path)
            self.is_trained = True
            print("Models initialized.")
        except:
            self.is_trained = False

    def preprocess_df(self, df):
        if 'Blood Pressure' in df.columns:
            df[['Systolic', 'Diastolic']] = df['Blood Pressure'].astype(str).str.split('/', expand=True).astype(int)

        df['Gender'] = df['Gender'].map({'Male': 1, 'Female': 0})

        bmi_map = {
            'Normal': 22.0, 'Normal Weight': 22.0,
            'Overweight': 27.5,
            'Obese': 34.0
        }
        if 'BMI Category' in df.columns:
            df['BMI Category'] = df['BMI Category'].map(bmi_map).fillna(df['BMI Category'])

        if 'Sleep Disorder' in df.columns:
            dis_map = {'None': 0, 'Sleep Apnea': 1, 'Insomnia': 2}
            df['Sleep Disorder'] = df['Sleep Disorder'].fillna('None').map(dis_map).fillna(0).astype(int)

        return df

    def train_from_data_folder(self):
        files = [
            "Sleep_health_and_lifestyle_dataset.csv",
            "Sleep_Health_and_Lifestyle.csv"
        ]

        all_dfs = []
        for f in files:
            f_path = os.path.join(self.data_dir, f)
            if os.path.exists(f_path):
                all_dfs.append(pd.read_csv(f_path))

        if not all_dfs:
            print("Error: Dataset not found.")
            return False

        combined_df = pd.concat(all_dfs, ignore_index=True).drop_duplicates()
        df = self.preprocess_df(combined_df)

        feature_names = ['Gender', 'Age', 'Sleep Duration', 'Physical Activity Level',
                         'Stress Level', 'BMI Category', 'Systolic', 'Diastolic',
                         'Heart Rate', 'Daily Steps']

        X = df[feature_names]

        from sklearn.model_selection import train_test_split

        X_train, X_test, y_q_train, y_q_test = train_test_split(X, df['Quality of Sleep'], test_size=0.2,
                                                                random_state=42)
        _, _, y_d_train, y_d_test = train_test_split(X, df['Sleep Disorder'], test_size=0.2, random_state=42)

        self.quality_model.fit(X_train, y_q_train)
        self.disorder_model.fit(X_train, y_d_train)

        q_score = self.quality_model.score(X_test, y_q_test) * 100
        d_score = self.disorder_model.score(X_test, y_d_test) * 100

        print("\n" + "=" * 49)
        print("✅ SLEEP-ENGINE MODEL TRAINING COMPLETE")
        print(f"📊 Sleep Quality Prediction Accuracy (R2): %{q_score:.2f}")
        print(f"📊 Sleep Disorder Diagnosis Accuracy: %{d_score:.2f}")
        print("=" * 49 + "\n")

        self.quality_model.fit(X, df['Quality of Sleep'])
        self.disorder_model.fit(X, df['Sleep Disorder'])

        joblib.dump(self.quality_model, self.quality_model_path)
        joblib.dump(self.disorder_model, self.disorder_model_path)

        self.is_trained = True
        return True

    def predict(self, input_data, lang="en"):
        if not self.is_trained:
            return 0.0, "Failed to train the model."

        columns = ['Gender', 'Age', 'Sleep Duration', 'Physical Activity Level',
                   'Stress Level', 'BMI Category', 'Systolic', 'Diastolic',
                   'Heart Rate', 'Daily Steps']

        df_input = pd.DataFrame([input_data], columns=columns)

        q = self.quality_model.predict(df_input)[0]
        d_idx = self.disorder_model.predict(df_input)[0]

        res_maps = {
        "tr": {0: "Sağlıklı / Belirti Yok", 1: "Uyku Apnesi Riski", 2: "İnsomnia Belirtileri"},
        "en": {0: "Healthy / Asymptomatic", 1: "Sleep Apnea Risk Detected", 2: "Insomnia Symptoms Detected"}
    }
        current_map = res_maps.get(lang, res_maps["en"])
        return round(float(q), 1), current_map.get(int(d_idx), current_map[0])

