import requests

# Send a prompt to the MCP server
url = "http://localhost:8090/generate"
prompt = "What are the benefits of AI in healthcare?"
response = requests.post(url, json={"prompt": prompt})

# Print the server's response
print("Response from MCP server:", response.json())
