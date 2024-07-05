import tiktoken
import pandas as pd
from openai import OpenAI


def num_tokens(text: str, model: str = 'gpt-3.5-turbo') -> int:
    """Return the number of tokens in a string."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def query_prompt(query: str, df: tuple[pd.DataFrame, pd.DataFrame], model: str = 'gpt-3.5-turbo'):
    """Return a prompt for GPT, with relevant definitions and source data pulled from a dataframe."""
    patient_vital_details = df[0]
    patient_medication_details = df[1]
    
    prompt = f"""You are a Blood-Pressure Question & Answer agent and you are restricted to talk only about patient details provided below. Use the below patients details and the definitions to answer the subsequent question. If the answer cannot be found, write "I don't know."

        Definition of Hypotension: Hypotension (low blood pressure) is generally considered a blood pressure reading lower than 90 mmHg for the top number (systolic) or 60 mm Hg for the bottom number (diastolic).

        Definition of Hypertension: Hypertension (high blood pressure) is when the pressure in your blood vessels is too high (140/90 mmHg or higher).
        
        Note: 
        
        - Make sure your answer contains information about each patient.
        - Answer the questions about blood-pressure based on the most recent blood-pressure record available for each patient.
        
        Patient Blood Pressure details:
        \"\"\"
        {patient_vital_details}
        \"\"\"

        Patient Medication details:
        \"\"\"
        {patient_medication_details}
        \"\"\"
        
        Question: {query}"""
    
    number_of_tokens = num_tokens(prompt, model= model)
    
    return prompt, number_of_tokens

def ask(query: str,
        data: tuple[pd.DataFrame, pd.DataFrame],
        client: 'OpenAI' = None,
        model: str = 'gpt-3.5-turbo',
        ):
    """Answers a query using GPT and a dataframe of relevant data."""
    
    message, num_tokens = query_prompt(query, data, model= model)
    
    
    response = client.chat.completions.create(
    messages=[
        {'role': 'system', 'content': 'You answer questions about the patient blood pressure records and details regarding medication prescribed to the patient.'},
        {'role': 'user', 'content': message},
    ],
    model=model,
    temperature=0,
)
    
    response_message = response.choices[0].message.content
    
    return response_message





