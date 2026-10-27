# HRL
Ham Radio Live Web Tools
==================================================

For People With True Passion For The Airwaves — A high-performance, responsive web application and telemetry dashboard built for amateur radio operators and Short Wave Listeners (SWL).
📡 Core FeaturesAuto-Detecting ITU Region Bandplan Engine: Automatically detects the user's local timezone and configures the correct amateur frequency allocations for ITU Region 1, 2, or 3 (80m down to 6m).

Per-Band Propagation Matrix: Real-time conditions (Good, Fair, Poor, Closed) for daytime and nighttime operations across amateur HF/VHF bands.
Short Wave Listening (SWL) Broadcast Bands Matrix: Dedicated matrix covering international shortwave broadcast bands (120m to 11m), tropical bands, time signals (WWV/CHU), and utility listening targets.
Space Weather Telemetry Dashboard: Live metrics tracking Solar Flux Index (SFI), Planetary K-Index, NOAA Boulder Magnetometer K-Index, Sunspot Numbers (SSN), A-Index, Solar Wind Speed, X-ray flare activity, and Interplanetary Magnetic Field ($B_z$).
Maximum Usable Frequency (MUF) & Tropospheric Ducting: Regional path MUF indicators (North America, Europe, Asia/Pacific, South America) and VHF/UHF tropo stability indexes.
Global MUF Propagation Map: Live-rendered SVG propagation maps via KC2G with lazy-loading performance optimizations.
Automated Server-Side Caching: Powered by an hourly GitHub Actions background pipeline that fetches fresh HamQsl XML and NOAA Boulder JSON telemetry feeds directly, bypassing client-side CORS limits and ensuring instantaneous page loads.
🛠️ Tech Stack & ArchitectureFrontend: Pure HTML5, Tailwind CSS (via CDN), and FontAwesome 6 icons.
Styling & Theme: Custom dark-mode "operator" color palette designed for night-shift logging and low eye strain.
Automation: GitHub Actions workflow (.github/workflows/poll-telemetry.yml) running hourly cron jobs to cache telemetry files (solar-cache.xml and boulder-cache.json).Performance: Client-side 1-hour localStorage caching engine with DNS prefetching, preconnecting, and lazy image loading.
