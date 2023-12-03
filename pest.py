import os
import pickle
import base64
import io
from PIL import Image
import numpy as np
from flask import Flask, request, render_template
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import save_model, load_model

class Pest(object):
    def __init__(self):
        self.APP_ROOT = os.path.dirname(os.path.abspath(__file__))
        self.model = None
        self.label_encoder = None

    
    def Upload(self):
        target = os.path.join(self.APP_ROOT, 'uploads')

        if not os.path.isdir(target):
            os.mkdir(target)
        
        print(request.files.getlist("file"))

        for file in request.files.getlist("file"):
            filename = file.filename
            destination = "/".join([target, filename])
            file.save(destination)
        
        
        default_image_size = tuple((256, 256))

        with open('uploads/' + filename, 'rb') as fid:
            data = fid.read()


        b64_bytes = base64.b64encode(data)
        b64_string = b64_bytes.decode()

        try:
            image = Image.open(io.BytesIO(base64.b64decode(b64_string)))
            if image is not None :
                image = image.resize(default_image_size, Image.ANTIALIAS)   
                image_array = img_to_array(image)
                return np.expand_dims(image_array, axis=0),filename,destination
            else:
                print("Error loading image file")
        except Exception as e:
            print(str(e))

    def process_images(self, root_folder):
        image_data = []
        labels = []
        label = []

        for class_idx, class_folder in enumerate(os.listdir(root_folder)):
            class_path = os.path.join(root_folder, class_folder)
            if os.path.isdir(class_path):
                # Check if the class name is already in labels
                if class_folder not in labels:
                    labels.append(class_folder)

                print(f"Processing images for class: {class_folder}")

                for filename in os.listdir(class_path):
                    if filename.endswith('.JPG'):
                        file_path = os.path.join(class_path, filename)
                        print(f"File: {file_path}, Label: {class_folder}")
                        img = load_img(file_path, target_size=(256, 256))
                        img_array = img_to_array(img)
                        image_data.append(img_array)
                        label.append(class_folder)

        # print(label)
        # print(labels)
        label_encoder = LabelEncoder()
        encoded_label = label_encoder.fit_transform(label)
        # Save label_encoder to use during prediction
        self.label_encoder = label_encoder
        self.save_to_pickle(self.label_encoder, 'label_encoder.pkl')

        return np.array(image_data), np.array(encoded_label), self.label_encoder, len(labels)

    def save_to_pickle(self, data, output_path):
        with open(output_path, 'wb') as f:
            pickle.dump(data, f)

    def train_and_save_model(self, image_data, label, label_less):
        # Normalize the image data
        image_data = image_data / 255.0

        # Build a simple neural network
        model = Sequential()
        model.add(Flatten(input_shape=(256, 256, 3)))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(label_less, activation='softmax'))  # Adjust the output layer based on the number of classes
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

        # Train the model
        model.fit(image_data, label, epochs=5)

        # Save the trained model
        save_model(model, "your_model.h5")

        self.model = model

    def predict_image(self, image_path):
        # Load and preprocess the image
        image = load_img(image_path, target_size=(256, 256))
        image_array = img_to_array(image)
        image_array = image_array / 255.0  # Normalize the image
        image_array = image_array.reshape(1, 256, 256, 3)

        # Perform prediction
        prediction = self.model.predict(image_array)

        # Decode the prediction using label_encoder
        predicted_class_index = np.argmax(prediction)
        decoded_prediction = self.label_encoder.inverse_transform([predicted_class_index])[0]

        return decoded_prediction, prediction[0, predicted_class_index]

if __name__ == "__main__":
    pest = Pest()

    # Example usage
    dataset_folder = 'E:\Sem 7\Last Year Project\Project\dataset\PlantVillage'
    output_pickle_path = 'E:\Sem 7\Last Year Project\Project\dataset\model.pkl'

    image_data, labels, _, label_less = pest.process_images(dataset_folder)
    pest.train_and_save_model(image_data, labels, label_less)

    # Now pest object has the trained model and label_encoder
    # You can use pest.predict_image(image_path) for predictions

