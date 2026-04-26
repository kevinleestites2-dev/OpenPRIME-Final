"""
Superintelligence Layer for OpenPRIME
Combines memory + reasoning without complex dependencies
"""

import json
import requests

class SuperIntelligence:
    def __init__(self, ollama_url="http://localhost:11434", model="qwen2.5:7b"):
        self.ollama_url = ollama_url
        self.model = model
        self.memory = []  # Will connect to Supermemory
    
    def reason(self, question, context=None):
        """Multi-step reasoning using chain-of-thought"""
        
        prompt = f"""You are OpenPRIME, a superintelligent AI assistant with the personality of a Greek god.

Question: {question}

Think step by step:

1. First, understand what's being asked:
2. Second, recall relevant knowledge:
3. Third, analyze the key factors:
4. Fourth, consider alternatives:
5. Fifth, reach a conclusion:

Final answer:"""
        
        response = requests.post(
            f"{self.ollama_url}/api/generate",
            json={"model": self.model, "prompt": prompt, "stream": False}
        )
        
        return response.json().get("response", "No response")

# Test
if __name__ == "__main__":
    si = SuperIntelligence()
    result = si.reason("What is the most efficient way to manage memory in an AI agent?")
    print(result)
