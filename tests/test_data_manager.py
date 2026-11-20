import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import pandas as pd
import data_manager as dm


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.patches = [
            patch.object(dm, "ROOT", self.root),
            patch.object(dm, "DATA_DIR", self.root / "data"),
            patch.object(dm, "REPORT_DIR", self.root / "reports"),
            patch.object(dm, "SUBJECTS_FILE", self.root / "data" / "subjects.csv"),
            patch.object(dm, "SEMESTERS_FILE", self.root / "data" / "semesters.csv"),
            patch.object(dm, "STUDENTS_FILE", self.root / "data" / "students.csv"),
        ]
        for item in self.patches: item.start()
        dm.initialize_storage()

    def tearDown(self):
        for item in reversed(self.patches): item.stop()
        self.temp.cleanup()

    def test_student_save_update_and_delete(self):
        dm.save_student("12", "A", "CSE AI-ML", "2026-27")
        dm.save_student("12", "Abhay", "CSE AI-ML", "2026-27")
        self.assertEqual(len(dm.read_csv(dm.STUDENTS_FILE)), 1)
        dm.delete_student("12")
        self.assertTrue(dm.read_csv(dm.STUDENTS_FILE).empty)

    def test_export_sanitizes_formula_like_text(self):
        row = {c: "" for c in dm.SUBJECT_COLUMNS}
        row.update(roll_no="12", student_name="=1+1", semester=1, subject_code="CS1", subject_name="Test", credits=3, total_marks=80, maximum_marks=100, grade="A", grade_point=9)
        dm.save_subjects([row])
        output = dm.export_semester("12", 1)
        exported = pd.read_csv(output, dtype=str)
        self.assertEqual(exported.loc[0, "student_name"], "'=1+1")

    def test_empty_export_raises(self):
        with self.assertRaises(ValueError): dm.export_semester("missing", 1)


if __name__ == "__main__":
    unittest.main()
