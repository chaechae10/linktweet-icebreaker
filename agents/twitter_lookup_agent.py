# 목표: LangChain으로 ReAct Agent 만들기

from dotenv import load_dotenv
import os, sys

pythonpath = os.path.dirname(os.path.abspath(__file__))  # 현재 파일 위치(=프로젝트 루트)
if pythonpath not in sys.path:
    sys.path.append(pythonpath)

load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent, #ReAct 알고리즘 기반의 에이전트 반환
    AgentExecutor, # 에이전트 런타임
)
from langchain import hub # 프롬프트 사용
from tools.tools import get_profile_url_tavily


def lookup(name: str) -> str:
    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-4o-mini",
    )

    template = """
    given the name {name_of_person} I want you to find a link to their Twitter profile page, and extract from it their username
    In Your Final answer only the person's username"""

    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )

    tools_for_agent = [
        Tool(
            name="Crawl Google 4 Twitter profile page", # 에이전트가 이 도구 지칭하는 용어
            func=get_profile_url_tavily, # 이 도구가 실행하기를 원하는 함수
            description="useful for when you need get the Twitter Page URL", # LLM이 이 도구 사용할지 말지 정하는 부분으로 중요
        )
    ]

    react_prompt = hub.pull("hwchase17/react") # ReAct 프롬프트를 가져옴, 에이전트에 연결 예정
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True) # 에이전트를 실제로 실행(run)할 수 있게 감싸주는 “실행기”, 광범위한 로깅 보기 위해 True로

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )

    linked_profile_url = result["output"]
    return linked_profile_url


if __name__ == "__main__":
    print(lookup(name="Elon Musk"))