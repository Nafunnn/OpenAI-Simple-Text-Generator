from openai import OpenAI
import wget

api_key = "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"
client = OpenAI(api_key=api_key)

response = client.images.generate(
  model="dall-e-3",
  prompt= input("Masukkan deskripsi gambar : "),
  size="1024x1024",
  quality="standard",
  n=1,
)

image_url = response.data[0].url
response = wget.download(image_url)