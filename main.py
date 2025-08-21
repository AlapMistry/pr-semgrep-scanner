# Use semgrep rules to find format issue in GitHub repo and create issue to resolve it
import os
from dotenv import load_dotenv
from portia import (
    Portia,
    Config,
    StorageClass,
    PortiaToolRegistry
)
from portia.cli import CLIExecutionHooks

load_dotenv()

GITHUB_PERSONAL_ACCESS_TOKEN = os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN')
branch = input("Enter branch name to create: ")

config = Config.from_default(
    #default_log_level=LogLevel.DEBUG,
    storage_class=StorageClass.DISK,
    storage_dir='demo_runs',
)

tool_registry = (PortiaToolRegistry(config))

# Instantiate a Portia instance. Load it with the config and with the tools.
portia = Portia(
    config=config,
    tools=tool_registry,
    execution_hooks=CLIExecutionHooks()
)

task = f"""
1. Get branches in GitHub repository AlapMistry/spring-boot-demo
2. Create a branch {branch} on that repo if not available
"""

plan_run = portia.run(
    task,
    tools=[
        "portia:mcp:api.githubcopilot.com:list_branches",
        "portia:mcp:api.githubcopilot.com:create_branch"
    ]
)

print(plan_run.outputs.final_output)
