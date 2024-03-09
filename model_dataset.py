import os
import pickle
from PIL import Image
import numpy as np
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import save_model
from tensorflow.keras.models import load_model

def process_images(root_folder):
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
    save_to_pickle(label_encoder, 'label_encoder.pkl')

    return np.array(image_data), np.array(encoded_label), label_encoder,len(labels)



def save_to_pickle(data, output_path):
    with open(output_path, 'wb') as f:
        pickle.dump(data, f)

def train_and_save_model(image_data, label, label_less):
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

if __name__ == "__main__":
    # Example usage
    dataset_folder = 'E:\Sem 7\Last Year Project\Project\dataset\PlantVillage'
    output_pickle_path = 'E:\Sem 7\Last Year Project\Project\dataset\model.pkl'

    image_data, labels, label_encoder, label_less = process_images(dataset_folder)
    save_to_pickle((image_data, labels, label_encoder), output_pickle_path)

    train_and_save_model(image_data, labels, label_less)

    # Load the model and label encoder during prediction
    model = load_model("your_model.h5")
    label_encoder = pickle.load(open('label_encoder.pkl', 'rb'))

    # Example: Load an image for prediction
    # Adjust the path as needed
    image_path = r'E:\Sem 7\Last Year Project\Project\dataset\PlantVillage\Potato_Late_blight\0c2628d4-8d64-48a9-a157-19a9c902e304___RS_LB 4590.JPG'
    image = load_img(image_path, target_size=(256, 256))
    image_array = img_to_array(image)
    image_array = image_array / 255.0  # Normalize the image

    # Reshape for prediction
    image_array = image_array.reshape(1, 256, 256, 3)

    # Perform prediction
    prediction = model.predict(image_array)

    # Decode the prediction using label_encoder
    predicted_class_index = np.argmax(prediction)
    decoded_prediction = label_encoder.inverse_transform([predicted_class_index])[0]

    # Print the predicted class and probability
    print("Predicted Class:", decoded_prediction)
    print("Predicted Probability:", prediction[0, predicted_class_index])