from crewai.flow.flow import Flow, start, listen
from litellm import completion
from dotenv import load_dotenv
import os


load_dotenv()

class BankFlow(Flow):
    @start()
    def generate_name(self):
        response = completion(
            api_key=os.getenv("GOOGLE_API_KEY"),
            model="gemini/gemini-2.0-flash-exp",
            messages=[
                {"role": "user", "content": "Generate a name of Pakistan's Top Bank"}
            ]
        )
        result = response.choices[0].message.content
        print(f"Name: {result}")
        return result

    @listen(generate_name)
    def points(self, bank_name):
        response = completion(
            api_key=os.getenv("GOOGLE_API_KEY"),
            model="gemini/gemini-1.5-flash",
            messages=[
                {"role": "user", "content": f"Give 3 Good Points And 3 Bad Points of {bank_name} return the Name Of Generated Bank Also"}
            ]
        )
        result = response.choices[0].message.content
        print(f"Points: {result}")
        return result



def final():
    flow = BankFlow()
    final_outline = flow.kickoff()
    with open("README.md", "w", encoding="utf-8") as file:
        file.write(final_outline)
    print("Final Output:")
    print(final_outline)
