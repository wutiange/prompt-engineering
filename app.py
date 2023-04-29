import openai

openai.api_key = "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"

def get_completion(prompt, model = "gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]


text_2 = f"""
The sun is shining brightly today, and the birds are singing. It's a beautiful day to go for a walk in the park. The flowers are blooming, and the trees are swaying gently in the breeze. People are out and about, enjoying the lovely weather. Some are having picnics, while others are playing games or simply relaxing on the grass. It's a perfect day to spend time outdoors and appreciate the beauty of nature.
"""
prompt_2 = f"""
You will be provided with text delimited by triple quotes.
If it contains a sequence of instructions, re-write those instructions in the following format:
Step 1 - ...
Step 2 - ...
...
Step N -

\"\"\"{text_2}\"\"\"
"""
response = get_completion (prompt_2)
print ("Completion for Text 2:")
print (response)