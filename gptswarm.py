"""
GPTSwarm - Swarm Orchestration for OpenPRIME
Manages multiple agents working together on tasks
"""

class GPTSwarm:
    def __init__(self, factory):
        self.factory = factory
        self.active_swarms = {}
        print("🐝 GPTSwarm initialized")
    
    def create_swarm(self, swarm_name, agent_names, coordinator_prompt=None):
        """Create a swarm of agents working together"""
        agents = []
        for name in agent_names:
            agent = self.factory.get_agent(name)
            if agent:
                agents.append(agent)
            else:
                print(f"⚠️ Agent '{name}' not found")
        
        if len(agents) < 2:
            print("⚠️ Need at least 2 agents for a swarm")
            return None
        
        swarm = {
            "name": swarm_name,
            "agents": agents,
            "coordinator": coordinator_prompt or "Coordinate these agents to complete the task",
            "tasks": []
        }
        self.active_swarms[swarm_name] = swarm
        print(f"🐝 Swarm '{swarm_name}' created with {len(agents)} agents")
        return swarm
    
    def execute_parallel(self, swarm_name, task):
        """Execute a task using all agents in parallel"""
        if swarm_name not in self.active_swarms:
            return {"error": f"Swarm '{swarm_name}' not found"}
        
        swarm = self.active_swarms[swarm_name]
        results = {}
        
        for agent in swarm["agents"]:
            try:
                result = agent.execute(task)
                results[agent.name] = result
            except Exception as e:
                results[agent.name] = f"Error: {str(e)}"
        
        swarm["tasks"].append({"task": task, "results": results})
        return results
    
    def execute_collaborative(self, swarm_name, complex_task):
        """Break down complex task and assign to specialists"""
        if swarm_name not in self.active_swarms:
            return {"error": f"Swarm '{swarm_name}' not found"}
        
        swarm = self.active_swarms[swarm_name]
        
        # Coordinator breaks down the task
        breakdown_prompt = f"""Break this task into subtasks for these specialists: {[a.name for a in swarm['agents']]}
Task: {complex_task}
Return as a list of (specialist_name, subtask) pairs."""
        
        # Simple breakdown (can be enhanced)
        subtasks = [(swarm["agents"][0].name, complex_task)]
        
        results = {}
        for agent_name, subtask in subtasks:
            for agent in swarm["agents"]:
                if agent.name == agent_name:
                    results[agent_name] = agent.execute(subtask)
        
        return results
    
    def get_swarm_status(self, swarm_name):
        if swarm_name not in self.active_swarms:
            return None
        swarm = self.active_swarms[swarm_name]
        return {
            "name": swarm["name"],
            "agent_count": len(swarm["agents"]),
            "agent_names": [a.name for a in swarm["agents"]],
            "tasks_completed": len(swarm["tasks"])
        }

def add_swarm_to_agent(agent):
    if hasattr(agent, 'factory') and not hasattr(agent, 'swarm'):
        agent.swarm = GPTSwarm(agent.factory)
    return agent

print("✅ GPTSwarm module loaded")
