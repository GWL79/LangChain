from langchain import hub
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_experimental.tools import PythonREPLTool #python shell that can execute python code
from langchain_experimental.agents.agent_toolkits import create_csv_agent, create_python_agent
from langchain_core.tools import Tool
from typing import Any
load_dotenv()
def main():
    llm = ChatOpenAI(model="gpt-4-turbo")

    print("Start")
    instructions = """You are an agent designed to write and execute python code to answer questions. You have access
    to a python REPL, which you can use to execute python code. If you get an error, debug your code and try again.
    Only use output of your code to answer the question.
    You might know the answer without running any code, but you should still run the code to get an answer.
    If it does not seem like you can write code to answer the question, just return "I don't know" as the answer. 

    """
    base_prompt = hub.pull("langchain-ai/react-agent-template")
    prompt = base_prompt.partial(instructions = instructions)
    tools_repl = [PythonREPLTool()]
    python_agent = create_react_agent(llm=llm, tools=tools_repl, prompt=prompt)
    python_agent_executor = AgentExecutor(agent=python_agent, tools=tools_repl, verbose=True)
    #agent_executor.invoke(input = {"input": "generate and save in current working directory 15 QR codes that point to www.udemy.com/course/langchain, you have qr code package installed already"})
    csv_agent_executor:AgentExecutor = create_csv_agent(llm=llm, path=r"C:\Users\wlgan\LangChain\code_interpreter\episode_info.csv", verbose=True, allow_dangerous_code=True)
    #csv_agent.invoke(input = {"input": "in the file episode_info.csv, which writer wrote the most episodes? How many episodes did he write"})
    #csv_agent.invoke(input = {"input": "in the file episode_info.csv, print the seasons by ascending order of the number of episodes they have"})
##########################################Router Agent#################################################3
    def python_agent_executor_wrapper(original_prompt:str) -> dict[str, Any]:
        return python_agent_executor.invoke({"input": original_prompt})

    
    
    tools = [
        Tool(
            name= "Python Agent",
            func = python_agent_executor_wrapper,
            description= """useful when you need to transform natural language to python and execute the python code,
            returning the results of the code execution
            DOES NOT ACCEPT CODE AS INPUT"""
        ),

        Tool(
            name= "CSV Agent",
            func = csv_agent_executor.invoke,
            description= """useful when you need to answer questions over episode_info.csv file
            takes an input the entire question and returns the answer after running pandas calculation"""
        )
    ]

    prompt = base_prompt.partial(instructions = "")
    grand_agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
    grand_agent_executor = AgentExecutor(agent= grand_agent, tools=tools, verbose=True)
    print(grand_agent_executor.invoke(input={"input": "generate and save in current working directory 15 QR codes that point to www.udemy.com/course/langchain, you have qr code package installed already"}))


if __name__ == "__main__":
    main()
