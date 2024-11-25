# Newsletter Generation System

A Python program that automatically generates newsletters using Llama 2 AI.

## Prerequisites
- Python 3.10+
- Git
- Ollama with Llama 2 model

## Setup

1. Install Ollama:
  - Go to [Ollama.ai](https://ollama.ai)
  - Download & install for your system

2. Install Llama 2:
  ```
  ollama pull llama2
  git clone [your-repo-url]
  cd [repo-name]
```
Install dependencies:
```
pip install ollama-python schedule
```
Usage

Start Ollama:
```
ollama start
```
Run program:
```
python newsletter1.py
```
Features

Random topic selection from topics.json
Scheduled newsletter generation (default 9:50 AM)
Auto-saves as newsletter_[timestamp].txt

Configuration
Change schedule in main():
```
newsletter_copilot.create_newsletter(topic, schedule_time="HH:MM")
```
Troubleshooting

Encoding errors: Check UTF-8 terminal support
Ollama issues: Verify running with ollama list
