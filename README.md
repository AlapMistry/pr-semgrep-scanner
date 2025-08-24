# PR Semgrep Scanner using Portia SDK Python

A web application that uses Portia SDK Python and Semgrep to scan GitHub Pull Requests for security vulnerabilities.

## Overview

This project demonstrates the use of Portia SDK Python to create an intelligent agent that can:
1. Retrieve GitHub Pull Request information 
2. Analyze code changes using Semgrep
3. Identify potential security vulnerabilities
4. Provide security insights through a real-time web interface

## Features

- **Web Interface**: Simple UI for entering repository name and PR number
- **GitHub Integration**: Fetches PR details and code diffs
- **Security Scanning**: Uses Semgrep to find security vulnerabilities
- **Real-time Analysis**: Streams results as they become available
- **Plan Persistence**: Stores execution plans for future reference and analysis

## Setup

### Prerequisites

- Python 3.13 or higher
- Portia API key
- Google API Key for Google AI Studio
- GitHub Personal Access Token with read access of contents and pull requests
- GitHub MCP and Semgrep MCP enabled in Portia

### Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with the following variables (see `.env.example` for a template):
   ```
   PORT=4000
   DEVELOPMENT=True
   PORTIA_API_KEY=your-portia-api-key
   GOOGLE_API_KEY=your-google-api-key
   ```

### Running the Application

#### Option 1: Direct Python Execution

Run the application with:
```
python start_server.py
```

#### Option 2: Using Docker

The application is containerized and can be run with Docker:

1. Build and start the container:
```
docker-compose up -d
```

2. View logs:
```
docker-compose logs -f
```

3. Stop the container:
```
docker-compose down
```

The application will be available at http://localhost:4000 by default. You can change the port by setting the `PORT` environment variable in your .env file.

## How it Works

1. User submits a GitHub repository name and PR number through the web interface
2. The application validates the input and formats a task for the Portia agent
3. Portia agent executes a multi-step process:
   - Get PR information from GitHub
   - Retrieve the diff of all changed files
   - Run Semgrep scan on the code changes
   - Perform a security check for potential vulnerabilities
4. Results are streamed back to the web UI in real-time as they become available
5. Plan execution details are stored in the `demo_runs` directory

## Tools Used

- **Portia AI**: Framework for creating transparent, steerable AI agents
- **Google AI Studio**: To use Google AI models using Google API key
- **Semgrep**: Static analysis tool for finding security vulnerabilities
- **Quart**: Asynchronous web framework for Python
- **Hypercorn**: ASGI server for running the web application
- **python-dotenv**: For environment variable management

## Portia Features Demonstrated

- Plan creation and execution
- Tool integration (GitHub, Semgrep)
- Streaming results from AI agent to web UI
- Storage of plan runs for later analysis (in `demo_runs` directory)
- Multi-step reasoning for complex security analysis tasks
- Error handling and graceful degradation

## Portia Tools Used

- GitHub MCP
- Semgrep MCP

## Technical Implementation

- **Asynchronous Processing**: Uses asyncio and Quart for non-blocking operations
- **Streaming Responses**: Implements server-sent events for real-time updates
- **Persistent Storage**: Stores execution plans in JSON format
- **User-friendly Interface**: Clean web UI for easy input and result viewing
- **Error Handling**: Robust error handling for network issues and invalid inputs

## Further Improvements

- Add authentication for the web interface
- Add support for custom Semgrep rules
- Support for scanning private repositories
- Run agent from GitHub Copilot chat as extension as stream response in a real time

## Resources

- [Portia SDK Python Documentation](https://docs.portialabs.ai/)
- [Google AI Studio](https://aistudio.google.com/)
- [GitHub MCP Server Documentation](https://github.com/github/github-mcp-server)
- [Semgrep MCP Server Documentation](https://github.com/semgrep/mcp)
- [Quart Documentation](https://pgjones.gitlab.io/quart/)
