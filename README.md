# GUDD - ChatGPT Integration

A Flask-based application that integrates OpenAI's ChatGPT API for intelligent conversational responses with file operations and code execution capabilities.

## Features

- 🤖 ChatGPT API Integration
- 💬 Single-turn and multi-turn conversations
- 📝 Text generation capabilities
- 📖 File Read operations
- ✍️ File Write operations
- 🗑️ File Delete operations
- 📋 List files in workspace
- ⚙️ Execute Python and Bash code
- 🔌 RESTful API endpoints
- 🔐 Environment-based configuration
- 📊 Health check endpoint
- 🔒 Path validation and security

## Prerequisites

- Python 3.8+
- OpenAI API key with GPT access (get from [platform.openai.com](https://platform.openai.com))

## OpenAI API Key Setup

### Getting Your API Key

1. Visit [OpenAI Platform](https://platform.openai.com)
2. Sign up or log in to your account
3. Go to **API Keys** section
4. Click **Create new secret key**
5. Copy the key (starts with `sk-`)
6. **Important**: Keep this key secret and never commit it to version control

### Checking API Access

Make sure your API key has access to:
- ✅ ChatGPT models (gpt-3.5-turbo, gpt-4, etc.)
- ✅ Text completion endpoints
- ✅ Active billing or free trial credits

### Troubleshooting 403 Error

If you get a **403 — Resource not accessible by integration** error:

1. **Verify API Key**
   - Go to [platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)
   - Confirm your key is active and not revoked
   - Try creating a new API key if the current one is old

2. **Check Billing**
   - Visit [Usage](https://platform.openai.com/account/billing/usage)
   - Ensure you have available credits or valid payment method
   - Free trial may have expired

3. **Verify Model Access**
   - Ensure your account has access to the model in `.env`
   - Default is `gpt-3.5-turbo` (most accounts have access)
   - Try using `gpt-3.5-turbo` instead of `gpt-4` if you don't have access

4. **Check Organization**
   - If using organization API keys, verify permissions
   - Go to [settings/organization/api-keys](https://platform.openai.com/settings/organization/api-keys)

5. **Rate Limiting**
   - If you're hitting rate limits, wait a moment before retrying
   - Check [Usage dashboard](https://platform.openai.com/account/billing/usage) for limits

## Installation

1. Clone the repository:
```bash
git clone https://github.com/RohanDevOpss/GUDD.git
cd GUDD
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
cp .env.example .env
```

5. Add your OpenAI API key to `.env`:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
OPENAI_MODEL=gpt-3.5-turbo
DEBUG=False
WORK_DIRECTORY=./workspace
```

## Usage

### Running the Flask App

```bash
python app.py
```

The app will run on `http://localhost:5000`

### API Endpoints

#### 1. Health Check
```bash
GET /health
```

Response:
```json
{"status": "healthy"}
```

#### 2. Single Message Chat
```bash
POST /chat
Content-Type: application/json

{
  "message": "Hello, how are you?",
  "system_prompt": "You are a helpful assistant"
}
```

Response:
```json
{
  "message": "Hello, how are you?",
  "response": "I'm doing well, thank you for asking!"
}
```

#### 3. Multi-turn Conversation
```bash
POST /conversation
Content-Type: application/json

{
  "messages": [
    {"role": "user", "content": "What is Python?"},
    {"role": "assistant", "content": "Python is a programming language..."},
    {"role": "user", "content": "Tell me more"}
  ]
}
```

Response:
```json
{
  "response": "Python is versatile...",
  "message_count": 3
}
```

#### 4. Text Generation
```bash
POST /generate
Content-Type: application/json

{
  "prompt": "Write a haiku about programming",
  "max_tokens": 500
}
```

Response:
```json
{
  "prompt": "Write a haiku about programming",
  "generated_text": "Code flows like water..."
}
```

#### 5. Read File
```bash
POST /file/read
Content-Type: application/json

{
  "file_path": "test.txt"
}
```

Response:
```json
{
  "status": "success",
  "file_path": "test.txt",
  "content": "File contents here"
}
```

#### 6. Write File
```bash
POST /file/write
Content-Type: application/json

{
  "file_path": "output.txt",
  "content": "Hello from ChatGPT!",
  "append": false
}
```

Response:
```json
{
  "status": "success",
  "file_path": "output.txt",
  "mode": "write",
  "size": 21,
  "full_path": "/path/to/workspace/output.txt"
}
```

#### 7. Delete File
```bash
POST /file/delete
Content-Type: application/json

{
  "file_path": "test.txt"
}
```

Response:
```json
{
  "status": "success",
  "action": "delete",
  "file_path": "test.txt"
}
```

#### 8. List Files
```bash
POST /file/list
Content-Type: application/json

{
  "directory": "."
}
```

Response:
```json
{
  "status": "success",
  "directory": ".",
  "files": ["file1.txt", "file2.py", "folder/"],
  "count": 3
}
```

#### 9. Execute Python Code
```bash
POST /execute/python
Content-Type: application/json

{
  "code": "print('Hello from Python!')",
  "timeout": 30
}
```

Response:
```json
{
  "status": "success",
  "language": "python",
  "return_code": 0,
  "output": "Hello from Python!\n",
  "error": "",
  "timeout": false
}
```

#### 10. Execute Bash Code
```bash
POST /execute/bash
Content-Type: application/json

{
  "code": "ls -la",
  "timeout": 30
}
```

Response:
```json
{
  "status": "success",
  "language": "bash",
  "return_code": 0,
  "output": "total 24\ndrwxr-xr-x  5 user  staff  160 Jun  6 19:30 .\n...",
  "error": "",
  "timeout": false
}
```

## Project Structure

```
GUDD/
├── app.py                      # Flask application with all endpoints
├── chatgpt_integration.py      # ChatGPT integration module
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore file
├── README.md                  # This file
└── workspace/                 # Directory for file operations
```

## Configuration

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-3.5-turbo
DEBUG=False
WORK_DIRECTORY=./workspace
```

### Environment Variables

- `OPENAI_API_KEY` - Your OpenAI API key (required)
- `OPENAI_MODEL` - Model to use (default: gpt-3.5-turbo)
- `DEBUG` - Enable debug mode (default: False)
- `WORK_DIRECTORY` - Workspace for file operations (default: ./workspace)

### Available Models

- `gpt-3.5-turbo` - Fastest, most affordable (recommended for most use cases)
- `gpt-4` - Most capable, higher cost (requires separate access)

## Error Handling

The API includes comprehensive error handling for:
- Missing or invalid API key
- Authentication errors (403 Forbidden)
- Rate limiting (429 Too Many Requests)
- Model not found errors
- Network errors
- File operation errors
- Code execution timeouts
- Invalid request format

## Testing

To test the integration manually:

```bash
# Test health endpoint
curl http://localhost:5000/health

# Test chat endpoint
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello"}'

# Test Python execution
curl -X POST http://localhost:5000/execute/python \
  -H "Content-Type: application/json" \
  -d '{"code":"print(\"test\")"}'
```

## Security Notes

- ⚠️ Never commit your `.env` file with actual API keys
- ⚠️ Store API keys in environment variables only
- Use GitHub Secrets for production deployments
- Rotate your API keys regularly
- Monitor your OpenAI API usage and costs
- Path validation prevents directory traversal attacks
- Code execution has timeout limits
- Workspace directory is isolated from system files

## Common Issues

### Issue: "403 — Resource not accessible by integration"
**Solution:**
1. Verify your API key is correct and active
2. Check your OpenAI account has valid billing/credits
3. Try creating a new API key
4. Ensure using correct model name (gpt-3.5-turbo recommended)

### Issue: "Model not found"
**Solution:**
1. Verify the model name is correct
2. Ensure your account has access to that model
3. Use `gpt-3.5-turbo` as default if unsure

### Issue: "Rate limit exceeded"
**Solution:**
1. Wait a moment before retrying
2. Check your usage on OpenAI dashboard
3. Upgrade your account for higher limits

### Issue: Code execution timeout
**Solution:**
1. Increase timeout parameter (max 300 seconds recommended)
2. Optimize your code to run faster
3. Break large tasks into smaller ones

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
1. Check this README's troubleshooting section
2. Visit [OpenAI Help Center](https://help.openai.com)
3. Open an issue on GitHub

## References

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [OpenAI Python Client](https://github.com/openai/openai-python)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python-dotenv](https://github.com/theskumar/python-dotenv)
