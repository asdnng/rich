import unittest
from rich.progress import TaskProgressColumn
from rich.text import Text

branch_hit = {
    "Branch 1": False,
    "Branch 2": False,
    "Branch 3": False,
    "Branch 4": False,
    "Branch 5": False,
    "Branch 6": False,
}

class MockTask:
    def __init__(self, total, finished_speed=None, speed=None):
        self.total = total
        self.finished_speed = finished_speed
        self.speed = speed

class TestTaskProgressColumn(unittest.TestCase):

    def setUp(self):
        self.column = TaskProgressColumn(
            show_speed=True,
            text_format="Progress: {task.total}",
            text_format_no_percentage="Progress",
            markup=True,
            style="bold",
            justify="center",
            highlighter=None
        )

    def test_render_with_total_none_and_show_speed(self):
        print("Testing Branch 1: task.total is None and self.show_speed is True")
        task = MockTask(total=None, finished_speed=5, speed=3)
        result = self.column.render(task)
        branch_hit["Branch 1"] = True
        self.assertIsInstance(result, Text)
        self.assertIn("5", str(result))

    def test_render_with_total_none_no_show_speed(self):
        print("Testing Branch 2: task.total is None and self.show_speed is False")
        self.column.show_speed = False
        task = MockTask(total=None)
        result = self.column.render(task)
        branch_hit["Branch 2"] = True
        self.assertIsInstance(result, Text)
        self.assertIn("Progress", str(result))

    def test_render_with_total_and_markup(self):
        print("Testing Branch 3: task.total is not None and self.markup is True")
        task = MockTask(total=100)
        result = self.column.render(task)
        branch_hit["Branch 3"] = True
        self.assertIsInstance(result, Text)
        self.assertIn("Progress: 100", str(result))

    def test_render_with_total_no_markup(self):
        print("Testing Branch 4: task.total is not None and self.markup is False")
        self.column.markup = False
        task = MockTask(total=100)
        result = self.column.render(task)
        branch_hit["Branch 4"] = True
        self.assertIsInstance(result, Text)
        self.assertIn("Progress: 100", str(result))

    def test_render_with_highlighter(self):
        print("Testing Branch 5: self.highlighter is not None")
        from rich.highlighter import NullHighlighter
        self.column.highlighter = NullHighlighter()
        task = MockTask(total=100)
        result = self.column.render(task)
        branch_hit["Branch 5"] = True
        self.assertIsInstance(result, Text)
        self.assertIn("Progress: 100", str(result))

    def test_render_without_highlighter(self):
        print("Testing Branch 6: self.highlighter is None")
        self.column.highlighter = None
        task = MockTask(total=100)
        result = self.column.render(task)
        branch_hit["Branch 6"] = True
        self.assertIsInstance(result, Text)
        self.assertIn("Progress: 100", str(result))

    @classmethod
    def tearDownClass(cls):
        hits = sum(hit for hit in branch_hit.values())
        total_branches = len(branch_hit)
        coverage_percent = (hits / total_branches) * 100
        print(f"Coverage: {coverage_percent:.2f}%")
        for branch, hit in branch_hit.items():
            print(f"{branch} was {'hit' if hit else 'not hit'}")

if __name__ == "__main__":
    unittest.main()