import unittest
from unittest.mock import Mock, patch, call
from word_frequency_analyzer import open_url, extract_text, clean_text, analyze_words, display_results, save_to_file


class TestWebPageAnalyzer(unittest.TestCase):

    @patch('requests.get')
    def test_open_url(self, mock_get):
        mock_response = Mock()
        mock_response.text = '<html><body>Hello, World!</body></html>'
        mock_get.return_value = mock_response

        url = 'https://example.com'
        result = open_url(url)

        self.assertEqual(result, '<html><body>Hello, World!</body></html>')

    def test_extract_text(self):
        html_content = '<html><body>Hello, World!</body></html>'
        result = extract_text(html_content)

        self.assertEqual(result, 'Hello, World!')

    def test_clean_text(self):
        raw_text = 'Hello, World! 123 #$%^'
        result = clean_text(raw_text)

        self.assertEqual(result, 'Hello World 123 ')

    def test_analyze_words(self):
        text = 'apple banana apple orange banana'
        result = analyze_words(text)

        expected_result = [('apple', 2), ('banana', 2), ('orange', 1)]

        self.assertEqual(result, expected_result)

    @patch('builtins.print')
    def test_display_results(self, mock_print):
        most_common_words = [('apple', 2), ('banana', 2), ('orange', 1)]
        display_results(most_common_words)

        expected_calls = [
            call('apple : 2'),
            call('banana : 2'),
            call('orange : 1'),
        ]

        mock_print.assert_has_calls(expected_calls, any_order=False)

    @patch('word_frequency_analyzer.open', create=True)
    def test_save_to_file(self, mock_open):
        most_common_words = [('apple', 2), ('banana', 2), ('orange', 1)]
        mock_file = mock_open.return_value.__enter__.return_value

        save_to_file(most_common_words, filename='test_results.txt')

        expected_calls = [call('apple: 2\n'), call('banana: 2\n'), call('orange: 1\n')]
        for expected_call in expected_calls:
            self.assertIn(expected_call, mock_file.write.call_args_list)
