# File Transfer Network

## Curriculum and purpose

This learning module is focused on practical file transfer and network access patterns for self-hosted services.

The goal is to understand how files move between machines, how transport choices affect reliability and security, and how to validate a setup using real commands and small experiments.

This lab is intentionally server-first: the Ubuntu server is the primary environment for learning SSH/SFTP, process binding, ports, users, and permissions. The laptop can act as the client when available, but localhost exercises remain valid for the initial socket and service-learning phases before a true remote client/server split is introduced.

## Learning goals

- Compare common transfer methods: `scp`, `rsync`, `sftp`, `curl`, and SMB/NFS where relevant.
- Understand when to prefer secure, authenticated transfer over simple file copies.
- Learn how local network topology, SSH access, firewall rules, and permissions affect transfer flows.
- Practice verifying transfer success with checksums, logs, and targeted tests.
- Document the difference between local network transfer, remote host access, and public HTTPS uploads.

## Suggested flow

1. Review the transfer methods and their tradeoffs.
2. Deploy a simple test target in the lab environment.
3. Transfer files using SSH-based and sync-based workflows.
4. Validate file integrity and permissions.
5. Capture observations and edge cases in the learning notes.

## Core topics

- SSH as the foundation for secure remote file movement
- Rsync for efficient incremental synchronization
- SFTP for interactive file exchange
- SMB/NFS for LAN file sharing
- Backups and restore workflows
- Monitoring and validating transfers

## Success criteria

By the end of this module, you should be able to explain:

- when to use `scp` vs `rsync` vs `sftp`
- how to secure a file transfer path
- how to confirm that files arrived intact and with the right ownership
- how a file transfer method fits into a broader backup or deployment workflow
