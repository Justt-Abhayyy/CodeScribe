import time
import yaml
import os

from pathlib import Path

from rich.console import Console
from rich.prompt import Confirm

from CodeScribe.utils.file_utils import (
    load_cache,
    save_cache,
    clean_cache
)
from CodeScribe.utils.extract import extract_file_content
from CodeScribe.utils.llm import generate_doc
from CodeScribe.schema.schema import LLMConfig
from CodeScribe.utils.readme import generate_readme_file
from CodeScribe.utils.logger import get_logger


logger = get_logger(__name__)
console = Console()


def update_docs(path, model=None, provider=None):
    """
    Update documentation for a specific file or all files.

    Use '.' to update all configured files.
    """

    start_time = time.time()

    logger.info(
        f"Update sequence triggered for path: {path}. "
        f"Overrides: model={model}, provider={provider}"
    )

    config_path = Path(
        "codescribe.yaml"
    )

    files_to_process = []
    llm_config = None

    # Load configuration
    if config_path.exists():

        try:
            config = yaml.safe_load(
                config_path.read_text(
                    encoding="utf-8"
                )
            ) or {}

            llm_data = config.get(
                "llm",
                {}
            )

            llm_config = (
                LLMConfig(**llm_data)
                if llm_data
                else LLMConfig()
            )

        except Exception as e:

            logger.error(
                f"Failed to read codescribe.yaml: "
                f"{str(e)}",
                exc_info=True
            )

            console.print(
                "[bold red]✖ Error:[/bold red] "
                f"Error reading [blue]codescribe.yaml[/blue]: {e}"
            )

            return

    else:
        config = {}
        llm_config = LLMConfig()

    # CLI overrides
    if model:
        llm_config.model = model

    if provider:
        llm_config.provider = provider

    # Determine files
    if path == ".":

        logger.info(
            "Universal update ('.') requested."
        )

        if not config_path.exists():

            logger.error(
                "codescribe.yaml missing during universal update."
            )

            console.print(
                "[bold red]✖ Error:[/bold red] "
                "[blue]codescribe.yaml[/blue] not found. "
                "Run [bold green]codescribe init[/bold green] first."
            )

            return

        files_to_process = config.get(
            "structure",
            []
        )

        logger.info(
            f"Loaded {len(files_to_process)} "
            "files from configuration for update."
        )

    else:

        logger.info(
            f"Single file update requested for: {path}"
        )

        files_to_process = [path]

    if not files_to_process:

        logger.warning(
            "Update list is empty. Nothing to process."
        )

        console.print(
            "[bold yellow]⚠ Warning:[/bold yellow] "
            "No files found to update."
        )

        return

    # Cache
    try:

        cache = load_cache()

        if path == ".":
            logger.info(
                "Universal update: "
                "cleaning cache of stale entries."
            )

            cache = clean_cache(
                cache,
                files_to_process
            )

            save_cache(cache)

    except Exception as e:

        logger.warning(
            f"Failed to load or clean cache: {e}"
        )

        cache = {
            "files": {}
        }

    session_id = time.strftime(
        "%Y-%m-%d_%H-%M:%S"
    )

    llm_metadata = {
        "session_id": session_id
    }

    all_file_contents = []

    # Reading phase
    with console.status(
        "[bold cyan]Reading[/bold cyan] "
        "project files...",
        spinner="dots"
    ):

        for file_path in files_to_process:

            logger.info(
                f"Extracting content for update: "
                f"{file_path}"
            )

            chunks = extract_file_content(
                file_path
            )

            if not any(
                c.startswith("Error")
                or c.startswith("File not found")
                for c in chunks
            ):

                all_file_contents.append(
                    {
                        "path": file_path,
                        "chunks": chunks
                    }
                )

            else:

                logger.warning(
                    f"File content extraction failed "
                    f"for {file_path}"
                )

    if not all_file_contents:

        logger.error(
            "No valid file content found to update."
        )

        console.print(
            "[bold yellow]⚠ Warning:[/bold yellow] "
            "No valid file content found to process."
        )

        return

    # Summarization
    total_files = len(
        all_file_contents
    )

    def process_file(item):

        file_path = item["path"]
        chunks = item["chunks"]

        summaries = []

        for chunk in chunks:

            try:

                summary = generate_doc(
                    chunk,
                    prompt_type="batch_summary",
                    llm_config=llm_config,
                    metadata=llm_metadata
                )

                if summary:
                    summaries.append(
                        summary.strip()
                    )

            except Exception as e:

                logger.error(
                    f"Error during update for "
                    f"file {file_path}: {str(e)}",
                    exc_info=True
                )

        return (
            file_path,
            "\n\n".join(summaries)
            if summaries
            else ""
        )

    with console.status(
        f"[bold cyan]Processing[/bold cyan] "
        f"Files (0/{total_files})...",
        spinner="dots"
    ) as status:

        processed_count = 0

        for item in all_file_contents:

            file_path, summary = process_file(
                item
            )

            if summary:

                if "files" not in cache:
                    cache["files"] = {}

                expected_filename = os.path.normpath(
                    file_path
                )

                cache["files"][
                    expected_filename
                ] = summary

            processed_count += 1

            status.update(
                f"[bold cyan]Processing[/bold cyan] "
                f"Files ({processed_count}/{total_files})..."
            )

    save_cache(cache)

    # Success message
    if path == ".":
        console.print(
            "[bold green]Updated[/bold green] "
            "artifacts for [white]all files[/white]"
        )
    else:
        console.print(
            "[bold green]Updated[/bold green] "
            f"artifacts for [white]{path}[/white]"
        )

    # README regeneration
    logger.info(
        "Prompting user for README regeneration."
    )

    if Confirm.ask(
        "Regenerate README with latest changes?"
    ):

        logger.info(
            "User confirmed README regeneration."
        )

        config = yaml.safe_load(
            config_path.read_text(
                encoding="utf-8"
            )
        )

        generate_readme_file(
            cache,
            config,
            llm_config=llm_config,
            metadata=llm_metadata
        )

        duration = (
            time.time() - start_time
        )

        console.print(
            "[bold green]Generated[/bold green] "
            f"README.md in "
            f"[white]{duration:.1f} secs[/white]"
        )

    else:

        logger.info(
            "User declined README regeneration."
        )