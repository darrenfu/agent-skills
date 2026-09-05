from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from xhs.feed_detail import (  # noqa: E402
    _extract_feed_detail,
    _extract_note_id_from_url,
    _validate_share_url,
)
from image_downloader import _normalize_image_url  # noqa: E402


class FakePage:
    def __init__(self, state: dict):
        self.state = state

    def evaluate(self, expression: str):
        if "noteDetailMap" in expression:
            return json.dumps(self.state)
        if "#detail-desc" in expression:
            return {"body": "公开正文", "tags": ["#读书"]}
        return None


def test_validate_share_url_accepts_only_xhs_hosts():
    _validate_share_url("https://xhslink.com/o/abc")
    _validate_share_url("https://www.xiaohongshu.com/discovery/item/abc")

    with pytest.raises(ValueError):
        _validate_share_url("file:///etc/passwd")
    with pytest.raises(ValueError):
        _validate_share_url("https://example.com/xhslink.com/o/abc")


def test_extract_note_id_from_public_url_shapes():
    assert _extract_note_id_from_url("https://www.xiaohongshu.com/explore/abc123?x=1") == "abc123"
    assert _extract_note_id_from_url("https://www.xiaohongshu.com/discovery/item/ABC123") == "ABC123"


def test_extract_share_state_matches_note_id_when_map_key_differs():
    state = {
        "prefixed-abc123": {
            "note": {
                "noteId": "abc123",
                "title": "测试笔记",
                "desc": "描述",
                "imageList": [{"width": 100, "height": 200, "urlDefault": "https://img.example/a.jpg"}],
            },
            "comments": {},
        }
    }

    detail = _extract_feed_detail(FakePage(state), "abc123")

    assert detail.note.note_id == "abc123"
    assert detail.note.body == "公开正文"
    assert detail.note.tags == ["#读书"]
    assert detail.note.image_list[0].url_default == "https://img.example/a.jpg"


def test_xhs_cdn_image_urls_are_upgraded_to_https():
    source = "http://sns-webpic-qc.xhscdn.com/path/to/image"
    assert _normalize_image_url(source) == "https://sns-webpic-qc.xhscdn.com/path/to/image"
    assert _normalize_image_url("http://example.com/image.jpg") == "http://example.com/image.jpg"
