import openai
import API_KEY

# Set up the OpenAI API client
openai.api_key = API_KEY.api_key

# Set up the model and prompt
model_engine = "text-davinci-003"


class TimedConversation:
    def __init__(self, company, role, transitions=(3, 5, 7), difficulty: int = 2):
        self.transitions = transitions  # in minutes
        self.phase = 0

        if difficulty == 1:
            self.difficulty = "easy"
        elif difficulty == 2:
            self.difficulty = "medium"
        else:
            self.difficulty = "hard"

        self.company = company
        self.role = role
        self.chat_gpt3 = None

    def get_prompt(self, prompt: str, time):
        if time < self.transitions[0]:
            print("SECTION 1 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            if self.phase <= 0:
                self.chat_gpt3 = ChatGPT3Conversation(initial_context="""
                You are a senior """ + self.role + """ called Ella interviewing me for a """ + self.role + """ position at your company, """ + self.company + """.
                You will ask several """ + self.difficulty + """ difficulty questions and I will respond to those questions.
                The only exception to this will be during the introductions at the start of the mock interview where I introduce myself first.
    
                """)
                self.phase = 1

        elif time < self.transitions[1]:
            print("SECTION 2 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            if self.phase <= 1:
                self.chat_gpt3 = ChatGPT3Conversation(initial_context="""
                You are a senior """ + self.role + """ called Ella interviewing me for a """ + self.role + """ position at your company, """ + self.company + """.
                Search for a """ + self.difficulty + """ LeetCode or HackerRank problem, and link it to me.
                If I need help, please give me hints.
                I may need to pause to think about the problem, so make sure I finished the last problem before giving me the next one.
                Once I have finished the problem, continue giving me problems and links, while offering me hints if needed.

                """)
                self.phase = 2

        elif time < self.transitions[2]:
            print("SECTION 3 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            if self.phase <= 2:
                self.chat_gpt3 = ChatGPT3Conversation(initial_context="""
                You are a senior """ + self.role + """ called Ella interviewing me for a """ + self.role + """ position at your company, """ + self.company + """.
                You will simulate the end of an interview right after you had given me some programming problems.
                You will ask if I have any questions about """ + self.company + """
                and if you wanted to know anything else.
                
                """)
                self.phase = 3

        else:
            print("SECTION 4 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            if self.phase <= 3:
                self.chat_gpt3 = ChatGPT3Conversation(initial_context="""
                You are a senior """ + self.role + """ called Ella interviewing me for a """ + self.role + """ position at your company, """ + self.company + """.
                The interview has ended and you are saying good bye to me.
                
                """)
                self.phase = 4

        return self.chat_gpt3.get_response(prompt)


class ChatGPT3Conversation:
    def __init__(self, initial_context: str = "", context_limit: int = 2000):
        self.context = initial_context
        self.context_limit = context_limit
        self.truncate_context()

    def get_response(self, prompt: str, use_context: bool = True):

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
            self.context = self.context[len(self.context) - self.context_limit:]


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
