"""UserProfileRepo behavior — round-trip, idempotency, anon hashing determinism."""

from __future__ import annotations

import os
import tempfile

import pytest

from services.user_profile import UserProfileRepo, make_anon_user_id


@pytest.fixture
def repo(tmp_path):
    return UserProfileRepo(db_path=tmp_path / "test.db", salt="unit-test-salt")


def test_create_then_get(repo):
    profile = repo.get_or_create("tg:1", default_language="ko", default_persona="buffett")
    assert profile.user_key == "tg:1"
    assert profile.persona_key == "buffett"
    assert profile.language == "ko"
    assert profile.intro_seen is False
    assert profile.interest_tags == []
    assert profile.watchlist_tickers == []
    assert profile.onboarding_step == "greeting"
    assert len(profile.anon_user_id) == 16


def test_get_or_create_is_idempotent(repo):
    a = repo.get_or_create("tg:7", default_language="en", default_persona="buffett")
    b = repo.get_or_create("tg:7", default_language="ja", default_persona="dalio")  # ignored once row exists
    assert a.anon_user_id == b.anon_user_id
    assert b.language == "en"           # default ignored
    assert b.persona_key == "buffett"   # default ignored


def test_update_round_trip(repo):
    repo.get_or_create("tg:42", default_language="en", default_persona="buffett")
    updated = repo.update(
        "tg:42",
        persona_key="dalio",
        language="zh",
        intro_seen=True,
        interest_tags=["AI 반도체", "ETF"],
        watchlist_tickers=["NVDA", "TSLA"],
    )
    assert updated.persona_key == "dalio"
    assert updated.language == "zh"
    assert updated.intro_seen is True
    assert updated.interest_tags == ["AI 반도체", "ETF"]
    assert updated.watchlist_tickers == ["NVDA", "TSLA"]

    reread = repo.get("tg:42")
    assert reread.interest_tags == ["AI 반도체", "ETF"]
    assert reread.watchlist_tickers == ["NVDA", "TSLA"]


def test_anon_id_is_deterministic_per_salt():
    a = make_anon_user_id("tg:99", salt="salt-A")
    b = make_anon_user_id("tg:99", salt="salt-A")
    c = make_anon_user_id("tg:99", salt="salt-B")
    assert a == b
    assert a != c
    assert len(a) == 16


def test_get_unknown_raises(repo):
    with pytest.raises(KeyError):
        repo.get("tg:does-not-exist")


def test_update_unknown_raises(repo):
    with pytest.raises(KeyError):
        repo.update("tg:does-not-exist", persona_key="dalio")


def test_delete_removes_row(repo):
    repo.get_or_create("tg:rm", default_language="en", default_persona="buffett")
    assert repo.delete("tg:rm") is True
    assert repo.delete("tg:rm") is False  # already gone
    with pytest.raises(KeyError):
        repo.get("tg:rm")
