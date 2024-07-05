from data_processing import data
from prompt import ask
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
GPT_MODEL = os.getenv("GPT_MODEL")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

qa_dict = {}

question1 = "Did the patient have Hypertension/Hypotension given blood-pressure records from vitals?"
question2 = "Did the patient get the medication order to treat hypertension/hypotension if any? "

answer1 = ask(question1,data,client)
answer2 = ask(question2,data,client)

qa_dict[question1] = answer1
qa_dict[question2] = answer2

print('Q1. :',question1,'\n','Ans :',answer1,'\n')
print('Q2. :',question2,'\n','Ans :',answer2,'\n')