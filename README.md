# InsightAI 🚀

[![PyPI version](https://badge.fury.io/py/insightai.svg)](https://badge.fury.io/py/insightai)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful open-source library that enables natural language conversations with your data using Large Language Models (LLMs). Transform complex data analysis into simple conversations - no coding required!

## ✨ Key Features

- **🗣️ Natural Language Interface**: Ask questions about your data in plain English
- **🔌 Multiple Model Support**: Works with OpenAI GPT models and Groq's high-speed inference
- **🧠 Smart Analysis**: Automatic code generation, data cleaning, and ML model suggestions
- **🛠️ Error Recovery**: Built-in debugging and error correction mechanisms
- **📊 Auto-Visualization**: Generates charts and graphs automatically
- **💾 SQL Support**: Native support for SQLite databases
- **📈 Report Generation**: Create comprehensive analysis reports automatically
- **🔍 Data Quality Analysis**: Identifies and fixes data quality issues
- **⚡ Real-time Processing**: Streaming responses for immediate feedback

## 🚀 Quick Start

### Installation

```bash
pip install insightai
```

### Environment Setup

Set up your API keys:

```bash
# Required: OpenAI API Key
export OPENAI_API_KEY="your-openai-api-key"

# Required: Groq API Key (for faster inference)
export GROQ_API_KEY="your-groq-api-key"
```

### Basic Usage

```python
import pandas as pd
from insightai import InsightAI

# Load your data
df = pd.read_csv('your_data.csv')

# Initialize InsightAI
ai = InsightAI(df)

# Start asking questions!
ai.pd_agent_converse("What are the main trends in this data?")
```

## 💡 Usage Examples

### 1. Interactive Data Analysis

```python
import pandas as pd
from insightai import InsightAI

# Load sales data
df = pd.read_csv('sales_data.csv')
ai = InsightAI(df)

# Interactive mode - ask multiple questions
ai.pd_agent_converse()
# Now you can ask: "Show me monthly revenue trends"
# Or: "Which product category has the highest profit margin?"
```

### 2. Single Question Analysis

```python
# Ask a specific question
ai = InsightAI(df)
ai.pd_agent_converse("What is the correlation between price and customer rating?")
```

### 3. SQL Database Analysis

```python
# Analyze SQLite database
ai = InsightAI(db_path='customer_database.db')
ai.pd_agent_converse("Find the top 10 customers by total purchase amount")
```

### 4. Automated Report Generation

```python
# Generate comprehensive analysis report
ai = InsightAI(df, generate_report=True, report_questions=5)
ai.pd_agent_converse()  # Generates a full report automatically
```

### 5. Data Cleaning and ML Suggestions

```python
# Get data cleaning recommendations and ML model suggestions
ai = InsightAI(df)
ai.pd_agent_converse("Clean this dataset and suggest appropriate machine learning models")
```

## 🔧 Advanced Configuration

### Constructor Parameters

```python
InsightAI(
    df=None,                    # pandas DataFrame
    db_path=None,              # Path to SQLite database
    max_conversations=4,        # Conversation memory length
    debug=False,               # Enable debug mode
    exploratory=True,          # Enable exploratory analysis
    df_ontology=False,         # Enable data ontology support
    generate_report=True,      # Auto-generate reports
    report_questions=5         # Number of questions for reports
)
```

### Custom Model Configuration

Create `LLM_CONFIG.json` in your working directory:

```json
[
  {
    "agent": "Code Generator",
    "details": {
      "model": "gpt-4o",
      "provider": "openai",
      "max_tokens": 4000,
      "temperature": 0
    }
  },
  {
    "agent": "Planner",
    "details": {
      "model": "llama-3.3-70b-versatile",
      "provider": "groq",
      "max_tokens": 2000,
      "temperature": 0.1
    }
  }
]
```

### Custom Prompts

Create `PROMPT_TEMPLATES.json` to customize agent behavior:

```json
{
  "planner_system": "You are a data analysis expert...",
  "code_generator_system_df": "You are an AI data analyst..."
}
```

## 🎯 What You Can Ask

### Data Exploration
- "What does this dataset contain?"
- "Show me the distribution of values in each column"
- "Are there any missing values or outliers?"

### Statistical Analysis
- "What's the correlation between sales and marketing spend?"
- "Perform a statistical summary of the numerical columns"
- "Which factors most influence customer satisfaction?"

### Visualizations
- "Create a bar chart of revenue by product category"
- "Plot the trend of monthly sales over time"
- "Show me a correlation heatmap of all numerical variables"

### Data Cleaning
- "Clean this dataset and prepare it for machine learning"
- "Handle missing values and suggest the best approach"
- "Identify and fix data quality issues"

### Machine Learning
- "What machine learning models would work best for this data?"
- "Prepare this data for predictive modeling"
- "Suggest features for predicting customer churn"

### Business Intelligence
- "Generate a comprehensive analysis report"
- "What are the key business insights from this data?"
- "Create an executive summary of the findings"

## 📊 Output Examples

### Automated Visualizations
InsightAI automatically saves visualizations to the `visualization/` folder:
- Bar charts, line plots, scatter plots
- Correlation heatmaps
- Distribution plots
- Custom business charts

### Analysis Reports
Generate professional markdown reports including:
- Executive summary
- Dataset overview
- Key findings and insights
- Recommendations
- Supporting visualizations

### Code Generation
View the actual Python code generated for your analysis:
```python
# Example generated code
import pandas as pd
import matplotlib.pyplot as plt

# Calculate monthly revenue trends
monthly_revenue = df.groupby('month')['revenue'].sum()
plt.figure(figsize=(10, 6))
plt.plot(monthly_revenue.index, monthly_revenue.values)
plt.title('Monthly Revenue Trends')
plt.savefig('visualization/monthly_revenue_trends.png')
plt.show()
```

## 🏗️ Architecture

InsightAI uses a multi-agent architecture with specialized AI agents:

- **Expert Selector**: Chooses the right agent for your task
- **Data Analyst**: Performs statistical analysis and visualizations  
- **SQL Analyst**: Handles database queries and operations
- **Data Cleaning Expert**: Identifies and fixes data quality issues
- **Code Generator**: Creates Python code for your analysis
- **Error Corrector**: Debugs and fixes code issues automatically
- **Report Generator**: Creates comprehensive analysis reports

## 📈 Supported Models

### OpenAI Models
- GPT-4o, GPT-4o-mini
- GPT-4 Turbo
- O1 series models

### Groq Models (High-Speed Inference)
- Llama 3.3 70B
- Llama 3.1 8B
- Mixtral 8x7B
- Gemma 2 9B

## 📝 Logging and Cost Tracking

All interactions are automatically logged with detailed cost tracking:

```json
{
  "chain_id": "1234567890",
  "agent": "Code Generator",
  "model": "gpt-4o-mini",
  "tokens_used": 1500,
  "cost": 0.03,
  "duration": "2.3s"
}
```

View logs in: `insightai_consolidated_log.json`

## 🔒 Security Features

- Input sanitization and validation
- Code execution sandboxing
- Blacklisted dangerous operations
- Rate limiting and error handling

## 🎓 Examples and Tutorials

### E-commerce Analysis
```python
# Analyze online store data
df = pd.read_csv('ecommerce_data.csv')
ai = InsightAI(df)
ai.pd_agent_converse("Which products have the highest return rate and why?")
```

### Financial Data Analysis
```python
# Stock market analysis
ai = InsightAI()
ai.pd_agent_converse("Download Apple stock data for 2024 and analyze the trends")
```

### Healthcare Data
```python
# Patient data analysis (anonymized)
df = pd.read_csv('patient_outcomes.csv')
ai = InsightAI(df)
ai.pd_agent_converse("What factors correlate with better patient outcomes?")
```

## 🛠️ Development Setup

```bash
git clone https://github.com/LeoRigasaki/InSightAI.git
cd InsightAI
pip install -e ".[dev]"
```
## 🆕 Version 0.5.0 Release Notes

### ✨ New Features
- **Dynamic API Key Management**: Only requires API keys for providers you actually use
- **Flexible Provider Support**: Mix and match OpenAI, Groq, and Gemini models freely
- **Cost Optimization**: Reduced overhead by eliminating unused API dependencies

### 🔧 Improvements  
- Smarter LLM configuration parsing
- Better error messages for missing API keys
- Enhanced provider validation

### 🐛 Bug Fixes
- Fixed requirement for all API keys even when not needed
- Improved initialization error handling
## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a Pull Request

## ⚠️ Known Limitations

- Token limits vary by model (check your plan)
- Large datasets may require chunking
- Rate limiting depends on your API plan
- Complex visualizations may need manual adjustment

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- Special thanks to [pgalko](https://github.com/pgalko/BambooAI) for the original inspiration
- OpenAI for providing powerful language models
- Groq for high-performance inference capabilities
- The open-source community for continuous improvements

## 💬 Support

- 📧 Email: riorigasaki65@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/LeoRigasaki/InSightAI/issues)
- 💡 Feature Requests: [GitHub Discussions](https://github.com/LeoRigasaki/InSightAI/discussions)

---

**Transform your data analysis workflow today with InsightAI - where natural language meets powerful analytics!** 🚀
