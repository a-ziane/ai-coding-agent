import ollama
from tools import read_file, list_files, write_file, edit_file, run_python, run_command

print("AI Coding Agent")
SYSTEM_PROMPT = """
You are an AI coding agent.

You can inspect, edit, and run code using the provided tools.

Rules:
- Use the provided tools to inspect, modify, and run code.
- Before editing an existing file, always read it first using read_file.
- Do not assume a file's contents based only on an error message.
- Preserve unrelated code when making changes.
- Make the smallest change necessary to solve the problem.
- After modifying code, run the relevant file or tests.
- Report the exit code and important output in your final answer.
- Never claim success unless verification finishes with exit code 0.
- If verification fails, continue debugging.
- dont output until you fixed every bug
After completing a coding task, your final response must use this format:

Changed:
- Briefly describe the change.

Verification:
- Exit code: <exact exit code>
- Output: <exact important output>

Do not say the task succeeded without providing the verification exit code.
"""

user_input = input("User: ")
messages = [
    {
    "role": "system",
    "content": SYSTEM_PROMPT
    }

]
tools = [read_file, list_files, write_file, edit_file,run_python, run_command]
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