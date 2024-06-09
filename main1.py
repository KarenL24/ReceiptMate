import pytesseract as tess
tess.pytesseract.tesseract_cmd=r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
from PIL import Image
import openai
import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

#image to text
img = Image.open('r4.png')
text = tess.image_to_string(img, config='--tessdata-dir "C:\\Program Files\\Tesseract-OCR\\tessdata"')

print(text)

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {
      "role": "system",
      "content": "You will be given several lines of text representing a receipt. Give me a only list of products and their corresponding prices. FIrst give me a list of products each seperated by commas, and then on a new line, give me a list of prices. your task is to parse it into CSV format."
    },
    {
      "role": "user",
      "content": text
    }
  ],
  temperature=0.7,
  max_tokens=64,
  top_p=1
)
data = response.choices[0].message.content
product = data[:data.index('\n')].split(',')
price = response.choices[0].message.content[data.index('\n')+1:].split(',')

print(product)
print(price)
#1:30 (categorize bills, monthly spendingm)
#2:30 (organize json)