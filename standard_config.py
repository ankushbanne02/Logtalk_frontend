# --- Mirror backend maps (state number -> name) ---
BARCODE_STATE_MAP = {
    "1": "Not used",
    "2": "Data too short",
    "3": "Data too long",
    "4": "No data received",
    "5": "No read (no label found)",
    "6": "Data OK (correct read)",
    "7": "Data not OK (incorrect read)",
}

VOLUME_STATE_MAP = {
    "1": "Not used",
    "2": "Data too short",
    "3": "Data too long",
    "4": "No data received",
    "5": "No read (no label found)",
    "6": "Data OK (correct read)",
    "7": "Data not OK (incorrect read)",
    "8": "Under limit",
    "9": "Over limit",
}

# Colors (HEX values for Plotly charts)
STATE_COLOR_MAP = {
    "Not used": "#d3d3d3",                     # Neutral grey
    "Data too short": "#ffb3b3",               # Soft red
    "Data too long": "#ff7f7f",                # Medium red
    "No data received": "#ff4c4c",             # Strong red
    "No read (no label found)": "#cc0000",     # Dark red
    "Data OK (correct read)": "#28a745",       # Green (success)
    "Data not OK (incorrect read)": "#ffc107", # Amber warning
    "Under limit": "#66b2ff",                  # Light blue
    "Over limit": "#0056b3",                   # Darker blue
    "Unknown state": "#808080"                 # Neutral grey
}

# --- Msg ID 6 Sort Codes ---
SORT_CODE_MAP_6 = {
    "0":  "Unknown state",
    "1":  "Good sort/divert",
    "2":  "Destination not reached",
    "3":  "Destination invalid",
    "4":  "Destination full",
    "5":  "Destination operational unavailable",
    "10": "Sorter not at speed",
    "12": "No sort initiated higher priority destination downstream",
    "13": "Max. circulations",
    "14": "Dimension error",
    "15": "Weight error",
    "16": "No sort initiated",
    "17": "Destination throughput limit",
    "25": "Destination unreachable",
    "26": "Destination technically unavailable",
    "27": "Failed to divert",
    "28": "Divert switch error"
}

# Colors for Msg ID 6 states (HEX values for Plotly)
SORT_CODE_COLOR_MAP_6 = {
    "Unknown state": "#808080",                     # Grey
    "Good sort/divert": "#28a745",                  # Green
    "Destination not reached": "#e74c3c",           # Bright red
    "Destination invalid": "#e67e22",               # Orange
    "Destination full": "#9b59b6",                  # Purple
    "Destination operational unavailable": "#8d6e63", # Brown
    "Sorter not at speed": "#3498db",               # Blue
    "No sort initiated higher priority destination downstream": "#95a5a6", # Grey
    "Max. circulations": "#6c5ce7",                 # Violet
    "Dimension error": "#ff6b81",                   # Pinkish red
    "Weight error": "#f1c40f",                      # Yellow
    "No sort initiated": "#f39c12",                 # Orange-yellow
    "Destination throughput limit": "#16a085",      # Teal
    "Destination unreachable": "#d35400",           # Burnt orange
    "Destination technically unavailable": "#c4f0d6", # Light green
    "Failed to divert": "#2980b9",                  # Dark blue
    "Divert switch error": "#f9e79f"                # Soft yellow
}