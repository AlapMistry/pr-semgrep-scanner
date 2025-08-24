import os
import time

from dotenv import load_dotenv
from portia import (
    Portia,
    Config,
    StorageClass,
    PortiaToolRegistry,
    LogLevel,
    LLMProvider,
)
from portia.cli import CLIExecutionHooks

def run_portia(repository, pull_request_id):
    yield "Starting Portia agent...\n"

    # Load environment variables from .env file
    load_dotenv()

    config = create_portia_config()
    tool_registry = create_tool_registry(config)
    portia = create_portia_instance(config, tool_registry)
    
    # Create the task based on repository and PR ID
    task = create_task(repository, pull_request_id)
    yield f"Analyzing PR #{pull_request_id} in repository {repository} with Semgrep...\n\n"
    
    # Define the tools we'll use
    tools = [
        "portia:mcp:api.githubcopilot.com:get_pull_request",
        "portia:mcp:api.githubcopilot.com:get_pull_request_diff",
        "portia:mcp:mcp.semgrep.ai:semgrep_scan",
        "portia:mcp:mcp.semgrep.ai:security_check"
    ]

    # Create the plan first
    yield "📝 Creating plan\n"
    plan = portia.plan(task, tools=tools)
    yield f"✅ Created plan\n"

    yield "\n🚀 Starting execution...\n"

    # Now execute the plan with progress indicators
    yield "⏳ Processing... this may take a minute or two...\n"
    
    try:
        plan_run = portia.run_plan(plan)
        yield f"🔍 Result:\n{plan_run.outputs.final_output.get_summary()}"
        # Add a small pause before ending to ensure the stream completes properly
        time.sleep(0.1)  # Small delay to ensure the final chunk is transmitted
    except Exception as e:
        yield f"Error during plan execution: {str(e)}\n"
        yield "Please check your network connection and API credentials."

def create_portia_config():
    storage_class = StorageClass.DISK
    storage_dir = 'demo_runs'
    DEVELOPMENT_MODE = os.getenv('DEVELOPMENT_MODE')
    if not DEVELOPMENT_MODE:
        storage_class = StorageClass.CLOUD
        storage_dir=None

    PORTIA_API_KEY = os.getenv('PORTIA_API_KEY')
    if not PORTIA_API_KEY:
        print("Warning: PORTIA_API_KEY not set in environment variables")

    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    config = Config.from_default(
        llm_provider=LLMProvider.GOOGLE,
        default_model="google/gemini-2.0-flash",
        google_api_key=GOOGLE_API_KEY,
        default_log_level=LogLevel.INFO,
        storage_class=storage_class,
        storage_dir=storage_dir,
        api_key=PORTIA_API_KEY,
        request_timeout=60,
    )

    return config

def create_tool_registry(config):
    tool_registry = PortiaToolRegistry(config)
    return tool_registry

def create_portia_instance(config, tool_registry):
    # Instantiate a Portia instance with the provided config and tools
    portia = Portia(
        config=config,
        tools=tool_registry,
        execution_hooks=CLIExecutionHooks()
    )
    return portia

def create_task(repository, pull_request_id):
    # Define the task with more detailed instructions for better results
    task = f"""
    Perform a comprehensive security analysis of pull request #{pull_request_id} in the GitHub repository {repository}:

    1. First, get the pull request metadata to understand what changes it contains
    2. Retrieve the diff of all changed files in the pull request
    3. Run a Semgrep security scan on the changed files to identify potential security issues
    4. Perform a fast security check to find any additional concerns
    """
    return task
