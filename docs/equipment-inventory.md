# HomeLab Equipment Inventory

**Last updated:** October 29, 2026

This inventory distinguishes equipment that is actively part of the running lab from equipment that has been purchased but is not yet verified/integrated, and from future purchases.

## In service

| Item | Role | Status |
|---|---|---|
| Dell OptiPlex 3070 | Proxmox Node #1 (`pve01`) | Running |
| Intel Core i5-9500 | Host compute | Verified |
| 16 GB DDR4-2666 memory | Host/VM memory | Verified; both slots occupied |
| Crucial MX500 500 GB SATA SSD | Proxmox, VM disks, local snapshots | Running |
| TP-Link Archer AX55 | Current lab LAN and DHCP reservations | Running |
| AT&T gateway | Upstream internet connection | Running |
| Administration Mac | Proxmox/Portainer/Grafana browser administration and SSH client | In use |
| 2014 Mac mini | Local Qwen model and repository-document assistant | Running; Intel x86_64, 8 GB RAM, approximately 1 TB HDD, macOS Monterey 12.7.6; automatic startup verified after reboot |
| iPhone | Termius SSH administration and Safari assistant access | LAN access verified |

## Purchased for the lab / integration status

| Item | Intended role | Current documentation status |
|---|---|---|
| USB flash drive | Proxmox installation/recovery media | Purchased and used for the Proxmox install workflow |
| RackMate T1 8U mini rack | Compact apartment rack | Purchased; final full rack integration is not yet documented |
| Varghesyla/Dell 1U mount accessory | Mount the Dell in the rack | Purchased; compatibility with the 10-inch RackMate remains unresolved/unverified in the documentation |

The rack-mount compatibility question should be resolved using the exact rack width and the exact Dell chassis dimensions before treating the mount as usable.

The Mac mini runs independently of the Dell/Proxmox platform. Its exact Intel CPU model, rack mounting, DHCP reservation, and power-loss restart behavior remain unverified. See [Local AI assistant](local-ai-assistant.md).

## Planned / not verified as acquired

| Item | Intended purpose | Trigger for purchase |
|---|---|---|
| UPS | Power protection and graceful shutdown | Add before relying on the lab for important stored data/services |
| Managed switch | VLANs, port controls, network-learning exercises | Buy when network segmentation is actually being implemented |
| NAS | Independent VM backups, restore tests, shared storage | High priority before claiming backup/recovery capability |
| Additional compute node | Cluster/HA/Kubernetes experiments | Add when workload or learning objective needs another failure domain |
| Dedicated firewall appliance | OPNsense/pfSense, VPN, segmentation | Add only when the network design justifies a separate device |
| Rack dashboard/display | Visual status/dashboard | Optional aesthetic/operational enhancement after core infrastructure |

## Purchase philosophy

The lab is intentionally incremental. New equipment should be purchased to solve an observed constraint or enable a defined experiment, not simply because a larger homelab can contain more hardware.

Examples of valid triggers:

- Memory pressure → consider RAM or another node.
- Local storage pressure → consider larger local storage.
- Need independent backups → acquire NAS/backup target.
- Need graceful power recovery → acquire/configure UPS.
- Need VLAN practice or segmentation → acquire/configure managed switch/firewall as appropriate.
- Need multi-node behavior → add a second/third compute node.
