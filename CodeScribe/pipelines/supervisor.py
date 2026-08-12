import click
from rich.console import Console
from dotenv import load_dotenv

from CodeScribe.components.init import init_project
from CodeScribe import __version__

console = Console()

# Load environment variables from a .env file if it exists
# in the current directory.
load_dotenv()


@click.group()
@click.version_option(version=__version__)
def cli():
    """
    CodeScribe: AI-powered project documentation generator.

    Automatically generate, update, and manage your project's
    README and codebase documentation using LLMs.
    """
    pass


@cli.command()
def init():
    """
    Initialize a new CodeScribe project and create codescribe.yaml.

    This command scans your current directory while respecting
    your .gitignore, creates a local caching folder, and generates
    a codescribe.yaml configuration file.
    """
    init_project()


@cli.group(name="set")
def set_group():
    """
    Set configuration settings for CodeScribe.

    Use this command group to modify your codescribe.yaml
    configuration directly from the command line.
    """
    pass


@set_group.command("default")
@click.argument("model")
def set_default(model):
    """
    Set the default LLM model in codescribe.yaml.

    MODEL: The exact model ID from Groq that you wish to use.
    """
    from CodeScribe.components.config import update_config

    update_config(model=model)


@cli.command()
@click.option(
    "--model",
    help="Temporarily override the LLM model specified in codescribe.yaml.",
)
@click.option(
    "--provider",
    help="Temporarily override the LLM provider.",
)
def run(model, provider):
    """
    Run the complete documentation generation pipeline.

    This command reads codescribe.yaml, extracts code from the
    specified files, generates AI summaries, and produces a
    professional README.md.

    If README.md already exists, it will be backed up to
    README-prev.md before being overwritten.
    """
    from CodeScribe.components.run import run_docs

    run_docs(model=model, provider=provider)


@cli.command()
@click.argument("path", type=click.Path(exists=True), required=True)
@click.option(
    "--model",
    help="Temporarily override the LLM model specified in codescribe.yaml.",
)
@click.option(
    "--provider",
    help="Temporarily override the LLM provider.",
)
def update(path, model, provider):
    """
    Update documentation for a specific file or all files.

    PATH: The specific file or directory to update.

    Pass '.' to regenerate README.md from the existing cache
    without making new API calls.
    """
    from CodeScribe.components.update import update_docs

    update_docs(path, model=model, provider=provider)


@cli.command()
def models():
    """
    List all available models from the Groq API.

    Displays a formatted table of currently available
    models on the Groq network.
    """
    from CodeScribe.components.models import list_models

    list_models()


if __name__ == "__main__":
    cli()