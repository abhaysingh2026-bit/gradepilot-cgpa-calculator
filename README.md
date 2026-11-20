# ABES Smart CGPA & SGPA Calculator (Upgraded)

A beginner-friendly command-line academic calculator built with **Python, NumPy and Pandas**. It retains the original project purpose and menu workflow while improving validation, data handling, exports and testing.

## Features

- Register/update a student profile.
- Enter subject credits and internal/external marks.
- Calculate credit-weighted SGPA and overall CGPA.
- View subject results and semester-wise performance.
- Export a semester result to CSV.
- Delete a student's stored records after an explicit confirmation.

## Setup (VS Code / Windows)

1. Install Python 3.10 or newer.
2. Extract this ZIP and open the `ABES_Smart_CGPA_Calculator` folder in VS Code.
3. Open Terminal → New Terminal.
4. (Recommended) Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
5. Activate it:
   - Windows PowerShell: `.venv\\Scripts\\Activate.ps1`
   - macOS/Linux: `source .venv/bin/activate`
6. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
7. Run the program:
   ```bash
   python main.py
   ```

## Run automated tests

From the project folder:

```bash
python -m unittest discover -s tests -v
```

## Calculation

- **SGPA** = Σ(subject credits × subject grade points) / Σ(subject credits)
- **CGPA** = Σ(semester SGPA × semester total credits) / Σ(semester total credits)

The calculations use NumPy arrays for numeric validation and vectorised dot products. Pandas manages CSV records and analysis.

## Important academic disclaimer

The supplied percentage-to-grade bands are retained as an editable estimate from the original project. They have **not** been independently verified as the current ABES/AKTU ordinance. This tool does not implement every possible course-specific component passing rule, moderation rule, backlog rule or official result rule. Verify the current applicable regulations with ABES/AKTU before using any output for official academic decisions. Do not present this calculator as an official university result system.

## Data and security

- Student and marks data are stored in local CSV files in `data/` (plain text, not encrypted).
- Keep the folder private and do not upload real student records to a public GitHub repository.
- Writes use a temporary file followed by replacement to reduce the chance of a partially written CSV.
- Exported text fields are guarded against common spreadsheet formula injection prefixes.
- This is a local educational application; it does not provide user authentication, encryption, cloud backup or access control.
- Back up the `data/` folder before making major changes. Deletion is permanent for the local CSV records.
