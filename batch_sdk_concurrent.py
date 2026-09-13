import asyncio
import os
import json
import time
import hashlib
from google.antigravity import Agent, LocalAgentConfig

BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = '/Users/markoates/Assets'
VIEWER_DATA_PATH = os.path.join(BASE_DIR, 'web', 'viewer_data.json')
PROPOSALS_PATH = os.path.join(BASE_DIR, 'scripts', 'ai_subagent_proposals.json')

system_instruction = """You are an expert game asset cataloger and data engineer.
Given an image path, you must view the file using your `view_file` tool and output ONLY valid JSON matching this schema: ..."""

# Wait, the SDK agents don't have view_file by default. They need CapabilitiesConfig to read files?
# "By default, it runs in read-only mode for safety." meaning it CAN read files! (e.g. view_file).
