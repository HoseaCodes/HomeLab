# HomeLab Hardware Validation — Node #1

**Recorded:** October 18, 2026  
**Status:** Hardware baseline and Dell pre-boot diagnostics are complete. Exact BIOS virtualization toggle values were not captured in the build record.

This document records the validation performed before the Dell was converted from a Windows PC into the first Proxmox host.

## Verified hardware

| Component | Verified value | Evidence/status |
|---|---|---|
| System | Dell OptiPlex 3070 | Windows System > About and Dell firmware screens |
| Processor | Intel Core i5-9500 @ 3.00 GHz | Verified in Windows; six physical cores |
| Memory | 16 GB DDR4, 2666 MT/s | Verified in Task Manager |
| Memory slots | 2 of 2 slots occupied | Verified in Task Manager; individual module capacities were not separately recorded |
| Storage | Crucial MX500 500 GB SATA SSD (`CT500MX500SSD1`) | Verified in Task Manager; about 466 GB usable capacity |
| Graphics | Intel UHD Graphics 630 | Verified in Windows; not material to the Proxmox role |
| Windows license | Windows 11 Pro, activated | Verified before the Proxmox conversion |

The project previously referred to this machine as a Micro system, but the exact Dell chassis/form-factor designation was not independently captured from the service-tag configuration in this build record. Rack-mount fit should therefore be treated as a separate physical compatibility check.

## Validation sequence

1. Completed enough of Windows setup to inspect the machine before erasing the operating system.
2. Windows feature/security update failed during the initial setup flow and returned to the update screen.
3. Chose **Update later** so hardware validation could continue instead of repeatedly troubleshooting a Windows installation that would soon be replaced.
4. Verified processor, memory, storage, and Windows activation.
5. Opened Dell BIOS/UEFI successfully through Windows Advanced Startup after the F12 timing shortcut was unreliable.
6. Reached Dell SupportAssist Pre-Boot System Performance Check after changing the keyboard approach.
7. Ran the Dell diagnostics, including the extended checks. No hardware error code was reported.

The Windows update failure is retained here as troubleshooting history. The later Dell diagnostics did not identify a hardware fault, and the machine subsequently became the working Proxmox node `pve01`.

## Keyboard/firmware access lesson

The original compact multi-function keyboard made the Dell F12 boot-menu shortcut unreliable during POST. A direct/wired USB keyboard was the practical workaround for pre-boot access.

For future maintenance, keep a basic wired USB keyboard available for:

- BIOS/UEFI changes
- One-time boot menu access
- Dell diagnostics
- Proxmox installation or recovery

## BIOS virtualization record

The BIOS showed a **Virtualization Support** section. The intended settings for this host were:

- Intel Virtualization Technology / VT-x — enabled
- VT for Direct I/O / VT-d — enabled
- UEFI boot mode — used for the Proxmox host

The exact final state of each BIOS toggle was **not captured in the chat screenshots or existing documentation**, so this document does not claim a screenshot-verified value. The later successful Proxmox VM deployment confirms that the host provides the virtualization capability needed for the current workload, but it does not substitute for a recorded BIOS configuration baseline.

## Capacity decision

No immediate RAM or SSD upgrade was required before starting the lab.

The initial decision was to learn on the existing 16 GB / 500 GB configuration and only spend money after a demonstrated resource constraint. The current host should not be treated as capable of running every planned platform component simultaneously.

A future memory upgrade would require replacing existing modules because both SODIMM slots are occupied.

## Items not recorded yet

- [ ] Exact Dell chassis/form-factor designation from service-tag configuration
- [ ] BIOS version
- [ ] Screenshot or exported record of final VT-x and VT-d settings
- [ ] SMART/SSD health baseline
- [ ] Exact RAM module manufacturer/part numbers and per-module capacity
- [ ] Idle/load power measurements
- [ ] Idle/load temperature and acoustic baseline
