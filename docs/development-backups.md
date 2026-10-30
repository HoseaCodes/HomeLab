# Remote Development and S3 Backups

**Last updated:** October 25, 2026

## Overview

Development now runs on a dedicated Ubuntu VM on the Dell Proxmox host. VS Code on the Mac connects through Remote SSH, so working repositories and development tools live on the VM.

| Component | Location |
|---|---|
| Editor interface | VS Code on the Mac |
| Development VM | VM 102 — `dev01` |
| Working repositories | `/home/dominique/projects` |
| First project | `PattonGroup/Social-Ring-Web` |
| Committed code and history | GitHub |
| Deployment | Existing GitHub Actions runner and application VM |
| Project backups | Private AWS S3 bucket |

Development folders are separate from the runner checkout and the live website files on `apps-01`.

The workflow is:

**Edit and preview on dev01 → commit and push → deployment workflow → live application.**

## VM configuration

| Setting | Configuration |
|---|---|
| Hypervisor | Proxmox on `pve01` |
| VM ID | 102 |
| Hostname | `dev01` |
| Operating system | Ubuntu Server 24.04.5 LTS |
| CPU | 2 virtual cores |
| Memory target | 4 GiB; final allocation needs reconfirmation |
| Virtual disk | 80 GB |
| Network | VirtIO on `vmbr0` |
| Access | OpenSSH and VS Code Remote SSH |

Ubuntu installation, development utilities, OpenSSH, and QEMU guest agent preparation were reported complete.

The final root filesystem size and DHCP reservation still need verification.

## Social Ring development

Repository:

https://github.com/PattonGroup/Social-Ring-Web

Remote working directory:

```text
/home/dominique/projects/Social-Ring-Web
```

To preview the static site, run inside that directory:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Forward port `8000` through VS Code’s Ports view and open its browser link. Press Ctrl+C to stop the preview.

This preview requires no Node dependencies. Previewing the development copy does not publish changes to the live website.

## S3 backup configuration

| Setting | Configuration |
|---|---|
| Region | `us-east-1` |
| Bucket | Private backup bucket; name stored in local configuration |
| Object prefix | `dev01/weekly/` |
| Object Ownership | ACLs disabled |
| Block Public Access | All four settings enabled |
| Default encryption | SSE-S3 |
| Versioning | Disabled |
| Archive naming | Unique UTC timestamp |
| Retention | Expire current objects after 35 days |
| Multipart cleanup | Abort incomplete uploads after 7 days |
| IAM user | `dev01-backup` |
| Inline policy | `Dev01WeeklyBackups` |
| AWS CLI profile | `homelab-backup` |

The backup identity has no console access. Its policy permits listing the weekly prefix and uploading, downloading, and aborting multipart uploads within that prefix.

It has no object-delete permission. S3 lifecycle handles expiration.

SSE-S3 encrypts objects on AWS storage; the archive is not encrypted locally before upload.

## Backup scope and exclusions

The script backs up:

```text
/home/dominique/projects
```

This includes source files, `.git` history, uncommitted work, and other project files unless excluded.

Excluded names at every directory depth:

- `node_modules`
- `.npm`
- `.cache`
- `.venv`
- `__pycache__`

The script checks the archive listing before uploading. If any archived path component is named `node_modules`, the upload is blocked.

This directory exclusion does not remove dependency data already embedded inside Git history or another archive.

Project `.env` files may be included. AWS credentials under `~/.aws` are outside the backup source directory.

These backups do not capture:

- Full VM images or the complete home directory.
- Live application databases.
- Docker volumes.
- Application uploads stored outside the projects directory.
- Deployment credentials stored elsewhere.

Live application data and full VM recovery require separate backup procedures.

## Script and scheduling

Installed script:

```text
/home/dominique/bin/backup-projects-s3.sh
```

The script uses a lock to prevent overlapping runs, creates a temporary archive, validates exclusions, uploads to S3, and removes the temporary archive on exit.

Log:

```text
/home/dominique/backup-logs/weekly.log
```

VM timezone:

```text
America/Chicago
```

User crontab:

```cron
0 3 * * 0 /home/dominique/bin/backup-projects-s3.sh >> /home/dominique/backup-logs/weekly.log 2>&1
```

The backup runs Sundays at 3 AM Houston time.

The VM must be running and have internet access. Cron does not replay a missed run after downtime. Failures are logged but do not currently send notifications.

Weekly backups can lose up to seven days of changes, or longer if jobs fail.

## Verification

Run on `dev01`:

```bash
crontab -l
systemctl is-active cron
timedatectl
tail -n 20 ~/backup-logs/weekly.log
```

Expected:

- One matching weekly cron entry.
- Cron service reports `active`.
- Timezone is `America/Chicago`.
- Successful backup runs produce a `SUCCESS` log entry.

To run a logged backup manually:

```bash
mkdir -p ~/backup-logs
~/bin/backup-projects-s3.sh >> ~/backup-logs/weekly.log 2>&1
tail -n 20 ~/backup-logs/weekly.log
```

## Restore procedure

Replace `YOUR_BUCKET` and `BACKUP_FILENAME` with actual values:

```bash
aws --profile homelab-backup s3 ls \
  s3://YOUR_BUCKET/dev01/weekly/

mkdir -p ~/restore-test

aws --profile homelab-backup s3 cp \
  "s3://YOUR_BUCKET/dev01/weekly/BACKUP_FILENAME" \
  ~/restore-test/backup.tar.gz

tar -tzf ~/restore-test/backup.tar.gz

tar -xzf ~/restore-test/backup.tar.gz \
  -C ~/restore-test

ls ~/restore-test/projects/Social-Ring-Web

find ~/restore-test/projects -name node_modules -print

cmp ~/projects/Social-Ring-Web/index.html \
  ~/restore-test/projects/Social-Ring-Web/index.html
```

Restore only trusted archives into an isolated test directory. Use a fresh test directory for repeated drills.

The `find` command should print nothing. The `cmp` command should exit successfully if the source file has not changed since the backup.

## Validation recorded

- S3 listing confirmed the initial archive:
  `dev01-projects-2026-10-25T20-13-45Z.tar.gz`
- Archive size: 6,258,180 bytes.
- Operator reported completing the restore and exclusion checks.
- Operator reported completing a manual logged backup test.
- Cron service returned `active`.
- Operator reported installing the weekly cron entry.
- First unattended Sunday run remains pending verification.

These results establish a project-file backup workflow, not full VM or live application recovery.

## Follow-up work

- Verify the first scheduled backup and periodically repeat restore drills.
- Add backup failure notifications and log rotation.
- Configure AWS billing alerts if not already done; alerts do not cap spending.
- Verify final VM RAM, root filesystem capacity, and DHCP reservation.
- Complete SSH-key authentication if not already configured.
- Add separate backups for live application data and full VM recovery.

Before removing a Mac repository copy, preserve uncommitted changes, untracked and ignored files, and unpushed branches. A fresh clone does not transfer those automatically.
