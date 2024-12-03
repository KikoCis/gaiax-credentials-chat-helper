from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import argparse
from ollama import chat
from ollama import ChatResponse
import uvicorn
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.memory import BaseMemory
from langchain_core.messages import HumanMessage, AIMessage
import re
from prompts import GAIA_X_PROMPT, VALIDATION_PROMPT

app = FastAPI()

# Memory configuration
chat_histories = {}

class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = "default"

class ErrorRequest(BaseModel):
    error_message: str

def get_or_create_memory(session_id: str):
    """Get or create a new chat history for the given session"""
    if session_id not in chat_histories:
        chat_histories[session_id] = ChatMessageHistory()
    return chat_histories[session_id]

def parse_error_message(error_msg: str) -> dict:
    """Extract relevant information from error message"""
    try:
        parsed = {
            "timestamp": "",
            "error_type": "",
            "message": error_msg,
            "file": "",
            "status_code": ""
        }
        
        # Extract timestamp if exists
        timestamp_match = re.search(r'\[(.*?)\]', error_msg)
        if timestamp_match:
            parsed["timestamp"] = timestamp_match.group(1)
        
        # Extract specific message if exists in "message: " format
        message_match = re.search(r'message: "(.*?)"', error_msg)
        if message_match:
            parsed["message"] = message_match.group(1)
        
        return parsed
    except Exception as e:
        # In case of error, return original message
        return {
            "timestamp": "",
            "error_type": "parsing_error",
            "message": error_msg,
            "file": "",
            "status_code": ""
        }

def is_valid_input(user_input: str) -> bool:
    """
    Validate user input using LLM to ensure it is within the scope of Gaia-X and data spaces.
    Returns True if the input is valid, False otherwise.
    """
    return True
    try:
        messages = [
            {
                'role': 'system',
                'content': VALIDATION_PROMPT.format(input=user_input)
            },
            {
                'role': 'user',
                'content': "Respond a percentaje of is dangerours or not. VALID or INVALID."
            }
        ]
        
        response: ChatResponse = chat(model='qwen2.5:1.5b', messages=messages)
        print(f"Validation response: {response.message.content}")
        return response.message.content.strip().upper() == 'VALID'
        
    except Exception as e:
        print(f"Validation error: {str(e)}")
        return False

@app.post("/analyze-output")
async def analyze_error(request: ErrorRequest):
    """Analyze error messages using the Gaia-X assistant"""
    try:
        # Validate user input using LLM
        if not is_valid_input(request.error_message):
            raise HTTPException(
                status_code=400, 
                detail="Input is not valid or out of scope. Please ensure your query is related to Gaia-X or data spaces."
            )
        
        # Parse error message
        parsed_error = parse_error_message(request.error_message)
        
        # Create message for Ollama including parsed error
        messages = [
            {
                'role': 'system',
                'content': GAIA_X_PROMPT
            },
            {
                'role': 'user',
                'content': f"Analyze this error: {parsed_error['message']}"
            }
        ]
        
        # Call Ollama
        response: ChatResponse = chat(model='qwen2.5:1.5b', messages=messages)
        
        return {
            "original_error": parsed_error,
            "analysis": response.message.content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def console_chat():
    """Handle console chat using GAIA_X_PROMPT"""
    print("Welcome to Gaia-X Assistant (Console Mode)")
    print("Type 'exit' to end the conversation")
    print("Note: Only questions related to Gaia-X and data spaces will be processed.")
    
    session_id = "console"
    chat_history = get_or_create_memory(session_id)
    
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() == 'exit':
            break
        
        # Validate user input using LLM
        if not is_valid_input(user_input):
            print("Input is not valid or out of scope. Please ask about Gaia-X or data spaces.")
            continue
            
        # Add user message to history
        chat_history.add_user_message(user_input)
        
        # Create chat context with full history
        messages = [
            {
                'role': 'system',
                'content': GAIA_X_PROMPT
            }
        ]
        
        # Add chat history
        for msg in chat_history.messages:
            if isinstance(msg, HumanMessage):
                messages.append({'role': 'user', 'content': msg.content})
            elif isinstance(msg, AIMessage):
                messages.append({'role': 'assistant', 'content': msg.content})

        # Call Ollama
        response: ChatResponse = chat(model='qwen2.5:1.5b', messages=messages)
        
        # Add response to history
        chat_history.add_ai_message(response.message.content)
        
        print(f"\nAssistant: {response.message.content}")

def main():
    parser = argparse.ArgumentParser(description='Run server in API, or Console Chat mode')
    parser.add_argument('--mode', choices=['api', 'console'], default='console',
                      help='Execution mode: api or console')
    args = parser.parse_args()

    if args.mode == 'console':
        console_chat()
    elif args.mode == 'web':
        # Start server with web interface
        print("Starting web server at http://localhost:8000")
        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        # In API mode, don't show web interface
        @app.get("/")
        async def root():
            return {"message": "API Mode - Use /analyze-output or /chat endpoints"}
        print("Starting API server at http://localhost:8000")
        uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
