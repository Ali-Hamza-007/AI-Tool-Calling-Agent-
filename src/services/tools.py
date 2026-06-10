import json
import base64
import os
from email.message import EmailMessage
from langchain.tools import tool
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import requests

# --- 1. Calculator Tool ---
@tool
def calculator(expression: str) -> str:
    """
    Performs math calculations using a web-based calculator API. 
    Use this for any mathematical expressions (e.g., '15 * 450').
    """
    # Using a public calculator API endpoint
    # Note: Replace this URL with your preferred stable math API
    url = "https://api.mathjs.org/v4/"
    try:
        # Some APIs expect 'expr' as a query parameter
        response = requests.post(url, json={"expr": expression})
        if response.status_code == 200:
            return str(response.text)
        else:
            return f"Calculator API error: {response.status_code}"
    except Exception as e:
        return f"Could not connect to calculator service: {str(e)}"

# --- 2. Task Tools ---
@tool
def create_task(owner: str, task: str, deadline: str) -> str:
    """
    Creates a task, stores it as JSON, and saves it to 'tasks.txt'.
    Use this whenever the user wants to create or add a task.
    """
    task_data = {
        "owner": owner,
        "task": task,
        "deadline": deadline
    }
    
    # Save as JSON string to file
    try:
        with open("tasks.txt", "a") as f:
            f.write(json.dumps(task_data) + "\n")
        
        # Return both the JSON string and a confirmation message
        return f"Task created and saved successfully! JSON: {json.dumps(task_data)}"
    except Exception as e:
        return f"Failed to save task: {str(e)}"

# --- 3. Document Search Tool ---
@tool
def document_search(query: str) -> str:
    """Searches documents for information. Use this when asked about company docs or reports."""
    simulated_docs = {
        "report": "The Q3 report indicates a 15% growth in revenue.",
        "policy": "Remote work is allowed 3 days a week."
    }
    for key, value in simulated_docs.items():
        if key in query.lower():
            return value
    return "No relevant documents found."

# --- 4. Real Gmail Draft Generator Tool ---
SCOPES = ['https://www.googleapis.com/auth/gmail.compose']

@tool
def generate_email_draft(subject: str, body: str, to: str) -> dict:
    """Creates and saves an email draft in the user's Gmail account."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('gmail', 'v1', credentials=creds)
        message = EmailMessage()
        message.set_content(body)
        message['To'] = to
        message['Subject'] = subject

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {'message': {'raw': encoded_message}}
        
        draft = service.users().drafts().create(userId="me", body=create_message).execute()
        return {"subject": subject, "body": body, "status": "Saved to Gmail Drafts", "draft_id": draft['id']}
    except Exception as e:
        return {"error": str(e)}

# List of tools to export
agent_tools = [calculator, create_task, document_search, generate_email_draft]