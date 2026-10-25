import os
import unittest
from unittest.mock import patch

import llm_client
from prompts import FORMATS, TASKS, build_messages


class PromptTemplateTests(unittest.TestCase):
    def test_all_tasks_support_all_output_formats(self):
        for task in TASKS:
            for output_format in FORMATS:
                with self.subTest(task=task, output_format=output_format):
                    system, user = build_messages(task, "sample material", "students", "friendly", output_format)
                    self.assertTrue(system)
                    self.assertIn("sample material", user)
                    self.assertIn(FORMATS[output_format], user)

    def test_invalid_task_is_rejected(self):
        with self.assertRaises(ValueError):
            build_messages("unknown", "text", "", "", "text")

    def test_invalid_format_is_rejected(self):
        with self.assertRaises(ValueError):
            build_messages("blog", "text", "", "", "xml")


class ProviderConfigurationTests(unittest.TestCase):
    def test_openai_requires_key_before_sdk_import(self):
        with patch.dict(os.environ, {"LLM_PROVIDER": "openai"}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "OPENAI_API_KEY is empty"):
                llm_client.generate("system", "user", 0.4, "text")

    def test_gemini_requires_key_before_sdk_import(self):
        with patch.dict(os.environ, {"LLM_PROVIDER": "gemini"}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "GEMINI_API_KEY is empty"):
                llm_client.generate("system", "user", 0.4, "text")

    def test_unknown_provider_is_rejected(self):
        with patch.dict(os.environ, {"LLM_PROVIDER": "unknown"}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "must be 'openai' or 'gemini'"):
                llm_client.generate("system", "user", 0.4, "text")


if __name__ == "__main__":
    unittest.main()
