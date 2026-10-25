# Hosea Homelab

**Building, operating, and documenting a compact platform for backend applications and distributed systems.**

This repository documents my home lab as it grows from a single Proxmox host into an environment for application deployment, observability, automation, networking, and recovery practice.

My goal is to become a stronger backend engineer by owning the full path from source code to a running service: the infrastructure, network, deployment process, data, monitoring, and operational decisions behind it.

**Current milestone:** Ubuntu, Docker, and Portainer are running in the first VM. Prometheus and Grafana display guest resource metrics; Uptime Kuma checks Proxmox, Portainer, and Grafana. Gmail outage and recovery notifications have been tested, and the `monitoring-ready` snapshot is saved.

Documentation set:

- [Hardware validation](docs/hardware-validation.md) — Node #1 baseline, Dell diagnostics, and BIOS-record gaps.
- [Current architecture](docs/architecture.md) — physical, virtual, and monitoring topology.
- [Build log](HomeLab/build-log.md) — dated milestones and incomplete details.
- [Monitoring and alerting](docs/monitoring.md) — metrics, availability checks, Gmail notifications, and outage validation.
- [Equipment inventory](HomeLab/equipment-inventory.md) — in-service, purchased, and planned hardware.
- [Documentation status](HomeLab/documentation-status.md) — what is documented, partial, planned, or deferred.

**Last updated:** October 24, 2026

## Why I am building this

I work with backend services and cloud infrastructure. This lab gives me a place to build the supporting systems myself, test assumptions, break things deliberately, and document how I recover them.

The long-term objective is a portfolio of working systems and engineering case studies. Installing a tool is a starting point; the useful evidence is deploying an application, explaining its behavior, observing failures, and demonstrating recovery.

The lab must also fit in a one-bedroom apartment, remain affordable to operate, and grow incrementally.

## Current hardware

| Component | Current role |
|---|---|
| Dell OptiPlex 3070 | Primary Proxmox host |
| Intel Core i5-9500, 6 cores | Shared compute for virtual machines |
| 16 GB RAM | Shared host and VM memory |
| 500 GB SATA SSD | Host installation, VM disks, and local snapshots |
| TP-Link Archer AX55 | Lab LAN connectivity and DHCP reservations |
| AT&T gateway | Upstream internet connection |
| Mac | Browser administration and SSH client |

A 2014 Mac mini is available for future experimentation; it is not yet part of the deployed platform.

## What is running today

```mermaid
flowchart TD
    P["Dell / Proxmox: pve01"] --> V["VM 100: docker01 / Ubuntu"]
    V --> D["Docker Engine"]
    V --> N["Node Exporter service"]
    D --> T["Portainer"]
    D --> M["Prometheus and Grafana"]
    D --> K["Uptime Kuma"]
    M -->|"Collects guest metrics"| N
    K -->|"Checks web interface"| P
    K -->|"Checks web interface"| T
    K -->|"Checks Grafana health"| M
    K -->|"Outage and recovery email"| G["Gmail SMTP"]
```

| Layer | Verified configuration |
|---|---|
| Hypervisor | Proxmox VE on node `pve01` |
| First VM | `docker01`, VM ID `100` |
| Guest OS | Ubuntu Server 24.04.5 LTS |
| VM resources | 2 vCPU, 4 GiB RAM, 64 GiB virtual disk |
| Guest networking | VirtIO interface bridged through `vmbr0`; DHCP reservation configured |
| Administration | SSH access from the Mac; Proxmox and Portainer web interfaces |
| Guest integration | QEMU guest agent installed and confirmed active |
| Container platform | Docker Engine and Docker Compose plugin installed |
| Management UI | Portainer CE connected to the local Docker environment |
| Resource monitoring | Node Exporter, Prometheus, and Grafana; Node Exporter Full dashboard |
| Availability monitoring | Uptime Kuma with checks for Proxmox, Portainer, and Grafana |
| Notifications | Gmail SMTP; test message and Grafana outage/recovery emails confirmed |

The Docker `hello-world` container completed with exit code `0`. Portainer is running and can list the local containers. No public application has been deployed through this lab yet.

## Completed foundation and monitoring

- [x] Install Proxmox on the Dell.
- [x] Configure the Proxmox management network.
- [x] Configure the no-subscription package repository for lab use and apply host updates.
- [x] Create the first Ubuntu Server VM.
- [x] Install Ubuntu and apply guest updates.
- [x] Verify SSH access over the local network.
- [x] Install and verify the QEMU guest agent.
- [x] Reserve the VM's DHCP address on the router.
- [x] Install Docker Engine and the Compose plugin.
- [x] Run the Docker `hello-world` test successfully.
- [x] Deploy Portainer and complete administrator setup.
- [x] Verify Portainer can manage the local Docker environment.
- [x] Create `ubuntu-base` and `docker-portainer-ready` recovery snapshots.
- [x] Install Node Exporter and verify successful Prometheus scrapes.
- [x] Connect Grafana and import Node Exporter Full, dashboard ID `1860`.
- [x] Deploy Uptime Kuma with SQLite and persistent storage.
- [x] Add HTTP checks for Proxmox, Portainer, and Grafana.
- [x] Verify Grafana outage detection and recovery.
- [x] Configure Gmail and confirm DOWN and UP emails.
- [x] Create the `monitoring-ready` snapshot with RAM excluded.

Snapshots currently live on the host's storage. They provide rollback points, but they are not independent backups and do not protect against host disk failure. Independent VM backups and restore testing are **deferred until a NAS is available**; neither has been completed.

## Service access

Replace `<VM_IP>` with the reserved LAN address of `docker01` and `<PROXMOX_IP>` with the management address of `pve01`. These are templates for local access, not public URLs. Keep actual bookmarks in private notes.

| Service | Local URL template | Purpose |
|---|---|---|
| Uptime Kuma | `http://<VM_IP>:3001/dashboard` | Availability, response times, and outage history |
| Grafana | `http://<VM_IP>:3000/dashboards` | Guest resource dashboards |
| Prometheus | `http://<VM_IP>:9090/targets` | Scrape target health |
| Portainer | `https://<VM_IP>:9443/` | Container administration |
| Proxmox | `https://<PROXMOX_IP>:8006/` | VM administration and snapshots |

The Portainer and Proxmox links use their base URLs so they do not depend on a particular screen or browser fragment.

## Roadmap

The table separates completed work from planned expansion. Resource allocations and placement will be revisited as the lab grows; the current 16 GB host is not intended to run every listed technology at once.

| Phase | Build | Evidence of completion |
|---|---|---|
| 1 — Foundation | Proxmox, Ubuntu, Docker, Portainer | Working VM, SSH access, successful container test, recovery snapshots. **Complete.** |
| 2 — Monitoring | Node Exporter, Prometheus, Grafana, Uptime Kuma, Gmail | **Guest metrics, three availability checks, and email alerts complete.** Physical host metrics and independent outage monitoring remain planned. |
| 3 — Backend service | A Java/Spring Boot API with PostgreSQL; Redis where justified | Repeatable deployment, health checks, persisted data, API tests, and documented design choices. |
| 4 — Delivery automation | Git-based configuration and a CI runner; evaluate GitLab Runner or Jenkins | A commit triggers tests, builds a versioned image, and deploys it with a documented rollback path. |
| 5 — Kubernetes | A small k3s environment | Deploy the API with service discovery, configuration, probes, and persistent storage; compare the tradeoffs with Compose. |
| 6 — Distributed systems | Messaging and asynchronous processing; evaluate Kafka | A documented event flow demonstrating retries, duplicate handling, and failure recovery. |
| 7 — Recovery and access | Independent backups, restore drills, private remote access, secrets management | Backups and restore testing deferred until NAS acquisition. Remaining access work is planned. |
| 8 — Personal services | Selected media, file-transfer, backup, and website workloads | A service with storage, access, monitoring, and recovery requirements documented before regular use. |

Initial guest monitoring and service alerts are running. A longer baseline will help evaluate later workloads. Server resource monitoring and whole-home internet monitoring are separate concerns: bandwidth, latency, and router visibility will need their own measurements.

## Engineering exercises

Each substantial addition should answer a practical question and produce something reviewable.

| Exercise | What I want to demonstrate |
|---|---|
| Trace a request from client to API to database | Understand routing, ports, DNS, application behavior, and data access. |
| Stop an application container | Detect the failure, inspect logs, and verify recovery behavior. |
| Reboot a VM | Verify service startup and persistence after restart. |
| Restore a backup into an isolated environment | Prove recovery works without risking the active service. |
| Apply controlled load | Measure latency, throughput, CPU, memory, and the first bottleneck. |
| Roll back a failed release | Restore a known version and explain database compatibility constraints. |
| Move a service from Compose to k3s | Compare operational cost and benefits using the same workload. |

Load and failure experiments will be scoped to lab workloads with clear stop conditions, particularly while the lab shares the household internet connection.

## Repository organization

The documentation now covers the current architecture, the initial hardware-validation/build history, monitoring, equipment status, and explicit documentation gaps. Configuration-as-code and operational runbooks remain future additions.

| Path | Purpose | Status |
|---|---|---|
| `docs/hardware-validation.md` | Node #1 hardware baseline, diagnostics, and BIOS-record gaps | Added |
| `docs/architecture.md` | Current topology, responsibilities, failure domains, and resource allocation | Added |
| `HomeLab/build-log.md` | Dated setup milestones and validation results | Added |
| `docs/monitoring.md` | Monitoring setup, service checks, alert validation, and recovery notes | Existing |
| `HomeLab/equipment-inventory.md` | Deployed, purchased, and planned physical equipment | Added |
| `HomeLab/documentation-status.md` | Audit of documented, partial, planned, and deferred work | Added |
| `docs/decisions/` | Short records of meaningful technical decisions | Planned |
| `docs/runbooks/` | Deployment, update, troubleshooting, and recovery procedures | Planned |
| `docs/incidents/` | Failure observations, causes, fixes, and follow-up work | Planned |
| `infra/` | Infrastructure configuration and automation added over time | Planned |
| `services/` | Reviewed Compose manifests and service configuration examples | Planned |
| `monitoring/` | Dashboard definitions, scrape configuration, and alert rules | Planned |
| `apps/` | Backend application code or links to separate application repositories | Planned |

## Documentation standards

For each project, I will record:

1. The problem and intended behavior.
2. The architecture and relevant constraints.
3. The configuration needed to reproduce the deployment.
4. Validation results, including failures and their resolution.
5. Monitoring, backup, and rollback considerations.
6. What I learned and what I would change next.

Public documentation will use sanitized examples. Passwords, setup tokens, private keys, recovery codes, and real `.env` files do not belong in the repository. Screenshots will be reviewed for unrelated personal information before publishing.

## Future physical expansion

Potential additions include a compact rack, UPS, managed switch, NAS, and a second compute node. Purchases will follow demonstrated requirements such as memory pressure, storage capacity, backup needs, power protection, or network isolation.

The objective is a useful, understood system rather than a fixed hardware shopping list.

## Success criteria

The lab is serving its larger goal when I can:

- Explain how a request reaches a service and where it can fail.
- Deploy a backend application from version-controlled configuration.
- Use metrics and logs to investigate behavior instead of guessing.
- Recover a service and its data from a tested backup.
- Measure performance and describe the limits of the measurements.
- Explain the tradeoffs behind the infrastructure I chose.
- Publish clear case studies supported by actual configuration and results.

Selected write-ups can later be published on [hoseacodes.com](https://hoseacodes.com), with this repository holding the supporting technical work.

## Reference documentation

- [Proxmox VE documentation](https://pve.proxmox.com/pve-docs/)
- [Ubuntu Server documentation](https://documentation.ubuntu.com/server/)
- [Docker Engine installation on Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
- [Portainer CE installation on Docker](https://docs.portainer.io/start/install-ce/server/docker/linux)
- [Uptime Kuma](https://github.com/louislam/uptime-kuma)
- [Prometheus documentation](https://prometheus.io/docs/)
- [Grafana documentation](https://grafana.com/docs/grafana/latest/)

---

Maintained by Dominique Hosea. This is an evolving learning environment; completed milestones reflect verified work, and the roadmap will change as experiments reveal new requirements.
