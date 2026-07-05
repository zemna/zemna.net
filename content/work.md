---
title: "Work"
description: "Selected engineering work by Shinjae Kang — web systems, Windows utilities, DevOps workflows, and the zemna.net publishing stack."
draft: false
layout: "page"
---

## Selected engineering work

This is not a full portfolio. It is a map of the kind of engineering work behind the writing on this site: web systems, desktop utilities, automation, infrastructure, and tools that solve small but concrete problems.

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

- web products and publishing systems
- Windows desktop utilities
- shell extensions and workflow helpers
- network configuration tools
- serial communication testers
- AI-assisted automation with verification gates

That range shapes how I evaluate new tools. I do not ask only whether a tool demos well. I ask whether it can survive maintenance, handoff, local constraints, operating-system edges, and the boring parts after launch.
