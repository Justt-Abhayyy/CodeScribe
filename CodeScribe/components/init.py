import yaml
from pathlib import Path
from rich.console import Console

from CodeScribe.utils.scanner import scan_repo
from CodeScribe.utils.logger import get_logger
from CodeScribe.config.constants import LiteLLMConfig


logger = get_logger(__name__)
console = Console()


def init_project():
    """
    Initialize or re-initialize a CodeScribe project.
    """

    logger.info(
        f"Init sequence started. Directory: {Path.cwd()}"
    )

    config_path = Path("codescribe.yaml")
    is_reinit = config_path.exists()

    try:
        # Scan repository
        with console.status(
            "[bold cyan]Analyzing[/bold cyan] Repository Structure",
            spinner="dots"
        ):
            repo_structure = scan_repo()

        logger.info(
            f"Scan complete. Found "
            f"{len(repo_structure.get('structure', []))} File Nodes."
        )

        # Update .gitignore
        gitignore_path = Path(".gitignore")

        codescribe_ignores = [
            ".codescribe/",
            "codescribe.yaml"
        ]

        try:
            lines = []

            if gitignore_path.exists():
                content = gitignore_path.read_text(
                    encoding="utf-8"
                )

                lines = [
                    line.strip()
                    for line in content.splitlines()
                    if line.strip()
                ]

            added_any = False

            for entry in codescribe_ignores:
                if entry not in lines:
                    lines.append(entry)
                    added_any = True
                    logger.info(
                        f"Adding {entry} to .gitignore"
                    )

            if added_any or not gitignore_path.exists():
                with open(
                    gitignore_path,
                    "w",
                    encoding="utf-8"
                ) as f:
                    f.write("\n".join(lines) + "\n")

                logger.info(
                    ".gitignore updated successfully"
                )

        except Exception as git_err:
            logger.warning(
                f"Could not update .gitignore: {git_err}"
            )

        # Preserve existing configuration
        existing_config = {}

        if is_reinit:
            try:
                with open(
                    config_path,
                    "r",
                    encoding="utf-8"
                ) as f:
                    existing_config = yaml.safe_load(f) or {}

            except Exception as e:
                logger.warning(
                    f"Could not read existing config: {e}"
                )

        # Default LLM configuration
        llm_defaults = {
            "model": LiteLLMConfig.DEFAULT_MODEL
        }

        llm_config = {
            **llm_defaults,
            **existing_config.get("llm", {})
        }

        final_config = {
            "project": (
                existing_config.get("project")
                or repo_structure.get(
                    "project",
                    Path.cwd().name
                )
            ),
            "structure": repo_structure.get(
                "structure",
                []
            ),
            "llm": llm_config
        }

        # Write configuration
        with open(
            config_path,
            "w",
            encoding="utf-8"
        ) as f:
            yaml.dump(
                final_config,
                f,
                default_flow_style=False,
                sort_keys=False
            )

        logger.info(
            f"Configuration written to {config_path}"
        )

    except Exception as e:
        logger.error(
            f"CodeScribe Initialization Failed: {str(e)}",
            exc_info=True
        )

        console.print(
            f"\n[bold red]✖ Error:[/bold red] "
            f"Failed to Initialize CodeScribe. {str(e)}"
        )

        return

    action = "Reinitialized" if is_reinit else "Initialized"

    console.print(
        f"[bold green]✔ {action}[/bold green] "
        f"[blue]{config_path}[/blue]"
    )

    console.print(
        "\n[bold cyan]Next steps[/bold cyan]"
    )

    console.print(
        f"  • Review [blue]{config_path}[/blue] "
        "to customize included files"
    )

    console.print(
        "  • Run [bold green]codescribe run[/bold green] "
        "to generate documentation"
    )

    logger.info(
        "Init process completed successfully."
    )