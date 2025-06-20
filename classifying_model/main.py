from groq import Groq

# Initialize the Groq client once
client = Groq(api_key="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")

# System prompt for the classifier
SYSTEM_MESSAGE = {
    "role": "system",
    "content": (
        "You are a Law AI Assistant. Your job is to take a case description from the user "
        "and classify it into one of the following categories: 'Criminal', 'Civil', 'Family', "
        "'Corporate', 'Intellectual Property', 'Real Estate', 'Employment'. "
        "Your answer should be just one of the categories. If you are asked about anything else, "
        "you should say 'I am a Law AI Assistant. I can only classify cases into categories.'"
    )
}

def classify_case_description(user_input: str) -> str:
    messages = [
        SYSTEM_MESSAGE,
        {"role": "user", "content": user_input}
    ]

    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=messages,
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
    )

    # Get the assistant's full response
    return completion.choices[0].message.content.strip()
