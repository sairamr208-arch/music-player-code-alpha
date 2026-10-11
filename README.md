# AuraPlay &bull; Professional Web Music Player

A high-fidelity, modular HTML5 web audio player engineered with modern web standards, the HTMLMediaElement API, Web Audio API frequency spectrum visualizer, glassmorphism aesthetics, responsive layouts, and accessibility.

---

## 🎧 Features Overview

- **Core Playback Controls**:
  - **Play / Pause**: Smooth state synchronization and Play Promise error/rejection handling.
  - **Next / Previous Track**: Circular or queue navigation with auto-advance upon track finish (`ended` event).
  - **Seek Bar (Scrubber)**: Interactive scrubbing via click and drag, real-time time display, hover seek preview tooltip, and buffered range visualization (`audio.buffered`).
  - **Volume & Mute**: Fine slider control with audio level memory saved in `localStorage`, accompanied by responsive volume icons.
  - **Playback Speed**: Selector for 0.75x, 1.0x, 1.25x, 1.5x, and 2.0x playback rates.
- **Playlist Management**:
  - Modular `PlaylistManager` decoupled from UI and playback engines.
  - Native **HTML5 Drag-and-Drop** reordering.
  - Dynamic **Search & Filtering** by track title, artist, and album.
  - Custom file import: Drag & drop your own audio files (`.mp3`, `.wav`, `.ogg`, `.m4a`) directly into the player or click "Browse files".
  - Add tracks dynamically via external streaming URLs.
- **Web Audio Real-Time Visualizer**:
  - Canvas-driven spectrum bars with glowing gradient color palette and floating ambient audio particles.
  - Graceful fallback animation when paused, muted, or in CORS-restricted environments.
- **Accessibility & UX**:
  - Full semantic markup with ARIA roles (`role="region"`, `role="slider"`, `role="listitem"`).
  - Screen reader announcements via dynamic `aria-live="polite"` region.
  - Full keyboard shortcuts navigation.

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
| :--- | :--- |
| <kbd>Space</kbd> | Toggle Play / Pause |
| <kbd>&rarr;</kbd> | Seek Forward 5 seconds |
| <kbd>&larr;</kbd> | Seek Backward 5 seconds |
| <kbd>&uarr;</kbd> | Volume Up (+5%) |
| <kbd>&darr;</kbd> | Volume Down (-5%) |
| <kbd>M</kbd> | Mute / Unmute Audio |
| <kbd>N</kbd> | Skip to Next Track |
| <kbd>P</kbd> | Return to Previous Track |
| <kbd>S</kbd> | Toggle Shuffle Mode |
| <kbd>R</kbd> | Cycle Repeat Mode (All &rarr; One &rarr; Off) |
| <kbd>?</kbd> | Open Shortcuts Reference Modal |

---

## 📁 File Structure

```text
/music player
├── index.html                  # Semantic, accessible HTML5 layout
├── playlist.json               # Structured playlist data with metadata & fallback sources
├── README.md                   # Project documentation
├── css/
│   └── style.css               # Glassmorphic responsive design system
├── js/
│   ├── player.js               # AudioPlayer module encapsulating <audio> element
│   ├── playlist.js             # PlaylistManager (queues, shuffle, drag-drop reordering)
│   ├── visualizer.js           # AudioVisualizer with Web Audio API & Canvas
│   └── main.js                 # UI controller, event delegations, keyboard shortcuts
├── assets/
│   ├── audio/                  # Preloaded audio files (WAV 44.1kHz stereo)
│   └── covers/                 # High-resolution album artwork
└── generate_music.py           # Audio synthesis script for offline audio files
```

---

## 🚀 Running Locally

Because ES6 modules (`import` / `export`) and `fetch('playlist.json')` require an HTTP server:

```bash
# Using Python
python -m http.server 8080

# Or using Node.js
npx serve .
```

Open `http://localhost:8080` in any modern web browser.
