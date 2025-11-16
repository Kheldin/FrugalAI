from rich.console import Console
from rich.panel import Panel
import importlib
import respond
from model_interface import call_ai_model

console = Console()

console.print(Panel("Welcome! What can I do for you?", 
                    title="Frugal AI ChatBot", 
                    border_style="cyan"))

while True:
    user_input = input("\nYou: ")
    
    # Commande reload
    if user_input.lower() == "reload":
        importlib.reload(respond)
        console.print("[green]✓ Code reloaded![/green]")
        continue
    
    # Validation du message
    if not respond.is_valid_message(user_input):
        console.print("[yellow]Please enter a valid message.[/yellow]")
        continue
    
    # Détecter la catégorie avec l'algo simple
    category = respond.detect_category(user_input)
    
    # Si catégorie détectée → réponse simple (FRUGAL !)
    if category:
        bot_response = respond.respond(user_input)
        console.print(f"[bold cyan]Bot:[/bold cyan] {bot_response}")
    else:
        # Pas de catégorie → utiliser le modèle IA
        console.print("[yellow]🤖 Redirecting to AI model...[/yellow]")
        call_ai_model(user_input)  # N'affiche plus "Bot: None"
    
    # Si au revoir, quitter
    if category == "reply_goodbye":
        break