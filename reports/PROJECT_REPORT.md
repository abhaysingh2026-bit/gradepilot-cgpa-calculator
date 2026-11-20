# Project Report: ABES Smart CGPA & SGPA Calculator (Upgraded)

## 1. Introduction

The ABES Smart CGPA & SGPA Calculator is a local command-line educational tool intended to help B.Tech students estimate semester grade point average (SGPA), cumulative grade point average (CGPA), and review stored academic performance. The upgrade preserves the original Python, NumPy and Pandas implementation.

## 2. Problem statement and scope

Students may need to calculate credit-weighted grade averages repeatedly and maintain semester-wise records. Manual calculations can be time-consuming and may lead to arithmetic or record-keeping mistakes. This project provides a simple, keyboard-operated tool for entering subject marks and credits, calculating weighted averages, storing records and reviewing results.

The tool is an educational estimator, not an official ABES/AKTU result generator. The percentage-to-grade bands remain configurable and must be checked against the current applicable academic regulations. Course-specific pass conditions and university moderation are not assumed.

## 3. Objectives

- Calculate SGPA from subject credits and grade points.
- Calculate CGPA using semester credit totals.
- Store student, subject and semester records in CSV files.
- Provide subject-level result viewing and semester-wise analysis.
- Export semester data and support intentional deletion of a student's local records.
- Improve input validation, maintainability, data-write reliability and test coverage.

## 4. Technology stack

| Technology | Use                                                              |
| ---------- | ---------------------------------------------------------------- |
| Python     | Application flow, prompts, validation and file operations        |
| NumPy      | Numeric arrays, validation and weighted dot-product calculations |
| Pandas     | CSV persistence, filtering, tabular display and analysis         |
| unittest   | Automated unit and storage tests                                 |

## 5. Calculation methodology

**SGPA** = Σ(Cᵢ × Gᵢ) / Σ(Cᵢ), where Cᵢ is subject credit and Gᵢ is subject grade point.

**CGPA** = Σ(Sⱼ × Tⱼ) / Σ(Tⱼ), where Sⱼ is semester SGPA and Tⱼ is the semester's total credits.

The calculator rejects empty or mismatched lists, non-positive credits, grade points outside 0–10, SGPA outside 0–10, and non-finite values such as NaN or infinity.

## 6. Improvements mapped to the five judging criteria

### 6.1 Code quality

- Kept separate modules for user interaction, calculation, grading configuration, persistence and analysis.
- Added clearer function documentation and more consistent error messages.
- Centralised numeric validation for the calculation functions.
- Removed guessed course-type pass thresholds from the input flow; academic rules are not silently invented.

### 6.2 Problem statement alignment

- Preserved the original purpose: subject entry, SGPA, CGPA, semester records and performance analysis.
- Kept the credit-weighted formulas central to the project.
- Added a clear scope statement and disclaimer that outputs are estimates, not official university results.
- Retained Python, NumPy and Pandas without adding an unrelated framework or feature set.

### 6.3 Efficiency

- NumPy uses vectorised dot products rather than manually iterating to calculate weighted averages.
- Pandas performs filtering and semester-wise analysis on tabular records.
- CSV writes use a temporary file and atomic replacement to reduce partial-write risk.
- The project is intended for small student-level datasets; no unsupported large-scale performance claim is made.

### 6.4 Accessibility

- The application remains keyboard-driven and can be operated from a terminal.
- Menu options are numbered, prompts describe expected ranges, and errors are communicated in text.
- Important academic limitations are displayed in the application rather than hidden in documentation.
- This is a CLI improvement, not a claim of full WCAG compliance or a screen-reader-tested graphical interface.

### 6.5 Security and testing

- Numeric input rejects NaN and infinity.
- Destructive deletion requires the exact word `DELETE`.
- Export filenames are built from a restricted roll-number character set.
- Exported text cells beginning with common spreadsheet formula characters are prefixed to reduce CSV formula-injection risk.
- CSV data remain plain text and are not encrypted. The app has no login, permissions system or cloud security; users must protect the local folder and avoid publishing personal records.
- Automated tests cover weighted SGPA/CGPA, invalid and boundary values, NaN/infinity, grade boundaries, student update/delete, empty export and spreadsheet-safe export.

## 7. Test execution and result

Run:

```bash
python -m unittest discover -s tests -v
```

At the time this upgraded package was prepared, **9 automated tests passed**. These tests cover the calculation module and key CSV storage/export paths. They do not prove that every interactive menu sequence or every institutional grading scenario is correct.

## 8. Limitations and future scope

- Confirm the current ABES/AKTU grade scale, subject-wise passing conditions, and percentage conversion rules with the official academic documents.
- Add a configurable official grading profile only after the college's current rules are obtained and verified.
- Consider a graphical interface and accessibility testing in a later version.
- Consider encrypted storage and authenticated access only if the project later becomes a multi-user application.
- Add more integration tests for all menu workflows and backup/restore.

## 9. Conclusion

The upgraded calculator strengthens the original project without changing its identity or technology stack. It is more defensive around numeric input, clearer about academic assumptions, safer when exporting CSV files, and supported by a repeatable automated test suite. Its results should be treated as estimates until the current official ABES/AKTU rules are verified.
