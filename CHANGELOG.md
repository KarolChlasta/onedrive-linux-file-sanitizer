# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2024-02-14

### Added
- Initial release
- GUI application for fixing OneDrive-incompatible filenames on Linux
- Scan mounted OneDrive directories for problematic files
- Fix invalid characters (`< > : " / \ | ? *`)
- Remove trailing spaces and periods
- Handle Windows reserved names (CON, PRN, AUX, NUL, COM1-9, LPT1-9)
- Detect and fix NTFS alternate data streams (files with colons)
- Preview changes before applying
- Batch rename functionality with confirmation dialog
- Process files depth-first to avoid parent/child conflicts
- Error handling and reporting
