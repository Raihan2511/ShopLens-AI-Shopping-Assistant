from app.config import settings
import google.generativeai as genai
import json

genai.configure(api_key=settings.GEMINI_API_KEY)


def infer_query(query, model='gemini-2.0-flash-thinking-exp-1219') :
  model = genai.GenerativeModel(model)

  prompt = f"""
  You are a assistant for a fashion e-commerce website. Your task is to determine if the user is asking for a "text based product search" or a "image based product search" also you have identify "how many" product results the user is asking.
  If you determine the user is aksing for a "text based product search" then you have to determine the actual "search term".
  For example, if the user is asking for "show me some red shoes. they should be for women" then you have to determine the "search term" as "red shoes for women".
  If you determine the user is aksing for a "image based product search" then you have to see if the user provided a "image link" or not.
  After that you have to return the result in a json format with the following keys:
  1. "query_type" (text based product search or image based product search)
  2. "no_of_results" (how many product results the user is asking for)
  3. "search_term"
  4. "image_url" (if the query type is image based product search and the user provided a image link then return the image link otherwise return None)
  If you can't determine the value of any of the keys then return None for that key, except for "no_of_results" which should by default be 6.

  Query: "{query}"

  Under no circumstances should you return any other text or explanation. Just return the result in json format.
  """

  response = model.generate_content(prompt)

  raw_response = response.text.strip()

  print("Raw response:", repr(raw_response))

  # Optional: try to extract just the JSON block if it adds anything else
  try:
      json_start = raw_response.index('{')
      json_end = raw_response.rindex('}') + 1
      json_str = raw_response[json_start:json_end]
  except ValueError:
      return None  # or raise a custom error

  try:
      parsed = json.loads(json_str)
      return parsed
  except json.JSONDecodeError as e:
      print("Failed to decode JSON:", e)
      print("Response was:", repr(json_str))
      return None