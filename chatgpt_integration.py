"""
ChatGPT Integration Module with File Operations
Provides functions to interact with OpenAI's ChatGPT API
and perform file read, write, and execute operations
"""

import os
import subprocess
import json
from dotenv import load_dotenv
import openai
from typing import List, Dict, Optional, Any
from pathlib import Path

# Load environment variables
load_dotenv()

class ChatGPTIntegration:
    """ChatGPT Integration class for API interactions with file operations"""
    
    def __init__(self):
        """Initialize ChatGPT integration with API key"""
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.model = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
        self.work_directory = os.getenv('WORK_DIRECTORY', './workspace')
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        openai.api_key = self.api_key
        
        # Create workspace directory if it doesn't exist
        Path(self.work_directory).mkdir(parents=True, exist_ok=True)
    
    def _validate_path(self, file_path: str) -> str:
        """
        Validate and normalize file path to prevent directory traversal
        
        Args:
            file_path: Path to validate
            
        Returns:
            Validated absolute path
            
        Raises:
            ValueError: If path is invalid or outside workspace
        """
        # Resolve to absolute path
        abs_path = Path(self.work_directory) / file_path
        abs_path = abs_path.resolve()
        
        # Ensure path is within workspace
        workspace_path = Path(self.work_directory).resolve()
        try:
            abs_path.relative_to(workspace_path)
        except ValueError:
            raise ValueError(f"Path {file_path} is outside workspace directory")
        
        return str(abs_path)
    
    def read_file(self, file_path: str) -> str:
        """
        Read file contents
        
        Args:
            file_path: Path to file relative to workspace
            
        Returns:
            File contents as string
        """
        try:
            abs_path = self._validate_path(file_path)
            
            if not os.path.exists(abs_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            if not os.path.isfile(abs_path):
                raise ValueError(f"Path is not a file: {file_path}")
            
            with open(abs_path, 'r', encoding='utf-8') as f:
                return f.read()
        
        except Exception as e:
            raise Exception(f"Error reading file: {str(e)}")
    
    def write_file(self, file_path: str, content: str, append: bool = False) -> Dict[str, Any]:
        """
        Write content to file
        
        Args:
            file_path: Path to file relative to workspace
            content: Content to write
            append: If True, append to file; if False, overwrite
            
        Returns:
            Dictionary with status and file info
        """
        try:
            abs_path = self._validate_path(file_path)
            
            # Create parent directories if needed
            os.makedirs(os.path.dirname(abs_path), exist_ok=True)
            
            mode = 'a' if append else 'w'
            with open(abs_path, mode, encoding='utf-8') as f:
                f.write(content)
            
            return {
                "status": "success",
                "file_path": file_path,
                "mode": "append" if append else "write",
                "size": len(content),
                "full_path": abs_path
            }
        
        except Exception as e:
            raise Exception(f"Error writing file: {str(e)}")
    
    def execute_code(self, code: str, language: str = "python", timeout: int = 30) -> Dict[str, Any]:
        """
        Execute code and return output
        
        Args:
            code: Code to execute
            language: Programming language (python, bash, etc.)
            timeout: Timeout in seconds
            
        Returns:
            Dictionary with execution results
        """
        try:
            if language.lower() == "python":
                return self._execute_python(code, timeout)
            elif language.lower() in ["bash", "shell"]:
                return self._execute_bash(code, timeout)
            else:
                raise ValueError(f"Unsupported language: {language}")
        
        except Exception as e:
            return {
                "status": "error",
                "language": language,
                "error": str(e)
            }
    
    def _execute_python(self, code: str, timeout: int) -> Dict[str, Any]:
        """Execute Python code safely"""
        try:
            # Create a temporary file for the code
            temp_file = os.path.join(self.work_directory, ".temp_script.py")
            
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(code)
            
            result = subprocess.run(
                [os.sys.executable, temp_file],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.work_directory
            )
            
            # Clean up
            os.remove(temp_file)
            
            return {
                "status": "success" if result.returncode == 0 else "error",
                "language": "python",
                "return_code": result.returncode,
                "output": result.stdout,
                "error": result.stderr,
                "timeout": False
            }
        
        except subprocess.TimeoutExpired:
            return {
                "status": "error",
                "language": "python",
                "error": f"Code execution timed out after {timeout} seconds",
                "timeout": True
            }
        
        except Exception as e:
            return {
                "status": "error",
                "language": "python",
                "error": str(e),
                "timeout": False
            }
    
    def _execute_bash(self, code: str, timeout: int) -> Dict[str, Any]:
        """Execute Bash code safely"""
        try:
            result = subprocess.run(
                code,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.work_directory
            )
            
            return {
                "status": "success" if result.returncode == 0 else "error",
                "language": "bash",
                "return_code": result.returncode,
                "output": result.stdout,
                "error": result.stderr,
                "timeout": False
            }
        
        except subprocess.TimeoutExpired:
            return {
                "status": "error",
                "language": "bash",
                "error": f"Code execution timed out after {timeout} seconds",
                "timeout": True
            }
        
        except Exception as e:
            return {
                "status": "error",
                "language": "bash",
                "error": str(e),
                "timeout": False
            }
    
    def list_files(self, directory: str = ".") -> List[str]:
        """
        List files in directory
        
        Args:
            directory: Directory path relative to workspace
            
        Returns:
            List of files
        """
        try:
            abs_path = self._validate_path(directory)
            
            if not os.path.isdir(abs_path):
                raise ValueError(f"Path is not a directory: {directory}")
            
            files = []
            for item in os.listdir(abs_path):
                item_path = os.path.join(abs_path, item)
                rel_path = os.path.relpath(item_path, self.work_directory)
                files.append(rel_path)
            
            return files
        
        except Exception as e:
            raise Exception(f"Error listing files: {str(e)}")
    
    def delete_file(self, file_path: str) -> Dict[str, Any]:
        """
        Delete a file
        
        Args:
            file_path: Path to file relative to workspace
            
        Returns:
            Status dictionary
        """
        try:
            abs_path = self._validate_path(file_path)
            
            if not os.path.exists(abs_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            if not os.path.isfile(abs_path):
                raise ValueError(f"Path is not a file: {file_path}")
            
            os.remove(abs_path)
            
            return {
                "status": "success",
                "action": "delete",
                "file_path": file_path
            }
        
        except Exception as e:
            raise Exception(f"Error deleting file: {str(e)}")
    
    def chat(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """
        Send a message to ChatGPT and get a response
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Controls randomness (0-1, default 0.7)
        
        Returns:
            Response text from ChatGPT
        """
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=temperature
            )
            return response.choices[0].message.content
        except openai.error.AuthenticationError:
            raise Exception("Invalid API key provided")
        except openai.error.RateLimitError:
            raise Exception("Rate limit exceeded. Please try again later")
        except Exception as e:
            raise Exception(f"Error communicating with OpenAI: {str(e)}")
    
    def ask_question(self, question: str, system_prompt: Optional[str] = None) -> str:
        """
        Ask ChatGPT a single question
        
        Args:
            question: The question to ask
            system_prompt: Optional system prompt to set context
        
        Returns:
            Response from ChatGPT
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": question})
        
        return self.chat(messages)
    
    def conversation(self, conversation_history: List[Dict[str, str]]) -> str:
        """
        Continue a conversation with ChatGPT
        
        Args:
            conversation_history: List of previous messages with roles
        
        Returns:
            Response from ChatGPT
        """
        return self.chat(conversation_history)
    
    def generate_text(self, prompt: str, max_tokens: int = 500) -> str:
        """
        Generate text based on a prompt
        
        Args:
            prompt: The prompt for text generation
            max_tokens: Maximum tokens in response
        
        Returns:
            Generated text
        """
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error generating text: {str(e)}")


def initialize_chatgpt() -> ChatGPTIntegration:
    """
    Initialize and return ChatGPT integration instance
    
    Returns:
        ChatGPTIntegration instance
    """
    return ChatGPTIntegration()
