from ipdb import set_trace as st
import click
import src.utility

@click.group()
def main():
    """A CLI for firecrawl-skills."""
    pass

@main.command("repl")
def repl_command():
    """Drops into an ipdb debugger session."""
    print("Starting repl (ipdb session)...")
    st()

if __name__ == "__main__":
    main()
