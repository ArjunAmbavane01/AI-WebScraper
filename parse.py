from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import concurrent.futures
import json

# Updated prompt template
template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty JSON object (`{{}}`)."
    "4. **Valid JSON Only:** Ensure the output is formatted as valid JSON. Do not return anything other than valid JSON."
)

model = OllamaLLM(model="llama3.1")

# Function to process a single chunk
def parse_chunk(chunk, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    return chain.invoke({"dom_content": chunk, "parse_description": parse_description})

# Function to safely parse response into JSON
def safe_parse_response(response):
    try:
        # Clean response and remove any non-JSON text
        response = response.strip().strip('```json').strip('```')
        
        # Attempt to parse the response as JSON
        return json.loads(response)
    except json.JSONDecodeError:
        # Return a placeholder if parsing fails
        return {"error": "Invalid JSON", "content": response}

# Main function to parse content with Ollama
def parse_with_ollama(dom_chunks, parse_description):
    parsed_results = []

    # Use ThreadPoolExecutor to parallelize the parsing
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(parse_chunk, chunk, parse_description)
            for chunk in dom_chunks
        ]
        for i, future in enumerate(concurrent.futures.as_completed(futures), start=1):
            try:
                response = future.result()
                print(f"Parsed batch {i} of {len(dom_chunks)}")
                parsed_json = safe_parse_response(response)
                parsed_results.append(parsed_json)
            except Exception as e:
                print(f"Error parsing batch {i}: {e}")
    return parsed_results

