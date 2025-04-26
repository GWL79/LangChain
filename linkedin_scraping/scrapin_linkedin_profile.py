from dotenv import load_dotenv
import os
import requests
load_dotenv()
def scrape_profile(url: str, mock: bool = False):
    if mock:
        linkedin_profile = "https://gist.githubusercontent.com/emarco177/859ec7d786b45d8e3e3f688c6c9139d8/raw/5eaf8e46dc29a98612c8fe0c774123a7a2ac4575/eden-marco-scrapin.json"
        response = requests.get(linkedin_profile, timeout=10)
    else:
        api_endpoint = "https://api.scrapin.io/enrichment/profile"
        params = {
            "apikey": os.environ["SCRAPIN_API_KEY"],
            "linkedInUrl": url
        }
        response = requests.get(
            api_endpoint,
            params,
            timeout=10
        )
    data = response.json().get("person")
    print(data)
    return data
if __name__ == "__main__":
    print(scrape_profile(url="https://www.linkedin.com/in/eden-marco/", mock=True))