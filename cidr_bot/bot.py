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
            single_host_or_p2p = False
            if network.prefixlen == 32:
                single_host_or_p2p = True
                message_lines.append(f"`{cidr}` is a single host address.")
            elif network.prefixlen == 31:
                single_host_or_p2p = True
                message_lines.append(
                    f"`{cidr}` contains two addresses and may be used for a point-to-point link "
                    "per "
                    "[RFC 3021](https://datatracker.ietf.org/doc/html/rfc3021)."
                )
            elif network.network_address.exploded == address:
                message_lines.append(f"`{cidr}` is a network ID.")
            elif network.broadcast_address.exploded == address:
                message_lines.append(
                    f"`{cidr}` is the broadcast address of network `{network.with_prefixlen}`."
                )
            else:
                message_lines.append(
                    f"`{cidr}` is a host address in the network `{network.with_prefixlen}`."
                )
            message_lines.append(f"- Available host addresses: `{network.num_addresses - 2}`")
            if not single_host_or_p2p:
                message_lines.append(f"- Network ID: `{network.network_address.exploded}`")
                message_lines.append(f"- Broadcast address: `{network.broadcast_address.exploded}`")
            message_lines.append(f"- Prefix: `{network.prefixlen}`")
            message_lines.append(f"- Netmask: `{network.netmask.exploded}`")
            message_lines.append(f"- PTR record name: `{network.reverse_pointer}`")
            if network.is_multicast:
                message_lines.append(
                    "Address is reserved for multicast use per "
                    "[RFC 3171](https://datatracker.ietf.org/doc/html/rfc3171.html)."
                )
            if network.is_private:
                message_lines.append(
                    "Address is private (not globally reachable) per the "
                    "[IANA IPv4 Special-Purpose Address Registry]"
                    "(https://www.iana.org/assignments/iana-ipv4-special-registry/"
                    "iana-ipv4-special-registry.xhtml)."
                )
            elif network.is_global:
                message_lines.append(
                    "Address is globally reachable per the "
                    "[IANA IPv4 Special-Purpose Address Registry]"
                    "(https://www.iana.org/assignments/iana-ipv4-special-registry/"
                    "iana-ipv4-special-registry.xhtml)."
                )
            else:
                message_lines.append(
                    "Address is designated for Carrier-Grade NAT (CGN) per "
                    "[RFC 6598](https://datatracker.ietf.org/doc/html/rfc6598)."
                )
            if network.is_loopback:
                message_lines.append(
                    "Address is a loopback address per "
                    "[RFC 3330](https://datatracker.ietf.org/doc/html/rfc3330.html)."
                )
            if network.is_link_local:
                message_lines.append(
                    "Address is reserved for link-local usage per "
                    "[RFC 3927](https://datatracker.ietf.org/doc/html/rfc3927.html)."
                )
            await evt.reply("\n".join(message_lines))
        except ValueError:
            await evt.reply("Invalid address.")
