from openai import AzureOpenAI
import json

client = AzureOpenAI(
    api_key="YOUR_KEY",
    api_version="2024-02-15-preview",
    azure_endpoint="YOUR_ENDPOINT"
)


def extract_signals(text: str):
    prompt = f"""
    Extract analytical business signals.

    Return valid JSON.

    Text:
    {text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You extract structured business features."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return response.choices[0].message.content