from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import save_model
import numpy as np

# Create a simple example dataset
X_train = np.random.rand(100, 256, 256, 3)  # Replace with your actual training data
y_train = np.random.randint(2, size=(100,))

# Build and compile a simple model
model = Sequential()
model.add(Dense(64, input_shape=(256, 256, 3), activation='relu'))
model.add(Dense(1, activation='sigmoid'))
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=5)

# Save the trained model
save_model(model, "your_model.h5")