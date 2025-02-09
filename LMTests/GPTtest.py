from openai import OpenAI

client = OpenAI(
  api_key="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"
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
)

print(completion.choices[0].message);
