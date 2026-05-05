"""i18n routing + bundle completeness."""

from __future__ import annotations

import dataclasses

import pytest

from services.i18n import SUPPORTED, normalize_language, t


@pytest.mark.parametrize("code,expected", [
    ("ko",       "ko"),
    ("ko-KR",    "ko"),
    ("en",       "en"),
    ("en-US",    "en"),
    ("ja",       "ja"),
    ("ja-JP",    "ja"),
    ("zh",       "zh"),
    ("zh-Hans",  "zh"),
    ("zh-CN",    "zh"),
    ("fr",       "en"),       # unsupported → fallback
    ("",         "en"),       # empty
    (None,       "en"),       # missing
    ("KO",       "ko"),       # case-insensitive
])
def test_normalize_language(code, expected):
    assert normalize_language(code) == expected


def test_supported_set_matches_constant():
    assert set(SUPPORTED) == {"ko", "en", "ja", "zh"}


@pytest.mark.parametrize("lang", ["ko", "en", "ja", "zh"])
def test_bundle_has_all_fields(lang):
    bundle = t(lang)
    # No field may be None or empty (every translation must exist)
    for field in dataclasses.fields(bundle):
        value = getattr(bundle, field.name)
        assert value not in (None, ""), f"{lang} bundle missing field {field.name}"


@pytest.mark.parametrize("lang", ["ko", "en", "ja", "zh"])
def test_disclaimer_strengthened(lang):
    """Both disclaimer lines (chatbot can err / responsibility on user) must be present."""
    intro = t(lang).intro
    assert "⚠" in intro
    # must mention both: chatbot mistakes AND user responsibility
    assert intro.count("⚠") >= 2


@pytest.mark.parametrize("lang", ["ko", "en", "ja", "zh"])
def test_policy_mentions_core_commands(lang):
    """The /policy text must reference /forget so users know how to exercise erasure."""
    body = t(lang).policy
    assert "/forget" in body
    assert "/lang" in body
    assert "/persona" in body
