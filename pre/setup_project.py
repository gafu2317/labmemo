import os

# プロジェクトのディレクトリ構成定義
structure = {
    "argument_mining": {
        ".env": "OPENAI_API_KEY=sk-...",
        "requirements.txt": """openai
streamlit
pydantic
python-dotenv
streamlit-mermaid
""",
        "main.py": """import streamlit as st
# Step 3でUIを実装します
def main():
    st.title("Argument Structure Miner")
    st.write("設定完了！ここにUIを作っていきます。")

if __name__ == "__main__":
    main()
""",
        "data": {
            "samples": {
                "01_tech_meeting.txt": """田中: 次のプロジェクトの言語は何にする？
佐藤: Pythonがいいと思います。ライブラリが豊富なので。
鈴木: でも実行速度が心配です。Go言語はどうですか？
田中: 確かに速度は大事だね。今回はGoでいきましょう。"""
            }
        },
        "src": {
            "__init__.py": "",
            "models.py": """from typing import List, Optional
from pydantic import BaseModel

class Node(BaseModel):
    id: str
    type: str       # issue, position, argument, decision
    content: str
    speaker: Optional[str] = None

class Edge(BaseModel):
    source: str
    target: str
    label: str      # supports, opposes, replies_to

class ArgumentGraph(BaseModel):
    nodes: List[Node]
    edges: List[Edge]
""",
            "llm.py": """class LLMClient:
    def __init__(self):
        pass
    
    def fetch_json(self, system_prompt: str, user_text: str) -> str:
        # Step 2でOpenAI API呼び出しを実装します
        return "{}" 
""",
            "visualizer.py": """from src.models import ArgumentGraph

class MermaidGenerator:
    @staticmethod
    def generate(graph: ArgumentGraph) -> str:
        # Step 2でグラフ変換ロジックを実装します
        return "graph TD\\n A[Start] --> B[End]"
""",
            "strategies": {
                "__init__.py": "",
                "base.py": """from abc import ABC, abstractmethod
from src.models import ArgumentGraph

class MiningStrategy(ABC):
    @abstractmethod
    def analyze(self, text: str) -> ArgumentGraph:
        pass
""",
                "ibis.py": """from src.strategies.base import MiningStrategy
from src.models import ArgumentGraph, Node, Edge

class IBISStrategy(MiningStrategy):
    def analyze(self, text: str) -> ArgumentGraph:
        # Step 2で具体的な抽出ロジックを実装します
        print(f"IBIS Strategy analyzing: {text[:10]}...")
        return ArgumentGraph(nodes=[], edges=[])
""",
                "toulmin.py": """from src.strategies.base import MiningStrategy
from src.models import ArgumentGraph

class ToulminStrategy(MiningStrategy):
    def analyze(self, text: str) -> ArgumentGraph:
        # 将来的な拡張用
        return ArgumentGraph(nodes=[], edges=[])
"""
            }
        }
    }
}

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        
        if isinstance(content, dict):
            # ディレクトリの場合
            os.makedirs(path, exist_ok=True)
            print(f"Created directory: {path}")
            create_structure(path, content)
        else:
            # ファイルの場合
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Created file: {path}")

if __name__ == "__main__":
    print("Generating project structure...")
    create_structure(".", structure)
    print("\\nDone! プロジェクトフォルダ 'argument_mining' が作成されました。")