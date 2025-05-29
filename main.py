from ipdb import set_trace as st
import click
from src.utility import get_firecrawl_api_key
from src.firecrawl import run_examples, app
from dotenv import load_dotenv
import os

FIRECRAWL_API_KEY = get_firecrawl_api_key()

print(f"Using Firecrawl API Key: {FIRECRAWL_API_KEY[:10]}...")


# ------------------------------------------------
# SUBCOMMANDS ------------------------------------
# ------------------------------------------------
@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    """A CLI for firecrawl-skills."""
    if ctx.invoked_subcommand is None:
        ctx.invoke(repl_command)


@main.command("repl")
def repl_command():
    """Drops into an ipdb debugger session."""
    print("Starting repl (ipdb session)...")
    st()


@main.command("scratch")
def scratch_command():
    """Runs the scratchpad code."""
    print("Running scratch command...")
    # You can add the logic from src/scratch.py here or import and call it
    # For now, it just prints a message.


@main.command("firecrawl-examples")
def firecrawl_examples_command():
    """Runs the Firecrawl examples."""
    print("Running Firecrawl examples...")
    run_examples()


@main.command("help")
@click.pass_context
def help_command(ctx):
    """Shows the help message."""
    # The parent context is the main command group
    click.echo(ctx.parent.get_help())


main.add_command(help_command, name="h")


if __name__ == "__main__":
    main()
