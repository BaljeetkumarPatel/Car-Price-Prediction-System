# 🚗 Car Price Prediction System

![Python](https://img.shields.io/badge/Python-3.8+-3776ab?style=flat-square&logo=python)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37726?style=flat-square&logo=jupyter)
![Machine Learning](https://img.shields.io/badge/ML-Scikit--Learn-F7931E?style=flat-square&logo=scikit-learn)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

> **Accurate car price prediction using machine learning algorithms**

## 📋 Overview

The **Car Price Prediction System** is an intelligent machine learning application designed to predict car prices based on various vehicle characteristics. This project leverages data analysis and predictive modeling techniques to provide accurate price estimations for used vehicles, utilizing the CarDekho dataset.

## ✨ Features

- 📊 **Data Analysis & Visualization** - Comprehensive exploratory data analysis (EDA)
- 🤖 **Multiple ML Models** - Decision Tree, Linear Regression, and other algorithms
- 🎯 **High Accuracy** - Optimized models for precise price predictions
- 🌐 **Web Interface** - User-friendly Flask-based web application
- 📈 **Interactive Predictions** - Real-time car price estimation
- 📑 **Jupyter Notebooks** - Detailed analysis and model training documentation

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.8+ |
| **Notebooks** | Jupyter Notebook |
| **ML Framework** | Scikit-Learn |
| **Web Framework** | Flask |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Matplotlib, Seaborn |
| **Frontend** | HTML5, CSS3, JavaScript |

## 📁 Project Structure

```
Car-Price-Prediction-System/
├── DecisionTreeReg.ipynb          # Decision Tree model training & analysis
├── app.py                          # Flask web application
├── cardekho_data.csv               # CarDekho dataset
├── cardekho_model                  # Trained model file
├── requirements.txt                # Project dependencies
├── static/                         # Static assets (CSS, JS, images)
├── templates/                      # HTML templates
└── README.md                       # Project documentation
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/BaljeetkumarPatel/Car-Price-Prediction-System.git
   cd Car-Price-Prediction-System
   ```

2. **Create a virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

#### Option 1: Web Application
```bash
python app.py
```
The application will start at `http://localhost:5000` in your browser.

#### Option 2: Jupyter Notebook Analysis
```bash
jupyter notebook DecisionTreeReg.ipynb
```

## 📊 Dataset

The project uses the **CarDekho Dataset** containing:
- **Records**: Vehicle pricing and specifications data
- **Features**: Brand, model, year, mileage, fuel type, transmission, etc.
- **Target**: Car price

## 🧠 Machine Learning Models

### Decision Tree Regressor
- Hierarchical decision-making for price prediction
- Excellent for capturing non-linear relationships
- Interpretable model structure

### Linear Regression
- Traditional baseline model
- Fast training and prediction
- Good for initial analysis

## 📈 Model Performance

The models are trained and evaluated using:
- **R² Score** - Coefficient of determination
- **Mean Squared Error (MSE)** - Prediction accuracy measure
- **Mean Absolute Error (MAE)** - Average prediction deviation

## 💻 Usage Examples

### Web Interface
1. Open the web application in your browser
2. Input vehicle specifications (brand, year, mileage, etc.)
3. Click "Predict" to get the estimated car price
4. View detailed predictions and recommendations

### Programmatic Usage
```python
import pickle
import pandas as pd

# Load the trained model
with open('cardekho_model', 'rb') as f:
    model = pickle.load(f)

# Prepare your data
car_features = pd.DataFrame({
    'feature1': [value1],
    'feature2': [value2],
    # ... add other features
})

# Make prediction
predicted_price = model.predict(car_features)
print(f"Predicted Price: ${predicted_price[0]:,.2f}")
```

## 📝 Project Workflow

1. **Data Exploration** - Analyze dataset structure and distributions
2. **Data Cleaning** - Handle missing values and outliers
3. **Feature Engineering** - Create and select relevant features
4. **Model Training** - Train multiple regression models
5. **Model Evaluation** - Compare performance metrics
6. **Deployment** - Deploy via Flask web application

## 🔍 Key Insights

- Vehicle age significantly impacts price
- Brand reputation affects market value
- Mileage is a crucial price determinant
- Transmission type influences valuation

## 📋 Requirements

See `requirements.txt` for complete dependency list:
- pandas
- numpy
- scikit-learn
- flask
- matplotlib
- seaborn

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License. See LICENSE file for details.

## 👨‍💻 Author

**Baljeet Kumar Patel**
- GitHub: [@BaljeetkumarPatel](https://github.com/BaljeetkumarPatel)

## 🙋 Support & Feedback

Have questions or suggestions? Feel free to:
- Open an issue on GitHub
- Submit a pull request
- Contact the maintainer

## 📚 Resources

- [Scikit-Learn Documentation](https://scikit-learn.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Pandas Guide](https://pandas.pydata.org/)
- [Machine Learning Basics](https://en.wikipedia.org/wiki/Machine_learning)

---

**Made with ❤️ by Baljeet Kumar Patel**

*Last Updated: 2026-05-26*
