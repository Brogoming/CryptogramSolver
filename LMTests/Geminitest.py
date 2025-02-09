import google.generativeai as genai

# Set your API key
client = genai.configure(api_key="AIzaSyAvmSv11ZZtbtAofwweyjQnZqC2npToqMs")

# Initialize the model
model = genai.GenerativeModel("gemini-2.0-flash")

# Define the prompt
prompt = "How do I bake cookies?"

# Generate response
response = model.generate_content(prompt)

# Print the response
print(response.text)