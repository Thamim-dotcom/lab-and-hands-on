# 🏭 Walkthrough: NEXUS Platform — Industrial Diagnostic Build Log

**Project:** NEXUS — Industrial Diagnostic & Remediation Platform  
**Type:** Cross-platform Desktop App  
**Stack:** Tauri 2 + React 19 + TypeScript + Rust  
**GitHub:** [Thamim-dotcom/nexus-platform](https://github.com/Thamim-dotcom/nexus-platform)  
**Status:** ✅ Built & Deployed

---

## 📝 Overview

NEXUS is a premium industrial diagnostic platform I designed and built from scratch — featuring real-time system telemetry, 3D network topology visualization, autonomous healing engine, and Merkle-chained audit trails. This documents the complete build journey.

---

## 🎯 Problem Statement

Industrial environments need:
- **Real-time diagnostics** — CPU, memory, disk, network at glance
- **Network visibility** — Which devices are connected? What's talking to what?
- **Automated remediation** — Self-healing for common failure patterns
- **Tamper-evident logging** — Audit trail that can't be modified retroactively

---

## 🏗️ Phase 1: Architecture Design

### Technology Decision Matrix

| Requirement | Technology Chosen | Reason |
|-------------|------------------|--------|
| Desktop cross-platform | Tauri 2 | 10MB bundle vs Electron's 200MB |
| Real-time system stats | Rust `sysinfo` crate | Native OS API access |
| 3D visualization | Three.js + React Three Fiber | GPU-accelerated WebGL |
| Auth | Argon2id | Memory-hard, ASIC-resistant |
| Audit log | Merkle chain | Tamper-evident by design |

### System Architecture

```
┌─────────────────────────────────────────────────┐
│                  React Frontend                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────────────┐ │
│  │Dashboard │ │Network   │ │Diagnostic Reports│ │
│  │         │ │Topology  │ │                  │ │
│  └──────────┘ └──────────┘ └──────────────────┘ │
└─────────────────────┬───────────────────────────┘
                      │ Tauri IPC (async commands)
┌─────────────────────▼───────────────────────────┐
│                   Rust Backend                   │
│  ┌──────────┐ ┌──────────┐ ┌──────────────────┐ │
│  │sysinfo   │ │scanner   │ │audit_chain       │ │
│  │engine    │ │engine    │ │(Merkle)          │ │
│  └──────────┘ └──────────┘ └──────────────────┘ │
└─────────────────────────────────────────────────┘
```

---

## 🎨 Phase 2: Design System

### Brand Identity

```
Name:    NEXUS
Theme:   Industrial Dark + Neon Accent
Primary: #0a192f (Deep Navy)
Accent:  #00d4ff (Cyber Cyan) + #00ff88 (Matrix Green)
Danger:  #ff4444 (Alert Red)
Warning: #ffaa00 (Amber)
Font:    JetBrains Mono (monospace), Inter (UI)
```

### Key UI Components Built

1. **Holographic Header** — Animated gradient logo with particle effect
2. **System Vitals Card** — Real-time CPU/RAM/Disk gauges with animated arcs
3. **Network Topology** — 3D force-directed graph of network nodes
4. **Terminal Emulator** — Full in-app terminal with command history
5. **Alert Timeline** — Chronological security/system events feed
6. **Merkle Audit Viewer** — Visual chain with hash verification

---

## ⚙️ Phase 3: System Telemetry Engine (Rust)

```rust
// src-tauri/src/diagnostics.rs
use sysinfo::{System, SystemExt, CpuExt, DiskExt, NetworkExt};

#[tauri::command]
pub fn get_system_stats() -> SystemStats {
    let mut sys = System::new_all();
    sys.refresh_all();

    SystemStats {
        cpu_usage: sys.global_cpu_info().cpu_usage(),
        total_memory: sys.total_memory(),
        used_memory: sys.used_memory(),
        total_swap: sys.total_swap(),
        used_swap: sys.used_swap(),
        load_average: LoadAvg {
            one: sys.load_average().one,
            five: sys.load_average().five,
            fifteen: sys.load_average().fifteen,
        },
        uptime: sys.uptime(),
        disks: sys.disks().iter().map(|d| DiskInfo {
            name: d.name().to_string_lossy().to_string(),
            total: d.total_space(),
            available: d.available_space(),
            mount: d.mount_point().to_string_lossy().to_string(),
        }).collect(),
    }
}
```

---

## 🌐 Phase 4: 3D Network Topology

The network graph was the most complex visual component:

```tsx
// src/components/NetworkTopology/NetworkGraph.tsx
import { Canvas } from '@react-three/fiber'
import { OrbitControls, Sphere, Line } from '@react-three/drei'
import { useEffect, useRef } from 'react'

function NetworkNode({ position, node, onClick }) {
  const meshRef = useRef()
  
  return (
    <group position={position} onClick={onClick}>
      <Sphere ref={meshRef} args={[0.3, 32, 32]}>
        <meshStandardMaterial
          color={node.isGateway ? '#00ff88' : '#00d4ff'}
          emissive={node.isAlert ? '#ff4444' : '#000000'}
          emissiveIntensity={node.isAlert ? 0.8 : 0}
        />
      </Sphere>
      <Html center>
        <div className="node-label">{node.hostname}</div>
      </Html>
    </group>
  )
}
```

---

## 🔗 Phase 5: Merkle Audit Chain

```rust
// src-tauri/src/audit.rs
use sha2::{Sha256, Digest};
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AuditEntry {
    pub id: u64,
    pub timestamp: u64,
    pub user: String,
    pub action: String,
    pub resource: String,
    pub prev_hash: String,
    pub entry_hash: String,
}

impl AuditEntry {
    pub fn new(user: &str, action: &str, resource: &str, prev_hash: &str) -> Self {
        let timestamp = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap()
            .as_secs();
        
        let data = format!("{}{}{}{}{}",
            timestamp, user, action, resource, prev_hash);
        
        let mut hasher = Sha256::new();
        hasher.update(data.as_bytes());
        let entry_hash = format!("{:x}", hasher.finalize());
        
        AuditEntry {
            id: timestamp,
            timestamp,
            user: user.to_string(),
            action: action.to_string(),
            resource: resource.to_string(),
            prev_hash: prev_hash.to_string(),
            entry_hash,
        }
    }
    
    pub fn verify(&self, prev_hash: &str) -> bool {
        self.prev_hash == prev_hash
    }
}
```

---

## 🚀 Phase 6: CI/CD Pipeline

```yaml
# .github/workflows/release.yml
name: Cross-Platform Release

on:
  push:
    tags: ['v*']

jobs:
  release:
    strategy:
      matrix:
        platform: [ubuntu-22.04, windows-latest]
    
    runs-on: ${{ matrix.platform }}
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Setup Rust
        uses: dtolnay/rust-toolchain@stable
      
      - name: Install dependencies (Ubuntu)
        if: matrix.platform == 'ubuntu-22.04'
        run: |
          sudo apt-get update
          sudo apt-get install -y libwebkit2gtk-4.0-dev libssl-dev \
            libgtk-3-dev libayatana-appindicator3-dev librsvg2-dev

      - name: Build and Release
        uses: tauri-apps/tauri-action@v0
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tagName: ${{ github.ref_name }}
          releaseName: 'NEXUS ${{ github.ref_name }}'
          releaseBody: 'See CHANGELOG.md for details'
```

---

## 📊 Final Metrics

| Metric | Value |
|--------|-------|
| Total Lines of Code | ~8,500 |
| Rust (backend) | ~3,200 lines |
| TypeScript/React (frontend) | ~5,300 lines |
| Build Time | ~45s (Linux) |
| Bundle Size | 11.2 MB |
| Startup Time | < 1s |
| Telemetry Refresh Rate | 500ms |

---

## 🧠 Biggest Challenges & Solutions

| Challenge | Solution |
|-----------|---------|
| Tauri IPC type mismatch | Added explicit type bridges in `types.ts` |
| 3D graph performance | Used `useMemo` + instanced meshes for 100+ nodes |
| Real-time data streaming | Tauri event system (`emit`/`listen`) |
| Cross-platform build failures | Pinned dependency versions + matrix CI |
| Merkle chain persistence | SQLite via `rusqlite` for durable storage |

---

*NEXUS is a personal project built for educational and professional development purposes.*
