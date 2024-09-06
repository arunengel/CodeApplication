from openai import OpenAI
import requests

class OpenAiService():
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)

    def extract_data(self, file_content):
        # Specify the ChatGPT model that should process the input
        MODEL="gpt-4o"

        try:
            response = self.client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that helps me extracting data from timesheets."},
                    {"role": "system", "content": "You extract the workers name."},
                    {"role": "system", "content": "You extract the working hours for each day."},
                    {"role": "system", "content": "You extract the notes for each day."},
                    {"role": "system", "content": "You extract the customer for each entry and refer to it as 'Customer'."},
                    {"role": "system", "content": "You structure it in a dictionary format with the keys 'Name' for the workers name and 'Times' containing an array of the keys 'Date', 'Hours', 'Notes' and 'Customer' for each day."},
                    {"role": "system", "content": "Only give back the Dictionary containing the information, nothing else."},
                    {"role": "user", "content": file_content}
                ]
            )

            # Only get the response message but not the whole JSON object that is retrieved
            extracted_data = response.choices[0].message.content
            return extracted_data
        except Exception as e:
            return {"error": str(e)}

        