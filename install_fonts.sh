#!/bin/bash
# Download and install MS Core Fonts
mkdir -p /tmp/msfonts
cd /tmp/msfonts

# Try to download from sourceforge mirrors
wget -q https://downloads.sourceforge.net/corefonts/trebuc32.exe || \
curl -sL https://downloads.sourceforge.net/corefonts/trebuc32.exe -o trebuc32.exe

if [ -f trebuc32.exe ]; then
    # Extract using cabextract if available
    if command -v cabextract &> /dev/null; then
        cabextract -q trebuc32.exe
        mkdir -p ~/.fonts
        cp *.ttf ~/.fonts/ 2>/dev/null
        fc-cache -f 2>/dev/null
        echo "Trebuchet MS installed to ~/.fonts/"
    else
        echo "cabextract not available, fonts not installed"
    fi
else
    echo "Could not download fonts"
fi
