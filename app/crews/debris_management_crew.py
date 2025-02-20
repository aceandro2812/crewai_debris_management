from crewai import Crew, Task
from agents.debris_agents import DebrisManagementAgents

class DebrisManagementCrew:
    def __init__(self):
        self.agents = DebrisManagementAgents()

    def analyze_debris(self, materials_data, debris_weight):
        analyzer = self.agents.analyzer_agent()
        disposal_expert = self.agents.disposal_expert_agent()
        environmental_expert = self.agents.environmental_impact_agent()

        analysis_task = Task(
            description=f"""Analyze the construction debris weighing {debris_weight}kg 
            considering the following materials used: {materials_data}. 
            Provide a detailed breakdown of likely debris composition.""",
            agent=analyzer,
            expected_output="A detailed analysis of debris composition based on provided materials and weight.")

        disposal_task = Task(
            description="""Based on the debris analysis, recommend environmentally 
            friendly disposal strategies for each type of material.""",
            agent=disposal_expert,
            expected_output="Environmentally friendly disposal recommendations for each material type."

        impact_task = Task(
            description="""Assess the environmental impact of the debris and suggest 
            mitigation strategies for sustainable disposal.""",
            agent=environmental_expert,
            expected_output="Environmental impact assessment and mitigation strategies for sustainable disposal."

        crew = Crew(
            agents=[analyzer, disposal_expert, environmental_expert],
            tasks=[analysis_task, disposal_task, impact_task],
            verbose=True
        )

        result = crew.kickoff()
        return result