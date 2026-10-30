# HomeLab Documentation Status

**Last audited:** October 29, 2026

This file answers two questions: **what is actually documented now, and what still needs documentation or implementation?** It should be updated whenever a milestone is completed.

## Coverage matrix

| Area | Implementation status | Documentation status | Primary record / gap |
|---|---|---|---|
| Node #1 hardware | Complete/verified | **Documented** | `hardware-validation.md` |
| Dell diagnostics | Complete/verified | **Documented** | `hardware-validation.md` |
| Windows pre-conversion baseline | Complete/verified | **Documented** | Activation, failed update, hardware inspection |
| BIOS virtualization | Sufficient for current VMs; exact toggles not captured | **Partial** | Final VT-x/VT-d values and BIOS version still need an explicit record |
| Proxmox installation | Complete | **Partial** | Running state is documented; exact ISO version, USB-writing method, filesystem/install options are not |
| Proxmox node/network | Complete | **Documented at operational level** | `pve01`, management network, repository, updates; public docs intentionally omit private IPs |
| Physical network | Operational | **Documented at topology level** | AT&T gateway → Archer AX55 → Proxmox/Mac; exact private addressing kept out of public docs |
| Ubuntu VM 100 | Complete | **Documented** | `docker01`, Ubuntu 24.04.5 LTS, 2 vCPU/4 GiB/64 GiB, VirtIO/`vmbr0`, DHCP reservation, SSH, QEMU agent |
| Docker/Compose | Complete | **Documented** | Docker install and `hello-world` validation recorded |
| Portainer | Complete | **Documented** | Administrator setup and local environment management verified |
| Guest resource monitoring | Complete | **Detailed** | `monitoring.md`: Node Exporter, Prometheus, Grafana |
| Availability monitoring | Complete | **Detailed** | `monitoring.md`: Uptime Kuma checks for Proxmox, Portainer, Grafana, and Social Ring |
| Email alerting | Complete | **Detailed** | Gmail SMTP test plus real DOWN/UP test recorded |
| Public static hosting | Complete | **Documented** | Nginx on `apps-01` serves `/srv/social-ring` through Cloudflare Tunnel |
| GitHub delivery automation | Complete | **Documented** | Public source repo triggers private workflow; runner updates website files without sudo or Docker access |
| Local recovery snapshots | Complete | **Documented** | `ubuntu-base`, `docker-portainer-ready`, `monitoring-ready`, and the pre-deploy apps snapshot |
| Development workspace | Operational; operator confirmed | **Documented** | VM 102, Remote SSH, Social Ring working copy |
| Off-site project backups | Manual test completed | **Documented** | Weekly S3 archives with dependency-directory exclusions |
| Project file restore | Operator reported complete | **Documented** | Isolated extraction, exclusion check, and source comparison |
| Weekly scheduled execution | Configured; first run pending | **Documented** | Sunday 03:00 America/Chicago |
| Full VM and live application recovery | Not complete | **Deferred** | Separate backup and restore procedures required |
| Physical host metrics | Not complete | **Documented as planned** | Monitoring currently describes `docker01`, not total Dell host resources |
| Independent outage observer | Not complete | **Documented as planned** | Current Kuma instance shares the host failure domain |
| Backend application | Not deployed | **Roadmap only** | Java/Spring Boot API + PostgreSQL; Redis only where justified |
| Kubernetes | Not deployed | **Roadmap only** | Small k3s environment |
| Messaging | Not deployed | **Roadmap only** | Kafka/event-driven experiment later |
| Secrets management | Not deployed | **Roadmap only** | Vault or equivalent later |
| Managed switch/VLANs | Not verified installed | **Planning only** | Do not claim VLAN lab until hardware/config is actually deployed |
| UPS | Not verified installed | **Planning only** | Power-protection design remains future work |
| NAS | Not verified installed | **Planning only** | Required before the planned independent backup/restore milestone |
| Additional Proxmox nodes | Not deployed | **Planning only** | Current lab is single-host |
| Dedicated firewall/VPN | Not deployed | **Planning only** | OPNsense/pfSense/VPN concepts discussed, no deployment claimed |
| Personal media/file services | Not deployed | **Idea/roadmap only** | Requirements should be documented before regular use |
| Mac mini AI node | Initial deployment verified | **Documented** | `local-ai-assistant.md`: local model, repository retrieval, iPhone access, and reboot startup |
| AI knowledge refresh | Manual pull only | **Documented** | Local Markdown clone is reread for each question; no automatic sync |
| AI live checks / control | Not implemented | **Explicit limit** | Assistant answers from documents and cannot inspect or operate services |
| AI access and recovery | LAN HTTP only; no app authentication or backup test | **Open work** | Monitoring, secure remote access, recovery, and broader quality tests remain pending |

## Documentation files now present

- `README.md` — project purpose, current state, roadmap, standards, and success criteria.
- `monitoring.md` — detailed metrics, service availability, Gmail alerting, outage test, and Social Ring monitoring notes.
- `local-ai-assistant.md` — verified local model deployment, retrieval, startup, operations, and limits; source in `services/local-ai/`.
- `social-ring.md` — the public app deployment guide, automation flow, operations, and remaining risks.
- `development-backups.md` — the `dev01` remote development workspace, weekly S3 project backups, and restore procedure.
- `hardware-validation.md` — pre-Proxmox hardware inspection, diagnostics, keyboard/firmware lessons, and BIOS-record gaps.
- `architecture.md` — current physical, virtual, public app flow, and monitoring topology with failure-domain boundaries.
- `build-log.md` — dated milestone history separating complete work from missing details.
- `equipment-inventory.md` — deployed/purchased/planned physical equipment and compatibility notes.
- `documentation-status.md` — this audit of documented, partial, planned, and deferred work.

## Highest-priority documentation gaps

These are documentation gaps even though some underlying functionality already works:

1. Record the exact Proxmox VE version currently installed.
2. Record the Dell BIOS version and final virtualization/VT-d values.
3. Record the exact current Proxmox storage layout (`lsblk`, Datacenter/Storage view, filesystem/LVM choices).
4. Export or record the current Proxmox network configuration (`/etc/network/interfaces`) in sanitized form.
5. Record exact Docker image versions/digests instead of moving `latest`/major tags.
6. Convert the manually created Docker services into reviewed Compose manifests or another version-controlled declaration.
7. Record a normal 24-hour/7-day monitoring baseline before drawing capacity conclusions.
8. Record the Mac mini’s exact CPU, model file checksum, and complete dependency/build versions; test assistant answer quality beyond the initial examples.

## Implementation gaps that must not be described as complete

- AI authentication/TLS, automated knowledge sync, live service integration, and assistant backup/restore testing
- Full VM and live application backups and restore testing
- NAS storage
- Managed switch/VLAN deployment
- UPS integration and graceful shutdown
- High-availability/second Proxmox node
- k3s/Kubernetes
- Backend application deployment and database migrations
- Kafka/messaging
- Vault/secrets platform
- Dedicated firewall/VPN appliance
- Public root-domain redirect and canonical HTTPS enforcement (pending verification)
- Clean URLs without `.html` suffixes (pending verification)
- Public HTTPS monitoring for the live site (pending verification)

## Documentation rule

A technology belongs in the **current architecture** only after it has been deployed and verified. Until then, it stays in the roadmap or equipment plan. This prevents the HomeLab portfolio from reading like a shopping list or a list of tools that were never actually operated.
