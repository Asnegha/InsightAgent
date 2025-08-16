import streamlit as st
import os
from crewai import Agent, Task, Crew
from dotenv import load_dotenv
import yaml
import litellm

# Load environment variables
load_dotenv()

# Set LiteLLM verbosity
litellm.set_verbose = True

# Load YAML configurations
def load_yaml_configs():
    files = {
        'agents': 'config/agents.yaml',
        'tasks': 'config/tasks.yaml'
    }
    configs = {}
    for config_type, file_path in files.items():
        with open(file_path, 'r') as file:
            configs[config_type] = yaml.safe_load(file)
    return configs['agents'], configs['tasks']

# Create and run Crew
def run_crew():
    agents_config, tasks_config = load_yaml_configs()
    chart_generation_agent = Agent(
        config=agents_config['chart_generation_agent'],
        allow_code_execution=True
    )
    chart_generation = Task(
        config=tasks_config['chart_generation'],
        agent=chart_generation_agent
    )
    support_report_crew = Crew(
        agents=[chart_generation_agent],
        tasks=[chart_generation],
        verbose=True
    )
    support_report_crew.test(n_iterations=1, openai_model_name='gpt-4o')

# Streamlit UI
st.title("InsightAgent")
if st.button("Generate Graphs"):
    st.info("Running CrewAI agent to generate graphs...")
    run_crew()
    st.success("Graph generation complete.")

    # Display image files in the current directory
    image_files = [f for f in os.listdir('.') if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if image_files:
        for img_file in image_files:
            st.image(img_file, caption=img_file)
    else:
        st.warning("No image files found in the current directory.")
