import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import pandas as pd
from tensorflow.keras.models import load_model
from PIL import Image
import matplotlib.pyplot as plt

model = load_model('resnet_attention_model.h5', compile=False)


def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(256, 256))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    return img_array



def predict_on_images(image_dir):
    predictions = []
    image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if not image_files:
        print(f"No images found in the directory: {image_dir}")
        return

    for img_file in image_files:
        img_path = os.path.join(image_dir, img_file)
        processed_img = preprocess_image(img_path)

        prediction = model.predict(processed_img)
        predicted_class = np.argmax(prediction, axis=1)[0]
        confidence_scores = prediction[0]

        predictions.append({
            "Image": img_file,
            "Predicted Class": predicted_class,
            "Confidence Scores": confidence_scores
        })
        print(f"Image: {img_file}")
        print(f"Predicted Class: {predicted_class}")
        print(f"Confidence Scores: {confidence_scores}\n")

    predictions_df = pd.DataFrame(predictions)
    return predictions_df


if __name__ == '__main__':
    new_image_dir = 'new_images'

    predictions_df = predict_on_images(new_image_dir)
    if predictions_df is not None:
        predictions_df.to_csv("predictions.csv", index=False)
        print("Predictions saved to predictions.csv")
