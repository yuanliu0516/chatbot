import requests
from bs4 import BeautifulSoup
import openai
import pandas as pd

# 设置 OpenAI API 密钥
openai.api_key = "your-api-key"  # 替换为你的实际 OpenAI API 密钥

# 设置目标 URL
url = "https://example.com"  # 替换为你需要爬取的页面 URL

# 1. 爬取页面数据
def scrape_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text()
        return text.strip()
    except Exception as e:
        print(f"Error scraping page: {e}")
        return None

# 2. 生成 embedding
def generate_embedding(text):
    try:
        response = openai.Embedding.create(
            model="text-embedding-ada-002",  # OpenAI 提供的文本嵌入模型
            input=text
        )
        embedding = response["data"][0]["embedding"]
        return embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None

# 3. 保存数据到 CSV
def save_to_csv(data, filename="qa_demo.csv"):
    try:
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

# 主逻辑
def main():
    # 检查是否已有现成的 CSV 文件
    filename = "qa_demo.csv"
    try:
        existing_data = pd.read_csv(filename)
        print(f"{filename} already exists. No need to regenerate embeddings.")
        print(existing_data.head())
    except FileNotFoundError:
        print(f"{filename} not found. Generating new embeddings...")

        # 爬取页面
        text = scrape_page(url)
        if text is None:
            print("Failed to scrape the page.")
            return

        # 生成 embedding
        embedding = generate_embedding(text)
        if embedding is None:
            print("Failed to generate embedding.")
            return

        # 保存到 CSV
        data = {"text": [text], "embedding": [embedding]}
        save_to_csv(data, filename)

# 执行主函数
if __name__ == "__main__":
    main()
