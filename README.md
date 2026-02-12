# SecureChat

A minimalist, high-performance Terminal User Interface (TUI) for interacting with local LLMs. Built with Python and powered by Textual and Ollama, this app provides a clean, markdown-rendered chat experience directly in your terminal.

Key Features:
- Local-First & Secure: Your data never leaves your machine. It talks directly to your local Ollama instance.
- Real-time Markdown Rendering: Watch as your model's response streams and formats instantly with full Markdown support. 
- Persistent Session Logging: Automatically tracks your conversation in a temporary Markdown file for easy debugging or export. (currently in development)
- Streaming Responses: No waiting for the full block; get tokens as they are generated for a fluid conversation. (in development)
- Automatic Model Management: Pre-loads the model on startup and can be configured to manage memory efficiently.
