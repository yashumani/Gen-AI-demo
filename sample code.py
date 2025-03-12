import google.cloud.aiplatform as aiplatform
from vertexai.language_models import TextGenerationModel
from google.oauth2 import service_account

# Load your service account credentials
credentials = service_account.Credentials.from_service_account_file('path/to/your/credentials.json')

# Initialize Vertex AI
import vertexai
vertexai.init(project='your-gcp-project-id', location='us-central1', credentials=credentials)

# Load the Generative model
model = TextGenerationModel.from_pretrained("text-bison")

# Define a simple prompt
prompt = "What is the capital of France?"

# Generate the response
response = model.predict(prompt)

# Output the response
print(response.text)
