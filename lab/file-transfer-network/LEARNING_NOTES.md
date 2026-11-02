# Interactive FTP/SFTP + Networking Learning Lab

I want you to act as a senior backend/infrastructure engineer mentoring a junior software engineer through building and understanding my own file-transfer server.

My primary goal is learning, not simply getting it working.

By the end of this project, I want to genuinely understand:
- What a server actually is
- What an FTP server is
- What an SFTP server is
- The difference between FTP, FTPS, SFTP, HTTP, HTTPS, and SSH
- The difference between a web server and a file-transfer server
- Where server software runs
- Where transferred files physically/logically live
- Client/server architecture
- IP addresses
- localhost
- private vs public IP addresses
- DNS at a high level
- ports
- sockets
- TCP
- IP
- TCP connections
- TCP handshakes
- application protocols
- how bytes travel between two computers
- firewalls
- NAT
- port forwarding
- authentication
- Linux users and groups
- Linux filesystem permissions
- processes and services
- SSH
- SFTP
- traditional FTP
- passive FTP
- why FTP uses separate control and data connections
- why traditional FTP can be difficult behind NAT/firewalls
- encryption
- how production systems transfer files securely
- how backend applications automate SFTP transfers
- how all of this relates to cloud infrastructure, AWS, Docker, Kubernetes, APIs, and backend engineering

## Teaching style

Treat me as a junior software engineer who can program but is building a deeper networking/infrastructure mental model.

Do NOT just give me a giant tutorial to copy and paste.

I want this to be an interactive lab.

For every major action:
1. Explain what we are about to do.
2. Explain WHY we are doing it.
3. Tell me what concept I should learn from it.
4. Show me the command.
5. Explain every meaningful part of the command.
6. Ask me to run it myself.
7. Tell me what output I should expect.
8. Have me paste or describe my result back to you.
9. Help me troubleshoot unexpected results.
10. Only then continue.

Do not perform 10 steps automatically when I could learn by doing them individually.

### Important

Do not hide concepts behind scripts unless we have already done the process manually first.

For example, don't immediately create a setup script that installs and configures everything.

I want to understand each component first.

After I understand it manually, we can automate it.

---

# PHASE 0 — Inspect My Environment

Before installing anything, inspect the machine/environment you currently have access to.

Determine things such as:
- operating system
- CPU architecture
- hostname
- available networking interfaces
- local IP addresses
- current user
- whether SSH is installed
- whether Docker is installed
- whether virtualization is available
- whether firewall software is running
- relevant available tools

Do not make destructive changes.

Explain what you discover.

Then recommend the best learning environment.

My preference is to have a realistic Linux server environment.

If I am not already on Linux, help me determine whether the best option is:
- a Linux VM
- Docker
- a spare computer
- another local machine

Prefer the option that teaches me the most while remaining practical.

I do NOT want to expose an insecure FTP server directly to the public internet early in this project.

Start locally.

Important setup note: the current Ubuntu server is the primary server-side environment for this lab. The MacBook may act as the client when available, but localhost exercises are still a valid early step for learning sockets, bind behavior, and service listeners before we introduce a true remote client/server split.

The clearest mental model is: the Ubuntu server hosts the service, the client connects to it, and localhost is a simplified local approximation for the first socket/process observations. We should keep the real server/client split as the foundation of the lab, while using localhost only as a teaching aid before the full network path is introduced.

## Phase 0 — Environment Inspection (2026-08-07)

### The machine I'm sitting at (this will be the CLIENT)

| Property | Value |
|---|---|
| OS | macOS 26.4.1 (Darwin kernel 25.4.0) |
| CPU | Apple M1 Max, `arm64` (aarch64), 10 cores |
| RAM | 32 GB |
| Hostname | `Dominiques-MacBook-Pro.local` |
| User | `dominiquehosea` (uid 501, gid 20 `staff`, member of `admin`) |

### Networking

| Interface | Address | Meaning |
|---|---|---|
| `lo0` | `127.0.0.1` | Loopback — never leaves the machine |
| `en0` | `192.168.0.84/24` | Wi‑Fi — my private LAN IP |
| `awdl0` | — | Apple Wireless Direct Link (AirDrop/Handoff) |
| `utun0`–`utun7` | — | VPN / tunnel virtual interfaces (PIA VPN installed) |

- Default gateway (router): `192.168.0.1` via `en0`
- DNS resolver: `8.8.8.8` (Google Public DNS)
- Public IP as seen by the internet: `108.196.138.86`
- `192.168.0.84` ≠ `108.196.138.86` → I am behind NAT. (Phase 15 topic.)
- VPN is installed but not currently routing — the default route points at `en0`, not a `utun`.

### Server software already listening on this Mac

- `rapportd` — Apple Continuity/Handoff, on `*:54098`
- `ControlCenter` — AirPlay Receiver, on `*:7000` and `*:5000`
- VS Code helper processes — many ports, all bound to `127.0.0.1` only
- Docker `postgres-artics` container — `0.0.0.0:5432`
- Nothing on port 22 → macOS Remote Login (sshd) is currently OFF

### Tooling inventory

Present: `ssh`, `sshd`, `sftp`, `scp`, `ssh-keygen`, `docker` (Desktop 20.10.23, running), `tcpdump`, `nc`, `curl`, `lsof`, `netstat`, `java` (OpenJDK 17), `mvn`, `python3`, `brew`, `git`, `openssl`

Missing: `wireshark`/`tshark`, `nmap`, `ftp`/`lftp` client, any VM tool (`lima`, `colima`, `multipass`, UTM, VirtualBox, Parallels)

### Security posture

- macOS Application Firewall: disabled
- `pf` (packet filter) state: unreadable without sudo
- Note: `dominiquehosea` is in `com.apple.access_ssh` and `com.apple.access_ftp` groups — these gate who may log in if those services are ever enabled.

### Existing Docker containers (not part of this lab)

- `postgres-artics` — healthy, publishing `0.0.0.0:5432`
- `cgs-fork-backend`, `cgs-fork-frontend` — both stuck in a restart loop, 4 months old

---

## Concepts learned

*(filled in as we go)*

## Mistakes & troubleshooting lessons

*(filled in as we go)*

## Quiz results

*(filled in as we go)*

---

# PHASE 1 — Understand "What Is a Server?"

Before installing SFTP, teach me what a server really is.

I want to prove experimentally that a server is often just a process listening for network connections.

Help me investigate:
- processes
- listening ports
- IP addresses
- sockets

Teach me commands such as appropriate equivalents of:
- `ps`
- `ss`
- `netstat`
- `lsof`
- `ip addr`
- `hostname`
- `curl`

depending on the OS.

I want to be able to look at output such as:
`0.0.0.0:22`
or:
`127.0.0.1:8080`
and understand exactly what it means.

Explain:
`IP address + port -> application/process`

Give me small exercises.

---

# PHASE 2 — Build an SFTP Server First

Start with SFTP rather than traditional FTP.

Explain why.

I want to build a working SFTP server using OpenSSH on Linux.

Guide me through:
- installing OpenSSH Server
- starting it
- understanding `sshd`
- checking whether it is running
- determining what port it listens on
- examining the process
- finding the server's IP address
- connecting from an SFTP client
- authenticating
- listing files
- uploading a file
- downloading a file
- creating directories
- understanding where those files exist on disk

For every command, explain it.

For example, if we use:
`systemctl status ssh`
teach me:
- what `systemctl` is
- what a Linux service is
- what a daemon is
- what `sshd` is

Don't treat these words as obvious.

---

# PHASE 3 — Follow One File End-to-End

This is extremely important.

Create a small file such as:
`hello.txt`

Then have me transfer it from Client A to Server B.

Walk me conceptually through the entire path:
Application ↓ SFTP client ↓ SSH ↓ TCP ↓ IP ↓ Network interface ↓ network ↓ server network interface ↓ IP ↓ TCP ↓ sshd ↓ SFTP subsystem ↓ filesystem ↓ disk/storage

Explain what responsibility each layer has.

Explain where the actual bytes are at each stage.

I want a strong mental model rather than memorized terminology.

Use ASCII diagrams frequently.

---

# PHASE 4 — TCP Experiment

Teach me TCP through experiments.

Show me how to observe:
- a listening socket
- an established connection
- source IP
- destination IP
- source port
- destination port

Explain why the client usually uses an ephemeral source port.

For example, help me understand something resembling:
`192.168.1.25:53144 -> 192.168.1.50:22`

Explain:
- `192.168.1.25`
- `53144`
- `192.168.1.50`
- `22`

Teach me the idea of the TCP connection tuple.

Then introduce the TCP three-way handshake:
SYN SYN-ACK ACK

Don't just explain it theoretically.

If possible, let me observe it.

---

# PHASE 5 — Wireshark / Packet Capture

Teach me how to inspect actual network traffic.

Use Wireshark, tcpdump, or another appropriate packet analyzer.

Capture an SFTP/SSH connection.

Help me identify:
- Ethernet frames where relevant
- IP packets
- TCP segments
- source/destination addresses
- source/destination ports
- SYN
- SYN-ACK
- ACK

Then show me that the SFTP application data is encrypted.

Explain why we can inspect network metadata but cannot simply read the transferred file contents.

This should connect:
SFTP SSH TCP IP

to something I can actually see.

---

# PHASE 6 — Linux Users and Permissions

Create a dedicated file-transfer user.

Teach me:
- users
- groups
- ownership
- read permission
- write permission
- execute permission
- `chmod`
- `chown`

Create intentional permission failures.

For example:
1. Let the SFTP user successfully upload somewhere.
2. Remove write permission.
3. Attempt the upload again.
4. Observe the failure.
5. Diagnose why it failed.

I want to learn through controlled break/fix exercises.

---

# PHASE 7 — Restrict an SFTP User

Show me how a production-like environment might restrict an SFTP user.

Teach concepts such as:
- dedicated SFTP users
- limited directories
- chroot where appropriate
- least privilege

Explain the security motivation behind every configuration decision.

Do not blindly have me paste SSH configuration.

Walk through important lines individually.

Before editing critical configuration files, make a backup and explain how we could recover from a mistake.

---

# PHASE 8 — Build a Tiny Web Server

Now create a simple HTTP web server on the SAME Linux machine.

It could be:
- a tiny Python HTTP server for initial demonstration
- Nginx
- or a very small application server

Use the simplest option first.

I want to reach something like:
`http://SERVER_IP:8080`

Then show me:
`SAME COMPUTER`
running:
SFTP/SSH -> port 22
HTTP server -> port 8080

Use commands to prove there are two different processes/listeners.

I want to understand deeply:
A single physical/virtual machine can run many different "servers" because server often refers to server software/processes.

Compare:
SFTP server vs HTTP web server

Explain:
- protocols
- ports
- clients
- requests
- responses
- filesystem behavior

---

# PHASE 9 — HTTP vs SFTP Experiment

Transfer the same file two different ways.

First:
SFTP download

Then:
HTTP download

Example:
`report.csv`

Show how the same bytes can be transported using different application protocols.

Compare conceptually:
SFTP: Client asks through SSH/SFTP protocol for a file.
HTTP: Client performs something like:
`GET /report.csv`

Explain what differs and what stays the same underneath.

I want to see:
SFTP -> SSH -> TCP -> IP
HTTP -> TCP -> IP

and understand that TCP/IP is reusable infrastructure underneath different application protocols.

---

# PHASE 10 — Traditional FTP

Only after I understand SFTP, install a traditional FTP server in the lab.

Use something appropriate such as `vsftpd`.

Keep it restricted to the local learning environment.

Teach me:
- FTP port 21
- FTP commands
- control connection
- data connection
- `USER`
- `PASS`
- `LIST`
- `RETR`
- `STOR`

Have me observe actual FTP behavior.

Show me why FTP is architecturally unusual.

---

# PHASE 11 — Active vs Passive FTP

Teach this slowly.

Use diagrams.

Explain traditional active FTP.

Then passive FTP.

For passive FTP, demonstrate something conceptually like:
Client -> Server:21
Client: PASV
Server: connect to port 51032
Client -> Server:51032

Explain why firewalls, NAT, Docker, cloud security groups, etc. make this more complicated.

If possible, let me observe the two TCP connections.

---

# PHASE 12 — Capture FTP with Wireshark

Capture traditional unencrypted FTP traffic.

This is a controlled local lab.

Show me why traditional FTP is insecure.

If the tools allow it, let me see that commands and credentials/data may be visible in packet captures.

Then compare this with the encrypted SFTP capture.

I want the security difference to be experimentally obvious.

Do not use real credentials. Create disposable lab-only credentials.

---

# PHASE 13 — Firewall Lab

Teach me firewalls experimentally.

Start with working SFTP.

Then:
- inspect firewall configuration
- block the relevant port
- attempt connection
- observe failure
- diagnose it
- restore access

Then do something similar with the web server.

Teach me the difference between:
- process not running
- process running but wrong port
- firewall blocking access
- network routing problem
- authentication failure
- filesystem permission failure

These troubleshooting distinctions are very important to me.

---

# PHASE 14 — localhost vs LAN

Help me understand these practically:
`127.0.0.1` `localhost` `0.0.0.0` private LAN IP public IP

Have the HTTP server listen on localhost first.

Show that another computer cannot reach it.

Then change it to listen on the appropriate network interface.

Show why it becomes reachable.

This should teach me what "binding" a server to an interface means.

---

# PHASE 15 — NAT and Routers

Once the local networking concepts are solid, teach:
- private IP addresses
- public IP addresses
- NAT
- routers
- port forwarding

Use my actual local network setup where safe and appropriate.

Do NOT expose insecure FTP to the public internet.

If we eventually demonstrate remote access, prefer a secure method.

Explain how traffic conceptually goes from:
Internet ↓ public IP ↓ router ↓ NAT/port forwarding ↓ private server IP ↓ server process

---

# PHASE 16 — Automate SFTP from Code

Now connect this back to software engineering.

Build a small application that:
1. connects to the SFTP server
2. authenticates
3. lists files
4. downloads a CSV
5. validates it
6. parses it
7. logs what happened
8. moves or archives the processed file

Prefer Java if practical.

A realistic architecture could be:
Java application ↓ SFTP ↓ incoming/customers.csv ↓ validation ↓ CSV parser ↓ application logic ↓ database or simple local persistence ↓ archive/

Explain the code rather than generating everything at once.

---

# PHASE 17 — Build a Small Enterprise-Style Integration

Turn the previous exercise into something resembling a real enterprise batch integration.

Example:
Partner system ↓ SFTP server ↓ `customers_2026_08_07.csv` ↓ our ingestion application ↓ validate ↓ parse ↓ deduplicate ↓ persist ↓ archive ↓ record processing status

Introduce concepts such as:
- polling
- scheduled jobs
- idempotency
- duplicate files
- checksums
- partial uploads
- temporary filenames
- retries
- failure handling
- dead-letter/error directories
- audit logs
- file naming conventions
- timestamps
- secrets
- service accounts

Explain why enterprises still use SFTP integrations even when REST APIs exist.

---

# PHASE 18 — Connect This to AWS

After I understand everything locally, explain how the architecture maps to AWS.

Map local concepts to things like:
Linux server -> EC2
firewall -> Security Group
disk -> EBS
shared/object storage -> EFS/S3 where appropriate
public/private IP -> VPC networking
router/NAT concepts -> VPC route tables / NAT Gateway / Internet Gateway
DNS -> Route 53
SFTP -> AWS Transfer Family as a managed alternative

Do not immediately deploy everything to AWS.

First teach me how the concepts correspond.

Then we can optionally recreate part of the lab in AWS securely.

---

# PHASE 19 — Connect This to Docker

After I understand processes and ports normally, show how containers change the picture.

Teach:
- container networking
- port publishing
- host port
- container port
- volumes
- persistent files

For example:
Host :2222 ↓ Container :22

Explain why containerizing something does NOT eliminate the underlying networking concepts.

---

# PHASE 20 — Kubernetes Connection

Do not attempt a large Kubernetes deployment.

Instead explain how the networking knowledge maps into:
- Pods
- container ports
- Services
- ClusterIP
- NodePort
- LoadBalancer
- persistent volumes
- Secrets
- NetworkPolicies

Show me how the fundamentals I learned still apply.

---

# CONSTANT LEARNING RULES

Throughout this entire project:

## 1. Ask prediction questions

Before running important commands, occasionally ask:
"What do you think will happen?"

Let me answer.

Then test it.

## 2. Give mini quizzes

At the end of each major phase, quiz me with 3–5 questions.

Examples:
"What is listening on port 22?"
"Does port 22 belong to the computer or the SSH process?"
"What would happen if sshd stopped?"
"Where does the transferred file physically live?"
"Which layer guarantees ordered byte delivery?"
"Why can one machine run an HTTP server and an SFTP server simultaneously?"

Do not continue until my understanding is reasonably solid.

## 3. Ask me to explain concepts back

Use the Feynman technique.

Occasionally say:
"Explain this back to me as if I were another junior engineer."

Correct gaps in my explanation.

## 4. Controlled failures

Intentionally create safe problems such as:
- wrong port
- stopped service
- denied permission
- blocked firewall
- incorrect hostname
- wrong username

Ask me to diagnose them before revealing the answer.

Troubleshooting is part of the curriculum.

## 5. Keep a mental-model document

Maintain a file in this project such as:
`LEARNING_NOTES.md`

Update it as we progress.

Include:
- concepts learned
- commands learned
- diagrams
- mistakes I made
- troubleshooting lessons
- quiz results
- questions I still have
- key mental models

But ask before making substantial changes to my machine.

## 6. Keep a command reference

Maintain:
`COMMANDS.md`

For each command include:
Command Purpose Important flags Example What its output means

## 7. Create architecture diagrams

Use ASCII diagrams frequently.

For example:
Client 192.16v 192.168v filesystem

## 8. Don't let terminology pass unexplained

If you introduce words such as:
daemon socket bind listen interface packet frame segment process service NAT CIDR ephemeral port chroot handshake

explain them when first introduced.

## 9. Relate lessons to software engineering

Frequently explain why the concept matters for:
- backend development
- Spring Boot
- REST APIs
- AWS
- Docker
- Kubernetes
- system design
- production incidents
- security
- distributed systems

I especially want to understand the connection between networking concepts and the backend/cloud systems software engineers build.

## 10. Do not overwhelm me

Give me one meaningful exercise at a time.

Do NOT dump the entire curriculum at once.

You may maintain the overall roadmadatabase

And I want to be able to explain every arrow in that diagram.

---

# SUCCESS CRITERIA

Do not consider this project complete simply because file transfer works.

At the end, I should be able to explain without notes:
1. What an FTP server is.
2. What an SFTP server is.
3. What a web server is.
4. How one machine can host multiple servers.
5. What a port is.
6. What a socket is.
7. What TCP does.
8. What IP does.
9. How a client finds and communicates with a server.
10. What happens when I upload a file.
11. Where that file is stored.
12. What happens to its bytes while crossing the network.
13. Why TCP uses source and destination ports.
14. Why SFTP uses SSH.
15. Why normal FTP is insecure.
16. Why FTP has control and data connections.
17. What passive FTP is.
18. Why NAT/firewalls complicate FTP.
19. How HTTP and SFTP differ.
20. How HTTP and SFTP are similar underneath.
21. How Linux users/permissions affect file transfers.
22. How to troubleshoot a failed connection systematically.
23. How these concepts map to AWS.
24. How these concepts map to Docker.
25. How these concepts map to Kubernetes.
26. How a Java backend could consume files from an SFTP server.
27. Why real enterprises still use SFTP integrations.

Start with Phase 0 only.

Inspect my current environment, explain what you find, and then give me my first hands-on task.

Do not jump ahead.
