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
def discover(ctx: click.Context, network: str, yes: bool, no_ping: bool) -> None:
    """Discover devices on a network and sync with Snipe-IT."""
    from rich.table import Table

    from network_tools.config import get_config
    from network_tools.oui import guess_device_type, lookup_manufacturer
    from network_tools.scanner import scan_network
    from network_tools.snipeit import (
        SnipeITClient,
        SnipeITConnectionError,
        SnipeITAuthError,
        DiscoveredDevice,
    )

    console = get_console()
    verbose = ctx.obj.get("verbose", False)
    config = get_config()

    console.print("[bold]Network Discovery[/bold]")
    console.print(f"  Network: {network}")
    console.print(f"  Auto-confirm: {yes}")
    console.print()

    try:
        # Step 1: Connect to Snipe-IT
        console.print("[cyan]Connecting to Snipe-IT...[/cyan]")

        if not config.snipeit_api_key:
            console.print("[red]ERROR[/red] SNIPEIT_API_KEY not configured")
            console.print("  Set the environment variable or update .env file")
            return

        client = SnipeITClient(
            base_url=config.snipeit_base_url,
            api_key=config.snipeit_api_key,
            timeout=config.snipeit_timeout,
        )

        try:
            client.test_connection()
            console.print(f"[green]OK[/green] Connected to {config.snipeit_base_url}")
        except SnipeITAuthError:
            console.print("[red]ERROR[/red] Authentication failed. Check API key.")
            return
        except SnipeITConnectionError as e:
            console.print(f"[red]ERROR[/red] Connection failed: {e}")
            return

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

        # Step 3: Get existing Snipe-IT assets
        console.print("[cyan]Fetching Snipe-IT inventory...[/cyan]")
        existing_assets = client.get_network_assets(
            category_id=config.snipeit_network_category_id
        )
        console.print(f"[green]OK[/green] Found {len(existing_assets)} network assets in Snipe-IT")
        console.print()

        # Build MAC -> Asset lookup
        mac_to_asset = {}
        for asset in existing_assets:
            if asset.mac_address:
                mac_normalized = asset.mac_address.upper().replace("-", ":")
                mac_to_asset[mac_normalized] = asset

        # Step 4: Compare with inventory
        console.print("[cyan]Comparing discovered devices...[/cyan]")

        new_devices: list[DiscoveredDevice] = []
        existing_devices: list[tuple] = []  # (discovered, asset)
        updated_devices: list[tuple] = []  # (discovered, asset, changes)

        for entry in arp_entries:
            manufacturer = lookup_manufacturer(entry.mac_address)
            device_type = guess_device_type(manufacturer)

            mac_normalized = entry.mac_address.upper().replace("-", ":")

            discovered = DiscoveredDevice(
                ip_address=entry.ip_address,
                mac_address=entry.mac_address,
                manufacturer=manufacturer,
                device_type_guess=device_type,
                discovery_method="arp",
            )

            # Check if device exists in Snipe-IT
            existing_asset = mac_to_asset.get(mac_normalized)

            if existing_asset is None:
                # New device
                discovered.status = "new"
                new_devices.append(discovered)
            else:
                # Existing device - check for IP changes
                discovered.matched_asset = existing_asset
                if existing_asset.ip_address != entry.ip_address:
                    discovered.status = "updated"
                    updated_devices.append(
                        (discovered, existing_asset, {"ip_address": entry.ip_address})
                    )
                else:
                    discovered.status = "existing"
                    existing_devices.append((discovered, existing_asset))

        console.print(f"[green]OK[/green] Comparison complete")
        console.print()

        # Step 5: Display results summary
        console.print("[bold]Summary:[/bold]")
        console.print(f"  New devices:      {len(new_devices)}")
        console.print(f"  Updated (IP):     {len(updated_devices)}")
        console.print(f"  Unchanged:        {len(existing_devices)}")
        console.print()

        # Show existing devices (brief)
        if existing_devices and verbose:
            console.print(f"[dim]Existing devices (no changes):[/dim]")
            for discovered, asset in existing_devices:
                console.print(f"  [dim]{discovered.ip_address} - {asset.name}[/dim]")
            console.print()

        # Show updated devices
        if updated_devices:
            console.print(f"[yellow]Devices with IP changes: {len(updated_devices)}[/yellow]")
            update_table = Table()
            update_table.add_column("Name", style="cyan")
            update_table.add_column("MAC", style="dim")
            update_table.add_column("Old IP", style="red")
            update_table.add_column("New IP", style="green")

            for discovered, asset, changes in updated_devices:
                update_table.add_row(
                    asset.name,
                    discovered.mac_address,
                    asset.ip_address or "-",
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

            # Validate model_id is configured
            if config.snipeit_default_model_id == 0:
                console.print(
                    "[yellow]WARNING[/yellow] SNIPEIT_DEFAULT_MODEL_ID not set. "
                    "Set this to a valid model ID in Snipe-IT."
                )
                console.print()

            # Step 6: Handle new devices
            if yes:
                # Auto-confirm all
                console.print("[cyan]Auto-confirming all new devices...[/cyan]")
                added_count = 0
                for discovered in new_devices:
                    try:
                        payload = discovered.to_snipeit_payload(
                            model_id=config.snipeit_default_model_id,
                            status_id=config.snipeit_default_status_id,
                        )
                        asset = client.create_hardware(payload)
                        added_count += 1
                        console.print(
                            f"  [green]+[/green] Added: {asset.name} "
                            f"(Tag: {asset.asset_tag})"
                        )
                    except Exception as e:
                        console.print(
                            f"  [red]x[/red] Failed to add {discovered.ip_address}: {e}"
                        )

                console.print()
                console.print(f"[green]OK[/green] Added {added_count} new devices to Snipe-IT")
            else:
                # Interactive mode
                console.print("[yellow]Interactive mode: Review each device[/yellow]")
                console.print("  [y] Add to Snipe-IT")
                console.print("  [n] Skip")
                console.print("  [a] Add all remaining")
                console.print("  [q] Quit")
                console.print()

                added_count = 0
                auto_add = False

                for i, discovered in enumerate(new_devices, 1):
                    if not auto_add:
                        console.print(f"[bold]Device {i}/{len(new_devices)}:[/bold]")
                        console.print(f"  IP: {discovered.ip_address}")
                        console.print(f"  MAC: {discovered.mac_address}")
                        console.print(f"  Manufacturer: {discovered.manufacturer or 'Unknown'}")
                        console.print(f"  Type: {discovered.device_type_guess or 'unknown'}")
                        console.print(f"  Asset Tag: {discovered.generate_asset_tag()}")

                    while True:
                        if auto_add:
                            response = "y"
                        else:
                            response = click.prompt(
                                "Add to Snipe-IT?", type=str, default="y"
                            )
                            response = response.lower().strip()

                        if response in ("y", "yes"):
                            try:
                                payload = discovered.to_snipeit_payload(
                                    model_id=config.snipeit_default_model_id,
                                    status_id=config.snipeit_default_status_id,
                                )
                                asset = client.create_hardware(payload)
                                added_count += 1
                                console.print(
                                    f"  [green]+[/green] Added: {asset.name} "
                                    f"(Tag: {asset.asset_tag})"
                                )
                            except Exception as e:
                                console.print(f"  [red]x[/red] Failed: {e}")
                            break
                        elif response in ("n", "no"):
                            console.print("  [dim]Skipped[/dim]")
                            break
                        elif response in ("a", "all"):
                            auto_add = True
                            console.print("[cyan]Adding all remaining devices...[/cyan]")
                            # Process this device
                            try:
                                payload = discovered.to_snipeit_payload(
                                    model_id=config.snipeit_default_model_id,
                                    status_id=config.snipeit_default_status_id,
                                )
                                asset = client.create_hardware(payload)
                                added_count += 1
                                console.print(
                                    f"  [green]+[/green] Added: {asset.name} "
                                    f"(Tag: {asset.asset_tag})"
                                )
                            except Exception as e:
                                console.print(f"  [red]x[/red] Failed: {e}")
                            break
                        elif response in ("q", "quit"):
                            console.print("[yellow]Quitting...[/yellow]")
                            console.print(f"[green]OK[/green] Added {added_count} devices")
                            return
                        else:
                            console.print("  [red]Invalid input. Use y/n/a/q[/red]")

                    if not auto_add:
                        console.print()

                console.print()
                console.print(f"[green]OK[/green] Added {added_count} new devices to Snipe-IT")
        else:
            console.print("[green]No new devices found - inventory is up to date[/green]")

    except Exception as e:
        console.print(f"[red]ERROR[/red] Discovery failed: {e}")
        if verbose:
            import traceback

            console.print(f"[dim]{traceback.format_exc()}[/dim]")


@cli.command()
@click.pass_context
def status(ctx: click.Context) -> None:
    """Show Snipe-IT connection status and asset summary."""
    from rich.table import Table

    from network_tools.config import get_config
    from network_tools.snipeit import (
        SnipeITClient,
        SnipeITConnectionError,
        SnipeITAuthError,
    )

    console = get_console()
    config = get_config()

    console.print("[bold]Snipe-IT Status[/bold]")
    console.print()

    if not config.snipeit_api_key:
        console.print("[red]ERROR[/red] SNIPEIT_API_KEY not configured")
        console.print("  Set the environment variable or update .env file")
        return

    try:
        client = SnipeITClient(
            base_url=config.snipeit_base_url,
            api_key=config.snipeit_api_key,
            timeout=config.snipeit_timeout,
        )

        client.test_connection()
        console.print(f"[green]OK[/green] Connected to {config.snipeit_base_url}")
        console.print()

        # Get counts
        counts = client.get_asset_counts()

        table = Table(title="Asset Summary")
        table.add_column("Category", style="cyan")
        table.add_column("Count", style="green", justify="right")

        table.add_row("Total Assets", str(counts.get("total", 0)))
        table.add_row("Network Assets", str(counts.get("network", 0)))

        console.print(table)

    except SnipeITAuthError:
        console.print("[red]FAIL[/red] Authentication failed. Check API key.")
    except SnipeITConnectionError as e:
        console.print(f"[red]FAIL[/red] Connection failed: {e}")
    except Exception as e:
        console.print(f"[red]FAIL[/red] Error: {e}")


@cli.command()
@click.option("--mac", help="Search by MAC address")
@click.option("--ip", help="Search by IP address")
@click.pass_context
def search(ctx: click.Context, mac: str | None, ip: str | None) -> None:
    """Search for an asset in Snipe-IT by MAC or IP address."""
    from network_tools.config import get_config
    from network_tools.snipeit import (
        SnipeITClient,
        SnipeITConnectionError,
        SnipeITAuthError,
    )

    console = get_console()
    config = get_config()

    if not mac and not ip:
        console.print("[red]ERROR[/red] Specify --mac or --ip to search")
        return

    if not config.snipeit_api_key:
        console.print("[red]ERROR[/red] SNIPEIT_API_KEY not configured")
        return

    try:
        client = SnipeITClient(
            base_url=config.snipeit_base_url,
            api_key=config.snipeit_api_key,
            timeout=config.snipeit_timeout,
        )

        asset = None
        search_type = ""

        if mac:
            console.print(f"[cyan]Searching for MAC: {mac}[/cyan]")
            asset = client.search_by_mac(mac)
            search_type = "MAC"
        elif ip:
            console.print(f"[cyan]Searching for IP: {ip}[/cyan]")
            asset = client.search_by_ip(ip)
            search_type = "IP"

        console.print()

        if asset:
            console.print(f"[green]Found asset:[/green]")
            console.print(f"  Name:         {asset.name}")
            console.print(f"  Asset Tag:    {asset.asset_tag}")
            console.print(f"  MAC Address:  {asset.mac_address or '-'}")
            console.print(f"  IP Address:   {asset.ip_address or '-'}")
            console.print(f"  Category:     {asset.category_name or '-'}")
            console.print(f"  Status:       {asset.status_name or '-'}")
            console.print(f"  Location:     {asset.location_name or '-'}")
            console.print(f"  Manufacturer: {asset.manufacturer_name or '-'}")
            if asset.notes:
                console.print(f"  Notes:        {asset.notes[:100]}...")
        else:
            console.print(f"[yellow]No asset found with {search_type}: {mac or ip}[/yellow]")

    except SnipeITAuthError:
        console.print("[red]FAIL[/red] Authentication failed. Check API key.")
    except SnipeITConnectionError as e:
        console.print(f"[red]FAIL[/red] Connection failed: {e}")
    except Exception as e:
        console.print(f"[red]FAIL[/red] Error: {e}")


if __name__ == "__main__":
    cli()
