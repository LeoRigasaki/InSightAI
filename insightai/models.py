import importlib
import os
import time
import json
import re


def get_best_available_provider():
    """Determine the best available provider based on environment variables."""
    if os.getenv('OPENAI_API_KEY'):
        return 'openai', 'gpt-4o-mini'
    if os.getenv('GROQ_API_KEY'):
        return 'groq', 'llama-3.3-70b-versatile'
    if os.getenv('GEMINI_API_KEY'):
        return 'gemini', 'gemini-1.5-flash'
    return 'openai', 'gpt-4o-mini' # Fallback to OpenAI if nothing found

def load_llm_config():
    """Load LLM configuration, using dynamic defaults if no config is found."""
    provider, model = get_best_available_provider()
    
    # Define generic defaults that adapt to the available key
    # High-performance agents get the 'best' model, utility agents get 'cheap' model
    default_llm_config = [
        {"agent": "Expert Selector", "details": {"model": model, "provider": provider, "max_tokens": 4000, "temperature": 0}},
        {"agent": "Analyst Selector", "details": {"model": model, "provider": provider, "max_tokens": 4000, "temperature": 0}},
        {"agent": "Theorist", "details": {"model": model, "provider": provider, "max_tokens": 4000, "temperature": 0}},
        {"agent": "SQL Analyst", "details": {"model": model, "provider": provider, "max_tokens": 2000, "temperature": 0}},
        {"agent": "SQL Generator", "details": {"model": model, "provider": provider, "max_tokens": 2000, "temperature": 0}},
        {"agent": "SQL Executor", "details": {"model": model, "provider": provider, "max_tokens": 2000, "temperature": 0}},
        {"agent": "Dataframe Inspector", "details": {"model": model, "provider": provider, "max_tokens": 4000, "temperature": 0}},
        {"agent": "Planner", "details": {"model": model, "provider": provider, "max_tokens": 4000, "temperature": 0}},
        {"agent": "Code Generator", "details": {"model": model, "provider": provider, "max_tokens": 4000, "temperature": 0}},
        {"agent": "Code Debugger", "details": {"model": model, "provider": provider, "max_tokens": 4000, "temperature": 0}},
        {"agent": "Error Corrector", "details": {"model": model, "provider": provider, "max_tokens": 4000, "temperature": 0}},
        {"agent": "Code Ranker", "details": {"model": model, "provider": provider, "max_tokens": 4000, "temperature": 0}},
        {"agent": "Solution Summarizer", "details": {"model": model, "provider": provider, "max_tokens": 4000, "temperature": 0}},
        {"agent": "Dataset Categorizer", "details": {"model": model, "provider": provider, "max_tokens": 1000, "temperature": 0}},
        {"agent": "Question Generator", "details": {"model": model, "provider": provider, "max_tokens": 2000, "temperature": 0.1}},
        {"agent": "Report Generator", "details": {"model": model, "provider": provider, "max_tokens": 4000, "temperature": 0}},
        {"agent": "Research Specialist", "details": {"model": model, "provider": provider, "max_tokens": 4000, "temperature": 0}},
    ]

    # Try to get config from environment variable
    if os.environ.get('LLM_CONFIG'):
        try:
            return json.loads(os.environ.get('LLM_CONFIG'))
        except json.JSONDecodeError:
            return default_llm_config
            
    # Try to load from file
    elif os.path.exists("LLM_CONFIG.json"):
        try:
            with open("LLM_CONFIG.json", 'r') as f:
                return json.load(f)
        except Exception:
            return default_llm_config
            
# Use default config
    return default_llm_config

def get_effective_config():
    """Merge user config with default config to get the full picture."""
    defaults = load_llm_config() # This gets the base list (either default or user file)
    
    # If load_llm_config returned the default list, we are already good.
    # But if it returned a user list, it might be partial.
    # The current load_llm_config implementation either returns the FULL user list OR the FULL default list.
    # However, users often provide partial lists.
    
    # Re-implementing merge logic here for safety
    if os.environ.get('LLM_CONFIG'):
        try:
            user_config = json.loads(os.environ.get('LLM_CONFIG'))
        except json.JSONDecodeError:
            user_config = []
    elif os.path.exists("LLM_CONFIG.json"):
        try:
            with open("LLM_CONFIG.json", 'r') as f:
                user_config = json.load(f)
        except Exception:
            user_config = []
    else:
        user_config = []

    # Get the static defaults (copy to avoid mutation)
    # We'll re-fetch the raw defaults by calling a private version or just hardcoding the logic
    effective_config = {item['agent']: item for item in load_llm_config()} # Start with what load_llm_config thinks is best
    
    # If the user provided a separate partial list, merge it
    for item in user_config:
        effective_config[item['agent']] = item
        
    return list(effective_config.values())

def get_agent_details(agent, llm_config):
    """Get model details for a specific agent from config."""
    # The llm_config passed here is usually from load_llm_config()
    for item in llm_config:
        if item['agent'] == agent:
            details = item.get('details', {})
            return (
                details.get('model', 'gpt-4o-mini'),
                details.get('provider', 'openai'),
                details.get('max_tokens', 2000),
                details.get('temperature', 0)
            )
    
    # Absolute fallback
    return 'gpt-4o-mini', 'openai', 2000, 0

def init(agent):
    """Initialize model parameters for an agent."""
    llm_config = get_effective_config()
    return get_agent_details(agent, llm_config)

def get_model_name(agent):
    """Get model name and provider for an agent."""
    model, provider, _, _ = init(agent)
    return model, provider

def try_import(module_name):
    """Import a module, trying package-relative import first."""
    try:
        return importlib.import_module(f'.{module_name}', 'insightai')
    except ImportError:
        return importlib.import_module(module_name)

def llm_call(log_and_call_manager, messages: str, agent: str = None, chain_id: str = None):
    """Make a non-streaming LLM call."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    model, provider, max_tokens, temperature = init(agent)

    provider_function_map = {
        'groq': 'llm_call',
        'openai': 'llm_call',
        'gemini': 'llm_call',
    }

    if provider not in provider_function_map:
        raise ValueError(f"Unsupported provider: {provider}")

    provider_module = try_import(f'{provider}_models')
    function_name = provider_function_map[provider]
    
    result = getattr(provider_module, function_name)(
        messages, model, temperature, max_tokens
    )
    
    # Unpack results
    (content_received, local_llm_messages, prompt_tokens_used,
     completion_tokens_used, total_tokens_used, elapsed_time,
     tokens_per_second) = result

    if agent == 'SQL Generator':
        # Strip any markdown or explanatory text from SQL
        content_received = re.sub(r'```sql\s*|\s*```', '', content_received)
        content_received = re.sub(r'^.*?--', '--', content_received, flags=re.DOTALL)

    # Log results
    log_and_call_manager.write_to_log(
        agent, chain_id, timestamp, model, local_llm_messages,
        content_received, prompt_tokens_used, completion_tokens_used,
        total_tokens_used, elapsed_time, tokens_per_second
    )

    return content_received

def llm_stream(log_and_call_manager, messages: str, agent: str = None, 
               chain_id: str = None, tools: str = None):
    """Make a streaming LLM call."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    model, provider, max_tokens, temperature = init(agent)

    provider_function_map = {
        'groq': 'llm_stream',
        'openai': 'llm_stream',
        'gemini': 'llm_stream',
    }

    if provider not in provider_function_map:
        raise ValueError(f"Unsupported provider: {provider}")

    provider_module = try_import(f'{provider}_models')
    function_name = provider_function_map[provider]
    
    result = getattr(provider_module, function_name)(
        log_and_call_manager, chain_id, messages,
        model, temperature, max_tokens, tools
    )
    
    # Unpack results
    (content_received, local_llm_messages, prompt_tokens_used,
     completion_tokens_used, total_tokens_used, elapsed_time,
     tokens_per_second) = result

    # Log results
    log_and_call_manager.write_to_log(
        agent, chain_id, timestamp, model, local_llm_messages,
        content_received, prompt_tokens_used, completion_tokens_used,
        total_tokens_used, elapsed_time, tokens_per_second
    )

    return content_received