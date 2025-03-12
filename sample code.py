import google.cloud.aiplatform as aiplatform
from vertexai.language_models import TextGenerationModel
from google.oauth2 import service_account

# Load your actual service account credentials JSON file
credentials = service_account.Credentials.from_service_account_file(
    'C:/Users/Sharya3/Desktop/vertexai-poc/your-service-account-key.json'
)

# Initialize Vertex AI
import vertexai
vertexai.init(
    project='vz-nonit-np-jaov-dev-fpasdo-0', 
    location='us-east4', 
    credentials=credentials
)

# Load the Generative model
model = TextGenerationModel.from_pretrained("text-bison")

# Define a simple prompt
prompt = "What is the capital of France?"

# Generate the response
response = model.predict(prompt)

# Output the response
print(response.text)
