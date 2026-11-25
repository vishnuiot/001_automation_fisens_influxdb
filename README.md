# FiSens FBG Sensor – LabVIEW Programs and Documentation (2026)

This branch (`main`, mirrored in `2026`) holds the current LabVIEW programs, documentation, and configuration files for the FiSens / FiSpec fibre Bragg grating (FBG) sensing system. Last year's Python data-logging code is kept on the `2025` branch.

## Contents

| Folder / file | What it is |
|---|---|
| `5.fisens_labview_programs/` | LabVIEW VIs (`.vi`) for reading, processing, and fitting FBG spectra, plus a demo VI |
| `5.fisens_labview_programs/LabView VIs/` | LabVIEW 2014 versions of the data-processing, UDP-example, and cubic-parameter VIs, and the processing instructions |
| `FiSens FiSpec Handbook ver. 1.12.pdf` / `.docx` | Hardware and software handbook (version 1.12) |
| `Fisens_batch_file/` | Batch and IExpress files used to package the software |
| `Saved Data/` | Example saved measurement data and its configuration file |
| `Software Configuration files/` | Program settings for the BraggSens software |
| `micronor/` | Vendor LabVIEW scripts for the FISENS system |

## Requirements

- LabVIEW (the `_LV2014` VIs were saved with LabVIEW 2014; newer versions can usually open them)
- A FiSpec / FiSens FBG interrogator and its vendor software (not included here; see below)

## Notes

- The vendor FBG interrogator software (`MICRONOR_SOFTWARE_FBG-Interrogator_V2.zip`, 280 MB) is not in this repository because GitHub limits files to 100 MB. Get it from the manufacturer.
- Measurement files in `Saved Data/` contain a local file path in their header, replaced here with `<local-path>`.
- Do not commit credentials, API tokens, or local configuration with personal paths.
