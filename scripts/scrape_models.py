import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import re
import json
from datetime import datetime
import time

def scrape_model_links(url):
    """Scrape model links from a provider page"""
    print(f"Scraping: {url}")
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find_all("a")

    # Keep only links that match the pattern `/provider/model`
    pattern = re.compile(r"^/[^/]+/[^/]+$")
    filtered_elements = [a for a in results if a.get('href') and pattern.match(a.get('href'))]

    links = [a.get('href') for a in filtered_elements]
    first_parts = [href.split('/')[1] for href in links]
    last_parts = [href.split('/')[-1] for href in links]
    return first_parts, last_parts, links

def extract_model_identifier(model_url, max_retries=3):
    """Extract model identifier with retry logic"""
    for attempt in range(max_retries):
        try:
            full_url = f"https://openrouter.ai{model_url}"
            response = requests.get(full_url, timeout=10)
            soup = BeautifulSoup(response.content, "html.parser")

            h3_tag = soup.find("div", class_="flex gap-2")
            if h3_tag:
                model_name = h3_tag.find("h3")
                if model_name:
                    return model_name.text.strip()
            
            # Fallback: use URL path as model name
            return model_url.split('/')[-1]
            
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for {model_url}: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)  # Wait before retry
            
    return "N/A"

def save_models_to_json(table_data, filename='models.json'):
    """Convert scraped data to JSON format optimized for InsightAI"""
    
    # Group models by provider
    models_by_provider = {}
    
    for provider, model_id, link in table_data:
        provider_key = provider.lower().replace(' ', '-').replace('ai-studio', 'gemini')
        
        # Map provider names to InsightAI conventions
        provider_mapping = {
            'openai': 'openai',
            'groq': 'groq', 
            'google-ai-studio': 'gemini'
        }
        
        normalized_provider = provider_mapping.get(provider_key, provider_key)
        
        if normalized_provider not in models_by_provider:
            models_by_provider[normalized_provider] = []
            
        models_by_provider[normalized_provider].append({
            "id": model_id,
            "name": model_id,
            "provider": normalized_provider,
            "link": f"https://openrouter.ai{link}",
            "available": True
        })

    # Create final JSON structure
    output_data = {
        "last_updated": datetime.utcnow().isoformat() + "Z",
        "total_models": sum(len(models) for models in models_by_provider.values()),
        "providers": models_by_provider,
        "recommended": {
            "cost_effective": "groq/deepseek-r1-distill-llama-70b",
            "coding": "groq/mixtral-8x7b-instruct", 
            "general": "groq/llama-3.3-70b-versatile",
            "reliable": "openai/gpt-4o-mini"
        }
    }
    
    # Save to JSON file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Models saved to {filename}")
    print(f"📊 Total providers: {len(models_by_provider)}")
    print(f"📊 Total models: {output_data['total_models']}")
    
    return output_data

def main():
    """Main scraping function"""
    print("🚀 Starting model scraping for InsightAI...")
    
    # Providers to scrape from
    provider_urls = {
        "OpenAI": "https://openrouter.ai/provider/openai",
        "Groq": "https://openrouter.ai/provider/groq",
        "Google AI Studio": "https://openrouter.ai/provider/google-ai-studio"
    }

    # Store results
    table_data = []
    total_models = 0

    for provider_name, url in provider_urls.items():
        try:
            print(f"\n📡 Scraping {provider_name}...")
            providers, models, links = scrape_model_links(url)
            
            provider_models = 0
            for i in range(len(links)):
                full_link = f"https://openrouter.ai{links[i]}"
                model_identifier = extract_model_identifier(links[i])
                
                if model_identifier != "N/A":
                    table_data.append([provider_name, model_identifier, links[i]])
                    provider_models += 1
                    
            print(f"✅ Found {provider_models} models for {provider_name}")
            total_models += provider_models
            
        except Exception as e:
            print(f"❌ Error scraping {provider_name}: {e}")
            continue

    print(f"\n🎯 Scraping complete! Total models found: {total_models}")

    # Save to JSON format for InsightAI
    if table_data:
        models_data = save_models_to_json(table_data)
        
        # Print summary table (for debugging)
        print(f"\n📋 Summary Table:")
        headers = ["Provider", "Model Identifier", "Model Link"]
        display_data = [[row[0], row[1], f"https://openrouter.ai{row[2]}"] for row in table_data[:10]]  # Show first 10
        print(tabulate(display_data, headers=headers, tablefmt="grid"))
        
        if len(table_data) > 10:
            print(f"... and {len(table_data) - 10} more models")
            
        return True
    else:
        print("❌ No models found!")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        exit(1)