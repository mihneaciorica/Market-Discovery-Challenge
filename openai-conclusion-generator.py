import openai

openai.api_key = 'API_KEY'

def generate_conclusion(prompt):
    base_prompt = "\n Context: Given a business description, the market discovery feature analyzes the description to generate relevant keywords and uses them to search social media platforms. It helps identify potential market trends, customer sentiments, and untapped opportunities for business expansion."
    full_prompt = f"{base_prompt}\n\nBusiness description: {prompt} \n\n What you need to do: Write a nice and convincing conclusion for this business based on the business description i told you above."

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=full_prompt,
        temperature=0.7,
        max_tokens=100,
        n=1,
        stop=None,
    )

    conclusion = response.choices[0].text.strip()
    return conclusion

# Usage example
custom_prompt = "The business is a technology startup focusing on developing innovative mobile applications for productivity and organization."

generated_conclusion = generate_conclusion(custom_prompt)
print(f"Conclusion: {generated_conclusion}")
