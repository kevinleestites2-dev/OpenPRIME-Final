"""
AIlice - Simple Agent Factory for OpenPRIME
Creates specialized agents on demand without heavy dependencies
"""

class SpecializedAgent:
    def __init__(self, name, specialization, system_prompt, parent_agent):
        self.name = name
        self.specialization = specialization
        self.system_prompt = system_prompt
        self.parent = parent_agent
        self.memory = []
        self.tasks_completed = 0
    
    def execute(self, task):
        """Execute a task within this agent's specialization"""
        prompt = f"""You are {self.name}, a {self.specialization} specialist.
System prompt: {self.system_prompt}
Task: {task}
Execute with precision and return the result."""
        
        # Use parent agent's LLM client
        result = self.parent.llmclient.chat(prompt)
        self.tasks_completed += 1
        self.memory.append({"task": task, "result": result})
        return result
    
    def get_stats(self):
        return {
            "name": self.name,
            "specialization": self.specialization,
            "tasks_completed": self.tasks_completed,
            "memory_size": len(self.memory)
        }

class AgentFactory:
    def __init__(self, parent_agent):
        self.parent = parent_agent
        self.agents = {}
        print("🏭 Agent Factory initialized")
    
    def create_agent(self, name, specialization, system_prompt):
        """Create a new specialized agent"""
        if name in self.agents:
            return self.agents[name]
        
        agent = SpecializedAgent(name, specialization, system_prompt, self.parent)
        self.agents[name] = agent
        print(f"✅ Created agent: {name} ({specialization})")
        return agent
    
    def get_agent(self, name):
        return self.agents.get(name)
    
    def list_agents(self):
        return list(self.agents.keys())
    
    def delete_agent(self, name):
        if name in self.agents:
            del self.agents[name]
            print(f"🗑️ Deleted agent: {name}")
            return True
        return False
    
    def get_all_stats(self):
        return {name: agent.get_stats() for name, agent in self.agents.items()}

# Integration helper
def add_factory_to_agent(agent):
    if not hasattr(agent, 'factory'):
        agent.factory = AgentFactory(agent)
    return agent

print("✅ Agent Factory module loaded")
