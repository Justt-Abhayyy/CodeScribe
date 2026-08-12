import yaml
from pathlib import Path
from rich.console import Console

from CodeScribe.utils.logger import get_logger


logger = get_logger(__name__)
console = Console()


def update_config(model=None):
    """
    Updates the codescribe.yaml configuration with new LLM settings
    while preserving the existing configuration.
    """

    config_path = Path("codescribe.yaml")

    if not config_path.exists():
        console.print(
            "[bold red]✖ Error:[/bold red] "
            "[blue]codescribe.yaml[/blue] not found. "
            "Run [bold green]codescribe init[/bold green] first."
        )
        return

    try:
        content = yaml.safe_load(
            config_path.read_text(encoding="utf-8")
        ) or {}

        if "llm" not in content:
            content["llm"] = {}

        if model:
            content["llm"]["model"] = model

        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(
                content,
                f,
                default_flow_style=False,
                sort_keys=False
            )

        logger.info(f"Config updated: {content}")

        console.print(
            f"[bold green]✔ Updated[/bold green] "
            f"[blue]Default Model[/blue] configuration: "
            f"[cyan]{model}[/cyan]"
        )

    except Exception as e:
        logger.error(f"Failed to update config: {e}")

        console.print(
            f"[bold red]✖ Error:[/bold red] "
            f"Could not update configuration. {e}"
        )