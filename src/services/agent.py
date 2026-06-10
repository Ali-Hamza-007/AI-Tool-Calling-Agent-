from langchain_openai import ChatOpenAI
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from services.tools import agent_tools
from langchain_groq import ChatGroq
import config

def run_agent(user_input: str):
    # Point the client to XAI(Grok's) API endpoint
    # llm = ChatOpenAI(
    #     api_key=config.XAI_API_KEY,
    #     base_url="https://api.x.ai/v1",
    #     model="grok-4-fast",
    #     temperature=0
    # )
    llm = ChatGroq(
        api_key=config.GROQ_API_KEY, # Make sure you update your config!
        model_name="llama-3.3-70b-versatile", # Groq supports many fast models
        temperature=0
    )
    
    # "agent_scratchpad" is required for the agent to store its reasoning/tool steps
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Use your tools to answer the user's request. Always summarize the tools you used and their outputs."),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # Bind tools and create agent
    agent = create_tool_calling_agent(llm, agent_tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=agent_tools, 
        verbose=True, 
        return_intermediate_steps=True
    )
    
    response = agent_executor.invoke({"input": user_input})
    
    # Format the requested JSON output structure
    structured_output = {
        "tools_used": [],
        "results": {}
    }
    
    # Extract intermediate steps (tool calls)
    for action, result in response.get("intermediate_steps", []):
        tool_name = action.tool
        structured_output["tools_used"].append(tool_name)
        structured_output["results"][tool_name] = result
        
    return {
        "structured_json": structured_output,
        "readable_response": response["output"]
    }