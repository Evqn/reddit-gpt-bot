import openai

class OpenAIBot:
    def __init__(self, api_key):
        openai.api_key = api_key

    def generate_explanation(self, post_title, post_content, subreddit, user_comment=None, context=None, settings=None):
        # New settings parameter includes the user's settings

        # Default settings
        sentence_limit = 5
        additional = ""
        tone = "" 

        # Check if settings exist, then replace the default settings
        if settings:
            sentence_limit = settings['max_sentence']
            tone = settings['tone']
            additional = settings['additional']

        # main prompt to ask
        request = "Summarize the following Reddit post"
        if additional:
            request = additional
        if tone:
            request += f" in a {tone} tone"
        
        
        task = f"{request} in less than {sentence_limit} sentences: \nSubreddit: {subreddit} \nTitle: {post_title}\nContent: {post_content}"


        # If context is provided, add it to the prompt
        if context:
            # Truncate the context if it's too long to fit within the token limit
            if len(context) + len(task) > 4000:  # leaving some room for other tokens
                context = context[:4000 - len(task)] + "..."
            prompt = f"Context: {context}\n\n" + task
        else:
            prompt = task

        print(f"Prompt for GPT: {prompt}")
        print("---------------------------------------------")

        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.7,
        )
        
        reply = response.choices[0].text.strip()
        return reply