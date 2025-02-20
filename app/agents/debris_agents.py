from crewai import Agent,LLM

llm  = LLM(
    model="openai/mistralai/mistral-small-24b-instruct-2501:free",
    temperature=0.2,
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
)

class DebrisManagementAgents:
    def analyzer_agent(self):
        return Agent(
            role='Debris Analysis Expert',
            goal='Analyze construction debris composition and provide detailed breakdown',
            backstory="""You are an expert in construction waste analysis with years of 
            experience in identifying material compositions and their environmental impact.""",
            verbose=True,
            llm=llm
        )

    def disposal_expert_agent(self):
        return Agent(
            role='Disposal Strategy Expert',
            goal='Develop environmentally friendly disposal strategies',
            backstory="""You are a specialist in sustainable waste management with deep 
            knowledge of recycling and disposal methods for construction materials.""",
            verbose=True,
             llm=llm
        )

    def environmental_impact_agent(self):
        return Agent(
            role='Environmental Impact Assessor',
            goal='Assess environmental impact and suggest mitigation strategies',
            backstory="""You are an environmental scientist specialized in construction 
            waste impact assessment and sustainability practices.""",
            verbose=True,
             llm=llm
        )