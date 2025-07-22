## Cat Dog Classifier 
This is a full-stack web-based image classifier that can identify if an uploaded image contains a cat or a dog. It leverages a Python Flask backend for the machine learning model inference (powered by TensorFlow/Keras and MobileNetV2), and a simple HTML/CSS/JavaScript frontend for the user interface.

## 🚀 Features
Image Upload: Easily upload an image from your local device.

Client-Server Architecture: Frontend handles UI, while the Python backend performs the heavy lifting of ML inference.

Real-time Classification: Get predictions quickly after uploading an image.

Confidence Score: Displays the predicted class (e.g., "tabby cat", "golden retriever") along with a confidence percentage.

Pre-trained Model: Uses the MobileNetV2 model, pre-trained on the ImageNet dataset, for robust image recognition.
 

## 🛠️ Technologies Used
Python 3.x: The core language for the backend logic.

Flask: A lightweight and flexible web framework for building the backend API.

TensorFlow / Keras: Powerful libraries for machine learning, used here to load and run the MobileNetV2 model.

MobileNetV2: A highly efficient pre-trained convolutional neural network (CNN) for image classification.

Pillow (PIL): Python Imaging Library, used for image processing (resizing, format conversion) on the backend.

NumPy: Essential for numerical operations, especially with image data arrays.

Flask-CORS: A Flask extension to handle Cross-Origin Resource Sharing, allowing the frontend to make requests to the backend.

HTML5, CSS3, JavaScript: For building the interactive and responsive frontend user interface.

Tailwind CSS (via CDN): A utility-first CSS framework used for rapid styling.



 ## Run the Flask Backend

python app.py
