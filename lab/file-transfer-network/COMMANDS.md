# Commands and explanations

This file collects useful commands for testing and learning file transfer patterns in a lab environment.

## SSH file transfer

### Copy a single file to a remote host

```bash
scp ./example.txt user@remote-host:/tmp/
```

Purpose: transfer one file securely over SSH.

### Copy a directory recursively

```bash
scp -r ./project-dir user@remote-host:/srv/shared/
```

Purpose: send a directory and its contents to a remote host.

### Use rsync for efficient synchronization

```bash
rsync -avz ./project-dir/ user@remote-host:/srv/shared/project-dir/
```

Purpose: copy only changed files while preserving structure and metadata.

### Verify the remote file exists

```bash
ssh user@remote-host "ls -l /srv/shared/project-dir"
```

Purpose: confirm the transferred content is present and in the expected location.

## Hash verification

### Generate a checksum

```bash
sha256sum ./example.txt
```

### Compare checksum on remote host

```bash
ssh user@remote-host "sha256sum /tmp/example.txt"
```

Purpose: confirm the file is identical after transfer.

## Remote shell and local checks

### Check disk space on the destination

```bash
df -h
```

### Check file permissions and ownership

```bash
ls -l /srv/shared/project-dir
```

Purpose: verify the transferred files have the expected access model.

## SFTP example

```bash
sftp user@remote-host
```

Then inside the session:

```bash
put ./example.txt /tmp/example.txt
ls -l /tmp
```

Purpose: interactive transfer for troubleshooting or manual file exchange.

## Useful comparison commands

```bash
rsync -av --dry-run ./project-dir/ user@remote-host:/srv/shared/project-dir/
```

Purpose: preview what would change before a real sync.

## Notes for lab practice

- Prefer SSH-based methods unless another protocol is specifically required.
- Use `rsync` when transferring large or frequently changing directories.
- Validate integrity with hashes or file comparisons after any transfer.
- Keep transfer commands documented so recovery and troubleshooting are repeatable.

## Quick practice workflow

1. Create a sample file locally.
2. Copy it with `scp`.
3. Sync it with `rsync`.
4. Compare hashes.
5. Inspect permissions and destination layout.
6. Record what behaved as expected and what did not.
