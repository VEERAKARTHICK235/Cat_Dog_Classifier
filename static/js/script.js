
const imageUpload = document.getElementById('image-upload');
const imagePreview = document.getElementById('image-preview');
const classifyBtn = document.getElementById('classify-btn');
const predictionResult = document.getElementById('prediction-result');
const confidenceScore = document.getElementById('confidence-score');
const buttonText = document.getElementById('button-text');
const buttonSpinner = document.getElementById('button-spinner');



const CLASSIFY_API_URL = '/classify';

/**
 
 * @param {boolean} isLoading 
 */
function toggleLoading(isLoading) {
    if (isLoading) {
        buttonText.textContent = 'Classifying...';
        buttonSpinner.style.display = 'block';
        classifyBtn.disabled = true; 
        predictionResult.textContent = ''; 
        confidenceScore.textContent = '';
    } else {
        buttonText.textContent = 'Classify Image';
        buttonSpinner.style.display = 'none';
        
        classifyBtn.disabled = !imagePreview.src || imagePreview.src === '#';
    }
}


imageUpload.addEventListener('change', function(event) {
    const file = event.target.files[0]; 
    if (file) {
        const reader = new FileReader(); 
        reader.onload = function(e) {
            imagePreview.src = e.target.result; 
            imagePreview.style.display = 'block'; 
            classifyBtn.disabled = false; 
            predictionResult.textContent = ''; 
            confidenceScore.textContent = ''; 
            
            predictionResult.classList.remove('text-green-700', 'text-red-600', 'text-gray-700');
        };
        reader.readAsDataURL(file); 
    } else {
        
        imagePreview.src = '#';
        imagePreview.style.display = 'none';
        classifyBtn.disabled = true;
        predictionResult.textContent = '';
        confidenceScore.textContent = '';
    }
});


classifyBtn.addEventListener('click', async function() {
    if (!imagePreview.src || imagePreview.src === '#') {
        predictionResult.textContent = 'Please upload an image first.';
        return;
    }

    toggleLoading(true); 

    try {
        
        const imageData = imagePreview.src;

    
        const response = await fetch(CLASSIFY_API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ image: imageData }), 
        });

        
        if (!response.ok) {
            const errorData = await response.json(); 
            throw new Error(errorData.error || `Server error! Status: ${response.status}`);
        }

        const result = await response.json(); 
        console.log('Backend Response:', result);

        if (result.isCatOrDog) {
            const confidence = (result.confidence * 100).toFixed(2);
            predictionResult.textContent = `${result.message}`;
            confidenceScore.textContent = `Confidence: ${confidence}%`;
            predictionResult.classList.remove('text-red-600', 'text-gray-700');
            predictionResult.classList.add('text-green-700'); 
        } else {
            const confidence = (result.confidence * 100).toFixed(2);
            predictionResult.textContent = `${result.message}`;
            confidenceScore.textContent = `Confidence: ${confidence}%`;
            predictionResult.classList.remove('text-green-700', 'text-red-600');
            predictionResult.classList.add('text-gray-700'); 
        }

    } catch (error) {
        console.error('Error during classification:', error);
        predictionResult.textContent = `Error: ${error.message || 'Could not classify image due to network or server issue.'}`;
        confidenceScore.textContent = '';
        predictionResult.classList.remove('text-green-700', 'text-gray-700');
        predictionResult.classList.add('text-red-600');
    } finally {
        toggleLoading(false);
    }
});
