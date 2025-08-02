# Scripts Repository

This repository contains a collection of scripts and tools I use for my day to day work and automation tasks. Each script is designed to be self-contained and focused on specific workflows.

## Table of Contents

### Data Export & API Tools

#### [Strava Data Export Tool](./strava/)
A comprehensive tool for authenticating with the Strava API and exporting activity data to CSV format.

**Features:**
- OAuth authentication with automatic token refresh
- Export activities from the past 2 years
- Generate detailed CSV files with activity metrics
- Create summary statistics by sport type
- Robust error handling and rate limiting
- Cross-platform compatibility (macOS, Linux, Windows)

**Files:**
- `strava_auth.sh` - Authentication script for Strava API
- `fetch_strava_activities.py` - Main data export script
- `requirements.txt` - Python dependencies
- `README.md` - Detailed usage instructions

**Usage:**
```bash
cd strava/
chmod +x strava_auth.sh
./strava_auth.sh
python3 fetch_strava_activities.py
```

**Output:**
- `strava_activities_last_2_years.csv` - Detailed activity data
- `strava_summary_by_sport.csv` - Summary statistics by sport

---

## Repository Structure

```
scripts/
├── README.md                    # This file
├── strava/                      # Strava data export tool
│   ├── strava_auth.sh          # Authentication script
│   ├── fetch_strava_activities.py  # Main export script
│   ├── requirements.txt         # Python dependencies
│   └── README.md               # Detailed documentation
└── .git/                       # Git repository
```

## Adding New Scripts

When adding new scripts to this repository:

1. **Create a dedicated directory** for each tool/script
2. **Include a README.md** with usage instructions
3. **Make scripts self-contained** with clear dependencies
4. **Add to this README** in the appropriate section
5. **Follow consistent naming** and documentation patterns

## Script Categories

- **Data Export & API Tools**: Scripts for extracting data from various APIs
- **Automation**: Workflow automation and task scheduling
- **Utilities**: Helper scripts for common tasks
- **Analysis**: Data processing and analysis tools

## Requirements

Most scripts require:
- **Python 3.7+** for Python-based tools
- **Bash** for shell scripts
- **Common Unix tools** (curl, jq, etc.)

Individual script requirements are documented in their respective directories.

## License

This repository contains personal scripts and tools. Each script may have its own licensing considerations, especially when interacting with third-party APIs. But feel free to reuse them sinsibly if needed. Enjoy!
