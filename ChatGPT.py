import openai
import API_KEY

# Set up the OpenAI API client
openai.api_key = API_KEY.api_key

# Set up the model and prompt
model_engine = "text-davinci-003"


class ChatGPT3:
    def __init__(self, initial_context: str = "", context_limit: int = 2000):
        self.context = initial_context
        self.context_limit = context_limit
        self.truncate_context()

    def get_prompt(self, prompt: str, use_context: bool = 1):
        prompt = "Prospect: " + prompt + "\nInterviewer: "

        # Generate a response
        if use_context:
            completion = openai.Completion.create(
                engine=model_engine,
                prompt="context:" + self.context + "prompt:" + prompt + "\n",
                max_tokens=1024,
                n=1,
                stop=["Prospect:"],
                temperature=0.5,
            )
        else:
            completion = openai.Completion.create(
                engine=model_engine,
                prompt="prompt:" + prompt,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5,
            )

        response = completion.choices[0].text
        self.context += (prompt + response + "\n")
        print("=================Context====================")
        print(self.context)
        print("-----------------Context--------------------")

        return response

    def truncate_context(self):
        if len(self.context) > self.context_limit:
            print("Warning, context limit exceeded, truncating input")
            self.context = self.context[self.context_limit - len(self.context):]


chat_gpt3 = ChatGPT3(initial_context="""You are a senior computer engineer interviewing me for a position at your company, Google. You will ask several questions and I will respond to those questions until you initiate the end of the interview after four or so questions. The only exception to this will be during the intrpductions at the start of the mock interview where I introduce myself first

""")

while True:
    user_input = input()
    if user_input == "quit":
        break
    print(chat_gpt3.get_prompt(user_input))





