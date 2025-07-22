import os
from flask import Flask, request, jsonify, render_template
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
import numpy as np
import base64
from io import BytesIO
from PIL import Image
from flask_cors import CORS 
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app) 


IMG_SIZE = (224, 224)


print("Loading MobileNetV2 model...")
try:
    model = MobileNetV2(weights='imagenet')
    print("MobileNetV2 model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None 

@app.route('/')
def index():
    """
    Renders the main HTML page for the classifier.
    """
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def classify_image():
    """
    API endpoint to classify an uploaded image.
    Expects a JSON payload with 'image' field containing base64 encoded image data.
    """
    if model is None:
        return jsonify({"error": "Model not loaded on the server. Please check server logs for errors during startup."}), 500

    if not request.json or 'image' not in request.json:
        return jsonify({"error": "No image data provided in the request body."}), 400

    try:
        
        image_data_b64 = request.json['image']
       
        if ',' in image_data_b64:
            image_data_b64 = image_data_b64.split(',')[1]

        image_bytes = base64.b64decode(image_data_b64) 
        
        img = Image.open(BytesIO(image_bytes))
        img = img.resize(IMG_SIZE)
        

        if img.mode != 'RGB':
            img = img.convert('RGB')
        img_array = image.img_to_array(img)
        
        
        img_array = np.expand_dims(img_array, axis=0)
        
        img_array = preprocess_input(img_array)

        
        predictions = model.predict(img_array)
        decoded_predictions = decode_predictions(predictions, top=5)[0]

        results = []
        for i, (imagenet_id, label, score) in enumerate(decoded_predictions):
            results.append({
                "label": label,
                "confidence": float(score)
            })

        is_cat_or_dog = False
        top_relevant_prediction = None
        
        # Keywords to check for cat/dog labels from ImageNet
        cat_dog_keywords = [
            'cat', 'dog', 'kitten', 'puppy', 'feline', 'canine',
            'tabby', 'persian_cat', 'siamese_cat', 'egyptian_cat', 'tiger_cat',
            'labrador_retriever', 'golden_retriever', 'german_shepherd', 'poodle',
            'chihuahua', 'bulldog', 'beagle', 'boxer', 'rottweiler', 'doberman',
            'collie', 'sheepdog', 'terrier', 'dalmatian', 'husky', 'dachshund',
            'basset_hound', 'shih-tzu', 'pug', 'malte', 'chow', 'cocker_spaniel',
            'great_dane', 'pit_bull', 'saint_bernard', 'siberian_husky', 'yorkshire_terrier'
        ]

        for pred in results:
            if any(keyword in pred['label'].lower() for keyword in cat_dog_keywords):
                is_cat_or_dog = True
                top_relevant_prediction = pred
                break 

        if is_cat_or_dog and top_relevant_prediction:
            return jsonify({
                "message": f"It looks like a {top_relevant_prediction['label']}!",
                "confidence": top_relevant_prediction['confidence'],
                "isCatOrDog": True,
                "predictions": results
            })
        elif results:
            top_general_prediction = results[0]
            return jsonify({
                "message": f"Could not find a specific cat/dog, but it looks like a {top_general_prediction['label']}.",
                "confidence": top_general_prediction['confidence'],
                "isCatOrDog": False,
                "predictions": results
            })
        else:
            return jsonify({
                "message": "Could not classify the image.",
                "confidence": 0.0,
                "isCatOrDog": False,
                "predictions": []
            }), 200

    except Exception as e:
        print(f"Error during classification: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"An unexpected error occurred during classification: {str(e)}"}), 500

if __name__ == '__main__':
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('templates', exist_ok=True)

    app.run(debug=True, host='0.0.0.0', port=5000)