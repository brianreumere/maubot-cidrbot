import ipaddress

from maubot import Plugin, MessageEvent
from maubot.handlers import command


class CidrBot(Plugin):
    @command.new(require_subcommand=True)
    @command.argument("cidr", pass_raw=True, required=True)
    async def cidr(self, evt: MessageEvent, cidr: str) -> None:
        await evt.mark_read()
        try:
            split = cidr.split("/")
            address = split[0]
            # prefix = split[1]
        except IndexError:
            await evt.reply("Address is not in CIDR notation.")
            return
        message_lines = []
        try:
            network = ipaddress.ip_network(cidr, strict=False)
            if network.network_address.exploded == address:
                message_lines.append(f"`{cidr}` is a network ID.")
            elif network.broadcast_address.exploded == address:
                message_lines.append(
                    f"`{cidr}` is the broadcast address of network `{network.with_prefixlen}`."
                )
            else:
                message_lines.append(
                    f"`{cidr}` is a host address in the network `{network.with_prefixlen}`."
                )
            message_lines.append("- Available host addresses: `{network.num_addresses - 2}`")
            message_lines.append("- Network ID: `{network.network_address.exploded}`")
            message_lines.append("- Prefix: `{network.prefixlen}`")
            message_lines.append("- Netmask: `{network.netmask.exploded}`")
            message_lines.append("- Broadcast address: `{network.broadcast_address.exploded}`")
            await evt.reply("\n".join(message_lines))
        except ValueError:
            await evt.reply("Invalid address.")
