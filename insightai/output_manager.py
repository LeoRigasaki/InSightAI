from termcolor import cprint
from IPython.display import display, HTML, Markdown as IPythonMarkdown
import sys
import time
import pandas as pd

# Rich UI Imports
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.syntax import Syntax
    from rich.markdown import Markdown as RichMarkdown
    from rich.text import Text
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

class OutputManager:
    def __init__(self):
        # Initialize console with force_jupyter if in notebook to ensure theme rendering
        if self.is_notebook():
            self.console = Console(force_jupyter=True) if RICH_AVAILABLE else None
        else:
            self.console = Console() if RICH_AVAILABLE else None
        
        # Professional Color Palette
        self.theme = {
            "primary": "bold cyan",
            "secondary": "bright_black",
            "success": "bold green",
            "error": "bold red",
            "warning": "bold orange3",
            "info": "bold blue",
            "code": "monokai",
            "panel_border": "cyan"
        }
        
        # Legacy color properties for backward compatibility
        self.color_tool_header = 'magenta'
        self.color_usr_input_prompt = 'blue'
        self.color_usr_input_rank = 'green'
        self.color_error_ntb = '#d86c00'

    def is_notebook(self):
        return 'ipykernel' in sys.modules

    # Display the results of the analysis
    def display_results(self, df=None, answer=None, code=None, rank=None, vector_db=False):
        if self.is_notebook():
            if df is not None:
                self.console.print(Panel(Text(f"{df.dtypes}"), title="DataFrame Structure", border_style="cyan"))
                display(df.head())
            
            if code is not None:
                syntax = Syntax(code, "python", theme=self.theme["code"], line_numbers=True)
                self.console.print(Panel(syntax, title="Applied Python Code", border_style="green"))
            
            if answer is not None:
                self.console.print(Panel(RichMarkdown(answer), title="Solution Summary", border_style="bold green"))
            
            if vector_db and rank is not None:
                self.console.print(Panel(Text(str(rank)), title="Solution Rank", border_style="blue"))
        else:
            if df is not None:
                self.console.print(Panel(Text(f"{df.dtypes}"), title="DataFrame Structure", border_style=self.theme["panel_border"]))
            
            if code is not None:
                syntax = Syntax(code, "python", theme=self.theme["code"], line_numbers=True)
                self.console.print(Panel(syntax, title="Applied Python Code", border_style="green"))
            
            if answer is not None:
                self.console.print(Panel(RichMarkdown(answer), title="Solution Summary", border_style=self.theme["success"]))
            
            if vector_db and rank is not None:
                self.console.print(Panel(Text(str(rank)), title="Solution Rank", border_style=self.theme["info"]))

    def display_expert_selection(self, expert, requires_dataset, confidence):
        grid = Table.grid(expand=True)
        grid.add_column(style="cyan", justify="left")
        grid.add_column(style="white", justify="right")
        grid.add_row("Assigned Expert:", f"[bold]{expert}[/]")
        grid.add_row("Requires Dataset:", "Yes" if requires_dataset else "No")
        grid.add_row("Confidence Score:", f"{confidence}/10")
        
        self.console.print(Panel(grid, title="🧠 Selection Result", border_style="bold green", expand=False))

    def display_analyst_selection(self, analyst, unknown, condition):
        grid = Table.grid(expand=True)
        grid.add_column(style="cyan", justify="left")
        grid.add_row(f"Target Analyst: [bold]{analyst}[/]")
        if unknown: grid.add_row(f"Objective: [italic]{unknown}[/]")
        if condition: grid.add_row(f"Constraints: [italic]{condition}[/]")
        
        self.console.print(Panel(grid, title="🎯 Analysis Strategy", border_style="bold blue", expand=False))

    def display_task_eval(self, task_eval):
        self.console.print(Panel(RichMarkdown(task_eval), title="Agent Reasoning & Strategy", border_style=self.theme["primary"]))
    
    # Display the header for the agent
    def display_tool_start(self, agent, model):
        # Emoji Mapping for professional look
        emojis = {
            "Planner": "📝",
            "SQL Generator": "🗄️",
            "SQL Executor": "⚡",
            "SQL Analyst": "📊",
            "Dataframe Inspector": "🔍",
            "Theorist": "💡",
            "Google Search Query Generator": "🌐",
            "Expert Selector": "🧠",
            "Code Generator": "⚙️",
            "Code Debugger": "🐛",
            "Code Ranker": "🏆",
            "Error Corrector": "🩹",
            "Solution Summarizer": "📋",
            "Analyst Selector": "🎯"
        }
        emoji = emojis.get(agent, "🤖")
        
        msg_map = {
            'Planner': 'Drafting a plan to provide a comprehensive answer...',
            'SQL Generator': 'Generating SQL query based on requirements...',
            'SQL Executor': 'Executing SQL query and formatting results...',
            'SQL Analyst': 'Analyzing the SQL query and providing insights...',
            'Dataframe Inspector': 'Inspecting the dataframe schema...',
            'Theorist': 'Working on an answer to your question...',
            'Google Search Query Generator': 'Generating queries and searching the internet...',
            'Expert Selector': 'Selecting the expert to best answer your query...',
            'Code Generator': 'Generating the first version of the code...',
            'Code Debugger': 'Reviewing and debugging code for inconsistencies...',
            'Code Ranker': 'Assessing, summarizing and ranking the answer...',
            'Error Corrector': 'Analyzing and correcting code errors...',
            'Solution Summarizer': 'Summarizing the solution and insights...',
            'Analyst Selector': 'Selecting the best analyst for your query...'
        }
        msg = msg_map.get(agent, f'Processing request with {agent}...')

        content = Text.assemble(
            ("Model: ", self.theme["secondary"]),
            (f"{model}", self.theme["info"]),
            ("\nAction: ", self.theme["secondary"]),
            (f"{msg}", "bold white")
        )
        self.console.print(Panel(content, title=f"{emoji} {agent}", border_style=self.theme["primary"], expand=False))

    # Display the footer for the agent
    def display_tool_end(self, agent):
        msg = ""
        if agent == 'Code Debugger':
            msg = 'Finished debugging, proceeding to execution...'
        elif agent == 'Code Generator':
            msg = 'Finished generating code, proceeding to execution...'
        
        if not msg: return
        self.console.print(Text(f"✓ {msg}", style=self.theme["success"]))
    
    # Display the error message
    def display_error(self, error):
        self.console.print(Panel(Text(str(error), style="red"), title="⚠️ Execution Error", border_style="red"))
        self.console.print(Text("Retrying with adjusted logic...", style="yellow italic"))
    
    # Display the input to enter the prompt
    def display_user_input_prompt(self):
        prompt_text = "Enter your question (or 'exit' to quit):"
        if self.is_notebook():
            self.console.print(f"\n[bold blue]❯[/] [white]{prompt_text}[/]")
            time.sleep(1)
            question = input()
        else:
            self.console.print(f"\n[bold blue]❯[/] [white]{prompt_text}[/]", end=" ")
            question = input()

        return question
    
    def display_user_input_rank(self):
        prompt_text = "Are you happy with the ranking? (type 'yes' or a new rank 1-10):"
        if self.is_notebook():
            self.console.print(f"\n[bold green]❯[/] [white]{prompt_text}[/]")
            time.sleep(1)
            rank_feedback = input()
        else:
            self.console.print(f"\n[bold green]❯[/] [white]{prompt_text}[/]", end=" ")
            rank_feedback = input()

        return rank_feedback
    
    def display_search_task(self, action, action_input):
        self.console.print(Text(f"🌐 Running {action}: ", style="cyan"), end="")
        self.console.print(f"\"{action_input}\"", style="italic yellow")

    def display_system_messages(self, message):
        self.console.print(Text(f"ℹ️ {message}", style="bold blue"))

    def display_call_summary(self, summary_text):
        table = Table(title="Chain Performance Summary", box=box.ROUNDED, header_style="bold magenta")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="white")
        
        for line in summary_text.split('\n'):
            if line.strip() and ':' in line:
                parts = line.split(':', 1)
                if len(parts) == 2:
                    key, value = parts
                    table.add_row(key.strip(), value.strip())
        
        self.console.print(table)

    def print_wrapper(self, message, end="\n", flush=False):
        if RICH_AVAILABLE and not self.is_notebook():
            self.console.print(message, end=end)
        else:
            print(message, end=end, flush=flush)
