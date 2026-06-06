"""
Main Flask application with ChatGPT integration
Enhanced with file operations and code execution
"""

from flask import Flask, request, jsonify
from chatgpt_integration import initialize_chatgpt
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Initialize ChatGPT
try:
    chatgpt = initialize_chatgpt()
except ValueError as e:
    print(f"Warning: {e}")
    chatgpt = None


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200


@app.route('/chat', methods=['POST'])
def chat():
    """
    Chat endpoint
    Expected JSON: {"message": "your message here"}
    """
    if not chatgpt:
        return jsonify({"error": "ChatGPT not initialized"}), 500
    
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({"error": "Message field is required"}), 400
        
        user_message = data.get('message')
        system_prompt = data.get('system_prompt', None)
        
        response = chatgpt.ask_question(user_message, system_prompt)
        
        return jsonify({
            "message": user_message,
            "response": response
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/conversation', methods=['POST'])
def conversation():
    """
    Conversation endpoint for multi-turn conversations
    Expected JSON: {"messages": [{"role": "user/assistant", "content": "..."}]}
    """
    if not chatgpt:
        return jsonify({"error": "ChatGPT not initialized"}), 500
    
    try:
        data = request.get_json()
        
        if not data or 'messages' not in data:
            return jsonify({"error": "Messages field is required"}), 400
        
        messages = data.get('messages')
        response = chatgpt.conversation(messages)
        
        return jsonify({
            "response": response,
            "message_count": len(messages)
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/generate', methods=['POST'])
def generate():
    """
    Text generation endpoint
    Expected JSON: {"prompt": "your prompt here", "max_tokens": 500}
    """
    if not chatgpt:
        return jsonify({"error": "ChatGPT not initialized"}), 500
    
    try:
        data = request.get_json()
        
        if not data or 'prompt' not in data:
            return jsonify({"error": "Prompt field is required"}), 400
        
        prompt = data.get('prompt')
        max_tokens = data.get('max_tokens', 500)
        
        response = chatgpt.generate_text(prompt, max_tokens)
        
        return jsonify({
            "prompt": prompt,
            "generated_text": response
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============== FILE OPERATIONS ==============

@app.route('/file/read', methods=['POST'])
def read_file():
    """
    Read file endpoint
    Expected JSON: {"file_path": "path/to/file"}
    """
    if not chatgpt:
        return jsonify({"error": "ChatGPT not initialized"}), 500
    
    try:
        data = request.get_json()
        
        if not data or 'file_path' not in data:
            return jsonify({"error": "file_path field is required"}), 400
        
        file_path = data.get('file_path')
        content = chatgpt.read_file(file_path)
        
        return jsonify({
            "status": "success",
            "file_path": file_path,
            "content": content
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/file/write', methods=['POST'])
def write_file():
    """
    Write file endpoint
    Expected JSON: {"file_path": "path/to/file", "content": "...", "append": false}
    """
    if not chatgpt:
        return jsonify({"error": "ChatGPT not initialized"}), 500
    
    try:
        data = request.get_json()
        
        if not data or 'file_path' not in data or 'content' not in data:
            return jsonify({"error": "file_path and content fields are required"}), 400
        
        file_path = data.get('file_path')
        content = data.get('content')
        append = data.get('append', False)
        
        result = chatgpt.write_file(file_path, content, append)
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/file/delete', methods=['POST'])
def delete_file():
    """
    Delete file endpoint
    Expected JSON: {"file_path": "path/to/file"}
    """
    if not chatgpt:
        return jsonify({"error": "ChatGPT not initialized"}), 500
    
    try:
        data = request.get_json()
        
        if not data or 'file_path' not in data:
            return jsonify({"error": "file_path field is required"}), 400
        
        file_path = data.get('file_path')
        result = chatgpt.delete_file(file_path)
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/file/list', methods=['POST'])
def list_files():
    """
    List files endpoint
    Expected JSON: {"directory": "."}
    """
    if not chatgpt:
        return jsonify({"error": "ChatGPT not initialized"}), 500
    
    try:
        data = request.get_json() or {}
        directory = data.get('directory', '.')
        
        files = chatgpt.list_files(directory)
        
        return jsonify({
            "status": "success",
            "directory": directory,
            "files": files,
            "count": len(files)
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============== CODE EXECUTION ==============

@app.route('/execute', methods=['POST'])
def execute_code():
    """
    Execute code endpoint
    Expected JSON: {"code": "...", "language": "python", "timeout": 30}
    """
    if not chatgpt:
        return jsonify({"error": "ChatGPT not initialized"}), 500
    
    try:
        data = request.get_json()
        
        if not data or 'code' not in data:
            return jsonify({"error": "code field is required"}), 400
        
        code = data.get('code')
        language = data.get('language', 'python')
        timeout = data.get('timeout', 30)
        
        result = chatgpt.execute_code(code, language, timeout)
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/execute/python', methods=['POST'])
def execute_python():
    """
    Execute Python code endpoint (shortcut)
    Expected JSON: {"code": "...", "timeout": 30}
    """
    if not chatgpt:
        return jsonify({"error": "ChatGPT not initialized"}), 500
    
    try:
        data = request.get_json()
        
        if not data or 'code' not in data:
            return jsonify({"error": "code field is required"}), 400
        
        code = data.get('code')
        timeout = data.get('timeout', 30)
        
        result = chatgpt.execute_code(code, 'python', timeout)
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/execute/bash', methods=['POST'])
def execute_bash():
    """
    Execute Bash code endpoint (shortcut)
    Expected JSON: {"code": "...", "timeout": 30}
    """
    if not chatgpt:
        return jsonify({"error": "ChatGPT not initialized"}), 500
    
    try:
        data = request.get_json()
        
        if not data or 'code' not in data:
            return jsonify({"error": "code field is required"}), 400
        
        code = data.get('code')
        timeout = data.get('timeout', 30)
        
        result = chatgpt.execute_code(code, 'bash', timeout)
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    debug_mode = os.getenv('DEBUG', 'False') == 'True'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
