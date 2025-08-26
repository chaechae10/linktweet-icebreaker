import os  # 환경변수 접근 위해
import requests  # API 사용 위해
from dotenv import load_dotenv

load_dotenv()

# 스크래핑 수행하는 함수
def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """Scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile"""

    if mock:
        # Gist에서 mock 데이터 불러오기
        linkedin_profile_url = "https://gist.githubusercontent.com/emarco177/0d6a3f93dd06634d95e46a2782ed7490/raw/fad4d7a87e3e934ad52ba2a968bad9eb45128665/eden-marco.json"
        
        response = requests.get(
            linkedin_profile_url,
            timeout=10
        )

    else:
        # Proxycurl API 호출
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        header_dic = {
            "Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'
        }
        response = requests.get(
            api_endpoint,
            params={"url": linkedin_profile_url},
            headers=header_dic,
            timeout=10,
        )
    data = response.json()
    
    # 불필요한 값 제거(스니펫) 반환되는 페이로드 간단해짐
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }

    # groups 안에 있는 profile_pic_url 제거
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url", None)

    return data

    
if __name__ == "__main__":
    print(
        scrape_linkedin_profile(linkedin_profile_url="https://www.linkedin.com/in/eden-marco/", mock=True)
    )