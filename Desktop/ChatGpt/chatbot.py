import traceback
import openai
import gradio as gr
import tiktoken

openai.api_key = "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"
# Specify a maximum token threshold
MAX_TOKENS = 100

class ChatBot:
    def __init__(self, system_role):
        self.messages = [{"role": "system", "content": system_role}]
    def count_tokens(self):
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        # Record the number of tokens
        token_num = 0
        for message in self.messages:
            # every message follows <im_start>{role/name}\n{content}<im_end>\n
            token_num += 4
            for key, value in message.items():
                token_num += len(encoding.encode(value))
                # if there's a name, the role is omitted
                if key == "name":
                    # role is always required and always 1 token
                    token_num -= 1
                # every reply is primed with <|start|>assistant<|message|>
                token_num += 3
        return token_num

    def launch(self):
        with gr.Blocks() as chat_demo:
            # gradio chatbot component
            chatbot = gr.Chatbot()
            # gradio textbox component
            msg = gr.Textbox()
            # gradio clear button component
            # click to clear msg&chatbot

            clear = gr.ClearButton([msg, chatbot])
            def respond(input, history):
                self.messages.append({"role": "user", "content": input})

                # If the total number of tokens is greater than the threshold(MAX_TOKENS)
                while len(self.messages) > 2 and self.count_tokens() > MAX_TOKENS:
                    # Keep the first and second elements and delete all the rest.
                    self.messages = self.messages[0:1] + self.messages[2:]

                    # If the current number of tokens is greater than the threshold(MAX_TOKENS)
                if self.count_tokens() > MAX_TOKENS:
                        # Keep the first element and delete all the rest.
                    self.messages = self.messages[0:1]
                        # Reply error
                    reply = "Sorry, messages are to long."
                else:
                        # Start an exception handling block
                    try:
                        # Try to execute the following code
                        chat = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=self.messages
                            )
                    except:
                        reply = traceback.format_exc()
                        pass
                    else:
                        reply = chat.choices[0].message["content"]
                        self.messages.append({"role": "assistant", "content":reply})

                # add input and reply to history
                history.append((input, reply))
                # return history instead of reply
                return "", history
            msg.submit(respond, [msg, chatbot], [msg, chatbot])
        chat_demo.launch()

ChatBot('You are a computer programmer.').launch()
