import unittest

from mastermind.model.game import get_feedback


class TestSerialDevices(unittest.TestCase):

    def test_get_feedback(self):

        code = "1234"

        guess = "1111"
        expected_result = "2___"
        result = get_feedback(code, guess)
        self.assertEquals(expected_result, result )

        guess = "4321"
        expected_result = "1111"
        result = get_feedback(code, guess)
        self.assertEquals(expected_result, result)

        guess = "4___"
        expected_result = "1___"
        result = get_feedback(code, guess)
        self.assertEquals(result, expected_result)

        guess = "5555"
        expected_result = "____"
        result = get_feedback(code, guess)
        self.assertEquals(result, expected_result)

        guess = "1234"
        expected_result = "2222"
        result = get_feedback(code, guess)
        self.assertEquals(result, expected_result)

if __name__ == '__main__':
    unittest.main()
