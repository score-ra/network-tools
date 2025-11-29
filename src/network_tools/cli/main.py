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
@click.option(
    "--no-ping",
    is_flag=True,
    help="Skip ping sweep (use existing ARP table only)",
)
@click.pass_context
def discover(ctx: click.Context, network: str, site: str, yes: bool, no_ping: bool) -> None:
    """Discover devices on a network and compare with inventory."""
    from rich.table import Table

    from network_tools.db import get_connection
    from network_tools.db.connection import close_pool
    from network_tools.db.models import DiscoveredDevice
    from network_tools.db.queries import get_device_by_mac, get_site_by_slug, insert_device
    from network_tools.oui import guess_device_type, lookup_manufacturer
    from network_tools.scanner import scan_network

    console = get_console()
    verbose = ctx.obj.get("verbose", False)

    console.print("[bold]Network Discovery[/bold]")
    console.print(f"  Network: {network}")
    console.print(f"  Site: {site}")
    console.print(f"  Auto-confirm: {yes}")
    console.print()

    try:
        # Step 1: Verify site exists
        console.print("[cyan]Checking site...[/cyan]")
        site_obj = get_site_by_slug(site)
        if not site_obj:
            console.print(f"[red]ERROR[/red] Site '{site}' not found in database")
            return
        console.print(f"[green]OK[/green] Site: {site_obj.name}")
        console.print()

        # Step 2: Scan network
        console.print(f"[cyan]Scanning network {network}...[/cyan]")
        if no_ping:
            console.print("  (using existing ARP table only)")
        else:
            console.print("  (ping sweep + ARP table)")

        arp_entries = scan_network(network, use_ping=not no_ping)
        console.print(f"[green]OK[/green] Found {len(arp_entries)} devices on network")
        console.print()

        if not arp_entries:
            console.print("[yellow]No devices found on network[/yellow]")
            return

        # Step 3: Compare with inventory
        console.print("[cyan]Comparing with inventory...[/cyan]")

        new_devices: list[DiscoveredDevice] = []
        existing_devices: list[tuple] = []  # (arp_entry, db_device)
        updated_devices: list[tuple] = []  # (arp_entry, db_device, changes)

        for entry in arp_entries:
            manufacturer = lookup_manufacturer(entry.mac_address)
            device_type = guess_device_type(manufacturer)

            # Check if device exists in DB
            db_device = get_device_by_mac(entry.mac_address)

            if db_device is None:
                # New device
                discovered = DiscoveredDevice(
                    ip_address=entry.ip_address,
                    mac_address=entry.mac_address,
                    manufacturer=manufacturer,
                    device_type_guess=device_type,
                    discovery_method="arp",
                )
                new_devices.append(discovered)
            else:
                # Existing device - check for IP changes
                if db_device.ip_address != entry.ip_address:
                    updated_devices.append((entry, db_device, {"ip_address": entry.ip_address}))
                else:
                    existing_devices.append((entry, db_device))

        console.print(f"[green]OK[/green] Comparison complete")
        console.print()

        # Step 4: Display results
        # Show existing devices (brief)
        if existing_devices:
            console.print(f"[dim]Existing devices (no changes): {len(existing_devices)}[/dim]")
            if verbose:
                for entry, device in existing_devices:
                    console.print(f"  [dim]{entry.ip_address} - {device.name}[/dim]")
            console.print()

        # Show updated devices
        if updated_devices:
            console.print(f"[yellow]Devices with IP changes: {len(updated_devices)}[/yellow]")
            update_table = Table()
            update_table.add_column("Name", style="cyan")
            update_table.add_column("MAC", style="dim")
            update_table.add_column("Old IP", style="red")
            update_table.add_column("New IP", style="green")

            for entry, device, changes in updated_devices:
                update_table.add_row(
                    device.name,
                    entry.mac_address,
                    device.ip_address or "-",
                    changes.get("ip_address", "-"),
                )
            console.print(update_table)
            console.print()

        # Show new devices
        if new_devices:
            console.print(f"[bold green]New devices found: {len(new_devices)}[/bold green]")
            new_table = Table()
            new_table.add_column("#", style="dim", width=3)
            new_table.add_column("IP Address", style="cyan")
            new_table.add_column("MAC Address", style="dim")
            new_table.add_column("Manufacturer", style="yellow")
            new_table.add_column("Type Guess", style="magenta")

            for i, device in enumerate(new_devices, 1):
                new_table.add_row(
                    str(i),
                    device.ip_address,
                    device.mac_address,
                    device.manufacturer or "Unknown",
                    device.device_type_guess or "unknown",
                )
            console.print(new_table)
            console.print()

            # Step 5: Handle new devices
            if yes:
                # Auto-confirm all
                console.print("[cyan]Auto-confirming all new devices...[/cyan]")
                added_count = 0
                for discovered in new_devices:
                    try:
                        device = discovered.to_device(site_id=site_obj.id)
                        device_id = insert_device(device)
                        added_count += 1
                        console.print(f"  [green]+[/green] Added: {device.name} ({device.ip_address})")
                    except Exception as e:
                        console.print(f"  [red]x[/red] Failed to add {discovered.ip_address}: {e}")

                console.print()
                console.print(f"[green]OK[/green] Added {added_count} new devices to inventory")
            else:
                # Interactive mode
                console.print("[yellow]Interactive mode: Review each device[/yellow]")
                console.print("  [y] Add to inventory")
                console.print("  [n] Skip")
                console.print("  [q] Quit")
                console.print()

                added_count = 0
                for i, discovered in enumerate(new_devices, 1):
                    console.print(f"[bold]Device {i}/{len(new_devices)}:[/bold]")
                    console.print(f"  IP: {discovered.ip_address}")
                    console.print(f"  MAC: {discovered.mac_address}")
                    console.print(f"  Manufacturer: {discovered.manufacturer or 'Unknown'}")
                    console.print(f"  Type: {discovered.device_type_guess or 'unknown'}")

                    while True:
                        response = click.prompt("Add to inventory?", type=str, default="y")
                        response = response.lower().strip()

                        if response in ("y", "yes"):
                            try:
                                device = discovered.to_device(site_id=site_obj.id)
                                device_id = insert_device(device)
                                added_count += 1
                                console.print(f"  [green]+[/green] Added: {device.name}")
                            except Exception as e:
                                console.print(f"  [red]x[/red] Failed: {e}")
                            break
                        elif response in ("n", "no"):
                            console.print("  [dim]Skipped[/dim]")
                            break
                        elif response in ("q", "quit"):
                            console.print("[yellow]Quitting...[/yellow]")
                            console.print(f"[green]OK[/green] Added {added_count} devices")
                            return
                        else:
                            console.print("  [red]Invalid input. Use y/n/q[/red]")

                    console.print()

                console.print(f"[green]OK[/green] Added {added_count} new devices to inventory")
        else:
            console.print("[green]No new devices found - inventory is up to date[/green]")

    except Exception as e:
        console.print(f"[red]ERROR[/red] Discovery failed: {e}")
        if verbose:
            import traceback
            console.print(f"[dim]{traceback.format_exc()}[/dim]")
    finally:
        close_pool()


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
