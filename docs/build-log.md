# HomeLab Build Log

**Last updated:** October 24, 2026

This log separates verified milestones from plans. A check mark means the work was observed or later confirmed in the project documentation; an open item means the detail is still missing or the work remains planned.

## October 18, 2026 — Node #1 hardware validation

- [x] Purchased/received Dell OptiPlex 3070 for HomeLab Node #1.
- [x] Completed Windows setup far enough to inspect the machine.
- [x] Verified Intel Core i5-9500 @ 3.00 GHz.
- [x] Verified 16 GB DDR4 memory at 2666 MT/s.
- [x] Verified both memory slots are occupied.
- [x] Verified Crucial MX500 500 GB SATA SSD (`CT500MX500SSD1`), about 466 GB usable.
- [x] Verified Windows 11 Pro was activated before conversion.
- [x] Recorded an initial Windows update failure during setup; selected **Update later** rather than spending time repairing an OS scheduled to be replaced.
- [x] Opened Dell BIOS/UEFI through Windows Advanced Startup when F12 timing was unreliable.
- [x] Reached Dell SupportAssist pre-boot diagnostics using a keyboard workaround.
- [x] Dell extended diagnostics completed without a reported hardware error code.
- [ ] Exact final BIOS VT-x/VT-d toggle values were not captured.
- [ ] BIOS version was not captured.
- [ ] Exact chassis/form-factor designation was not independently recorded.

## October 18–20, 2026 — Physical-lab planning and purchases

- [x] Chose a compact apartment-friendly rack direction rather than a full-depth enterprise rack for this build.
- [x] Purchased a USB flash drive for installation/recovery work.
- [x] Purchased a RackMate T1 8U mini rack.
- [x] Purchased a 1U Dell rack mount/shelf accessory.
- [ ] Final mechanical fit of the Dell mount in the 10-inch RackMate has not been documented as verified; the purchased mount may target a different rack width.
- [ ] UPS not documented as purchased/installed.
- [ ] Managed switch not documented as purchased/installed.
- [ ] NAS not documented as purchased/installed.

## October 21, 2026 — Proxmox host

- [x] Proxmox installed on the Dell from USB.
- [x] Proxmox management network configured.
- [x] Node established as `pve01`.
- [x] No-subscription repository configured for lab use.
- [x] Host updates applied.
- [ ] Exact Proxmox VE installer ISO/version used was not recorded in the current documentation.
- [ ] USB-writing tool and exact write options were not recorded.
- [ ] Exact install-time filesystem/storage choices were not recorded in the build log.
- [ ] Exact BIOS virtualization screenshots/settings were not recorded.

## Foundation — Ubuntu, Docker, and Portainer

- [x] Created VM `100`, hostname `docker01`.
- [x] Installed Ubuntu Server 24.04.5 LTS.
- [x] Allocated 2 vCPU, 4 GiB RAM, and 64 GiB virtual disk.
- [x] Connected the VM by VirtIO through Proxmox bridge `vmbr0`.
- [x] Reserved the guest address on the router.
- [x] Verified SSH access from the Mac.
- [x] Installed and verified the QEMU guest agent.
- [x] Created `ubuntu-base` snapshot.
- [x] Installed Docker Engine and Docker Compose plugin.
- [x] Ran Docker `hello-world` successfully with exit code `0`.
- [x] Deployed Portainer CE and completed administrator setup.
- [x] Verified Portainer can manage the local Docker environment.
- [x] Created `docker-portainer-ready` snapshot.

## October 23–24, 2026 — Monitoring and alerting

- [x] Installed Node Exporter on `docker01`.
- [x] Deployed Prometheus and verified self/guest targets `UP`.
- [x] Deployed Grafana and connected Prometheus.
- [x] Imported Node Exporter Full dashboard ID `1860` and verified populated metrics.
- [x] Deployed Uptime Kuma with persistent SQLite storage.
- [x] Added HTTP checks for Proxmox, Portainer, and Grafana.
- [x] Performed controlled Grafana outage/recovery validation.
- [x] Configured Gmail SMTP and received a test message.
- [x] Verified real Grafana DOWN and UP email alerts.
- [x] Created `monitoring-ready` snapshot with RAM excluded.

See `monitoring.md` for the detailed monitoring configuration and validation notes.

## October 25, 2026 — Public static-site deployment and delivery automation

- [x] Created VM `101`, hostname `apps-01`, on Ubuntu Server 24.04.5 LTS.
- [x] Allocated 2 vCPU, 2 GiB RAM, and 32 GiB virtual disk for the apps VM.
- [x] Installed Docker Engine and Docker Compose on `apps-01` and confirmed the VM is reachable with a DHCP reservation.
- [x] Connected `apps-01` to the existing Portainer installation via Portainer Agent.
- [x] Configured a static website runtime using Nginx and published website files to `/srv/social-ring`.
- [x] Confirmed the local site endpoint at `http://<APPS_VM_IP>:8080` responded as expected.
- [x] Deployed a self-hosted GitHub Actions runner as `github-runner` with file-write access only to the website directory and no sudo or Docker access.
- [x] Verified the private workflow triggered from the public source repository and published updated website files.
- [x] Confirmed the site responds over Cloudflare Tunnel using HTTPS at `https://lab.social-ring.com` and `https://www.social-ring.com`.
- [x] Confirmed no router port forwarding was required for public access.
- [x] Ran a local Uptime Kuma check and controlled outage/recovery validation for the Social Ring site.
- [x] Saved a pre-deploy snapshot before the GitHub-driven deployment changes were applied.
- [ ] Root-domain redirect and `Always Use HTTPS` behavior were instructed but not explicitly confirmed in a live test.
- [ ] Clean URLs without `.html` extensions were instructed but not explicitly confirmed in a live test.
- [ ] Rollback execution and recovery testing for the Nginx or workflow configuration were not explicitly confirmed.
- [ ] Public HTTPS Uptime Kuma monitoring was suggested but not confirmed.
- [ ] Independent VM backups and isolated restore drills remain deferred.

See `social-ring.md` for the detailed deployment and operations guide.

## October 25, 2026 — Remote development and S3 backups

- [x] Installed Ubuntu Server on VM `102 (dev01)`.
- [x] Connected VS Code on the Mac through Remote SSH.
- [x] Cloned `PattonGroup/Social-Ring-Web` into `~/projects`.
- [x] Reported successful static-site preview.
- [x] Created private S3 backup storage in `us-east-1`.
- [x] Configured restricted backup IAM permissions.
- [x] Configured 35-day archive retention and 7-day incomplete multipart cleanup.
- [x] Uploaded the initial project archive; confirmed by S3 listing.
- [x] Reported completing an isolated file restore and exclusion check.
- [x] Reported completing a manual logged backup test.
- [x] Reported installing the Sunday 03:00 America/Chicago cron entry.
- [x] Confirmed the cron service is active.
- [ ] Verify the first unattended scheduled backup.
- [ ] Verify final VM RAM, root filesystem size, and DHCP reservation.
- [ ] Add backup failure notifications.
- [ ] Implement full VM and live application data backups.

See [Remote Development and S3 Backups](development-backups.md).

## Current deferred work

- [ ] Deploy first backend application and database workload.
- [ ] Record and pin exact container image versions/digests.
- [ ] Establish a longer monitoring baseline before capacity conclusions.
- [ ] Add physical Proxmox host metrics.
- [ ] Add an app/push notification channel if needed.
- [ ] Add an external/independent observer if whole-host outage alerting is required.
- [ ] Acquire/configure independent backup storage.
- [ ] Run a VM backup and isolated restore drill.
- [ ] Build broader CI/CD automation for backend workloads and release validation.
- [ ] Build k3s Kubernetes environment.
- [ ] Evaluate messaging, secrets management, and additional platform services only as projects require them.
