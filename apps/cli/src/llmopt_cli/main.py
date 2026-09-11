"""Thin CLI shell with no product execution behavior."""

from typing import Annotated

import typer

app = typer.Typer(
    name="llmopt",
    help="Orionix LLM inference optimization platform (foundation milestone).",
    no_args_is_help=True,
)


def _not_implemented(command: str) -> None:
    typer.echo(f"'{command}' is not implemented in this milestone.")


@app.command()
def inspect() -> None:
    """Inspect model and hardware capabilities (placeholder)."""
    _not_implemented("inspect")


@app.command()
def analyze() -> None:
    """Analyze a workload (placeholder)."""
    _not_implemented("analyze")


@app.command()
def benchmark() -> None:
    """Execute a benchmark plan (placeholder)."""
    _not_implemented("benchmark")


@app.command()
def optimize(
    profile: Annotated[
        str | None,
        typer.Option(help="Reserved optimization profile name."),
    ] = None,
) -> None:
    """Optimize a serving configuration (placeholder)."""
    del profile
    _not_implemented("optimize")


@app.command()
def quality() -> None:
    """Validate candidate quality (placeholder)."""
    _not_implemented("quality")


@app.command()
def status() -> None:
    """Show optimization-job status (placeholder)."""
    _not_implemented("status")


@app.command()
def report() -> None:
    """Render an optimization report (placeholder)."""
    _not_implemented("report")


@app.command()
def capsule() -> None:
    """Manage Execution Capsule metadata (placeholder)."""
    _not_implemented("capsule")


@app.command(name="export")
def export_command() -> None:
    """Export a configuration or capsule (placeholder)."""
    _not_implemented("export")


@app.command()
def agent() -> None:
    """Manage the customer agent (placeholder)."""
    _not_implemented("agent")


@app.command()
def diagnostics() -> None:
    """Collect redacted diagnostics (placeholder)."""
    _not_implemented("diagnostics")


@app.command()
def cleanup() -> None:
    """Clean local generated artifacts (placeholder)."""
    _not_implemented("cleanup")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
