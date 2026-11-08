"""R15 publisher HTML link-discovery security tests; all are offline."""
import json
from pathlib import Path
import unittest
from experiments.p1_r15_upstream_probe import (
    MIRROR_SHA256,SourceLinks,interpret_html,_lanl_url,audit
)

HTML="""<html><table>
<tr><td>All systems failure/interrupt data 1996-2005</td><td>23,741</td>
<td><a href="/data/files/failure.tar.gz">Data</a></td></tr>
<tr><td>System 20 usage with node info</td>
<td><a href="https://usrc.lanl.gov/data/usage20.tar.gz">Data</a></td></tr>
<tr><td>System 20 event info</td>
<td><a href="https://evil.example/steal">Data</a></td></tr>
</table></html>"""

class R15PublisherLinkTests(unittest.TestCase):
    def test_safe_link_capture(self):
        result=interpret_html(HTML)
        self.assertEqual(result["publisher_link_targets_verified_in_html"],2)
        self.assertIn("https://usrc.lanl.gov/data/files/failure.tar.gz",
            result["relevant_publisher_table_rows"][0]["publisher_lanl_links"])
        self.assertEqual(result["relevant_publisher_table_rows"][2][
            "third_party_links_removed"],1)

    def test_physical_event_and_usage_links_are_separate(self):
        result=interpret_html(HTML)
        self.assertEqual(len(result["relevant_publisher_table_rows"]),3)
        self.assertNotEqual(result["relevant_publisher_table_rows"][0]["publisher_lanl_links"],
                            result["relevant_publisher_table_rows"][1]["publisher_lanl_links"])
        self.assertFalse(result["mirror_authenticity_independently_proven"])

    def test_admission_never_derived_from_page_text_or_link(self):
        for markup in (HTML,"<html><p>23,741 jobs recovered under policy</p></html>"):
            obj=interpret_html(markup)
            self.assertTrue(obj["no_service_restoration_join_proven"])
            self.assertFalse(obj["any_original_data_downloaded"])

    def test_off_domain_urls_excluded(self):
        for candidate in ("https://evil.example/file.tar.gz",
                          "http://usrc.lanl.gov/data/file.tar.gz",
                          "javascript:alert(1)",
                          "//attacker.example/file.tar.gz"):
            self.assertIsNone(_lanl_url("https://usrc.lanl.gov/data/failure-data.php",
                                        candidate))
        self.assertIsNotNone(_lanl_url(
            "https://usrc.lanl.gov/data/failure-data.php","/data/a.tar.gz"))

    def test_empty_table_is_not_invented(self):
        item=interpret_html("<html><body>All systems failure data</body></html>")
        self.assertEqual(item["publisher_link_targets_verified_in_html"],0)
        self.assertEqual(item["relevant_publisher_table_rows"],[])

    def test_r14_sha256_is_unchanged(self):
        archived=json.loads((Path(__file__).resolve().parents[1]/
            "research/R14-lanl-mirror-raw-audit-20261108.json").read_text())
        self.assertEqual(archived["compressed_sha256"],MIRROR_SHA256)
        self.assertEqual(archived["strict_restoration_eligible_labels"],0)

if __name__=="__main__":
    unittest.main()
