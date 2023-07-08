import openai

openai.api_key = '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'

prompt = "Given a business description, the market discovery feature analyzes the description to generate relevant keywords and uses them to search social media platforms. It helps identify potential market trends, customer sentiments, and untapped opportunities for business expansion."

response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    temperature=0.7,
    max_tokens=100,
    n=1,
    stop=None,
)

conclusion = response.choices[0].text.strip()
print(f"Conclusion: {conclusion}")
