# IOT Lab Assignment - Raspberry Pi Camera

## Project Overview

Lab assignment exploring the Raspberry Pi Camera module using Python 3.
Target platform: Raspberry Pi (runs in Thonny IDE).

## Project Structure

```
Lab_Assignment/
  src/           - Python source files
  images/        - Captured images output
  videos/        - Captured video output
  docs/          - Lab notes and documentation
  requirements.txt
  README.txt
```

## Environment

- Platform: Raspberry Pi (Linux ARM)
- Python: 3.x
- IDE: Thonny
- Camera library: picamera2 (for newer Raspberry Pi OS) or picamera (legacy)

## Code Style

- Plain ASCII characters only, no Unicode symbols or special formatting
- No f-strings with complex expressions (keep Thonny-compatible)
- Keep imports minimal and standard
- Use descriptive variable names in plain English

## Running Code

All scripts run directly in Thonny or via:
  python3 src/script_name.py

## Notes

- Do not use emoji or special characters in code or comments
- Prefer simple, readable code over clever one-liners
- Camera must be enabled in raspi-config before use
