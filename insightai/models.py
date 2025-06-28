import importlib
import os
import time
import json
import re
import requests
from typing import Dict, List, Tuple, Optional

def load_models_from_github(repo_url: str = None) -> Dict:
    """Load available models from GitHub Actions generated models.json"""
    if repo_url is None:
        # Use your repository URL - update this with your actual repo
        repo_url = "https://raw.githubusercontent.com/LeoRigasaki/InSightAI/main/models.json"
    
    try:
        # Try to load from online first
        response = requests.get(repo_url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Could not fetch models from GitHub: {e}")
    
    # Fallback to local file if it exists
    if os.path.exists("models.json"):
        try:
            with open("models.json", 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Could not load local models.json: {e}")
    
    # Fallback to minimal default
    return {
        "providers": {
            "groq": [{"id": "deepseek-r1-distill-llama-70b", "name": "deepseek-r1-distill-llama-70b"}],
            "openai": [{"id": "gpt-4o-mini", "name": "gpt-4o-mini"}],
            "google-gemini": [{"id": "gemini-2.0-flash", "name": "gemini-2.0-flash"}]
        },
        "recommended": {
            "cost_effective": "groq/deepseek-r1-distill-llama-70b",
            "coding": "groq/mixtral-8x7b-instruct",
            "general": "groq/llama-3.3-70b-versatile",
            "reliable": "openai/gpt-4o-mini"
        }
    }
def detect_available_providers() -> Dict[str, bool]:
    """Detect which API keys are available"""
    return {
        'openai': bool(os.getenv('OPENAI_API_KEY')),
        'groq': bool(os.getenv('GROQ_API_KEY')),
        'google-gemini': bool(os.getenv('GEMINI_API_KEY'))
    }

def get_available_models_by_provider(provider: str) -> List[Dict]:
    """Get available models for a specific provider"""
    models_data = load_models_from_github()
    providers = models_data.get('providers', {})
    return providers.get(provider.lower(), [])

def get_recommended_model(available_providers: Dict[str, bool], task_type: str = 'general') -> Optional[str]:
    """Get recommended model based on available providers and task type"""
    models_data = load_models_from_github()
    recommendations = models_data.get('recommended', {})
    
    # Priority order for different tasks
    task_priorities = {
        'general': ['cost_effective', 'general', 'reliable'],
        'coding': ['coding', 'cost_effective', 'reliable'], 
        'reliable': ['reliable', 'general', 'cost_effective']
    }
    
    priorities = task_priorities.get(task_type, task_priorities['general'])
    
    for priority in priorities:
        recommended = recommendations.get(priority, '')
        if '/' in recommended:
            provider, model = recommended.split('/', 1)
            if available_providers.get(provider, False):
                return recommended
    
    # Fallback to first available provider
    for provider, available in available_providers.items():
        if available:
            models = get_available_models_by_provider(provider)
            if models:
                return f"{provider}/{models[0]['id']}"
    
    return None

def generate_simple_config(selected_model: str) -> str:
    """Generate LLM_CONFIG with one model for all agents"""
    if '/' not in selected_model:
        raise ValueError("Model must be in format 'provider/model'")
    
    provider, model = selected_model.split('/', 1)
    
    agents = [
        "Expert Selector", "Analyst Selector", "SQL Analyst", "SQL Generator", 
        "SQL Executor", "Theorist", "Planner", "Code Generator", "Code Debugger",
        "Error Corrector", "Code Ranker", "Solution Summarizer", "Google Search Query Generator",
        "Google Search Summarizer", "Dataset Categorizer", "Question Generator", 
        "Report Generator", "Data Quality Analyzer", "Data Cleaning Expert",
        "Data Cleaning Planner", "ML Model Suggester", "Diagram Generator"
    ]
    
    # Smart token allocation based on agent type
    token_mapping = {
        "Expert Selector": 500, "Analyst Selector": 500, "Code Ranker": 500,
        "SQL Analyst": 2000, "SQL Generator": 2000, "SQL Executor": 2000,
        "Code Generator": 3000, "Code Debugger": 3000, "Error Corrector": 3000,
        "Report Generator": 4000, "Dataset Categorizer": 4000, "Question Generator": 4000
    }
    
    config = []
    for agent in agents:
        max_tokens = token_mapping.get(agent, 2000)  # Default 2000
        config.append({
            "agent": agent,
            "details": {
                "model": model,
                "provider": provider,
                "max_tokens": max_tokens,
                "temperature": 0
            }
        })
    
    return json.dumps(config)

def generate_advanced_config(agent_models: Dict[str, str]) -> str:
    """Generate LLM_CONFIG with different models per agent"""
    config = []
    
    for agent, selected_model in agent_models.items():
        if '/' not in selected_model:
            continue
            
        provider, model = selected_model.split('/', 1)
        
        # Smart token allocation
        token_mapping = {
            "Expert Selector": 500, "Analyst Selector": 500, "Code Ranker": 500,
            "SQL Analyst": 2000, "SQL Generator": 2000, "SQL Executor": 2000,
            "Code Generator": 3000, "Code Debugger": 3000, "Error Corrector": 3000,
            "Report Generator": 4000, "Dataset Categorizer": 4000, "Question Generator": 4000
        }
        
        max_tokens = token_mapping.get(agent, 2000)
        
        config.append({
            "agent": agent,
            "details": {
                "model": model,
                "provider": provider,
                "max_tokens": max_tokens,
                "temperature": 0
            }
        })
    
    return json.dumps(config)

def validate_model_availability(model: str, provider: str) -> bool:
    """Check if a model is available for the given provider"""
    available_models = get_available_models_by_provider(provider)
    return any(m['id'] == model for m in available_models)

def get_provider_models_list(provider: str) -> List[Tuple[str, str]]:
    """Get a formatted list of (model_id, display_name) for a provider"""
    models = get_available_models_by_provider(provider)
    return [(m['id'], m.get('name', m['id'])) for m in models]
def load_llm_config():
    """Enhanced version that can fall back to auto-generation"""
    
    # Your existing logic (keep this unchanged)
    default_llm_config = [
        {"agent": "Expert Selector", "details": {"model": "deepseek-r1-distill-llama-70b", "provider":"groq","max_tokens": 500, "temperature": 0}},
        {"agent": "Analyst Selector", "details": {"model": "deepseek-r1-distill-llama-70b", "provider":"groq","max_tokens": 500, "temperature": 0}},
        {"agent": "Theorist", "details": {"model": "deepseek-r1-distill-llama-70b", "provider":"groq","max_tokens": 2000, "temperature": 0}},
        {"agent": "SQL Analyst", "details": {"model": "deepseek-r1-distill-llama-70b", "provider": "groq", "max_tokens": 2000, "temperature": 0}},
        {"agent": "SQL Generator", "details": {"model": "deepseek-r1-distill-llama-70b", "provider": "groq", "max_tokens": 2000, "temperature": 0}},
        {"agent": "SQL Executor", "details": {"model": "deepseek-r1-distill-llama-70b", "provider": "groq", "max_tokens": 2000, "temperature": 0}},
        {"agent": "Dataframe Inspector", "details": {"model": "deepseek-r1-distill-llama-70b", "provider":"groq","max_tokens": 2000, "temperature": 0}},
        {"agent": "Planner", "details": {"model": "deepseek-r1-distill-llama-70b", "provider":"groq","max_tokens": 2000, "temperature": 0}},
        {"agent": "Code Generator", "details": {"model": "deepseek-r1-distill-llama-70b", "provider":"groq","max_tokens": 3000, "temperature": 0}},
        {"agent": "Code Debugger", "details": {"model": "deepseek-r1-distill-llama-70b", "provider":"groq","max_tokens": 3000, "temperature": 0}},
        {"agent": "Error Corrector", "details": {"model": "deepseek-r1-distill-llama-70b", "provider":"groq","max_tokens": 3000, "temperature": 0}},
        {"agent": "Code Ranker", "details": {"model": "deepseek-r1-distill-llama-70b", "provider":"groq","max_tokens": 500, "temperature": 0}},
        {"agent": "Solution Summarizer", "details": {"model": "deepseek-r1-distill-llama-70b", "provider":"groq","max_tokens": 2000, "temperature": 0}},
        {"agent": "Dataset Categorizer", "details": {"model": "deepseek-r1-distill-llama-70b", "provider":"groq","max_tokens": 4000, "temperature": 0}},
        {"agent": "Question Generator", "details": {"model": "deepseek-r1-distill-llama-70b", "provider":"groq","max_tokens": 4000, "temperature": 0}},
        {"agent": "Report Generator", "details": {"model": "deepseek-r1-distill-llama-70b", "provider":"groq","max_tokens": 4000, "temperature": 0}},
        {"agent": "Data Quality Analyzer", "details": {"model": "deepseek-r1-distill-llama-70b", "provider":"groq","max_tokens": 2000, "temperature": 0}},
        {"agent": "Data Cleaning Expert", "details": {"model": "deepseek-r1-distill-llama-70b", "provider":"groq","max_tokens": 2000, "temperature": 0}},
        {"agent": "Data Cleaning Planner", "details": {"model": "deepseek-r1-distill-llama-70b", "provider":"groq","max_tokens": 2000, "temperature": 0}},
        {"agent": "ML Model Suggester", "details": {"model": "deepseek-r1-distill-llama-70b", "provider":"groq","max_tokens": 2000, "temperature": 0}},
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
    
    # NEW: Check if we should trigger auto-configuration
    # This will be called by InsightAI.__init__() later
    elif os.getenv('INSIGHTAI_AUTO_CONFIG', 'true').lower() == 'true':
        # Signal that auto-configuration should be triggered
        return None  # This tells InsightAI to run the wizard
            
    # Use default config as final fallback
    return default_llm_config
def get_agent_details(agent, llm_config):
    """Get model details for a specific agent from config."""
    for item in llm_config:
        if item['agent'] == agent:
            details = item.get('details', {})
            return (
                details.get('model', 'gpt-4o-mini'),  # Default model
                details.get('provider', 'openai'),     # Default provider
                details.get('max_tokens', 2000),       # Default max tokens
                details.get('temperature', 0)          # Default temperature
            )
    # Return defaults if agent not found
    return 'gpt-4o-mini', 'openai', 2000, 0

def init(agent):
    """Initialize model parameters for an agent."""
    llm_config = load_llm_config()
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
        'google-gemini': 'llm_call',
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
        'google-gemini': 'llm_stream',
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