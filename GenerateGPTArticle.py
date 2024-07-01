import openai

class GenerateGPTArticle:
    def __init__(self, prompt):
        self. prompt = prompt 
    
openai.api_key = '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'
model_engine = "text-davinci-002"

def generate_article(prompt):
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=3125,
        n=1,
        stop=None,
        temperature=0.7,
    )
    article = response.choices[0].text.strip()
    return article