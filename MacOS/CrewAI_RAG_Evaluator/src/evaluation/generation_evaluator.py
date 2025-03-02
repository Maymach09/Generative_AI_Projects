import openai

def evaluate_generation(response, ground_truth):
    """Evaluates the AI-generated response using GPT-4."""
    
    client = openai.OpenAI()  # New API client

    prompt = f"""Evaluate the following response against the expected answer.
    Response: {response}
    Expected: {ground_truth}
    Give a score from 1 to 10 based on accuracy and coherence."""

    completion = client.chat.completions.create(  # New OpenAI method
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an evaluation assistant."},
            {"role": "user", "content": prompt},
        ]
    )
    
    return float(completion.choices[0].message.content.strip()) # Return the score