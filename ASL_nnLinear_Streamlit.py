import streamlit as st
import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import os

# --- Streamlit UI ---
st.set_page_config(page_title="ASL Classifier", page_icon="🤟")

# --- Model Definition ---
class ASL_Linear_Classifier(nn.Module):
    def __init__(self, input_size=784, hidden_size=256, num_classes=26):
        super(ASL_Linear_Classifier, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.3)
        self.fc2 = nn.Linear(hidden_size, num_classes)
    
    def forward(self, x):
        x = x.view(x.size(0), -1)
        x = self.fc1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        return x

# --- Configuration ---
INPUT_SIZE = 28 * 28
HIDDEN_SIZE = 256
NUM_CLASSES = 26
MODEL_PATH = "asl_linear_classifier.pt"

# --- Load Model ---
@st.cache_resource
def load_model():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = ASL_Linear_Classifier(INPUT_SIZE, HIDDEN_SIZE, NUM_CLASSES).to(device)
    
    if os.path.exists(MODEL_PATH):
        checkpoint = torch.load(MODEL_PATH, map_location=device)
        if 'model_state_dict' in checkpoint:
            model.load_state_dict(checkpoint['model_state_dict'])
        else:
            model.load_state_dict(checkpoint)
        model.eval()
        return model, device
    else:
        return None, device

model, device = load_model()

# --- Preprocessing ---
transform = transforms.Compose([
    transforms.Grayscale(num_output_channels=1),
    transforms.Resize((28, 28)),
    transforms.ToTensor(),
])

st.title("🤟 ASL Alphabet Classifier")
st.write("Upload an image of an ASL hand sign to classify it!")

with st.sidebar:
    st.header="Model Info"
    st.write("This model uses a simple Linear Neural Network trained on the Sign Language MNIST dataset.")
    if model is None:
        st.error(f"Model file not found at {MODEL_PATH}. Please make sure the model is trained and saved.")
    else:
        st.success("Model loaded successfully!")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', width=300)
        
        if model:
            with st.spinner('Classifying...'):
                # Preprocess
                input_tensor = transform(image).unsqueeze(0).to(device)
                
                # Predict
                with torch.no_grad():
                    output = model(input_tensor)
                    probabilities = torch.nn.functional.softmax(output, dim=1)
                    confidence, predicted_idx = torch.max(probabilities, 1)
                    predicted_idx = predicted_idx.item()
                    confidence = confidence.item()
                
                predicted_char = chr(ord('A') + predicted_idx)
                
                st.success(f"Prediction: **{predicted_char}**")
                st.info(f"Confidence: {confidence:.2%}")
                
                # Optional: Show top 3 predictions
                st.subheader("Top 3 Predictions")
                top3_prob, top3_idx = torch.topk(probabilities, 3)
                for i in range(3):
                    char = chr(ord('A') + top3_idx[0][i].item())
                    prob = top3_prob[0][i].item()
                    st.write(f"{char}: {prob:.2%}")
                    st.progress(prob)

    except Exception as e:
        st.error(f"Error processing image: {e}")
