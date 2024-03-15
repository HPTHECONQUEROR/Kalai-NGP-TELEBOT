# response.py
import requests

class RunBot:
    def __init__(self, first_name):
        self.first_name = first_name
        self.API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
        self.headers = {"Authorization": "Bearer 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"}
        self.load_prompt()

    def load_prompt(self):
        with open("kalai.txt", "r", encoding="utf-8") as file:
            self.prompt_text = file.read()

    def bot_output(self, command):
        if command == "/start":
            return "Hello, this is kalai, nice to meet you!"
        response = requests.post(self.API_URL, headers=self.headers,
                                 json={"inputs": self.prompt_text + f"\n <|user|> {command} <u/> <|assistant|> "})
        output = response.json()
        op = output[0]["generated_text"]
        output_final = self.print_text_after_last_occurrence(op, command)
        start = output_final.find(f"<|assistant|>") + len("<|assistant|>")
        end = output_final.find("<a/>")
        output_final = output_final[start:end]
        return output_final

    def print_text_after_last_occurrence(self, input_string, command):
        index = input_string.rfind(command)
        result = input_string[index + len(command):]
        return result

