"""
SAFLA - Self-Adaptive Feedback Learning Architecture
Oracle feedback loop that learns from outcomes
"""

class SAFLA:
    def __init__(self, agent):
        self.agent = agent
        self.feedback_history = []
        self.performance_scores = {}
        self.adaptation_rules = []
        print("🔮 SAFLA Oracle initialized")
    
    def evaluate_outcome(self, task, result, expected=None):
        """Evaluate the quality of an outcome"""
        score = {
            "task": task,
            "result": result[:100] if isinstance(result, str) else str(result)[:100],
            "timestamp": None,  # Would add datetime if available
            "score": 0
        }
        
        # Simple scoring (can be enhanced with LLM)
        if expected and expected in result:
            score["score"] = 100
        elif len(result) > 50:
            score["score"] = 70
        else:
            score["score"] = 50
        
        self.feedback_history.append(score)
        
        # Track performance by agent/specialization
        if "specialization" in str(task):
            spec = task.split()[:1]
            spec_key = str(spec)
            if spec_key not in self.performance_scores:
                self.performance_scores[spec_key] = []
            self.performance_scores[spec_key].append(score["score"])
        
        print(f"📊 Outcome evaluated: score={score['score']}")
        return score
    
    def analyze_performance(self):
        """Analyze performance and suggest adaptations"""
        analysis = {}
        for spec, scores in self.performance_scores.items():
            if scores:
                avg_score = sum(scores) / len(scores)
                analysis[spec] = {
                    "average_score": avg_score,
                    "sample_count": len(scores),
                    "trend": "improving" if len(scores) > 1 and scores[-1] > scores[-2] else "stable"
                }
        return analysis
    
    def suggest_improvement(self, task_type):
        """Suggest improvements based on historical feedback"""
        analysis = self.analyze_performance()
        
        if task_type in analysis:
            avg = analysis[task_type]["average_score"]
            if avg < 60:
                return f"⚠️ Low performance on {task_type} (avg={avg}). Consider adjusting prompts or adding specialized training."
            elif avg < 80:
                return f"📈 Moderate performance on {task_type} (avg={avg}). Could benefit from refinement."
            else:
                return f"✅ Strong performance on {task_type} (avg={avg}). Maintain current approach."
        else:
            return f"🆕 No historical data for {task_type}. First attempt recommended."
    
    def get_feedback_summary(self):
        """Get summary of all feedback"""
        if not self.feedback_history:
            return "No feedback recorded yet."
        
        avg_score = sum(f["score"] for f in self.feedback_history) / len(self.feedback_history)
        return {
            "total_evaluations": len(self.feedback_history),
            "average_score": avg_score,
            "performance_by_area": self.analyze_performance()
        }

def add_safla_to_agent(agent):
    if not hasattr(agent, 'safla'):
        agent.safla = SAFLA(agent)
    return agent

print("✅ SAFLA Oracle module loaded")
