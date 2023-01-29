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

    def get_prompt(self, prompt: str, final_prompt: bool, use_context: bool = True):
        # This helps the AI determine when it should end.
        if final_prompt:
            prompt = "This is my final answer. Do not ask me another question. " + prompt

        # THIS IS REALLY IMPORTANT
        # Without this, it gets confused and starts responding to itself. This is not the best place to put this,
        # this is where I have put it for now. Basically this sets up the two roles for it to know who is leading.
        prompt = "Prospect: " + prompt + "\nInterviewer: "

        # Generate a response
        if use_context:
            completion = openai.Completion.create(
                engine=model_engine,
                prompt="context:" + self.context + "prompt:" + prompt + "\n",
                max_tokens=1024,
                n=1,
                # This is the other portion that is REALLY important. Without this it was getting confused.
                # This tells it to stop talking when it reaches the prospective employee's dialog section.
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

class RankByQualifier:
    def __init__(self, qualifier: str):
        self.qualifier = qualifier

        completion = openai.Completion.create(
            engine=model_engine,
            prompt="Tell me the opposite of the following sentence. " + qualifier + "\n",
            max_tokens=1024,
            n=1,
            # This is the other portion that is REALLY important. Without this it was getting confused.
            # This tells it to stop talking when it reaches the prospective employee's dialog section.
            stop=None,
            temperature=0.5,
        )

        self.anti_qualifier = completion.choices[0].text

    def get_prompt(self, prompt: str):
        completion = openai.Completion.create(
            engine=model_engine,
            prompt="Rank the sentiment of the following sentence from 1 (" + self.anti_qualifier + ") to 10 (" + self.qualifier + "). " + prompt + "\n",
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )

        return completion.choices[0].text
