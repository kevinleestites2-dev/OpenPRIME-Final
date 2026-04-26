import os

# Read agentmain.py
with open('agentmain.py', 'r') as f:
    content = f.read()

# Add imports if not present
if 'from superintelligence import Superintelligence' not in content:
    # Find location to add imports (after existing imports)
    lines = content.split('\n')
    insert_pos = 0
    for i, line in enumerate(lines):
        if line.startswith('from llmcore import') or line.startswith('from agent_loop import'):
            insert_pos = i + 1
    
    lines.insert(insert_pos, 'from superintelligence import Superintelligence')
    lines.insert(insert_pos + 1, 'from supermemory_bridge import openprime_memory')
    content = '\n'.join(lines)

# Add superintelligence to GeneraticAgent.__init__
if 'self.si =' not in content:
    content = content.replace(
        'self.llmclient = self.llmclients[self.llm_no]',
        'self.llmclient = self.llmclients[self.llm_no]\n        self.si = Superintelligence()\n        self.memory = openprime_memory'
    )

# Write back
with open('agentmain.py', 'w') as f:
    f.write(content)

print("✅ Superintelligence added to agentmain.py")
