import openai
    
    
openai.api_key = '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'
model_engine = "text-davinci-002"
prompt = "Hello, how are you today?"
    
completion = openai.Completion.create(
    engine = model_engine,
    prompt = prompt,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.5,
    )
    
response = completion.choices[0].text
print(response)