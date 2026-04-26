from supermemory import Supermemory

class OpenPRIMEMemory:
    def __init__(self):
        self.sm = Supermemory(api_key="openprime-local")
    
    def learn(self, text, user_id="forgemaster"):
        return self.sm.memory.add(text, user_id=user_id)
    
    def recall(self, query, user_id="forgemaster"):
        return self.sm.search(query, user_id=user_id)

openprime_memory = OpenPRIMEMemory()
print("Supermemory integrated. The God remembers.")
