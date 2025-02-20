from crewai import Agent

class DebrisManagementAgents:
    def analyzer_agent(self):
        return Agent(
            role='Debris Analysis Expert',
            goal='Analyze construction debris composition and provide detailed breakdown',
            backstory="""You are an expert in construction waste analysis with years of 
            experience in identifying material compositions and their environmental impact.""",
            verbose=True
        )

    def disposal_expert_agent(self):
        return Agent(
            role='Disposal Strategy Expert',
            goal='Develop environmentally friendly disposal strategies',
            backstory="""You are a specialist in sustainable waste management with deep 
            knowledge of recycling and disposal methods for construction materials.""",
            verbose=True
        )

    def environmental_impact_agent(self):
        return Agent(
            role='Environmental Impact Assessor',
            goal='Assess environmental impact and suggest mitigation strategies',
            backstory="""You are an environmental scientist specialized in construction 
            waste impact assessment and sustainability practices.""",
            verbose=True
        )