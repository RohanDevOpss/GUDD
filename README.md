# GUDD - ChatGPT Integration

A Flask-based application that integrates OpenAI's ChatGPT API for intelligent conversational responses.

## Features

- 🤖 ChatGPT API Integration
- 💬 Single-turn and multi-turn conversations
- 📝 Text generation capabilities
- 🔌 RESTful API endpoints
- 🔐 Environment-based configuration
- 📊 Health check endpoint

## Prerequisites

- Python 3.8+
- OpenAI API key (get from [platform.openai.com](https://platform.openai.com))

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
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-3.5-turbo
DEBUG=False
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

## Project Structure

```
GUDD/
├── app.py                      # Flask application
├── chatgpt_integration.py      # ChatGPT integration module
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore file
└── README.md                  # This file
```

## Configuration

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-3.5-turbo
DEBUG=False
```

### Available Models
- `gpt-3.5-turbo` (faster, more affordable)
- `gpt-4` (more capable, higher cost)

## Error Handling

The API includes error handling for:
- Missing API key
- Invalid API key (Authentication errors)
- Rate limiting
- Network errors
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
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Security Notes

- ⚠️ Never commit your `.env` file with actual API keys
- Use GitHub Secrets for production deployments
- Rotate your API keys regularly
- Monitor your OpenAI API usage

## Support

For issues and questions, please open an issue on GitHub.

## References

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python-dotenv](https://github.com/theskumar/python-dotenv)
