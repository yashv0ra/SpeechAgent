import os
from groq import Groq
from time import sleep
def is_blank(s):
    return s.strip() == ''
# Create the Groq client
def main():
    # run 
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"), )

    # Set the system prompt
    system_prompt = {
        "role": "system",
        "content":
        "Your name is Terry and you are a strict personal trainer who has been taught that being mean to your student is the best way to inspire discipline. " + 
            "You are to only answer questions related to fitness and working out and attempt to inspire your student" + 
            "(who you are speaking to) to work out through tough love. Limit responses to 30 words. You like to namecall your clients in creative ways."
    }

    # Initialize the chat history
    chat_history = [system_prompt]
    repeat_check = ""
    question = ""
    x = open('useroutput.txt','w')
    while True:
    # Get user input from the console
    
        while repeat_check == question or is_blank(question):
            with open('useroutput.txt', 'r') as f:
                question = f.readline()
            sleep(0.1)
        repeat_check = question
            

        # Append the user input to the chat history
        chat_history.append({"role": "user", "content": question})

        response = client.chat.completions.create(model="llama3-70b-8192",
                                                    messages=chat_history,
                                                    max_tokens=1000,
                                                    temperature=1.2)
        # Append the response to the chat history
        chat_history.append({
            "role": "assistant",
            "content": response.choices[0].message.content
        })
        # Print the response
        print("User: " + question)
        print("Assistant:", response.choices[0].message.content)
        with open('botoutput.txt', 'w') as f:
            f.write(response.choices[0].message.content)   
if __name__ == "__main__":
    main()