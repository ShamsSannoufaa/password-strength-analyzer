# 🔐 Password Strength Analyzer (Machine Learning)

This project analyzes password strength using machine learning techniques.  
It classifies passwords into **weak, medium, and strong** categories and suggests stronger alternatives.

---

## 🚀 Features

- Password strength classification (Weak / Medium / Strong)
- Feature-based analysis (length, character types, entropy)
- Improved labeling strategy (V1 vs V2 comparison)
- Password suggestion system
- Interactive web interface (Streamlit)

---

## 🧠 Models

Two versions of the model were developed:

- **V1** → Initial rule-based labeling  
- **V2** → Improved labeling (penalizes low diversity)

---

## 📂 Project Structure

password_project/
│
├── src/
├── main.py
├── predict.py
├── suggest.py
├── app.py
├── requirements.txt
├── README.md
└── .gitignore

## ⚠️ Dataset

Datasets are **not included** due to size limitations.

You can download them from:

- RockYou password dataset
- Kaggle strong password dataset

After downloading, place them inside a `data/` folder:
data/
├── rockyou.txt
├── strong_passwords.txt


---

## ⚙️ Installation

Install required libraries:

```bash
pip install -r requirements.txt
🏋️ Train Model

To train the model:

python main.py

This will generate trained model files (.pkl).

🔍 Run Prediction
python predict.py
🌐 Run Web Interface
streamlit run app.py
📊 Example
Input: pestisist
Output: Weak
📌 Notes
Model files (.pkl) are not included
Datasets are not included
These must be generated or downloaded locally
📚 Technologies Used
Python
Pandas / NumPy
Scikit-learn
Streamlit
👥 Authors
Sueda Ünal
Shams Sannoufa