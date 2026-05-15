from openai import AzureOpenAI

client = AzureOpenAI(
    api_key="YOUR_KEY",
    azure_endpoint="YOUR_ENDPOINT",
    api_version="2024-02-15-preview"
)


def summarize(reasoning):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You generate grounded analytical summaries."
            },
            {
                "role": "user",
                "content": str(reasoning)
            }
        ]
    )

    return response.choices[0].message.content