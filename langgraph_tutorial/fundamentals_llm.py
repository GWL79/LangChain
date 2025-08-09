from langgraph.graph import StateGraph, END, START
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
import random
from typing import Union, List, TypedDict
from dotenv import load_dotenv
load_dotenv()
class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]
llm = ChatOpenAI(model = "gpt-4o")
def process(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    state["messages"].append(AIMessage(content=response.content))
    print(f"\nAI: {response.content}")
    return state


graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)
agent = graph.compile()
converation_history = []
user_input = input("Enter:")
while user_input != "exit":
    converation_history.append(HumanMessage(content=user_input))
    result = agent.invoke({"messages": converation_history})
    conversation_history = result["messages"]
    user_input = input("Enter")