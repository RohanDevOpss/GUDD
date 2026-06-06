"""
Main Flask application with ChatGPT integration
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


if __name__ == '__main__':
    debug_mode = os.getenv('DEBUG', 'False') == 'True'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
