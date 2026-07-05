---
title: "Work"
description: "Selected engineering work by Shinjae Kang — Laravel SaaS projects, Windows utilities, DevOps workflows, and the zemna.net publishing stack."
draft: false
layout: "page"
---

## Selected engineering work

This is not a full portfolio. It is a map of the kind of engineering work behind the writing on this site: Laravel SaaS projects, desktop utilities, automation, infrastructure, and tools that solve concrete operational problems.

## Laravel SaaS projects

Modoo appears here as a set of software projects I built, not as an employer label. Each project is listed by repository/project name, system purpose, and link.

| Project | System | Stack signal | Link |
|---|---|---|---|
| **Modoo Smart** | Smart business solution for managing operational workflows across a business platform. | PHP / Laravel-style backend system | [modoo-smart](https://github.com/modoo-id/modoo-smart) |
| **Modoo Permit** | Company permit management SaaS for tracking permit-related business processes. | Vue-based SaaS UI | [modoo-permit](https://github.com/modoo-id/modoo-permit) |
| **Modoo Order** | Order workflow system for handling order-side business operations. | Vue-based product system | [modoo-order](https://github.com/modoo-id/modoo-order) |
| **Modoo PickPack** | Fulfillment solution for pick-and-pack operational workflows. | Laravel / PHP fulfillment system | [modoo-pickpack](https://github.com/modoo-id/modoo-pickpack) |
| **Modoo Ingredient** | Ingredient management SaaS for cataloging and managing ingredient data. | Vue-based SaaS UI | [modoo-ingredient](https://github.com/modoo-id/modoo-ingredient) |
| **Modoo Apps** | Application platform layer for the Modoo product ecosystem. | JavaScript application platform | [modoo-apps](https://github.com/modoo-id/modoo-apps) |
| **Modoo Catalog** | Catalog management SaaS for managing product/catalog data. | Vue-based SaaS UI | [modoo-catalog](https://github.com/modoo-id/modoo-catalog) |
| **Modoo Website** | Website for the Modoo project surface. | Blade / Laravel presentation layer | [modoo-website](https://github.com/modoo-id/modoo-website) |

**Engineering signal:** these are product systems, not portfolio mockups. They represent the Laravel/Vue/PHP/Blade side of my work: SaaS-style business tools, operational workflows, catalog/order/permit/fulfillment domains, documentation, and deployment/maintenance discipline.

## Documentation and automation projects

| Project | System | Link |
|---|---|---|
| **Modoo Docs** | Product and developer documentation surface. | [docs](https://github.com/modoo-id/docs) |
| **Modoo Mintlify Docs** | MDX/Mintlify documentation project. | [mintlify-docs](https://github.com/modoo-id/mintlify-docs) |
| **Autoworker YouTube** | Python automation work. | [autoworker-youtube](https://github.com/modoo-id/autoworker-youtube) |
| **GitHub organization profile** | Organization-level GitHub metadata and automation surface. | [.github](https://github.com/modoo-id/.github) |

**Engineering signal:** product software is not only application code. It also includes docs, automation, dependency maintenance, security updates, and repository hygiene.

## Current platform

### [zemna.net](https://github.com/zemna/zemna.net)

A Hugo-based technical blog with a custom theme, token-first design system, Cloudflare Pages deployment, and an automated content pipeline.

**Why it matters:** this site is not just a publication surface. It is a working lab for design systems, AI-assisted writing, fact-check gates, image generation constraints, social distribution, and deployment verification.

**Stack:** Hugo, custom CSS design tokens, Cloudflare Pages, automation, content pipeline tooling.

## Windows and desktop utilities

### [ZemnaNameCopier](https://github.com/zemna/ZemnaNameCopier)

A Windows shell extension for copying one or more file names or paths.

**Engineering signal:** small workflow tools matter. They remove repetitive friction and require integration with real operating-system behavior, not just web UI code.

### [ZemnaFileRenamer](https://github.com/zemna/ZemnaFileRenamer)

A C# utility for renaming single or multiple files with rules.

**Engineering signal:** file-system tooling, batch operations, and safe utility design.

### [ZemnaCmd](https://github.com/zemna/ZemnaCmd)

A Windows command prompt execution shell extension.

**Engineering signal:** developer ergonomics inside Windows workflows.

### [WirelessConfigurationChanger](https://github.com/zemna/WirelessConfigurationChanger)

A C# Windows utility for changing wireless configuration by SSID.

**Engineering signal:** pragmatic system tooling around local network conditions and environment switching.

### [TextEncryptor](https://github.com/zemna/TextEncryptor)

A small text encryption utility.

**Engineering signal:** security-adjacent utility work, data handling, and user-facing desktop tooling.

### [RS232CTest](https://github.com/zemna/RS232CTest)

A C++ RS-232C communication device tester.

**Engineering signal:** hardware-adjacent software, serial communication, and the kind of legacy/industrial interfaces that still exist in real operations.

## What this range says

The through-line is not one framework. It is the habit of building practical systems across layers:

- Laravel/Vue SaaS projects
- product documentation and automation
- web publishing systems
- Windows desktop utilities
- shell extensions and workflow helpers
- network configuration tools
- serial communication testers
- AI-assisted automation with verification gates

That range shapes how I evaluate new tools. I do not ask only whether a tool demos well. I ask whether it can survive maintenance, handoff, local constraints, operating-system edges, and the boring parts after launch.
