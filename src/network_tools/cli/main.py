"""Main CLI entry point for network-tools."""

import click

from network_tools import __version__


def get_console():
    """Get a Rich console configured for Windows compatibility."""
    from rich.console import Console

    # Force UTF-8 for Windows compatibility
    return Console(force_terminal=True, legacy_windows=False)


@click.group()
@click.version_option(version=__version__, prog_name="network-tools")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.pass_context
def cli(ctx: click.Context, verbose: bool) -> None:
    """Network Tools - Automated network device discovery and inventory management."""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose


@cli.command()
@click.option(
    "--network",
    "-n",
    required=True,
    help="Network CIDR to scan (e.g., 192.168.68.0/24)",
)
@click.option(
    "--site",
    "-s",
    default="ra-home-31-nt",
    help="Site slug for inventory association",
)
@click.option(
    "--yes",
    "-y",
    is_flag=True,
    help="Auto-confirm all new devices (non-interactive)",
)
@click.pass_context
def discover(ctx: click.Context, network: str, site: str, yes: bool) -> None:
    """Discover devices on a network and compare with inventory."""
    console = get_console()

    console.print("[bold]Network Discovery[/bold]")
    console.print(f"  Network: {network}")
    console.print(f"  Site: {site}")
    console.print(f"  Auto-confirm: {yes}")
    console.print()

    # TODO: Implement discovery logic
    console.print("[yellow]Discovery not yet implemented. Coming in Phase 1.[/yellow]")


@cli.command()
@click.pass_context
def status(ctx: click.Context) -> None:
    """Show database connection status and inventory summary."""
    from rich.table import Table

    from network_tools.db import get_connection
    from network_tools.config import get_config

    console = get_console()
    config = get_config()

    console.print("[bold]Database Status[/bold]")
    console.print()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                # Get device count
                cur.execute("SELECT COUNT(*) FROM devices")
                device_count = cur.fetchone()[0]

                # Get site count
                cur.execute("SELECT COUNT(*) FROM sites")
                site_count = cur.fetchone()[0]

                # Get network count
                cur.execute("SELECT COUNT(*) FROM networks")
                network_count = cur.fetchone()[0]

        table = Table(title="Inventory Summary")
        table.add_column("Entity", style="cyan")
        table.add_column("Count", style="green", justify="right")

        table.add_row("Sites", str(site_count))
        table.add_row("Networks", str(network_count))
        table.add_row("Devices", str(device_count))

        console.print(f"[green]OK[/green] Connected to {config.db_name}@{config.db_host}")
        console.print()
        console.print(table)

    except Exception as e:
        console.print(f"[red]FAIL[/red] Database connection failed: {e}")
    finally:
        # Clean up connection pool to avoid shutdown warnings
        from network_tools.db.connection import close_pool
        close_pool()


if __name__ == "__main__":
    cli()
