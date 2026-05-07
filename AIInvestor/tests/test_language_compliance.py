"""Tests for the language-compliance detector in persona_engine.

We can't easily test the LLM retry path without hitting the API, but the
detector is pure-function and covers the main bug: 'cached English content
under a ko/ja/zh key' detection on cache read + post-LLM retry trigger.
"""

from __future__ import annotations

from services.persona_engine import _looks_like_english


class TestLooksLikeEnglish:
    """Returns True when content is English even though ko/ja/zh was requested."""

    def test_pure_english(self) -> None:
        assert _looks_like_english(
            "Alphabet operates a dominant digital advertising ecosystem through "
            "Search, YouTube, and Cloud, with additional bets in devices. "
            "The fundamentals show a high-quality growth compounder."
        )

    def test_pure_korean(self) -> None:
        assert not _looks_like_english(
            "알파벳은 검색·광고 시장에서 지배적인 디지털 광고 생태계를 운영하며, "
            "YouTube와 Cloud, 그리고 디바이스와 구독 서비스에 추가 베팅을 하고 있습니다. "
            "ROE 39%, 매출 성장 82%로 우수한 펀더멘털을 보입니다."
        )

    def test_pure_japanese(self) -> None:
        assert not _looks_like_english(
            "アルファベットは検索・広告市場で支配的なデジタル広告エコシステムを"
            "運営しており、YouTubeとCloud、およびデバイスとサブスクリプション"
            "サービスに追加投資しています。"
        )

    def test_pure_chinese(self) -> None:
        assert not _looks_like_english(
            "字母公司在搜索和广告市场运营着主导地位的数字广告生态系统,"
            "通过搜索、YouTube和云,以及在设备和订阅服务上的额外投注。"
        )

    def test_english_body_with_korean_tail(self) -> None:
        """The actual bug case: LLM produces English body and a stripped
        Korean disclaimer remnant. Should still detect as English."""
        mixed = (
            "Alphabet operates a dominant digital advertising ecosystem through "
            "Search, YouTube, and Cloud. The fundamentals show high-quality "
            "growth compounder. ROE 39%, earnings growth 82%. PE 30 suggests "
            "premium price. I'd be inclined to hold given the price near "
            "52-week high. Price surged 30% in one month. "
            "이것은 재정적 조언이 아닙니다."
        )
        assert _looks_like_english(mixed)

    def test_short_text_not_flagged(self) -> None:
        """< 100 ASCII letters is too short to confidently flag — skip."""
        assert not _looks_like_english("Short hi.")

    def test_empty_text(self) -> None:
        assert not _looks_like_english("")
