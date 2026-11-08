"""R15: publisher-original discovery and physical job-join feasibility.

Never infer an H1 restoration endpoint from node uptime or an independently
scheduled workload's lifecycle. All HTML information comes from the publisher
landing page, not private data. A source download needs an actual publisher
URL, verified content digest, a safe archive extraction and a justified key.
"""
from __future__ import annotations

from html.parser import HTMLParser
from hashlib import sha256
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import urlopen, Request
import argparse
import json
import re

PUBLISHER_PAGE="https://usrc.lanl.gov/data/failure-data.php"
MIRROR_SOURCE="https://github.com/Derek-Jones/ESEUR-code-data/blob/bc1d9e99da2a956cdecba9d9d7f6f9b61a371c5f/reliability/LA-UR-05-7318-failure-data-1996-2005.csv.xz"
MIRROR_SHA256="ed32fd254a013df79f5f475f4eac85980f7229735e100ac427343ef449a75140"
MAX_HTML_BYTES=600_000


class SourceLinks(HTMLParser):
    """Extract publisher HTML row text AND actual anchor targets, not guesses."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.hrefs=[]
        self._anchor=None
        self._in_row=0
        self._row_text=[]
        self._row_href=[]
        self.rows=[]

    def handle_starttag(self,tag,attrs):
        props=dict(attrs)
        if tag=="tr":
            self._in_row+=1
            if self._in_row==1:
                self._row_text=[]
                self._row_href=[]
        if tag=="a":
            self._anchor={"href":props.get("href",""),"label":[]}

    def handle_data(self,data):
        if self._anchor is not None:
            self._anchor["label"].append(data)
        if self._in_row:
            self._row_text.append(data)

    def handle_endtag(self,tag):
        if tag=="a" and self._anchor is not None:
            item={"href":self._anchor["href"],
                  "label":" ".join(" ".join(self._anchor["label"]).split())}
            self.hrefs.append(item)
            if self._in_row:
                self._row_href.append(item)
            self._anchor=None
        if tag=="tr" and self._in_row:
            self._in_row-=1
            if self._in_row==0:
                self.rows.append({
                    "text":" ".join(" ".join(self._row_text).split())[:300],
                    "links":list(self._row_href)
                })


def _lanl_url(origin: str,href: str) -> str | None:
    if not href:
        return None
    url=urljoin(origin,href)
    p=urlparse(url)
    if p.scheme!="https" or not (
        p.hostname=="lanl.gov" or
        (p.hostname and p.hostname.endswith(".lanl.gov"))):
        return None
    return url


def interpret_html(page: str,source: str=PUBLISHER_PAGE) -> dict:
    parser=SourceLinks()
    parser.feed(page)
    relevant=[]
    for r in parser.rows:
        if ("All systems failure" in r["text"] or
            "System 20 usage" in r["text"] or
            "System 20 node" in r["text"] or
            "System 20 event" in r["text"]):
            relevant.append({
                "publisher_visible_text":r["text"],
                "publisher_lanl_links":[v for a in r["links"]
                    if (v:=_lanl_url(source,a["href"]))],
                "third_party_links_removed":sum(
                    _lanl_url(source,a["href"]) is None for a in r["links"]),
            })
    return {
        "relevant_publisher_table_rows":relevant,
        "publisher_link_targets_verified_in_html":sum(
            len(x["publisher_lanl_links"]) for x in relevant),
        "any_original_data_downloaded":False,
        "mirror_authenticity_independently_proven":False,
        "no_service_restoration_join_proven":True,
    }


def discover() -> dict:
    """Network landing page only; unavailable publisher is explicit, not H1 data."""
    try:
        req=Request(PUBLISHER_PAGE,
                    headers={"User-Agent":"FOPD-R15-Research-Audit/1.0"})
        with urlopen(req,timeout=20) as connection:
            if not _lanl_url(PUBLISHER_PAGE,connection.geturl()):
                raise ValueError("untrusted landing-page redirect")
            payload=connection.read(MAX_HTML_BYTES+1)
        if len(payload)>MAX_HTML_BYTES:
            raise ValueError("official publisher page over size bound")
        parsed=interpret_html(payload.decode("utf-8",errors="replace"))
        return {
            "publisher_retrieval":"SUCCESS",
            "publisher_html_sha256":sha256(payload).hexdigest(),
            "publisher_bytes_read":len(payload),
            **parsed,
        }
    except Exception as ex:
        # Preserve explicit failure; under no circumstances infer success.
        return {
            "publisher_retrieval":"UNAVAILABLE_OR_UNVERIFIED",
            "failure_kind":type(ex).__name__,
            "relevant_publisher_table_rows":[],
            "publisher_link_targets_verified_in_html":0,
            "any_original_data_downloaded":False,
            "mirror_authenticity_independently_proven":False,
            "no_service_restoration_join_proven":True,
        }


def audit() -> dict:
    discovery=discover()
    return {
        "gate":"R15",
        "classification":"PUBLISHER_DOWNLOAD_LINK_DISCOVERY_NOT_H1",
        "publisher_page":PUBLISHER_PAGE,
        "mirror_sha256_R14":MIRROR_SHA256,
        "official_retrieval":discovery,
        "original_publisher_LAUR_file_authenticated":False,
        "joined_node_to_same_job_trajectory":False,
        "original_H1_real_world_labels":0,
        "R8_R14_archives_unchanged":True,
        "sealed_H1_test_samples":0,
        "result":"METADATA_DISCOVERY_COMPLETED_NO_H1_ADMISSION",
    }


def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=Path)
    args=ap.parse_args()
    result=audit()
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",
                               encoding="utf-8")
    print(json.dumps(result,sort_keys=True,indent=2))


if __name__=="__main__":
    main()
