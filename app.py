import joblib
import numpy as np
import pandas as pd
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

MODEL_PATH = "cardekho_model"
DATA_PATH = "cardekho_data (1).csv"

model = joblib.load(MODEL_PATH)
df = pd.read_csv(DATA_PATH)

TRAIN_COLUMNS = [
    "Car_Name",
    "Year",
    "Present_Price",
    "Kms_Driven",
    "Fuel_Type",
    "Seller_Type",
    "Transmission",
    "Owner",
]

categorical_cols = ["Car_Name", "Fuel_Type", "Seller_Type", "Transmission"]
encoders = {}
for col in categorical_cols:
    encoders[col] = {name: idx for idx, name in enumerate(sorted(df[col].astype(str).unique()))}

num_stats = {
    col: {
        "min": float(df[col].min()),
        "max": float(df[col].max()),
        "median": float(df[col].median()),
        "std": float(df[col].std() if df[col].std() else 1.0),
    }
    for col in ["Year", "Present_Price", "Kms_Driven", "Owner"]
}

brand_base_price = (
    df.groupby("Car_Name")["Present_Price"].mean().to_dict()
    if "Car_Name" in df.columns
    else {}
)

fuel_bias = {"Petrol": 0.0, "Diesel": 0.25, "CNG": -0.3}
seller_bias = {"Dealer": 0.35, "Individual": -0.15}
transmission_bias = {"Manual": -0.1, "Automatic": 0.3}


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def estimate_present_price(payload):
    car_name = payload.get("car_name", "")
    year = int(payload.get("year", 2017))
    fuel_type = payload.get("fuel_type", "Petrol")
    seller_type = payload.get("seller_type", "Dealer")
    transmission = payload.get("transmission", "Manual")
    km = float(payload.get("kms_driven", 30000))
    engine = float(payload.get("engine", 1200))
    max_power = float(payload.get("max_power", 80))

    base = brand_base_price.get(car_name, float(df["Present_Price"].median()))
    age_penalty = (2026 - year) * 0.18
    km_penalty = (km / 100000.0) * 1.6

    heuristic = (
        base
        + (engine - 1200) / 1100.0
        + (max_power - 80) / 55.0
        + fuel_bias.get(fuel_type, 0)
        + seller_bias.get(seller_type, 0)
        + transmission_bias.get(transmission, 0)
        - age_penalty
        - km_penalty
    )

    return float(clamp(heuristic, num_stats["Present_Price"]["min"], num_stats["Present_Price"]["max"]))


def encode_value(col, raw):
    mapping = encoders[col]
    if raw in mapping:
        return mapping[raw]
    return int(np.median(list(mapping.values())))


def format_lakhs(value):
    return f"{value:.2f} Lakhs"


def make_explanation(year, km, fuel_type, owner, transmission):
    impacts = []
    current_year = 2026
    age = current_year - year

    if age >= 8:
        impacts.append("Older manufacturing year significantly reduces resale value")
    elif age >= 4:
        impacts.append("Moderate vehicle age slightly lowers expected market value")
    else:
        impacts.append("Relatively newer model year supports stronger market pricing")

    if km > 90000:
        impacts.append("High kilometers driven creates notable depreciation pressure")
    elif km > 45000:
        impacts.append("Average mileage creates moderate depreciation")
    else:
        impacts.append("Lower kilometers driven helps retain car value")

    if fuel_type == "Diesel":
        impacts.append("Diesel variants often keep stable highway-use demand")
    elif fuel_type == "CNG":
        impacts.append("CNG gives running-cost advantage but can limit premium resale")
    else:
        impacts.append("Petrol variants maintain broad buyer demand in city markets")

    if owner >= 2:
        impacts.append("Multiple ownership history can reduce buyer confidence")
    else:
        impacts.append("Low ownership count supports better trust and pricing")

    if transmission == "Automatic":
        impacts.append("Automatic transmission generally commands better urban resale value")
    else:
        impacts.append("Manual transmission keeps affordability but may limit premium segment")

    return impacts


def confidence_score(year, present_price, kms, owner):
    z_year = abs(year - num_stats["Year"]["median"]) / num_stats["Year"]["std"]
    z_price = abs(present_price - num_stats["Present_Price"]["median"]) / num_stats["Present_Price"]["std"]
    z_kms = abs(kms - num_stats["Kms_Driven"]["median"]) / num_stats["Kms_Driven"]["std"]
    z_owner = abs(owner - num_stats["Owner"]["median"]) / max(num_stats["Owner"]["std"], 1.0)

    z_mean = (z_year + z_price + z_kms + z_owner) / 4
    score = 95 - (z_mean * 9)
    return float(clamp(score, 62, 96))


@app.route("/")
def index():
    return render_template(
        "index.html",
        car_names=sorted(df["Car_Name"].astype(str).unique().tolist()),
        brands=sorted({name.split()[0] for name in df["Car_Name"].astype(str).tolist()}),
    )


@app.route("/predict", methods=["POST"])
def predict():
    payload = request.get_json(force=True)

    year = int(payload.get("year"))
    kms_driven = float(payload.get("kms_driven"))
    fuel_type = str(payload.get("fuel_type"))
    seller_type = str(payload.get("seller_type"))
    transmission = str(payload.get("transmission"))
    owner = int(payload.get("owner_type"))

    present_price = estimate_present_price(payload)

    features = {
        "Car_Name": encode_value("Car_Name", str(payload.get("car_name", ""))),
        "Year": year,
        "Present_Price": present_price,
        "Kms_Driven": kms_driven,
        "Fuel_Type": encode_value("Fuel_Type", fuel_type),
        "Seller_Type": encode_value("Seller_Type", seller_type),
        "Transmission": encode_value("Transmission", transmission),
        "Owner": owner,
    }

    input_df = pd.DataFrame([features], columns=TRAIN_COLUMNS)
    pred = float(model.predict(input_df)[0])
    pred = max(pred, 0.35)

    confidence = confidence_score(year, present_price, kms_driven, owner)
    explanation_points = make_explanation(year, kms_driven, fuel_type, owner, transmission)

    response = {
        "estimated_price_lakhs": round(pred, 2),
        "estimated_price_text": format_lakhs(pred),
        "confidence": round(confidence, 1),
        "present_price_proxy": round(present_price, 2),
        "analytics": {
            "car_age": int(2026 - year),
            "mileage_band": "High" if kms_driven > 90000 else "Medium" if kms_driven > 45000 else "Low",
            "owner_risk": "Elevated" if owner >= 2 else "Low",
        },
        "explanation": explanation_points,
    }
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)

