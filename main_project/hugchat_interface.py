from hugchat import hugchat
from hugchat.login import Login

import voice

sign = Login("kingservice69@gmail.com", "Redpyro@12345")
cookies = sign.login()

cookie_path_dir = "./cookies_snapshot"
sign.saveCookiesToDir(cookie_path_dir)

chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
id = chatbot.new_conversation()
chatbot.change_conversation(id)

prompt = "tell me about mars in few line only"

is_chatting = False

print(chatbot.chat(prompt))
voice.speak(new_answer=chatbot.chat(prompt))

# def main():
#     if is_chatting:
#         pass

# if __name__ == "__main__":
#     main()