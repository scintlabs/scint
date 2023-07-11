import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Image.create(
  prompt="A logo depicting a high quality scintillating gem with gradients and blended colors, using shades of red, orange, yellow, and pink, but with a simplistic, brutalist outline.",
  n=3,
  size="2056x2056"
)