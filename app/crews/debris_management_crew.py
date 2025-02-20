import json
import os
from crewai import Crew, Task
from agents.debris_agents import DebrisManagementAgents
from crewai_tools import FileReadTool

class DebrisManagementCrew:
    def __init__(self):
        self.agents = DebrisManagementAgents()
        # Create output directory if it doesn't exist
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')
        os.makedirs(self.output_dir, exist_ok=True)

    def _safe_read_markdown(self, file_path):
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            return {"error": f"File not found: {os.path.basename(file_path)}"}
        except Exception as e:
            return {"error": f"Error reading file {os.path.basename(file_path)}: {str(e)}"}

    def analyze_debris(self, materials_data, debris_weight):
        try:
            if not materials_data or not isinstance(materials_data, list):
                raise ValueError("Invalid materials data format")
            
            # Validate each material in the list has required fields
            for material in materials_data:
                if not isinstance(material, dict) or 'name' not in material or 'weight' not in material:
                    raise ValueError("Each material must have 'name' and 'weight' fields")
                if not isinstance(material['weight'], (int, float)) or material['weight'] <= 0:
                    raise ValueError(f"Invalid weight for material {material['name']}")
            
            if not isinstance(debris_weight, (int, float)) or debris_weight <= 0:
                raise ValueError("Invalid debris weight")

            analyzer = self.agents.analyzer_agent()
            disposal_expert = self.agents.disposal_expert_agent()
            environmental_expert = self.agents.environmental_impact_agent()

            # Format materials for clear task description
            materials_list = ", ".join([f"{m['name']} ({m['weight']}kg)" for m in materials_data])

            # Initialize crew
            crew = Crew(
                agents=[analyzer, disposal_expert, environmental_expert],
                tasks=[],
                verbose=True
            )

            analysis_task = Task(
                description=f"""Analyze the construction debris weighing {debris_weight}kg.
                The debris contains ONLY the following materials: {materials_list}.
                Provide a detailed breakdown of the likely composition based STRICTLY on these materials.
                Focus your analysis ONLY on the listed materials.""",
                agent=analyzer,
                expected_output="A detailed analysis of debris composition based on provided materials and weight.",
                output_file=os.path.join(self.output_dir, "analysis.md")
            )

            file_reader_tool = FileReadTool()
            disposal_task = Task(
                description=f"""Based on the debris analysis in /output/analysis.md, provide specific disposal strategies for these materials: {materials_list}.
                Focus ONLY on the listed materials and their environmentally friendly disposal methods.
                For each material, provide:
                1. Recommended disposal method
                2. Recycling potential
                3. Special handling requirements""",
                agent=disposal_expert,
                expected_output="Specific disposal recommendations for each material type.",
                output_file=os.path.join(self.output_dir, "disposal_strategies.md"),
                tools=[file_reader_tool]
            )

            impact_task = Task(
                description=f"""Assess the environmental impact specifically for: {materials_list}.
                For each material:
                1. Calculate its environmental impact based on the total debris weight of {debris_weight}kg
                2. Suggest specific mitigation strategies
                3. Provide sustainability recommendations""",
                agent=environmental_expert,
                expected_output="Environmental impact assessment and mitigation strategies.",
                output_file=os.path.join(self.output_dir, "environmental_impact.md"),
                tools=[file_reader_tool]
            )

            # Add tasks to crew
            crew.tasks = [analysis_task, disposal_task, impact_task]

            # Execute crew tasks
            result = crew.kickoff()

            # Wait for a short time to ensure files are written
            import time
            time.sleep(2)

            # Collect and combine results from output files
            analysis_file = os.path.join(self.output_dir, "analysis.md")
            disposal_file = os.path.join(self.output_dir, "disposal_strategies.md")
            impact_file = os.path.join(self.output_dir, "environmental_impact.md")

            combined_results = {
                "crew_result": result,
                "analysis": self._safe_read_markdown(analysis_file),
                "disposal": self._safe_read_markdown(disposal_file),
                "environmental_impact": self._safe_read_markdown(impact_file)
            }

            return combined_results

        except Exception as e:
            raise Exception(f"Error in debris analysis: {str(e)}")

    def _safe_read_json(self, file_path):
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {"error": f"File not found: {os.path.basename(file_path)}"}
        except json.JSONDecodeError:
            return {"error": f"Invalid JSON in file: {os.path.basename(file_path)}"}
        except Exception as e:
            return {"error": f"Error reading file {os.path.basename(file_path)}: {str(e)}"}

        return results
