# Steganography-P1

Simple LSB steganography tools to hide a file inside an image and recover it later. The encoder embeds the file name and content into the least-significant bits of the image pixels; the decoder reconstructs and saves the original file.

## Overview
- Encoder flow: pick a file → pick a cover image → produce an encoded image named `enc_<original_image_name>` in the same folder as the chosen image.
- Decoder flow: pick an encoded image → the original file is rebuilt (using the embedded file name) in the current working directory.
- Data format embedded:
	- 1 byte: file name length (in bytes)
	- N bytes: file name
	- M bytes: base64-encoded file content
	- 1 byte: null terminator `00000000`

## Requirements
- Python 3.10+ (Windows, macOS, or Linux)
- Packages: `Pillow`, `bitarray`

Install dependencies (Windows PowerShell):

Option A — use the included installer:
```
cd "./EncoderDecoder/Steganography-P1"
./install_requirements.bat
```

Option B — install via pip:
```
cd "./EncoderDecoder/Steganography-P1"
python -m pip install -r requirements.txt
```

Optional: create and use a virtual environment (recommended):
```
cd "./EncoderDecoder/Steganography-P1"
python -m venv .venv
./.venv/Scripts/Activate.ps1
python -m pip install -r requirements.txt
```

## How to Run

All scripts open native file pickers (Tkinter). No command-line arguments are needed.

Encode a file into an image:
```
cd "./EncoderDecoder/Steganography-P1"
python ./Encoder.py
```
Steps in the UI:
- Choose the file to embed (any type).
- Choose the cover image (`.png`, `.jpg`, `.jpeg`, `.bmp`).
- Wait for encoding to complete; the output image is saved alongside the chosen image as `enc_<image_name>`.

Decode an encoded image:
```
cd "./EncoderDecoder/Steganography-P1"
python ./Decoder.py
```
Steps in the UI:
- Choose the encoded image (the one starting with `enc_...`).
- The original file is reconstructed and saved in the current working directory using the embedded file name.

## Capacity Notes
- Approximate capacity in bytes ≈ floor((width × height × 3) / 8) minus small overhead (file name length, file name, and terminator).
- If you see "Your image is too small!" pick a larger or higher-resolution image, or a smaller file.

## Tips and Common Issues
- "ModuleNotFoundError" for `PIL` or `bitarray`: install requirements using the commands above.
- Tk dialog doesn’t show: it may be behind other windows; check the taskbar.
- Output location:
	- Encoded image is saved next to the chosen cover image.
	- Decoded file is written to the current working directory you launched the script from.
