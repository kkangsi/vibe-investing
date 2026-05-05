"""Language detection and localized strings.

Telegram delivers the user's UI language in `update.effective_user.language_code`
(e.g. "ko", "en-US", "ja", "zh-Hans"). We support four languages and fall back
to English for everything else. Users can switch via /lang or the inline keyboard.
"""

from __future__ import annotations

from dataclasses import dataclass

SUPPORTED = ("ko", "en", "ja", "zh")
DEFAULT = "en"


def normalize_language(code: str | None) -> str:
    if not code:
        return DEFAULT
    head = code.lower().split("-")[0]
    if head in SUPPORTED:
        return head
    return DEFAULT


@dataclass(frozen=True)
class _Bundle:
    greeting: str
    intro: str
    language_switch_hint: str
    persona_prompt: str
    persona_buffett: str
    persona_dalio: str
    persona_wood: str
    persona_set: str
    report_offer: str
    report_yes: str
    report_skip: str
    interest_prompt: str
    interest_preset_btn: list[tuple[str, str]]
    interest_custom_btn: str
    interest_done_btn: str
    interest_saved: str
    interest_saved_with_tickers: str
    free_query_invite: str
    persona_changed: str
    lang_changed: str
    disclaimer: str
    unknown_input: str
    error_market_data: str
    error_llm: str


_KO = _Bundle(
    greeting="안녕하세요, AI Investor 입니다.",
    intro=(
        "당신만의 투자 멘토 페르소나로 매일 미국 시황(NASDAQ / S&P 500)을 해설해 드립니다.\n\n"
        "• 데이터 출처: Yahoo Finance (yfinance)\n"
        "• AI 모델: DeepSeek\n"
        "• ⚠ 본 챗봇은 실수할 수 있으며, 어떤 응답도 투자 자문이 아닙니다.\n"
        "• ⚠ 모든 투자 판단과 그 결과에 대한 책임은 전적으로 본인에게 있습니다."
    ),
    language_switch_hint=(
        "현재 한국어로 대화 중입니다. 다른 언어로 전환하려면 /lang 을 입력하세요. "
        "(English / 日本語 / 中文 / 한국어 지원)"
    ),
    persona_prompt="투자 멘토 페르소나를 선택해 주세요:",
    persona_buffett="Warren Buffett (장기 가치)",
    persona_dalio="Ray Dalio (매크로/올웨더)",
    persona_wood="Cathie Wood (혁신 성장)",
    persona_set="✓ {persona} 로 설정되었습니다.",
    report_offer="오늘의 시황 리포트가 준비되어 있습니다. 받아보시겠어요?",
    report_yes="예, 보기",
    report_skip="건너뛰기",
    interest_prompt=(
        "주로 어떤 분야나 종목에 투자하시나요?\n"
        "버튼을 눌러 선택하시거나, 자유롭게 입력해 주세요 (예: \"AI 반도체\", \"NVDA TSLA AAPL\")."
    ),
    interest_preset_btn=[
        ("AI 반도체", "interest:ai_chip"),
        ("빅테크", "interest:bigtech"),
        ("배당주", "interest:dividend"),
        ("ETF", "interest:etf"),
        ("BTC 관련주", "interest:btc"),
        ("원자재/에너지", "interest:energy"),
        ("헬스케어", "interest:health"),
    ],
    interest_custom_btn="✏ 직접 입력",
    interest_done_btn="✅ 완료",
    interest_saved="관심 분야를 저장했습니다: {tags}",
    interest_saved_with_tickers="관심 분야를 저장했습니다.\n• 분야: {tags}\n• 종목: {tickers}",
    free_query_invite="궁금한 주식이나 지금 시장 상황이 궁금하세요? 종목 티커나 자유 질문을 보내 주세요.",
    persona_changed="✓ {persona} 로 페르소나가 변경됐습니다.{interests}",
    lang_changed="✓ 언어가 한국어로 변경되었습니다.",
    disclaimer="본 응답은 투자 자문이 아닙니다.",
    unknown_input="이해하지 못했어요. /help 를 입력하시면 명령 목록을 볼 수 있습니다.",
    error_market_data="지금 시장 데이터를 불러오지 못했습니다. 잠시 후 다시 시도해 주세요.",
    error_llm="지금 답변을 생성하지 못했습니다. 잠시 후 다시 시도해 주세요.",
)

_EN = _Bundle(
    greeting="Hello, this is AI Investor.",
    intro=(
        "I explain U.S. market action (NASDAQ / S&P 500) in the voice of a famous investor.\n\n"
        "• Data: Yahoo Finance (yfinance)\n"
        "• AI: DeepSeek\n"
        "• ⚠ This chatbot can make mistakes; nothing it says is financial advice.\n"
        "• ⚠ All investment decisions and their consequences are entirely your own responsibility."
    ),
    language_switch_hint=(
        "Speaking English. To switch, send /lang. "
        "(한국어 / English / 日本語 / 中文 supported)"
    ),
    persona_prompt="Choose your investor persona:",
    persona_buffett="Warren Buffett (long-term value)",
    persona_dalio="Ray Dalio (macro / all-weather)",
    persona_wood="Cathie Wood (disruptive growth)",
    persona_set="✓ Set to {persona}.",
    report_offer="Today's market report is ready. Want to see it?",
    report_yes="Yes, show me",
    report_skip="Skip",
    interest_prompt=(
        "What sectors or tickers do you mainly invest in?\n"
        "Tap presets below or type freely (e.g. \"AI chips\", \"NVDA TSLA AAPL\")."
    ),
    interest_preset_btn=[
        ("AI chips", "interest:ai_chip"),
        ("Big Tech", "interest:bigtech"),
        ("Dividends", "interest:dividend"),
        ("ETF", "interest:etf"),
        ("BTC-linked", "interest:btc"),
        ("Energy", "interest:energy"),
        ("Healthcare", "interest:health"),
    ],
    interest_custom_btn="✏ Type custom",
    interest_done_btn="✅ Done",
    interest_saved="Interests saved: {tags}",
    interest_saved_with_tickers="Interests saved.\n• Sectors: {tags}\n• Tickers: {tickers}",
    free_query_invite="Curious about a specific stock or the market right now? Send a ticker or a question.",
    persona_changed="✓ Persona changed to {persona}.{interests}",
    lang_changed="✓ Language switched to English.",
    disclaimer="This is not financial advice.",
    unknown_input="I didn't catch that. Send /help for commands.",
    error_market_data="I couldn't fetch market data right now. Please try again shortly.",
    error_llm="I couldn't generate a response right now. Please try again shortly.",
)

_JA = _Bundle(
    greeting="こんにちは、AI Investor です。",
    intro=(
        "有名投資家のペルソナで毎日の米国市況（NASDAQ / S&P 500）を解説します。\n\n"
        "• データ: Yahoo Finance (yfinance)\n"
        "• AI: DeepSeek\n"
        "• ⚠ 本チャットボットは誤りを含むことがあり、いかなる応答も投資助言ではありません。\n"
        "• ⚠ すべての投資判断とその結果については、ご自身が全責任を負うものとします。"
    ),
    language_switch_hint=(
        "日本語で対話中です。言語を切り替えるには /lang を送信してください。"
        "（한국어 / English / 日本語 / 中文 対応）"
    ),
    persona_prompt="投資メンターのペルソナを選んでください:",
    persona_buffett="ウォーレン・バフェット (長期バリュー)",
    persona_dalio="レイ・ダリオ (マクロ / オールウェザー)",
    persona_wood="キャシー・ウッド (破壊的成長)",
    persona_set="✓ {persona} に設定しました。",
    report_offer="本日の市況レポートをご用意しています。ご覧になりますか?",
    report_yes="はい、見る",
    report_skip="スキップ",
    interest_prompt=(
        "主にどのセクターや銘柄に投資されていますか?\n"
        "ボタンで選択するか、自由にご入力ください (例: \"AI半導体\", \"NVDA TSLA AAPL\")。"
    ),
    interest_preset_btn=[
        ("AI半導体", "interest:ai_chip"),
        ("ビッグテック", "interest:bigtech"),
        ("配当株", "interest:dividend"),
        ("ETF", "interest:etf"),
        ("BTC関連株", "interest:btc"),
        ("エネルギー", "interest:energy"),
        ("ヘルスケア", "interest:health"),
    ],
    interest_custom_btn="✏ 自由入力",
    interest_done_btn="✅ 完了",
    interest_saved="関心分野を保存しました: {tags}",
    interest_saved_with_tickers="関心分野を保存しました。\n• 分野: {tags}\n• 銘柄: {tickers}",
    free_query_invite="気になる銘柄や市場の状況についてお気軽にどうぞ。ティッカーや質問を送ってください。",
    persona_changed="✓ ペルソナを {persona} に変更しました。{interests}",
    lang_changed="✓ 言語を日本語に切り替えました。",
    disclaimer="本回答は投資助言ではありません。",
    unknown_input="理解できませんでした。/help でコマンド一覧を確認できます。",
    error_market_data="市場データを取得できませんでした。しばらくしてから再度お試しください。",
    error_llm="回答を生成できませんでした。しばらくしてから再度お試しください。",
)

_ZH = _Bundle(
    greeting="您好,我是 AI Investor。",
    intro=(
        "我会以著名投资人的角色解读每日美股(NASDAQ / S&P 500)行情。\n\n"
        "• 数据来源: Yahoo Finance (yfinance)\n"
        "• AI: DeepSeek\n"
        "• ⚠ 本聊天机器人可能出错,所有回复均不构成投资建议。\n"
        "• ⚠ 一切投资决策及其后果由您本人完全自行承担。"
    ),
    language_switch_hint=(
        "当前使用中文对话。如需切换语言,请发送 /lang。"
        "(支持 한국어 / English / 日本語 / 中文)"
    ),
    persona_prompt="请选择您的投资导师人设:",
    persona_buffett="沃伦·巴菲特 (长期价值)",
    persona_dalio="瑞·达利欧 (宏观 / 全天候)",
    persona_wood="凯西·伍德 (颠覆性增长)",
    persona_set="✓ 已设置为 {persona}。",
    report_offer="今日的市场报告已准备好,是否查看?",
    report_yes="好的,查看",
    report_skip="跳过",
    interest_prompt=(
        "您主要投资哪些行业或个股?\n"
        "请点击预设或自由输入(例如 \"AI 芯片\", \"NVDA TSLA AAPL\")。"
    ),
    interest_preset_btn=[
        ("AI 芯片", "interest:ai_chip"),
        ("大型科技", "interest:bigtech"),
        ("股息股", "interest:dividend"),
        ("ETF", "interest:etf"),
        ("BTC 概念", "interest:btc"),
        ("能源", "interest:energy"),
        ("医疗", "interest:health"),
    ],
    interest_custom_btn="✏ 自定义输入",
    interest_done_btn="✅ 完成",
    interest_saved="已保存关注领域: {tags}",
    interest_saved_with_tickers="已保存关注领域。\n• 行业: {tags}\n• 个股: {tickers}",
    free_query_invite="想了解某只股票或当前市场吗?请发送股票代码或自由提问。",
    persona_changed="✓ 已将人设切换为 {persona}。{interests}",
    lang_changed="✓ 语言已切换为中文。",
    disclaimer="本回复不构成投资建议。",
    unknown_input="我没理解。发送 /help 查看命令列表。",
    error_market_data="目前无法获取市场数据,请稍后再试。",
    error_llm="目前无法生成回复,请稍后再试。",
)

_BUNDLES: dict[str, _Bundle] = {"ko": _KO, "en": _EN, "ja": _JA, "zh": _ZH}


def t(lang: str) -> _Bundle:
    return _BUNDLES.get(lang, _EN)


PERSONA_LANGUAGE_INSTRUCTION: dict[str, str] = {
    "ko": "Always respond in Korean (한국어).",
    "en": "Always respond in English.",
    "ja": "Always respond in Japanese (日本語).",
    "zh": "Always respond in Simplified Chinese (简体中文).",
}
