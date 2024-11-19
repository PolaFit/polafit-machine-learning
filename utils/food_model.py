import os
import numpy as np
import tensorflow as tf
import csv
import json

MODEL_PATH = 'models/food_model.h5'
FOOD_NUTRITION_CSV = 'food_nutrition.csv'

def load_food_model():
    model = tf.keras.models.load_model(MODEL_PATH)
    return model

def predict_food(image_path):
    model = load_food_model()
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(160, 160))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0 

    prediction = model.predict(img_array)
    predicted_class = np.argmax(prediction, axis=1)[0]

    nutrition_json = get_nutrition(predicted_class)
    return nutrition_json

def get_nutrition(predicted_class):
    with open(FOOD_NUTRITION_CSV, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if int(row['ID']) == predicted_class:
                nutrition_info = {
                    "ID": int(row['ID']),
                    "Makanan": row['Makanan'],
                    "Berat per Serving (g)": row['Berat per Serving (g)'],
                    "Kalori (kcal)": row['Kalori (kcal)'],
                    "Protein (g)": row['Protein (g)'],
                    "Lemak (g)": row['Lemak (g)'],
                    "Karbohidrat (g)": row['Karbohidrat (g)'],
                    "Serat (g)": row['Serat (g)'],
                    "Gula (g)": row['Gula (g)']
                }
                return nutrition_info
    return json.dumps({"error": "Nutrition information not found for the predicted class."})

