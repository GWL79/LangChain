import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv, find_dotenv
from langchain_ollama import ChatOllama
from linkedin_scraping.scrapin_linkedin_profile import scrape_profile
from linkedin_lookup_agent import lookup as find_linkedin_user
def ice_break_with(name: str) -> str:
    linkedin_username = find_linkedin_user(name=name)
    linkedin_data = scrape_profile(url=linkedin_username, mock=False)
    # print("Hello LangChain")
    # print(os.environ['OPENAI_API_KEY'])
    summary_template = "given the Linkedin {information} about a person from I want you to create:" \
    "1. a short summary" \
    "2. two interesting facts about them"\
    "3. where he is working now"

    summary_prompt_template = PromptTemplate(input_variables=["information"], template=summary_template)
    llm = ChatOpenAI(temperature=0, model = "gpt-4o-mini")
    # llm = ChatOllama(model = "deepseek-r1")
    # linkedin_data = scrape_profile(
    #     url="https://www.linkedin.com/in/eden-marco/", 
    #     mock=True
    # )
    chain = summary_prompt_template | llm | StrOutputParser()
    res = chain.invoke(input={"information": linkedin_data})
    print(res)
    return res
if __name__ == "__main__":
    load_dotenv(find_dotenv())
    ice_break_with(name="Eden Marco")