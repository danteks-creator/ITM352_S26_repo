import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("Asst3.py")
SPEC = importlib.util.spec_from_file_location("asst3_module", str(MODULE_PATH))
asst3 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(asst3)


class TestAsst3Parts(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        tdir = Path(self._tmpdir.name)

        self._orig_paths = (
            asst3.QUESTIONS_FILE,
            asst3.USERS_FILE,
            asst3.SCORES_FILE,
            asst3.HIGHSCORE_FILE,
        )

        asst3.QUESTIONS_FILE = str(tdir / "questions.json")
        asst3.USERS_FILE = str(tdir / "users.json")
        asst3.SCORES_FILE = str(tdir / "scores.json")
        asst3.HIGHSCORE_FILE = str(tdir / "highscore.txt")

        questions = [
            {
                "question": "2 + 2 = ?",
                "options": {"a": "3", "b": "4", "c": "5"},
                "correct_answers": ["b"],
            },
            {
                "question": "Primary colors?",
                "options": {"a": "Red", "b": "Blue", "c": "Green"},
                "correct_answers": ["a", "b"],
                "match_type": "any",
            },
        ]

        with open(asst3.QUESTIONS_FILE, "w", encoding="utf-8") as question_file:
            json.dump(questions, question_file)

        asst3.ensure_data_files()
        asst3.app.config["TESTING"] = True
        asst3.app.config["SECRET_KEY"] = "test-secret"
        asst3.app.template_folder = str(Path(__file__).with_name("templates"))
        asst3.app.static_folder = str(Path(__file__).with_name("static"))

    def tearDown(self):
        (
            asst3.QUESTIONS_FILE,
            asst3.USERS_FILE,
            asst3.SCORES_FILE,
            asst3.HIGHSCORE_FILE,
        ) = self._orig_paths
        self._tmpdir.cleanup()

    def _client_with_user(self, username="tester1"):
        client = asst3.app.test_client()
        with client.session_transaction() as sess:
            sess["username"] = username
        return client

    def _show(self, test_label, details):
        print(f"\n{test_label} RESULT")
        for key, value in details.items():
            print(f"  - {key}: {value}")

    def test_03_data_file_initialization(self):
        users_exists = Path(asst3.USERS_FILE).exists()
        scores_exists = Path(asst3.SCORES_FILE).exists()
        highscore_exists = Path(asst3.HIGHSCORE_FILE).exists()
        high_score_value = asst3.read_high_score()

        self._show(
            "Test 3",
            {
                "users_file_exists": users_exists,
                "scores_file_exists": scores_exists,
                "highscore_file_exists": highscore_exists,
                "initial_high_score": high_score_value,
            },
        )

        self.assertTrue(users_exists)
        self.assertTrue(scores_exists)
        self.assertTrue(highscore_exists)
        self.assertEqual(high_score_value, 0)

    def test_04_validation_helpers(self):
        details = {
            "validate_username('ab')": asst3.validate_username("ab"),
            "validate_username('ok_user1')": asst3.validate_username("ok_user1"),
            "validate_password('abcdef')": asst3.validate_password("abcdef"),
            "validate_password('abc123')": asst3.validate_password("abc123"),
            "validate_display_name('*')": asst3.validate_display_name("*"),
            "validate_display_name('Dante S')": asst3.validate_display_name("Dante S"),
        }
        self._show("Test 4", details)

        self.assertNotEqual(details["validate_username('ab')"], "")
        self.assertEqual(details["validate_username('ok_user1')"], "")
        self.assertNotEqual(details["validate_password('abcdef')"], "")
        self.assertEqual(details["validate_password('abc123')"], "")
        self.assertNotEqual(details["validate_display_name('*')"], "")
        self.assertEqual(details["validate_display_name('Dante S')"], "")

    def test_05_register_login_and_password_hashing(self):
        client = asst3.app.test_client()

        register_response = client.post(
            "/register",
            data={
                "username": "reguser1",
                "password": "abc123",
                "confirm_password": "abc123",
            },
            follow_redirects=False,
        )

        login_response = client.post(
            "/login",
            data={"username": "reguser1", "password": "abc123"},
            follow_redirects=False,
        )

        users = asst3.load_json(asst3.USERS_FILE, {})
        password_hash = users["reguser1"]["password_hash"]

        self._show(
            "Test 5",
            {
                "register_status": register_response.status_code,
                "login_status": login_response.status_code,
                "stored_usernames": list(users.keys()),
                "password_hash_prefix": password_hash.split(":", 1)[0],
            },
        )

        self.assertEqual(register_response.status_code, 302)
        self.assertEqual(login_response.status_code, 302)
        self.assertIn("reguser1", users)
        self.assertNotEqual(password_hash, "abc123")
        self.assertTrue(password_hash.startswith("scrypt:") or password_hash.startswith("pbkdf2:"))

    def test_06_quiz_start_mode_validation(self):
        client = self._client_with_user()
        response = client.post("/api/quiz/start", json={"challenge_mode": "speedrun"})
        body = response.get_json() or {}

        self._show(
            "Test 6",
            {
                "status": response.status_code,
                "error": body.get("error"),
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_07_quiz_start_standard_payload(self):
        client = self._client_with_user()
        response = client.post("/api/quiz/start", json={"challenge_mode": "standard"})
        body = response.get_json() or {}
        question = body.get("question") or {}

        self._show(
            "Test 7",
            {
                "status": response.status_code,
                "challenge_mode": body.get("challenge_mode"),
                "question_number": question.get("question_number"),
                "total_questions": question.get("total_questions"),
                "option_keys": sorted((question.get("options") or {}).keys()),
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(question, dict)
        self.assertIn("options", question)
        self.assertIn("question_number", question)
        self.assertEqual(body.get("challenge_mode"), "standard")

    def test_08_answer_payload_validation(self):
        client = self._client_with_user()
        client.post("/api/quiz/start", json={"challenge_mode": "standard"})
        response = client.post("/api/quiz/answer", json={"answers": "a"})
        body = response.get_json() or {}

        self._show(
            "Test 8",
            {
                "status": response.status_code,
                "error": body.get("error"),
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_09_scoring_and_completion_flow(self):
        client = self._client_with_user()
        client.post("/api/quiz/start", json={"challenge_mode": "standard"})

        with client.session_transaction() as sess:
            question_one = sess["quiz_questions"][0]
            first_answer = list(question_one["correct_answers"])

        first_response = client.post("/api/quiz/answer", json={"answers": first_answer})

        with client.session_transaction() as sess:
            question_two = sess["quiz_questions"][1]
            second_answer = (
                [question_two["correct_answers"][0]]
                if question_two.get("match_type") == "any"
                else list(question_two["correct_answers"])
            )

        second_response = client.post("/api/quiz/answer", json={"answers": second_answer})
        first_body = first_response.get_json() or {}
        second_body = second_response.get_json() or {}

        self._show(
            "Test 9",
            {
                "first_answer_status": first_response.status_code,
                "score_after_first": first_body.get("score"),
                "second_answer_status": second_response.status_code,
                "completed": second_body.get("completed"),
                "final_score": (second_body.get("result") or {}).get("score"),
                "redirect_url": second_body.get("redirect_url"),
            },
        )

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(first_body.get("score"), 1)
        self.assertEqual(second_response.status_code, 200)
        self.assertTrue(second_body.get("completed"))
        self.assertEqual((second_body.get("result") or {}).get("score"), 2)

    def test_10_timed_timeout_endpoint(self):
        client = self._client_with_user()
        start_response = client.post(
            "/api/quiz/start",
            json={"challenge_mode": "timed", "time_limit_seconds": 10},
        )

        timeout_response = client.post("/api/quiz/timeout", json={})
        start_body = start_response.get_json() or {}
        timeout_body = timeout_response.get_json() or {}

        self._show(
            "Test 10",
            {
                "start_status": start_response.status_code,
                "timed_mode": start_body.get("challenge_mode"),
                "timeout_status": timeout_response.status_code,
                "timed_out": timeout_body.get("timed_out"),
                "completed": timeout_body.get("completed"),
            },
        )

        self.assertEqual(start_response.status_code, 200)
        self.assertEqual(timeout_response.status_code, 200)
        self.assertTrue(timeout_body.get("timed_out"))
        self.assertTrue(timeout_body.get("completed"))

    def test_11_ranking_sort_and_rank_assignment(self):
        sample_scores = [
            {"username": "u1", "score": 8, "total_questions": 10, "time_taken_seconds": 40},
            {"username": "u2", "score": 9, "total_questions": 10, "time_taken_seconds": 60},
            {"username": "u3", "score": 8, "total_questions": 10, "time_taken_seconds": 30},
        ]

        ranked = asst3.compute_rankings(sample_scores)

        self._show(
            "Test 11",
            {
                "ranked_user_order": [row.get("username") for row in ranked],
                "ranked_scores": [row.get("score") for row in ranked],
                "assigned_ranks": [row.get("rank") for row in ranked],
            },
        )

        self.assertEqual(ranked[0]["username"], "u2")
        self.assertEqual(ranked[1]["username"], "u3")
        self.assertEqual(ranked[0]["rank"], 1)
        self.assertEqual(ranked[-1]["rank"], 3)

    def test_12_display_name_update_and_persistence(self):
        client = self._client_with_user("nameuser")
        client.post("/api/quiz/start", json={"challenge_mode": "standard"})

        with client.session_transaction() as sess:
            question_one = sess["quiz_questions"][0]
            question_two = sess["quiz_questions"][1]

        client.post("/api/quiz/answer", json={"answers": list(question_one["correct_answers"])})
        second_answer = (
            [question_two["correct_answers"][0]]
            if question_two.get("match_type") == "any"
            else list(question_two["correct_answers"])
        )
        client.post("/api/quiz/answer", json={"answers": second_answer})

        invalid_name_response = client.post("/api/quiz/display-name", json={"display_name": "*bad*"})
        valid_name_response = client.post("/api/quiz/display-name", json={"display_name": "Dante S"})

        scores = asst3.load_json(asst3.SCORES_FILE, [])
        saved_names = [row.get("display_name") for row in scores]

        self._show(
            "Test 12",
            {
                "invalid_name_status": invalid_name_response.status_code,
                "valid_name_status": valid_name_response.status_code,
                "saved_display_names": saved_names,
            },
        )

        self.assertEqual(invalid_name_response.status_code, 400)
        self.assertEqual(valid_name_response.status_code, 200)
        self.assertTrue(any(name == "Dante S" for name in saved_names))


if __name__ == "__main__":
    unittest.main(verbosity=2)
