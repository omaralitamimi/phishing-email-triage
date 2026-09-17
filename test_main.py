import unittest
from main import analyze


class EmailTests(unittest.TestCase):
    def test_domains_and_url(self):
        raw = b"From: Support <a@example.test>\r\nReply-To: x@reply.test\r\nSubject: Test\r\nContent-Type: text/plain\r\n\r\nVisit https://portal.example.test/login"
        result = analyze(raw)
        self.assertEqual(result["from_domain"], "example.test")
        self.assertEqual(result["reply_to_domain"], "reply.test")
        self.assertEqual(result["url_hosts"], ["portal.example.test"])


if __name__ == "__main__":
    unittest.main()
