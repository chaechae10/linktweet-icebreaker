from typing import List, Dict, Any
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field # 데이터 구조 표현 시 Pydantic 사용

class Summary(BaseModel): #  LLM이 생성해야 할 출력 형식을 정의
    summary: str = Field(description="summary")
    facts: List[str] = Field(description="interesting facts about them")

    def to_dict(self) -> Dict[str, Any]: # Python dict 형태로 변환하는 헬퍼 메서드
        return {"summary": self.summary, "facts": self.facts}
summary_parser = PydanticOutputParser(pydantic_object=Summary) #  LLM 출력 → Summary 객체 변환기