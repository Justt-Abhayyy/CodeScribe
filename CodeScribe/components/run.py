import yaml
import time
import os

from typing import Optional
from pathlib import Path

from rich.console import Console

from CodeScribe.utils.extract import extract_file_content
from CodeScribe.utils.llm import generate_doc
from CodeScribe.utils.file_utils import (
    load_cache,
    save_cache,
    clean_cache
)
from CodeScribe.config.constants import LiteLLMConfig
from CodeScribe.schema.schema import LLMConfig
from CodeScribe.utils.readme import generate_readme_file
from CodeScribe.utils.logger import get_logger


logger = get_logger(__name__)
console = Console()


def run_docs(model=None, provider=None):
    """
    Generates documentation with a 200k token-based batching strategy.
    """

    logger.info(
        f"Starting documentation generation pipeline. "
        f"Overrides: model={model}"
    )

    start_time = time.time()

    # Configuration
    config_path = Path("codescribe.yaml")

    if not config_path.exists():
        logger.warning(
            f"Configuration file {config_path} missing."
        )

        console.print(
            "[bold red]✖ Error:[/bold red] "
            "[blue]codescribe.yaml[/blue] not found. "
            "Run [bold green]codescribe init[/bold green] first."
        )

        return

    try:
        config = yaml.safe_load(
            config_path.read_text(
                encoding="utf-8"
            )
        ) or {}

        logger.info(
            "codescribe.yaml found and loaded successfully."
        )

        files = config.get(
            "structure",
            []
        )

        llm_model = config.get(
            "llm",
            {}
        ).get(
            "model",
            ""
        )

        generate_readme = True

        logger.info(
            f"Retrieved {len(files)} files "
            f"from codescribe.yaml."
        )

        logger.info(
            f"Retrieved {llm_model} model "
            f"from codescribe.yaml."
        )

        if not llm_model or not llm_model.strip():
            llm_model = LiteLLMConfig.DEFAULT_MODEL

        llm_config_data = config.get(
            "llm",
            {}
        )

        llm_config = LLMConfig(
            **llm_config_data
        )

        # CLI overrides
        if model:
            llm_config.model = model

        if provider:
            llm_config.provider = provider

        session_id = time.strftime(
            "%Y-%m-%d_%H-%M:%S"
        )

        project_name = config.get(
            "project",
            os.path.basename(
                os.getcwd()
            )
        )

        llm_metadata = {
            "session_id": session_id,
            "project_name": project_name
        }

        if not files:
            logger.warning(
                "No files found in codescribe.yaml structure."
            )

            console.print(
                "[bold yellow]⚠ Warning:[/bold yellow] "
                "No files found in [blue]codescribe.yaml[/blue]"
            )

            return

        # Cache handling
        logger.info(
            "Initializing cache for file summaries."
        )

        cache = load_cache()

        if "files" not in cache:
            cache["files"] = {}

        for file_path in files:
            if file_path not in cache["files"]:
                cache["files"][file_path] = ""

        cache = clean_cache(
            cache,
            files
        )

        save_cache(cache)

        console.print(
            f"[bold cyan]Found[/bold cyan] "
            f"[white]{len(files)} Files[/white] to Process"
        )

        extracted_files = []

        # File reading phase
        with console.status(
            "[bold cyan]Extracting[/bold cyan] "
            "Repository Files",
            spinner="dots"
        ):

            for file_path in files:
                chunks = extract_file_content(
                    file_path
                )

                if not any(
                    c.startswith("Error")
                    or c.startswith("File not found")
                    for c in chunks
                ):
                    tokens = (
                        sum(len(c) for c in chunks)
                        // 4
                    )

                    extracted_files.append(
                        {
                            "path": file_path,
                            "chunks": chunks,
                            "tokens": tokens
                        }
                    )

                else:
                    logger.warning(
                        f"Skipping {file_path} "
                        "due to extraction errors."
                    )

        if not extracted_files:
            logger.error(
                "No valid file content found to process."
            )

            console.print(
                "[bold yellow]⚠ Warning:[/bold yellow] "
                "No valid file content found to process."
            )

            return

        # Process each file
        def process_file(
            item,
            llm_config: Optional[LLMConfig] = None,
            metadata: Optional[dict] = None
        ):
            """
            Processes a single file and generates
            a documentation summary.
            """

            file_path = item["path"]
            chunks = item["chunks"]

            summaries = []

            for chunk in chunks:
                try:
                    summary = generate_doc(
                        code_content=chunk,
                        prompt_type="batch_summary",
                        llm_config=llm_config,
                        metadata=metadata
                    )

                    if summary:
                        summaries.append(
                            summary.strip()
                        )

                except Exception as e:
                    logger.error(
                        f"Error processing chunk for "
                        f"{file_path}: {str(e)}",
                        exc_info=True
                    )

            return (
                item,
                "\n\n".join(summaries)
                if summaries
                else ""
            )

        total_files = len(
            extracted_files
        )

        processed_count = 0

        for item in extracted_files:

            with console.status(
                f"[bold cyan]Summarizing[/bold cyan] "
                f"({processed_count}/{total_files})...",
                spinner="dots"
            ):

                item_ret, summary = process_file(
                    item,
                    llm_config=llm_config,
                    metadata=llm_metadata
                )

            if summary:
                norm_path = os.path.normpath(
                    item["path"]
                )

                cache["files"][norm_path] = summary

            processed_count += 1

        save_cache(cache)

        # Generate README
        if generate_readme:
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
            f"[bold green]Generated[/bold green] "
            f"README.md in "
            f"[white]{duration:.1f} secs[/white]"
        )

        logger.info(
            f"Pipeline completed successfully "
            f"in {duration:.2f}s"
        )

    except Exception as e:
        logger.critical(
            f"Pipeline failed: {str(e)}",
            exc_info=True
        )

        console.print(
            "[bold red]✖ Failed[/bold red] "
            f"to generate Documentation: {e}"
        )