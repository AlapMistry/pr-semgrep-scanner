import json
import portia_agent
import asyncio

from quart import Quart, request, Response, render_template
from http import HTTPStatus

app = Quart(__name__)

@app.route('/', methods=['GET'])
async def home():
    return await render_template('index.html')

@app.route('/', methods=['POST'])
async def scan_pull_request():
    payload = await request.get_json()
    
    try:
        # Parse the content which now contains both repository and PR number
        content = json.loads(payload['messages'][1].get('content'))
        repository = content.get('repository', '')
        pull_request_id = content.get('prNumber', '')
        
        # Validate repository format
        if not repository or '/' not in repository:
            raise ValueError("Repository must be in the format 'user/reponame'")
        
        # Validate that pull_request_id is a number
        pull_request_id = int(pull_request_id)
        if pull_request_id <= 0:
            raise ValueError("PR ID must be a positive integer")
    except json.JSONDecodeError:
        return Response("Error: Invalid request format", status=400)
    except (ValueError, TypeError) as e:
        return Response(f"Error: {str(e)}", status=400)
    
    print(f"Repository: {repository}, PR ID: {pull_request_id}")

    async def stream():
        # Initial response to ensure connection is established
        yield "Processing started...\n"
        
        try:
            # Stream each chunk from portia agent
            for chunk in portia_agent.run_portia(repository, pull_request_id):
                yield chunk
                # Small delay to allow chunks to be processed
                await asyncio.sleep(0.01)
            
            # Add a final end message to properly close the stream
            yield "\n✅ Analysis complete.\n"
        except Exception as e:
            yield f"\nError: An unexpected error occurred: {str(e)}\n"
            yield "Please check your network connection, API credentials, and try again.\n"
            yield "\n❌ Analysis failed.\n"

    return Response(
        stream(),
        status=HTTPStatus.OK,
        mimetype='text/plain',
        # Ensure no buffering at HTTP level and proper stream handling
        headers={
            'X-Accel-Buffering': 'no',
            'Cache-Control': 'no-cache, no-transform',
            'Transfer-Encoding': 'chunked',
            'Connection': 'keep-alive'
        }
    )
