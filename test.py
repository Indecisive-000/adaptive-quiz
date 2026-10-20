import unittest
from adaptive_engine import calculate_performance, change_difficulty
from data_handler import load_questions, questions_by_difficulty, questions_by_topic


class TestPerformanceScore(unittest.TestCase):
    def test_correct_fast(self):
        self.assertAlmostEqual(calculate_performance(True, 5, 15), 0.9, places=2)

    def test_wrong_fast(self):
        self.assertAlmostEqual(calculate_performance(False, 5, 15), 0.2, places=2)

    def test_correct_at_limit(self):
        self.assertAlmostEqual(calculate_performance(True, 15, 15), 0.7, places=2)

    def test_over_limit_is_clamped(self):
        self.assertAlmostEqual(calculate_performance(True, 20, 15), 0.7, places=2)

    def test_wrong_over_limit(self):
        self.assertAlmostEqual(calculate_performance(False, 20, 15), 0.0, places=2)


class TestChangeDifficulty(unittest.TestCase):
    def test_increase(self):
        self.assertEqual(change_difficulty([0.9, 0.9, 0.9, 0.9, 0.9], 1), 2)

    def test_decrease(self):
        self.assertEqual(change_difficulty([0.1, 0.1, 0.1, 0.1, 0.1], 2), 1)

    def test_no_change(self):
        self.assertEqual(change_difficulty([0.5, 0.6, 0.5, 0.6, 0.5], 2), 2)

    def test_does_not_exceed_max(self):
        self.assertEqual(change_difficulty([0.9, 0.9, 0.9, 0.9, 0.9], 3), 3)

    def test_does_not_go_below_min(self):
        self.assertEqual(change_difficulty([0.1, 0.1, 0.1, 0.1, 0.1], 1), 1)

    def test_empty_history(self):
        self.assertEqual(change_difficulty([], 2), 2)

    def test_too_few_answers(self):
        self.assertEqual(change_difficulty([0.9, 0.9], 1), 1)

    def test_only_recent_answers_count(self):
        # three old low scores followed by five high ones
        self.assertEqual(change_difficulty([0.1, 0.1, 0.1, 0.9, 0.9, 0.9, 0.9, 0.9], 1), 2)


class TestDataHandler(unittest.TestCase):
    def setUp(self):
        self.sample = [
            {"id": 1, "difficulty": 1, "topic": "OOP"},
            {"id": 2, "difficulty": 2, "topic": "OOP"},
            {"id": 3, "difficulty": 1, "topic": "Binary"}
        ]

    def test_filter_by_difficulty(self):
        result = questions_by_difficulty(self.sample, 1)
        self.assertEqual(len(result), 2)

    def test_filter_by_topic(self):
        result = questions_by_topic(self.sample, "OOP")
        self.assertEqual(len(result), 2)

    def test_filter_no_match(self):
        self.assertEqual(questions_by_topic(self.sample, "Logic Gates"), [])

    def test_question_bank_is_valid(self):
        # every question must be usable by the quiz
        questions = load_questions()
        ids = []
        for q in questions:
            self.assertNotIn(q["id"], ids)
            ids.append(q["id"])
            self.assertIn(q["answer"], q["options"])
            self.assertEqual(len(q["options"]), 4)
            self.assertIn(q["difficulty"], [1, 2, 3])


if __name__ == "__main__":
    unittest.main()