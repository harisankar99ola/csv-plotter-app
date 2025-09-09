# CSV Plotter App

An interactive Streamlit application to explore and plot CSV data with multiple plot types, subplots, and dual y‑axes.


## Features

- Upload any CSV file (UTF-8 / standard delimiter).
- Data preview in a scrollable interactive table.
- Multiple plot types: Line, Scatter, Bar, Area, Histogram, Box.
- Select multiple Y columns; optional secondary Y-axis (for line/scatter/area).
- Generate per-column subplots (stacked rows) for quick comparison.
- Automatic numeric column detection for plotting.
- Overlay histograms (with opacity) and multi-series box plots.
- Dual-axis support with independent labeling.
- Desktop shortcut creator for Windows (optional).
- Batch installer / updater (`installer.bat`).

## Installation (Direct)

Install directly from GitHub (replace `<username>` first):

```bash
pip install --upgrade git+https://github.com/harisankar99ola/csv-plotter-app.git
```

Windows users who want desktop shortcut support can include the optional extra to pull in `pywin32`:

```bash
pip install --upgrade "git+https://github.com/harisankar99ola/csv-plotter-app.git#windows"
```

> If using PowerShell, quotes around the URL are optional but sometimes safer.

## Usage

Run from any terminal after install:

```bash
csvplotter
```

The default browser opens a local Streamlit session (typically http://localhost:8501).

### Windows Desktop Shortcut

After installing with the `[windows]` extra (or manually installing `pywin32`), create a shortcut:

```bash
csvplotter-shortcut
```

This creates `CSV Plotter App.lnk` on your Desktop. Double-click to launch the app directly.

### Upgrading

Re-run the install command:

```bash
pip install --upgrade git+https://github.com/harisankar99ola/csv-plotter-app.git
```

Or use the provided batch installer (below) which handles update + launch.

### Plotting Workflow
1. Upload a CSV.
2. Choose plot type.
3. Select X-axis (if required by plot type) and one or more Y columns.
4. (Optional) Choose secondary Y-axis series (line/scatter/area only).
5. (Optional) Enable subplots for multi-series breakdown.
6. Click Generate Plot.

### Notes
- Histograms & Box plots ignore secondary axis and X selection.
- Non-numeric columns appear only where appropriate (X-axis or categorical grouping scenarios).
- Large files: consider sampling externally before loading for better responsiveness.

## Batch Installer / Updater (Windows)

`installer.bat` automates:
1. Virtual environment creation (`.venv`)
2. Pip upgrade
3. Install / update from the Git repo
4. Launch the app

Run it by double-clicking in Explorer or from a terminal:

```powershell
./installer.bat
```

(Edit the `REPO_URL` inside if you fork the project.)

## Development

Clone and install in editable mode:

```bash
git clone https://github.com/harisankar99ola/csv-plotter-app.git
cd csv-plotter-app
pip install -e .[windows]
```

Then run:

```bash
csvplotter
```

## Packaging Notes

- The app exposes two console scripts: `csvplotter` (launch) and `csvplotter-shortcut` (Windows shortcut creator).
- The icon file (`icon.ico`) is bundled as package data; ensure it exists in `csv_plotter_app/` before building distributions.

## Roadmap / Ideas
- Theming presets
- CSV delimiter auto-detect enhancements
- Time-series specific controls (resampling, rolling averages)
- Export of plot configuration as JSON

