# `blender-webstatus`

A Blender addon for _monitoring_ rendering status _remotely_. Designed for hobbyists
and independents without rendering farms, money, or need for complicated and professional
setups.

## Overview

`blender-webstatus` runs a minimal HTTP server within Blender that exposes render progress information with a simple web interface. Check your render status from your phone, receive notifications on completion, and optionally trigger system actions when rendering finishes.

**Target Users:** Individual artists, hobbyists, anyone rendering longer workloads on _local workstations_ who need remote monitoring without the complexity of commercial render farm solutions.

**License:** GPL-3.0-or-later

## Features

### Supported Systems

| System                         | Support Level               |
| ------------------------------ | --------------------------- |
| 🐧 Linux (Tested on Debian 13) | ✅ Primary                  |
| 🍎 MacOS                       | ❓ Unsupported but may work |
| 🪟 Windows                     | ❓ Unsupported but may work |

### Planned Core Features

- [ ] Simple JSON API for third-party integrations
- [ ] Real-time web-based status dashboard
  - [ ] Scene metadata (name, render engine, output path)
  - [ ] Current frame progress (n out of N frames)
  - [ ] Sample progress (m out of M samples for this frame)
  - [ ] Render start time and estimated completion
  - [ ] Visual progress bars
- [ ] Webinterface for mobile and desktop
- [ ] Configurable network settings (IP binding, port selection)
- [ ] Post-render actions
  - [ ] System shutdown on completion
  - [ ] Audio notifications
  - [ ] Custom Commands

### Technical Specifications

- **Blender Version:** 5.0+ (tested on 5.0.0 release candidate)
- **Python Version:** 3.11 (bundled with Blender 5.0)
- **Dependencies:** Python standard library only (no external packages required)
- **Architecture:** Multi-threaded HTTP server running alongside Blender's main process

## Installation

_Coming soon - installation instructions will be added once the addon is functional_

Expected installation method:

1. Download the addon as a `.zip` file with the big green button
2. Drag the zip file into your blender window and install
3. Configure addon preferences

## Development Status

**Current Phase:** Initial development

This project is in early development.

## TODO

### Phase 1: Foundation (Current)

- [ ] Create basic addon structure with `bl_info`
- [ ] Implement `AddonPreferences` for user configuration
- [ ] Set up render event handlers (`bpy.app.handlers`)
- [ ] Create `RenderState` tracking class

### Phase 2: Web Server

- [ ] Implement HTTP server using `http.server` module
- [ ] Create threaded server lifecycle management
- [ ] Implement `/api/status` JSON endpoint
- [ ] Design and implement static HTML/CSS/JS frontend
- [ ] Test on mobile devices (responsive design)

### Phase 3: Features

- [ ] Extract scene metadata from Blender API
- [ ] Calculate render progress and time estimates
- [ ] Implement progress tracking for Cycles samples
- [ ] Add EEVEE compatibility testing
- [ ] Create Blender UI panel for server control

### Phase 4: Post-Render Actions

- [ ] Implement completion detection
- [ ] Add optional system shutdown capability
- [ ] Add audio notification system
- [ ] Create user-configurable action preferences

### Phase 5: Polish & Release

- [ ] Write comprehensive user documentation
- [ ] Add error handling and edge case management
- [ ] Security review (input validation, rate limiting)
- [ ] Create demo video/screenshots
- [ ] Publish to Blender Extensions platform
- [ ] Set up issue tracker for bug reports

## Technical Architecture

### Components

**Render State Tracker**

- Hooks into `render_init`, `render_pre`, `render_post`, `render_stats`, `render_complete` handlers
- Maintains thread-safe state accessible from HTTP server thread
- Calculates derived metrics (progress percentage, ETA)
- No external dependencies (no frameworks, no build process) except for Post Render Actions

**HTTP Server**

- Runs in separate thread to avoid blocking Blender's UI
- Serves static HTML on root path
- Provides JSON API for status polling
- Configurable binding address and port

**Frontend**

- Single-page application with vanilla JavaScript
- Polls `/api/status` endpoint every 1-2 seconds
- Mobile-first responsive design

## References

- [Blender Python API Documentation](https://docs.blender.org/api/current/)
- [Blender App Handlers Reference](https://docs.blender.org/api/current/bpy.app.handlers.html)
- [Python http.server Documentation](https://docs.python.org/3.11/library/http.server.html)

## Contributing

Contributions are welcome! This project is in early development. Please open an issue to discuss major changes before submitting pull requests.

## AI Assistance Acknowledgment

This project was developed with assistance from Anthropic's Claude LLM (Claude Sonnet 4.5) for:

- Initial architecture design and technical feasibility assessment
- Python/Blender API code examples and best practices
- Documentation structure and technical writing

All code is reviewed, and maintained by human developers. AI-generated suggestions are used as a development aid, not as a replacement for understanding and verification.

## License

GPL-3.0-or-later - See LICENSE file for details.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
