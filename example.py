
import pandas as pd
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from insightai import InsightAI

# Load complex e-commerce data
df = pd.read_csv('complex_sales_data.csv')
ai = InsightAI(df)

# Complex multi-step analysis
query = "Show me a summary of total sales and profit by Region and Product Category. Also, which are the top 3 most profitable products?"
ai.pd_agent_converse(query)
# Now you can ask: "Show me monthly revenue trends"
# Or: "Which product category has the highest profit margin?"
