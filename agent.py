import ollama
from tools import read_file, list_files, write_file, edit_file, run_python

print("AI Coding Agent")

user_input = input("User: ")
messages = []
tools = [read_file, list_files, write_file, edit_file,run_python]
tool_map = {
    tool.__name__: tool
    for tool in tools

}

while user_input != '':
    #add user message to history
    messages.append(
        {
            "role":"user",
            "content":user_input
        }
    )
    ##############################

    #get llm response
    response = ollama.chat(
        model="qwen3:14b",
        messages= messages,
        tools=tools,
        think=False
    )
    ##############################
    tool_calls = response["message"].get("tool_calls") or []
    while tool_calls:
        messages.append(response["message"])
        
        for tool_call in tool_calls:
            func = tool_call["function"]["name"]
            function = tool_map[func]
            execution = function(**tool_call["function"]["arguments"])
            messages.append(
                {
                    "role":"tool",
                    "content":str(execution)
                }
            )
        response = ollama.chat(
            model="qwen3:14b",
            messages=messages,
            tools=tools,
            think=False
        )
        print("DEBUG RESPONSE:", response["message"])
        tool_calls = response["message"].get("tool_calls") or []

    ##############################
    #add llm respose to history
    messages.append(
        {
            "role":"assistant",
            "content":response["message"]["content"]
        }
    )
    ##############################
    #print llm reponse
    print("Agent:",response["message"]["content"])
    #get new user input
    user_input = input("User: ")