# KNIME Python Node Integration with Vertex AI
import vertexai
from vertexai.language_models import TextGenerationModel
import pandas as pd

# Initialize Vertex AI with your project and region (ensure authentication is handled via gcloud ADC)
vertexai.init(project='vz-nonit-np-jaov-dev-fpasdo-0', location='us-east4')

# Load the Generative model
model = TextGenerationModel.from_pretrained("text-bison")

# Assume input_table_1 is passed from KNIME as a DataFrame
# Convert the DataFrame to a string representation to embed in the prompt
table_as_str = input_table_1.to_csv(index=False)

# Construct a meaningful prompt embedding your data
prompt = f"""
Summarize the following data table concisely, highlighting any important insights or anomalies:

{table_as_str}

Provide the summary as clearly structured insights:
"""

# Generate response from Vertex AI
response = model.predict(prompt)

# Prepare the response as a DataFrame for KNIME output
output_table_1 = pd.DataFrame({"AI_Summary": [response.text]})
