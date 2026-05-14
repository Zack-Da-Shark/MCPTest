from ollama import chat
from tools import searchTool

# will be running importing the command to get it

# Tool metdata
tools = [
    {
        "type": "function",
        "function": {
            "name": "searchTool",
            "description": "Searches arXive for research papers based on a topic or query given",
            "parameters": {
                "type": "object",
                "properties":{
                    "topic":{
                        "type": "string",
                        "description": "The topic to be searched for on arXive's database"
                    },
                    "amount":{
                        "type": "number",
                        "description": "The amount of papers the user asked for"
                    }
                },
                "required": ["topic", "amount"]
            }
        }
    }
]

# Start of the conversation
conversation = []

def askAI(conversation):
    response = chat(
        model='gemma4:26b',
        messages=[personality, equipment] + conversation,
        tools = tools,
    )

    reply = response.message.content
    conversation.append({'role': 'assistant', 'content': reply})
    return response

# AI's personality
personality = {"role": "system", "content": """
                You are a helpful AI assistant named Pam
               USE EMOJIS BECAUSE FUN
               """}

# AI's Tools
equipment = {"role": "system", "content": """
            You have access to a tool called searchTool that accesses arXive through an API
             It takes in a topic and amount of papers wanted as an argument
             use it whenever the user wants you to search for research papers
             """}

maxMessages = 10

while True:
    query = input("Your query here")

    if query.lower() == 'exit':
        break

    conversation.append({'role': 'user', 'content': query})

    response = askAI(conversation)
    tool_calls = getattr(response.message, "tool_calls", None)
    print(response)
    print("------------------------------------------------------------")
    print(tool_calls)
    print(response.message.thinking)
    print(response.message.content)



    if(len(conversation) >= maxMessages):
        conversation.pop(0)
        conversation.pop(0)
    
    if tool_calls:
        print("Calling tools")
        for call in tool_calls:
            if call.function.name == "searchTool":
                item = call.function.arguments.get("topic")
                value = call.function.arguments.get("amount", 3)
                print("Search tool has been called!")
                papers = searchTool(item, value)
                print(papers)
    print("End of response")

# Use this command docker run --rm -it --gpus all 23/04/2026
# This one uses the 26 Billion parameter version