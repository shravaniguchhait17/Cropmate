import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from pykrige.ok import OrdinaryKriging
import pandas as pd
from sklearn.cluster import KMeans

class Fertilizer:
    def __init__(self,csv_file):
        # Load your data and preprocess it here
        self.data = pd.read_csv(csv_file)  # Replace with your actual dataset file

        # Preprocess data
        self.preprocess_data()

    def preprocess_data(self):
        # Your preprocessing logic here
        # Example: Handling missing values and scaling numeric features
        numeric_features = ["Nitrogen", "Phosphorus", "Potassium", "pH", "Rainfall", "Temperature"]
        categorical_features = ["District_Name", "Soil_color", "Crop"]

        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='mean')),
            ('scaler', StandardScaler())
        ])

        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent'))
        ])

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)
            ])

        # Apply the preprocessing steps to the data
        self.data = preprocessor.fit_transform(self.data)

    def predict_fertilizer(self, district_name, crop):
        # Filter data for the given district and crop
        district_column_index = -3
        crop_column_index = -1
        input_data = self.data[(self.data[:, district_column_index] == district_name) & (self.data[:, crop_column_index] == crop)]

        # Check if input_data is not empty before applying KMeans
        if input_data.shape[0] == 0:
            print(f"No samples available for clustering in {district_name}, {crop}.")
            return ["Urea", "DAP", "Potash"," Superphosphate","19:19:19 NPK"]
    
        # Clustering
        kmeans = KMeans(n_clusters=3, random_state=42)
        input_data[:, -5] = kmeans.fit_predict(input_data[:, [0, 1]])


        # Kriging
        ok = OrdinaryKriging(input_data[:, 0], input_data[:, 1], input_data[:, 2], variogram_model='linear')
        
        rounded_nitrogen = np.round(input_data[:, 0].astype(float), 2)
        rounded_phosphorus = np.round(input_data[:, 1].astype(float), 2)
        probabilities = ok.execute('points', rounded_nitrogen, rounded_phosphorus)[0]

        # Combine fertilizers with their probabilities into a list of tuples
        fertilizers_with_probabilities = list(zip(
            ['Urea', 'DAP', 'MOP', '10:26:26 NPK', 'SSP', 'Magnesium Sulphate', '13:32:26 NPK',
            '12:32:16 NPK', '50:26:26 NPK', '19:19:19 NPK', 'Chilated Micronutrient', 'SSP',
            '18:46:00 NPK', 'Sulphur', 'Ammonium Sulphate', 'Ferrous Sulphate', 'White potash',
            '10:10:10 NPK', 'Hydrated Lime'],
            probabilities
        ))

        # Sort the list of tuples by probability in descending order
        sorted_fertilizers = sorted(fertilizers_with_probabilities, key=lambda x: x[1], reverse=True)

        # Limit the display to the top 5 fertilizers
        top_5_fertilizers = [fertilizer for fertilizer, _ in sorted_fertilizers[:5]]

        return top_5_fertilizers


