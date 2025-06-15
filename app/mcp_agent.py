import os
import json
import time
from openai import OpenAI
from typing import Dict, Any, Optional
from tools.db_query import run_query
from tools.get_table_names import get_table_names
from tools.summarize_table import summarize_table

class DatabaseAssistant:
    def __init__(self, api_key: str):
        """Initialize the OpenAI client and create assistant."""
        self.client = OpenAI(api_key=api_key)
        self.assistant = None
        self.thread = None
        self._create_assistant()
    
    def _create_assistant(self):
        """Create an OpenAI Assistant with database tools."""
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "run_query",
                    "description": "Execute a SQL SELECT query on the database. Only SELECT queries are allowed for security. Results are limited to 5 rows.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "sql": {
                                "type": "string",
                                "description": "The SQL SELECT query to execute"
                            }
                        },
                        "required": ["sql"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_table_names",
                    "description": "Get a list of all table names in the database.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "summarize_table",
                    "description": "Get detailed information about a table including schema, column types, and sample data.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "table_name": {
                                "type": "string",
                                "description": "The name of the table to summarize"
                            }
                        },
                        "required": ["table_name"]
                    }
                }
            }
        ]
        
        self.assistant = self.client.beta.assistants.create(
            name="Database Query Assistant",
            instructions="""You are a helpful database assistant that can help users query and understand their PostgreSQL database.

You have access to three tools:
1. get_table_names() - Lists all tables in the database
2. summarize_table(table_name) - Shows table schema and sample data
3. run_query(sql) - Executes SELECT queries (limited to 5 rows for safety)

When users ask questions:
- Start by understanding what tables are available if needed
- Use summarize_table to understand table structure before writing queries
- Write clear, efficient SQL queries
- Always explain what the query does and what the results mean
- Be helpful in interpreting the data and suggesting follow-up questions

Security notes:
- Only SELECT queries are allowed
- Results are limited to 5 rows to protect sensitive data
- Email addresses and other PII may be present but should be handled carefully

Be conversational and helpful while being precise about database operations.""",
            model="gpt-4o",
            tools=tools
        )
    
    def _execute_tool_call(self, tool_call) -> str:
        """Execute a tool call and return the result as a string."""
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        
        try:
            if function_name == "run_query":
                result = run_query(arguments["sql"])
            elif function_name == "get_table_names":
                result = get_table_names()
            elif function_name == "summarize_table":
                result = summarize_table(arguments["table_name"])
            else:
                result = {"success": False, "error": f"Unknown function: {function_name}"}
            
            return json.dumps(result, indent=2, default=str)
            
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})
    
    def create_thread(self) -> str:
        """Create a new conversation thread."""
        self.thread = self.client.beta.threads.create()
        return self.thread.id
    
    def ask_question(self, question: str, thread_id: Optional[str] = None) -> str:
        """Ask a question to the assistant and get a response."""
        try:
            # Use existing thread or create new one
            if thread_id:
                self.thread = self.client.beta.threads.retrieve(thread_id)
            elif not self.thread:
                self.create_thread()
            
            # Add the user's message to the thread
            self.client.beta.threads.messages.create(
                thread_id=self.thread.id,
                role="user",
                content=question
            )
            
            # Run the assistant
            run = self.client.beta.threads.runs.create(
                thread_id=self.thread.id,
                assistant_id=self.assistant.id
            )
            
            # Wait for completion and handle tool calls
            while True:
                run_status = self.client.beta.threads.runs.retrieve(
                    thread_id=self.thread.id,
                    run_id=run.id
                )
                
                if run_status.status == "completed":
                    break
                elif run_status.status == "requires_action":
                    # Handle tool calls
                    tool_outputs = []
                    for tool_call in run_status.required_action.submit_tool_outputs.tool_calls:
                        output = self._execute_tool_call(tool_call)
                        tool_outputs.append({
                            "tool_call_id": tool_call.id,
                            "output": output
                        })
                    
                    # Submit tool outputs
                    self.client.beta.threads.runs.submit_tool_outputs(
                        thread_id=self.thread.id,
                        run_id=run.id,
                        tool_outputs=tool_outputs
                    )
                elif run_status.status in ["failed", "cancelled", "expired"]:
                    return f"Run failed with status: {run_status.status}"
                
                time.sleep(1)  # Wait before checking again
            
            # Get the assistant's response
            messages = self.client.beta.threads.messages.list(
                thread_id=self.thread.id,
                order="desc",
                limit=1
            )
            
            if messages.data:
                return messages.data[0].content[0].text.value
            else:
                return "No response received from assistant."
                
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_thread_id(self) -> Optional[str]:
        """Get the current thread ID."""
        return self.thread.id if self.thread else None 