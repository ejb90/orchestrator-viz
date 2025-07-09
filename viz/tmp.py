from rich.console import Console
from rich.table import Table

console = Console()

# Create a table
table = Table(title="Sales Report")

# Add columns
table.add_column("Product", style="cyan")
table.add_column("Quantity", style="magenta")
table.add_column("Price", style="green")

# Add regular rows
table.add_row("Apple", "5", "$1.00")
table.add_row("Orange", "3", "$1.50")

# Add a section subheader with a different style
table.add_row("IMPORTED PRODUCTS", "", "", style="bold yellow")

# Add more rows under the subheader
table.add_row("Kiwi", "8", "$2.00")
table.add_row("Mango", "2", "$3.50")

# Display the table
console.print(table)