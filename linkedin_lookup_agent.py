import os
print(os.getcwd())

from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from tools import get_profile_url
'''
    create_react_agent -> create agent based on ReAct (Reasoning + Action) framework, LLM decides which tool to use
    Agent_Executor     -> call LLM to select which tool to use and execute the tool
'''
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub # to use pre-made prompts by langchain community
load_dotenv()



def lookup(name: str) -> str:
    #llm = ChatOllama(model="deepseek-v3")
    llm = ChatOpenAI(temperature=0, model = "gpt-4o-mini")
    template = """Given the full name {name_of_person}, I want you to get me the link to their Linkedin profile page.
                Your answer should contain only a URL"""
    prompt_template = PromptTemplate(template=template, input_variables=["name_of_person"])

    """
    create a list for tools for the agent to use
    """
    tools_for_agent = [
        Tool(
            name= "Crawl google for Linkedin profile page",
            func= get_profile_url,
            description = "useful when you need to get Linkedin page url"
            
        )
       
    ]
    # Load the default ReAct prompt (or customize it)
    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm = llm, tools = tools_for_agent,prompt=react_prompt)# create a react agent
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True, handle_parsing_errors=True)# create executor function for agent
    result = agent_executor.invoke(input={"input": prompt_template.format_prompt(name_of_person = name)})
    linkedin_profile_url = result["output"]
    print(linkedin_profile_url)
    return linkedin_profile_url

if __name__ == "__main__":
    lookup(name="Chan Qin Xuan")

    