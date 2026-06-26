import os

# Per defecte: lector sèrie/raw PL2303
UICC_BIN_DEFAULT = os.environ.get("UICC_BIN", "/usr/local/bin/program_uicc")
UICC_PORT_DEFAULT = os.environ.get("UICC_PORT", "/dev/ttyUSB0")

# Per defecte: mode real
UICC_SIMULATE_DEFAULT = os.environ.get("UICC_SIMULATE", "0") == "1"
