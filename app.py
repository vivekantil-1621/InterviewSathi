import streamlit as st
import random
import re
import json
import uuid
import requests
from datetime import datetime, timezone

from google import genai
from streamlit_mic_recorder import speech_to_text


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="InterviewSathi | AI Valuation Interview Practice",
    page_icon="🎯",
    layout="wide",
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 3rem;
    }

    /* ---------- BASIC ---------- */

    .main-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 18px;
        color: #666;
        margin-bottom: 25px;
    }

    .question-box {
        padding: 20px;
        border-radius: 12px;
        background: linear-gradient(135deg, #eef4ff, #f5efff);
        border: 1px solid #d9e2ff;
        margin-bottom: 20px;
    }

    .score-box {
        padding: 20px;
        border-radius: 12px;
        background: #f5f5f5;
        margin-top: 15px;
        margin-bottom: 15px;
    }

    .ai-box {
        padding: 20px;
        border-radius: 12px;
        background: linear-gradient(135deg, #f5f8ff, #faf5ff);
        border: 1px solid #d9dfff;
        margin-top: 15px;
        margin-bottom: 15px;
    }

    .small-text {
        color: #666;
        font-size: 14px;
    }

    .interviewer-reaction {
        padding: 12px 16px;
        border-left: 4px solid #6366f1;
        background: #f8fafc;
        border-radius: 10px;
        margin: 10px 0 16px 0;
        color: #334155;
    }

    /* ---------- DASHBOARD ---------- */

    .dashboard-shell {
        max-width: 1250px;
        margin: 0 auto;
    }

    .hero-dashboard {
        background: linear-gradient(135deg, #eef4ff 0%, #f6f0ff 100%);
        border: 1px solid #dfe7f5;
        border-radius: 24px;
        padding: 30px 34px;
        margin-bottom: 22px;
    }

    .hero-kicker {
        color: #6366f1;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: .12em;
    }

    .hero-title {
        color: #111827;
        font-size: 38px;
        line-height: 1.08;
        font-weight: 850;
        margin-top: 5px;
    }

    .hero-subtitle {
        color: #475569;
        font-size: 16px;
        line-height: 1.6;
        margin-top: 10px;
        max-width: 760px;
    }

    .pill-row {
        margin-top: 18px;
    }

    .pill {
        display: inline-block;
        background: white;
        border: 1px solid #dbe3f0;
        border-radius: 999px;
        padding: 7px 12px;
        margin: 3px 5px 3px 0;
        color: #334155;
        font-size: 12px;
        font-weight: 700;
    }

    .section-title {
        color: #0f172a;
        font-size: 23px;
        font-weight: 800;
        margin: 18px 0 5px;
    }

    .section-subtitle {
        color: #64748b;
        font-size: 14px;
        margin-bottom: 14px;
    }

    .metric-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 17px 18px;
        min-height: 105px;
        box-shadow: 0 4px 14px rgba(15, 23, 42, .04);
    }

    .metric-label {
        color: #64748b;
        font-size: 12px;
        font-weight: 700;
    }

    .metric-value {
        color: #111827;
        font-size: 27px;
        font-weight: 850;
        margin-top: 5px;
    }

    .metric-note {
        color: #94a3b8;
        font-size: 11px;
        margin-top: 3px;
    }

    .case-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 20px 22px;
        margin: 12px 0 18px;
        line-height: 1.55;
    }

    .interview-card {
        background: #fff;
        border: 1px solid #e2e8f0;
        border-radius: 18px;
        padding: 19px;
        min-height: 205px;
        box-shadow: 0 4px 14px rgba(15, 23, 42, .04);
    }

    .card-icon {
        width: 42px;
        height: 42px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 12px;
        background: #eef2ff;
        font-size: 21px;
        margin-bottom: 12px;
    }

    .card-title {
        color: #111827;
        font-size: 17px;
        font-weight: 800;
    }

    .card-meta {
        color: #64748b;
        font-size: 12px;
        margin-top: 5px;
    }

    .card-desc {
        color: #475569;
        font-size: 13px;
        line-height: 1.45;
        margin: 12px 0 13px;
    }

    .recent-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 16px;
    }

    .quote-card {
        background: linear-gradient(135deg, #111827, #312e81);
        color: white;
        border-radius: 18px;
        padding: 20px;
        min-height: 140px;
    }

    .quote-text {
        font-size: 16px;
        line-height: 1.55;
        font-weight: 650;
    }

    .quote-small {
        color: #cbd5e1;
        font-size: 12px;
        margin-top: 12px;
    }

    /* ---------- INTERVIEW ROOM ---------- */

    .interview-shell {
        max-width: 1100px;
        margin: 0 auto;
    }

    .interviewer-card {
        background: linear-gradient(135deg, #111827 0%, #1e293b 100%);
        color: white;
        border-radius: 18px;
        padding: 22px 26px;
        margin: 8px 0 18px;
        border: 1px solid #334155;
    }

    .interviewer-avatar {
        display: inline-flex;
        width: 46px;
        height: 46px;
        border-radius: 50%;
        align-items: center;
        justify-content: center;
        background: #334155;
        font-size: 23px;
        margin-right: 12px;
        vertical-align: middle;
    }

    .interviewer-name {
        font-size: 19px;
        font-weight: 750;
    }

    .interviewer-role {
        color: #cbd5e1;
        font-size: 13px;
    }

    .interviewer-note {
        color: #e2e8f0;
        font-size: 15px;
        margin-top: 12px;
        line-height: 1.55;
    }

    .question-card {
        background: linear-gradient(135deg, #eef4ff 0%, #f7f3ff 100%);
        border: 1px solid #dbe4ff;
        border-radius: 18px;
        padding: 24px 26px;
        margin: 12px 0 20px;
    }

    .question-label {
        color: #6366f1;
        font-size: 13px;
        font-weight: 800;
        letter-spacing: .05em;
        text-transform: uppercase;
    }

    .question-text {
        color: #0f172a;
        font-size: 25px;
        line-height: 1.35;
        font-weight: 700;
        margin-top: 8px;
    }

    .reaction-card {
        background: #f8fafc;
        border-left: 4px solid #6366f1;
        border-radius: 10px;
        padding: 14px 18px;
        margin: 15px 0;
    }

    .score-pill {
        font-size: 28px;
        font-weight: 800;
        color: #312e81;
    }

    .final-card {
        background: linear-gradient(135deg, #eef4ff 0%, #faf5ff 100%);
        border: 1px solid #dbe4ff;
        border-radius: 18px;
        padding: 24px;
    }

    .small-muted {
        color: #64748b;
        font-size: 13px;
    }

    /* ---------- SIDEBAR ---------- */

    .sidebar-brand {
        font-size: 22px;
        font-weight: 850;
        color: #172554;
        margin-bottom: 3px;
    }

    .sidebar-tag {
        color: #64748b;
        font-size: 11px;
        line-height: 1.45;
        margin-bottom: 16px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# QUESTION BANK
# =========================================================

QUESTION_BANK = {

    # =====================================================
    # EQUITY VALUATION
    # =====================================================

    "Equity Valuation": {

        "Associate": [

            {
                "question": "What are the three main valuation approaches used to value a business?",
                "keywords": [
                    "income approach",
                    "market approach",
                    "cost approach",
                ],
            },

            {
                "question": "What is the difference between Enterprise Value and Equity Value?",
                "keywords": [
                    "enterprise value",
                    "equity value",
                    "debt",
                    "cash",
                ],
            },

            {
                "question": "What is WACC and why is it used in valuation?",
                "keywords": [
                    "WACC",
                    "cost of debt",
                    "cost of equity",
                    "capital structure",
                ],
            },

            {
                "question": "What is CAPM and how is it used to calculate the cost of equity?",
                "keywords": [
                    "CAPM",
                    "risk free rate",
                    "beta",
                    "equity risk premium",
                ],
            },

            {
                "question": "What is Beta and what does it represent in valuation?",
                "keywords": [
                    "beta",
                    "systematic risk",
                    "market risk",
                ],
            },

            {
                "question": "What is the difference between Equity Risk Premium and Company Specific Risk Premium?",
                "keywords": [
                    "equity risk premium",
                    "company specific risk premium",
                    "CSRP",
                    "risk",
                ],
            },

            {
                "question": "What factors would you consider while selecting comparable companies?",
                "keywords": [
                    "industry",
                    "size",
                    "growth",
                    "profitability",
                    "business model",
                ],
            },

            {
                "question": "What is a precedent transaction analysis?",
                "keywords": [
                    "precedent transactions",
                    "transaction multiples",
                    "acquisition",
                ],
            },

            {
                "question": "What is a terminal value in a DCF valuation?",
                "keywords": [
                    "terminal value",
                    "DCF",
                    "perpetuity",
                    "exit multiple",
                ],
            },

            {
                "question": "What is the difference between an enterprise value multiple and an equity value multiple?",
                "keywords": [
                    "enterprise value",
                    "equity value",
                    "EV EBITDA",
                    "P E",
                ],
            },
        ],

        "Senior Associate": [

            {
                "question": "Walk me through the DCF valuation process from start to finish.",
                "keywords": [
                    "revenue",
                    "EBITDA",
                    "free cash flow",
                    "WACC",
                    "terminal value",
                    "present value",
                ],
            },

            {
                "question": "How would you select an appropriate WACC for a private company?",
                "keywords": [
                    "risk free rate",
                    "beta",
                    "ERP",
                    "size premium",
                    "CSRP",
                    "capital structure",
                ],
            },

            {
                "question": "What factors would cause the WACC of a private company to be different from a public company?",
                "keywords": [
                    "size",
                    "liquidity",
                    "CSRP",
                    "capital structure",
                    "beta",
                ],
            },

            {
                "question": "How would you select an appropriate EBITDA multiple for a company?",
                "keywords": [
                    "growth",
                    "margin",
                    "size",
                    "industry",
                    "risk",
                    "comparable companies",
                ],
            },

            {
                "question": "What are the key differences between the Guideline Public Company method and Precedent Transaction method?",
                "keywords": [
                    "public companies",
                    "transactions",
                    "control premium",
                    "synergies",
                    "multiples",
                ],
            },

            {
                "question": "How would you value a company that has negative EBITDA?",
                "keywords": [
                    "revenue multiple",
                    "DCF",
                    "growth",
                    "business model",
                    "future profitability",
                ],
            },

            {
                "question": "How would you evaluate whether a Company Specific Risk Premium is appropriate?",
                "keywords": [
                    "CSRP",
                    "company specific risk",
                    "size",
                    "customer concentration",
                    "management",
                    "financial performance",
                ],
            },

            {
                "question": "How does an increase in WACC affect the value of a business?",
                "keywords": [
                    "WACC",
                    "discount rate",
                    "present value",
                    "valuation decreases",
                ],
            },

            {
                "question": "How would you perform a sensitivity analysis in a DCF?",
                "keywords": [
                    "WACC",
                    "terminal growth",
                    "sensitivity",
                    "valuation range",
                ],
            },
        ],

        "Assistant Manager": [

            {
                "question": "You are given a private company with limited historical financial information. How would you approach the valuation?",
                "keywords": [
                    "management projections",
                    "historical financials",
                    "comparable companies",
                    "DCF",
                    "market approach",
                    "risk",
                ],
            },

            {
                "question": "A company has significantly higher margins than its peer group. How would you assess whether this should affect the selected valuation multiple?",
                "keywords": [
                    "margin",
                    "peer group",
                    "growth",
                    "multiple",
                    "sustainability",
                ],
            },

            {
                "question": "A company has high customer concentration and dependence on two major customers. How would this affect your valuation?",
                "keywords": [
                    "customer concentration",
                    "risk",
                    "CSRP",
                    "cash flow",
                    "multiple",
                ],
            },

            {
                "question": "How would you determine whether management projections are reasonable for a DCF valuation?",
                "keywords": [
                    "historical performance",
                    "industry growth",
                    "margin",
                    "management assumptions",
                    "market data",
                ],
            },

            {
                "question": "How would you select the appropriate valuation multiple when comparable companies have a wide range of multiples?",
                "keywords": [
                    "growth",
                    "margin",
                    "size",
                    "risk",
                    "median",
                    "comparable companies",
                ],
            },

            {
                "question": "Explain how changes in working capital affect free cash flow in a DCF.",
                "keywords": [
                    "working capital",
                    "cash flow",
                    "increase",
                    "decrease",
                    "free cash flow",
                ],
            },
        ],
    },

    # =====================================================
    # EQUITY ALLOCATION
    # =====================================================

    "Equity Allocation": {

        "Associate": [

            {
                "question": "What is equity allocation and why is it performed?",
                "keywords": [
                    "equity allocation",
                    "capital structure",
                    "common stock",
                    "preferred stock",
                ],
            },

            {
                "question": "What is the Current Value Method?",
                "keywords": [
                    "CVM",
                    "current value",
                    "liquidation",
                    "waterfall",
                ],
            },

            {
                "question": "What is the Option Pricing Method?",
                "keywords": [
                    "OPM",
                    "option",
                    "volatility",
                    "strike price",
                ],
            },

            {
                "question": "When would you use OPM instead of CVM?",
                "keywords": [
                    "OPM",
                    "CVM",
                    "complex capital structure",
                    "future outcomes",
                ],
            },

            {
                "question": "What are liquidation preferences?",
                "keywords": [
                    "liquidation preference",
                    "preferred stock",
                    "priority",
                    "liquidation",
                ],
            },

            {
                "question": "What are conversion rights in preferred stock?",
                "keywords": [
                    "conversion rights",
                    "preferred stock",
                    "common stock",
                ],
            },

            {
                "question": "What is a non-1:1 conversion ratio?",
                "keywords": [
                    "conversion ratio",
                    "preferred stock",
                    "common stock",
                ],
            },
        ],

        "Senior Associate": [

            {
                "question": "Walk me through an OPM allocation for a company with common and preferred shares.",
                "keywords": [
                    "OPM",
                    "breakpoints",
                    "waterfall",
                    "volatility",
                    "time to liquidity",
                ],
            },

            {
                "question": "What are the key inputs required for an OPM?",
                "keywords": [
                    "equity value",
                    "volatility",
                    "risk free rate",
                    "time to liquidity",
                    "strike price",
                ],
            },

            {
                "question": "How does volatility affect the value allocated under OPM?",
                "keywords": [
                    "volatility",
                    "option value",
                    "higher",
                    "value",
                ],
            },

            {
                "question": "How would you handle a preferred stock with a 1.5:1 conversion ratio?",
                "keywords": [
                    "conversion ratio",
                    "1.5",
                    "preferred",
                    "common",
                ],
            },

            {
                "question": "How are employee stock options considered in equity allocation?",
                "keywords": [
                    "stock options",
                    "exercise price",
                    "option",
                    "equity allocation",
                ],
            },
        ],

        "Assistant Manager": [

            {
                "question": "You are given a company with multiple preferred share classes, liquidation preferences, conversion rights and employee options. How would you allocate the equity value?",
                "keywords": [
                    "OPM",
                    "CVM",
                    "waterfall",
                    "liquidation preference",
                    "conversion rights",
                    "options",
                ],
            },

            {
                "question": "How would you determine the breakpoints in an OPM?",
                "keywords": [
                    "breakpoints",
                    "liquidation preference",
                    "conversion",
                    "waterfall",
                ],
            },

            {
                "question": "How would you decide between OPM, PWERM and CVM for an equity allocation?",
                "keywords": [
                    "OPM",
                    "PWERM",
                    "CVM",
                    "scenario",
                    "capital structure",
                ],
            },
        ],
    },

    # =====================================================
    # PPA
    # =====================================================

    "PPA": {

        "Associate": [

            {
                "question": "What is Purchase Price Allocation?",
                "keywords": [
                    "PPA",
                    "purchase price",
                    "assets",
                    "liabilities",
                ],
            },

            {
                "question": "What are the major intangible assets commonly valued in a PPA?",
                "keywords": [
                    "customer relationships",
                    "developed technology",
                    "trade name",
                ],
            },

            {
                "question": "What is the Relief-from-Royalty method?",
                "keywords": [
                    "relief from royalty",
                    "royalty rate",
                    "trade name",
                    "present value",
                ],
            },

            {
                "question": "What is the Multi-Period Excess Earnings Method?",
                "keywords": [
                    "MPEEM",
                    "customer relationships",
                    "excess earnings",
                    "contributory asset charges",
                ],
            },

            {
                "question": "What valuation methods may be used for Developed Technology, and what factors influence the method selection?",
                "keywords": [
                    "developed technology",
                    "relief from royalty",
                    "income approach",
                    "cost approach",
                    "method selection",
                ],
            },
        ],

        "Senior Associate": [

            {
                "question": "Walk me through the valuation of Customer Relationships using MPEEM.",
                "keywords": [
                    "MPEEM",
                    "revenue",
                    "attrition",
                    "contributory asset charges",
                    "present value",
                ],
            },

            {
                "question": "What are contributory asset charges and why are they used in MPEEM?",
                "keywords": [
                    "contributory asset charges",
                    "CAC",
                    "double counting",
                    "customer relationships",
                ],
            },

            {
                "question": "How would you determine the useful life of Customer Relationships?",
                "keywords": [
                    "useful life",
                    "attrition",
                    "customer retention",
                    "economic life",
                ],
            },

            {
                "question": "How would you determine an appropriate royalty rate for a Trade Name?",
                "keywords": [
                    "royalty rate",
                    "comparable agreements",
                    "trade name",
                    "profitability",
                ],
            },

            {
                "question": "What is the With-and-Without Method?",
                "keywords": [
                    "with-and-without",
                    "cash flow",
                    "difference",
                    "intangible asset",
                ],
            },
        ],

        "Assistant Manager": [

            {
                "question": "You are performing a PPA for an acquisition with significant Customer Relationships, Developed Technology and Trade Name. How would you approach the valuation?",
                "keywords": [
                    "customer relationships",
                    "developed technology",
                    "trade name",
                    "MPEEM",
                    "relief from royalty",
                    "useful life",
                ],
            },

            {
                "question": "How would you assess whether the projected attrition rate for Customer Relationships is reasonable?",
                "keywords": [
                    "attrition",
                    "historical",
                    "customer retention",
                    "industry",
                    "benchmark",
                ],
            },

            {
                "question": "What factors would you consider when selecting the useful life of Developed Technology?",
                "keywords": [
                    "useful life",
                    "technology",
                    "obsolescence",
                    "replacement",
                    "economic life",
                ],
            },

            {
                "question": "How would you perform a valuation of a Trade Name using the Relief-from-Royalty method?",
                "keywords": [
                    "relief from royalty",
                    "royalty rate",
                    "revenue",
                    "tax",
                    "present value",
                ],
            },
        ],
    },

    # =====================================================
    # CASE STUDIES
    # =====================================================

    "Case Studies": {

        "Associate": [

            {
                "question": "A company has $20 million of revenue and $4 million of EBITDA. How would you approach valuing the company?",
                "keywords": [
                    "EBITDA",
                    "multiple",
                    "comparable companies",
                    "enterprise value",
                    "market approach",
                ],
            },

            {
                "question": "You are given a startup with limited historical financial information. What information would you request from management before starting the valuation?",
                "keywords": [
                    "financial statements",
                    "projections",
                    "cap table",
                    "business plan",
                    "revenue",
                ],
            },

            {
                "question": "A company has three classes of shares with different rights. Which equity allocation method would you consider?",
                "keywords": [
                    "OPM",
                    "CVM",
                    "liquidation preference",
                    "conversion rights",
                ],
            },
        ],

        "Senior Associate": [

            {
                "question": "A fund has 30 portfolio investments and asks you to perform a valuation of the entire portfolio. Walk me through your process from start to finish.",
                "keywords": [
                    "portfolio",
                    "data request",
                    "valuation methodology",
                    "review",
                    "quality control",
                    "reporting",
                ],
            },

            {
                "question": "You are valuing a startup with no meaningful historical earnings. What information would you request and which valuation approach would you consider?",
                "keywords": [
                    "projections",
                    "cap table",
                    "funding",
                    "revenue",
                    "DCF",
                    "market approach",
                ],
            },

            {
                "question": "How would you select the appropriate GPC multiple for a private company when the comparable companies have different growth rates and margins?",
                "keywords": [
                    "GPC",
                    "growth",
                    "margin",
                    "multiple",
                    "comparable",
                ],
            },

            {
                "question": "How would you determine an appropriate venture capital rate of return for a startup valuation?",
                "keywords": [
                    "venture capital",
                    "rate of return",
                    "risk",
                    "stage",
                    "expected return",
                ],
            },
        ],

        "Assistant Manager": [

            {
                "question": "A portfolio contains 30 investments across different industries and stages. You are responsible for the entire valuation engagement. How would you manage the engagement from data collection through final reporting?",
                "keywords": [
                    "portfolio",
                    "data collection",
                    "methodology",
                    "team",
                    "review",
                    "quality control",
                    "reporting",
                ],
            },

            {
                "question": "A startup valuation uses PWERM with three scenarios: IPO 30%, Acquisition 50% and Downside 20%. The valuation date is December 31, 2025 and the expected exit is two years later. Walk me through the valuation.",
                "keywords": [
                    "PWERM",
                    "IPO",
                    "acquisition",
                    "downside",
                    "probability",
                    "discount rate",
                    "two years",
                ],
            },

            {
                "question": "A private company has a wide range of GPC multiples. What factors would you consider before selecting the final multiple?",
                "keywords": [
                    "GPC",
                    "growth",
                    "margin",
                    "size",
                    "risk",
                    "business model",
                ],
            },

            {
                "question": "You are asked to value a startup using a Venture Capital Method. Walk me through the key steps and assumptions.",
                "keywords": [
                    "venture capital method",
                    "exit value",
                    "exit multiple",
                    "rate of return",
                    "present value",
                ],
            },
        ],
    },
}


# =========================================================
# ALIASES FOR CONCEPT MATCHING
# =========================================================

ALIASES = {

    "income approach": [
        "income approach",
        "income method",
    ],

    "market approach": [
        "market approach",
        "market method",
    ],

    "cost approach": [
        "cost approach",
        "cost method",
    ],

    "company specific risk premium": [
        "company specific risk premium",
        "company-specific risk premium",
        "csrp",
    ],

    "equity risk premium": [
        "equity risk premium",
        "erp",
    ],

    "risk free rate": [
        "risk free rate",
        "risk-free rate",
        "riskfree rate",
    ],

    "customer relationships": [
        "customer relationships",
        "customer relationship",
    ],

    "developed technology": [
        "developed technology",
        "technology",
    ],

    "trade name": [
        "trade name",
        "tradename",
    ],

    "relief from royalty": [
        "relief from royalty",
        "relief-from-royalty",
    ],

    "contributory asset charges": [
        "contributory asset charges",
        "contributory asset charge",
        "cac",
    ],

    "liquidation preference": [
        "liquidation preference",
        "liquidation preferences",
    ],

    "conversion rights": [
        "conversion rights",
        "conversion right",
    ],

    "OPM": [
        "opm",
        "option pricing method",
    ],

    "CVM": [
        "cvm",
        "current value method",
    ],

    "PWERM": [
        "pwerm",
        "probability weighted expected return method",
    ],
}


# =========================================================
# RULE-BASED CONCEPT MATCHING
# =========================================================

def concept_found(answer, keyword):

    answer_lower = answer.lower()

    if keyword.lower() in answer_lower:
        return True

    if keyword in ALIASES:

        for alias in ALIASES[keyword]:

            if alias.lower() in answer_lower:
                return True

    return False


# =========================================================
# RULE-BASED EVALUATION
# =========================================================

def evaluate_answer(question_data, answer):

    answer = answer.strip()

    if not answer:

        return {
            "score": 0,
            "feedback": "No answer provided.",
            "matched_keywords": [],
            "missing_keywords": question_data["keywords"],
            "improvement": "Provide a structured technical answer.",
            "length_feedback": "No answer provided.",
        }

    keywords = question_data["keywords"]

    matched = []
    missing = []

    for keyword in keywords:

        if concept_found(answer, keyword):
            matched.append(keyword)

        else:
            missing.append(keyword)

    keyword_score = (
        len(matched) / len(keywords)
        if keywords
        else 0
    )

    word_count = len(answer.split())

    length_score = min(
        word_count / 100,
        1,
    )

    structure_score = 1 if (
        "." in answer
        or "\n" in answer
        or word_count >= 40
    ) else 0.5

    final_score = (
        keyword_score * 7
        + length_score * 2
        + structure_score
    )

    final_score = round(
        min(final_score, 10),
        1,
    )

    # Feedback must point to actual concepts found/missed, never praise generically.
    matched_text = ", ".join(matched[:4]) if matched else "no key concepts clearly demonstrated"
    missing_text = ", ".join(missing[:5]) if missing else "no major keyword gaps identified by the basic checker"

    if final_score >= 8.5:
        feedback = (
            f"Strong coverage of {matched_text}. Check the technical details below "
            "for any remaining nuance; the keyword check alone cannot confirm full accuracy."
        )
        improvement = (
            f"To strengthen the answer further, explicitly address any relevant gaps such as: {missing_text}. "
            "Use a brief explanation or example where useful."
        )
    elif final_score >= 7:
        feedback = (
            f"You addressed {matched_text}, but the answer may not fully cover the question. "
            f"Concepts to verify or add: {missing_text}."
        )
        improvement = (
            f"Explain the missing or underdeveloped concepts—especially {missing_text}—and connect them "
            "to the valuation question rather than listing terms."
        )
    elif final_score >= 5.5:
        feedback = (
            f"The answer demonstrates some relevant understanding ({matched_text}), "
            f"but important areas may be absent: {missing_text}."
        )
        improvement = (
            f"Rebuild the answer around the core definition, method and assumptions. "
            f"Then address: {missing_text}."
        )
    elif final_score >= 4:
        feedback = (
            f"Only partial coverage was detected ({matched_text}). "
            f"The main gaps to review are: {missing_text}."
        )
        improvement = (
            f"Start with a precise definition, explain the key steps, and cover {missing_text}. "
            "Add a practical valuation example if appropriate."
        )
    else:
        feedback = (
            f"The response does not yet demonstrate the core concepts clearly. "
            f"Review these areas first: {missing_text}."
        )
        improvement = (
            f"Give a direct definition, explain the methodology in sequence, and then apply it. "
            f"Begin by learning: {missing_text}."
        )

    if word_count < 25:

        length_feedback = (
            "Answer is quite short. Try explaining the concept "
            "with a little more technical depth."
        )

    elif word_count < 50:

        length_feedback = (
            "Answer has reasonable length but could use "
            "additional supporting details."
        )

    else:

        length_feedback = "Answer has sufficient detail."

    return {
        "score": final_score,
        "feedback": feedback,
        "matched_keywords": matched,
        "missing_keywords": missing,
        "improvement": improvement,
        "length_feedback": length_feedback,
    }


# =========================================================
# AI INTERVIEW EVALUATION
# =========================================================

def evaluate_with_gemini(
    question,
    answer,
    level,
    area,
    rule_score,
    next_topic=None,
):

    try:

        client = genai.Client()

        prompt = f"""
You are a senior valuation professional conducting a technical
interview for a valuation professional.

Evaluate the candidate's answer based on its ACTUAL MEANING,
not simply on keyword matching.

Interview Area:
{area}

Candidate Level:
{level}

Interview Question:
{question}

Candidate Answer:
{answer}

Existing rule-based score (a rough signal only; do not copy it blindly):
{rule_score}/10

NON-NEGOTIABLE: SPECIFIC, EVIDENCE-BASED FEEDBACK
- Do not use generic praise such as "Excellent answer", "Strong answer", "Good understanding" or "covered the major concepts" unless immediately supported by specific evidence from this answer.
- Never repeat the same sentence in interviewer_reaction and overall_feedback. These fields have different jobs.
- Identify what the candidate actually explained correctly, what is missing, and any technical error or imprecision. Quote or paraphrase the relevant part of the candidate's answer when useful.
- Treat the question as the grading rubric: identify 2-5 essential concepts a competent answer to THIS question should cover, then compare the response with those concepts. Do not rely on the broad topic list or the rule-based score as the rubric.
- If the answer is vague, say exactly what is vague and what detail should have been provided. If it is wrong, explain the correction. If it is genuinely complete, explain specifically why and identify only meaningful refinements. Do not invent gaps.
- areas_to_improve must contain concrete, question-specific omissions, weak explanations, or corrections—not generic advice like "add more detail". If there are no material gaps, state that clearly and provide one useful refinement.
- strengths must refer to specific content actually present in the answer. Never fill the list with generic compliments.
- overall_feedback: 2-4 sentences, including at least one specific strength or gap and the reason it matters.
- technical_accuracy: explicitly classify the answer as accurate, partly accurate, inaccurate, or too vague to assess, and explain why.
- how_to_improve: tell the candidate what to say/add next time, using the actual topic and gaps.
- interviewer_reaction: one short natural spoken sentence only; acknowledge a specific point or ask/probe the relevant gap. Do not give a second overall assessment here.
- If the candidate gives a very short answer, do not assume understanding they have not demonstrated. Score only demonstrated knowledge.

IMPORTANT EVALUATION PRINCIPLES:

Evaluate the candidate according to the expected knowledge
for their stated level.

Do NOT require every possible technical detail.

For an Associate, focus primarily on strong fundamentals,
correct definitions, basic methodology and logical understanding.

For a Senior Associate, expect deeper technical knowledge,
practical application and reasonable judgment.

For an Assistant Manager, expect technical depth,
structured thinking, judgment and practical engagement experience.

Distinguish between:

Required concepts

Useful additional depth

Advanced technical details

Do NOT penalize a candidate heavily for omitting an advanced
detail when the core answer is technically correct.

For example, when discussing Enterprise Value versus Equity
Value, an Associate can reasonably explain the basic bridge
using debt and cash. Preferred stock, minority interest and
other detailed bridge adjustments may be treated as additional
depth rather than mandatory omissions unless the question
specifically requires a detailed bridge.

Do NOT give credit simply because a keyword appears.
Judge whether the candidate demonstrates the concept correctly.

Do not invent errors that are not actually present.

Prefer practical valuation interview expectations over
unnecessarily textbook-heavy answers.

Evaluate the answer on:

Technical accuracy

Completeness

Understanding of valuation concepts

Practical application

Logical reasoning

Interview communication

Appropriateness for the candidate's experience level

Important valuation concepts may include:

Business Valuation
Income Approach
Market Approach
Cost Approach
DCF
Guideline Public Companies
Precedent Transactions
WACC
CAPM
Beta
Risk Free Rate
Equity Risk Premium
Size Premium
Company Specific Risk Premium
Enterprise Value
Equity Value
Equity Allocation
CVM
OPM
PWERM
Liquidation Preferences
Conversion Rights
Stock Options
Purchase Price Allocation
ASC 805
Customer Relationships
Developed Technology
Trade Name
MPEEM
Relief-from-Royalty
Contributory Asset Charges
Portfolio Valuation
Venture Capital Method

The score must be from 0 to 10.

INTERVIEW FLOW:

This is a connected interview, not a random quiz.

Listen to the candidate's response and make the next question
feel like a natural interviewer follow-up.

Next topic that must be covered (if provided):
{next_topic if next_topic else "No next question"}

If a next topic is provided, also create:

interviewer_reaction:
one short, natural sentence reacting to the candidate's answer.

next_question:
ONE concise technical question on the specified next topic.

Use something from the candidate's answer in the wording when useful.

If the answer is weak, probe the relevant gap, but stay on the
specified next topic.

Do not jump to a later topic.

Do not ask a generic "tell me more" question.

If no next topic is provided, return an empty next_question.

For an Associate, expect strong fundamentals.

For a Senior Associate, expect deeper technical understanding
and practical application.

For an Assistant Manager, expect structured thinking,
technical depth, judgment and practical engagement experience.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "score": 0,
    "overall_feedback": "",
    "technical_accuracy": "",
    "strengths": [],
    "areas_to_improve": [],
    "how_to_improve": "",
    "model_answer": "",
    "interviewer_reaction": "",
    "next_question": ""
}}

Requirements:

score must be a number between 0 and 10

overall_feedback must be specific to this exact question and answer, not generic praise

technical_accuracy must classify correctness and explain the evidence

strengths should contain 1 to 3 concise points grounded in the candidate's actual answer

areas_to_improve should contain 1 to 4 specific gaps/corrections grounded in the question; do not invent gaps

how_to_improve should provide practical interview advice

model_answer should be a professional answer that the candidate could give
in an interview

The model answer should be technically accurate

Do not make the model answer unnecessarily long

Do not mention the underlying evaluation technology

Do not mention any AI model, provider, API or software name
"""

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )

        raw_text = response.text.strip()

        raw_text = re.sub(
            r"^```json\s*",
            "",
            raw_text,
            flags=re.IGNORECASE,
        )

        raw_text = re.sub(
            r"^```\s*",
            "",
            raw_text,
        )

        raw_text = re.sub(
            r"\s*```$",
            "",
            raw_text,
        )

        result = json.loads(raw_text)

        if "score" not in result:
            return None

        try:
            result["score"] = float(
                result["score"]
            )

        except Exception:
            return None

        result["score"] = round(
            max(
                0,
                min(
                    10,
                    result["score"],
                ),
            ),
            1,
        )

        return result

    except Exception as e:

        print(
            "AI evaluation error:",
            str(e),
        )

        return None


# =========================================================
# INTERVIEW SCENARIOS
# =========================================================

INTERVIEW_SCENARIOS = {

    "Equity Valuation — Fundamentals": {

        "area": "Equity Valuation",
        "level": "Associate",
        "interviewer": "Sarah",
        "interviewer_title": "Senior Valuation Manager",

        "intro": (
            "You are interviewing for a valuation role. We will start "
            "with fundamentals and gradually move into practical "
            "valuation judgment."
        ),

        "questions": [1, 9, 2, 5, 6],

        "topics": [
            "valuation approaches",
            "Enterprise Value versus Equity Value",
            "enterprise value multiples versus equity value multiples",
            "WACC and why it is used",
            "Equity Risk Premium versus Company Specific Risk Premium",
        ],
    },

    "Equity Valuation — Private Company": {

        "area": "Equity Valuation",
        "level": "Senior Associate",
        "interviewer": "Sarah",
        "interviewer_title": "Senior Valuation Manager",

        "intro": (
            "Let's discuss a private company valuation. I will start "
            "with methodology and then probe your assumptions and judgment."
        ),

        "questions": [0, 1, 2, 3, 6],

        "topics": [
            "DCF process",
            "private-company WACC",
            "WACC risk differences",
            "EBITDA multiple selection",
            "Company Specific Risk Premium",
        ],
    },

    "Equity Valuation — Manager Case": {

        "area": "Equity Valuation",
        "level": "Assistant Manager",
        "interviewer": "David",
        "interviewer_title": "Valuation Director",

        "intro": (
            "Assume you are leading a private-company valuation with "
            "limited information. I am interested in how you structure "
            "the problem and defend your judgment."
        ),

        "questions": [0, 1, 2, 3, 4],

        "topics": [
            "private-company valuation approach",
            "margin versus peers",
            "customer concentration and valuation risk",
            "management projections",
            "selecting a multiple from a wide comparable range",
        ],
    },

    "Equity Allocation — Capital Structure": {

        "area": "Equity Allocation",
        "level": "Senior Associate",
        "interviewer": "Michael",
        "interviewer_title": "Valuation Director",

        "intro": (
            "We are valuing a company with preferred and common equity. "
            "We will move from the allocation framework into OPM assumptions "
            "and conversion rights."
        ),

        "questions": [0, 1, 3, 4, 2],

        "topics": [
            "OPM allocation",
            "OPM inputs",
            "conversion ratios",
            "employee stock options",
            "OPM versus CVM and PWERM",
        ],
    },

    "PPA — Intangible Assets": {

        "area": "PPA",
        "level": "Senior Associate",
        "interviewer": "Priya",
        "interviewer_title": "PPA Senior Manager",

        "intro": (
            "Assume we have completed an acquisition and identified "
            "Customer Relationships, Developed Technology and Trade Name. "
            "Let's work through the valuation logic."
        ),

        "questions": [0, 1, 2, 3, 4],

        "topics": [
            "PPA fundamentals",
            "major intangible assets",
            "Relief-from-Royalty",
            "MPEEM",
            "With-and-Without Method",
        ],
    },

    "PPA — Acquisition Case": {

        "area": "PPA",
        "level": "Assistant Manager",
        "interviewer": "Priya",
        "interviewer_title": "PPA Senior Manager",

        "intro": (
            "You are leading the PPA for an acquisition with significant "
            "intangible assets. I will test both methodology and the "
            "assumptions behind your valuation."
        ),

        "questions": [0, 1, 2, 3],

        "topics": [
            "PPA acquisition approach",
            "customer relationship attrition",
            "developed technology useful life",
            "Trade Name Relief-from-Royalty valuation",
        ],
    },

    "Portfolio Valuation — Senior": {

        "area": "Case Studies",
        "level": "Senior Associate",
        "interviewer": "Alex",
        "interviewer_title": "Portfolio Valuation Director",

        "intro": (
            "You have been asked to support a portfolio valuation engagement. "
            "We will move from engagement planning into individual valuation "
            "judgments."
        ),

        "questions": [0, 1, 2, 3],

        "topics": [
            "portfolio valuation engagement process",
            "startup information and valuation approach",
            "GPC multiple selection",
            "venture capital rate of return",
        ],
    },

    "Startup Valuation — Manager Case": {

        "area": "Case Studies",
        "level": "Assistant Manager",
        "interviewer": "Alex",
        "interviewer_title": "Portfolio Valuation Director",

        "intro": (
            "Let's work through a startup valuation where historical "
            "earnings are limited and multiple future outcomes are possible."
        ),

        "questions": [1, 3, 2, 0],

        "topics": [
            "startup information request",
            "venture capital method",
            "GPC multiple selection",
            "basic business valuation approach",
        ],
    },
}


def get_scenario_questions(scenario_name):

    scenario = INTERVIEW_SCENARIOS[
        scenario_name
    ]

    bank_questions = QUESTION_BANK[
        scenario["area"]
    ][
        scenario["level"]
    ]

    questions = []

    topics = scenario.get(
        "topics",
        [],
    )

    for pos, bank_index in enumerate(
        scenario["questions"]
    ):

        if bank_index < len(bank_questions):

            q = dict(
                bank_questions[bank_index]
            )

            q["topic"] = (
                topics[pos]
                if pos < len(topics)
                else "technical valuation"
            )

            q["base_question"] = q["question"]

            questions.append(q)

    return questions


# =========================================================
# ANONYMOUS USAGE TRACKING
# =========================================================
# Configure SUPABASE_URL and SUPABASE_KEY in Streamlit Secrets.
# For a private admin dashboard, use a server-side secret/service-role key
# stored only in Streamlit Secrets, never in client-side code or GitHub.

SUPABASE_URL = ""
SUPABASE_KEY = ""

try:
    SUPABASE_URL = str(st.secrets.get("SUPABASE_URL", "")).strip().rstrip("/")
    SUPABASE_KEY = str(st.secrets.get("SUPABASE_KEY", "")).strip()
except Exception:
    pass

SUPABASE_TABLE = "usage_events"


def get_visitor_id():
    """A session identifier, not a guaranteed cross-session person identifier."""
    if "visitor_id" not in st.session_state:
        st.session_state.visitor_id = str(uuid.uuid4())
    return st.session_state.visitor_id


def supabase_headers(return_rows=False):
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
    }
    headers["Prefer"] = "return=representation" if return_rows else "return=minimal"
    return headers


def supabase_configured():
    return bool(SUPABASE_URL and SUPABASE_KEY)


def track_event(event_name, **details):
    """Write one event. Failure is non-fatal but retained for admin diagnostics."""
    if not supabase_configured():
        st.session_state["analytics_last_write_error"] = "Supabase is not configured"
        return False

    row = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "visitor_id": get_visitor_id(),
        "event": str(event_name),
        "interview_id": details.get("interview_id") or st.session_state.get("interview_id"),
        "scenario": details.get("scenario"),
        "area": details.get("area"),
        "level": details.get("level"),
        "questions": details.get("questions", details.get("questions_total")),
        "question_number": details.get("question_number"),
    }
    try:
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}",
            headers=supabase_headers(),
            json=row,
            timeout=8,
        )
       if not response.ok:
    raise RuntimeError(
        f"Supabase HTTP {response.status_code}: {response.text}"
    )


def get_usage_events(limit=10000):
    """Fetch most recent rows first; return (rows, error, truncated_possible)."""
    if not supabase_configured():
        return [], "Supabase URL/key missing in Streamlit Secrets", False
    try:
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
            },
            params={
                "select": "id,timestamp_utc,visitor_id,event,interview_id,scenario,area,level,questions,question_number",
                "order": "timestamp_utc.desc",
                "limit": str(limit),
            },
            timeout=12,
        )
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, list):
            return [], "Supabase returned an unexpected response format", False
        return data, "", len(data) >= limit
    except Exception as exc:
        return [], f"{type(exc).__name__}: {exc}", False


def track_interview_started():
    # Each attempt gets a stable ID, allowing start/completion counts to be paired.
    if not st.session_state.get("interview_id"):
        st.session_state.interview_id = str(uuid.uuid4())
    return track_event(
        "interview_started",
        interview_id=st.session_state.interview_id,
        scenario=st.session_state.get("selected_scenario"),
        area=st.session_state.get("selected_area"),
        level=st.session_state.get("selected_level"),
        questions=st.session_state.get("number_of_questions"),
    )


get_visitor_id()


# =========================================================
# SESSION STATE
# =========================================================

defaults = {

    "interview_started": False,

    "interview_completed": False,

    "selected_questions": [],

    "current_index": 0,

    "answers": {},

    "evaluations": {},

    "answer_submitted": False,

    "selected_area": "Equity Valuation",

    "selected_level": "Associate",

    "number_of_questions": 5,

    "voice_text_box_version": {},

    "selected_scenario": (
        "Equity Valuation — Fundamentals"
    ),

    "page": "Home",

    "history": [],

    "usage_started_tracked": False,

    "usage_completed_tracked": False,

    "interview_id": None,

    "interviewer_reaction": "",
}


for key, value in defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value


# =========================================================
# TRACK ONE APP-OPEN EVENT PER SESSION
# =========================================================

if not st.session_state.usage_started_tracked:
    # Only mark the event as tracked after Supabase confirms the insert.
    # If configuration/schema/permissions are wrong, the next rerun can retry.
    st.session_state.usage_started_tracked = bool(track_event("app_opened"))


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

with st.sidebar:

    st.html(
        '<div class="sidebar-brand">🎯 InterviewSathi</div>'
    )

    st.html(
        """
        <div class="sidebar-tag">
            Better Practice.<br>
            Stronger Interviews.<br>
            Bigger Opportunities.
        </div>
        """
    )

    page = st.radio(
        "",
        [
            "Home",
            "Interviews",
            "Performance",
            "Analytics",
            "Settings",
        ],
        index=[
            "Home",
            "Interviews",
            "Performance",
            "Analytics",
            "Settings",
        ].index(
            st.session_state.page
        ),
        label_visibility="collapsed",
    )

    st.session_state.page = page

    st.divider()

    st.caption(
        "AI-style technical valuation practice"
    )


# =========================================================
# KEEP ACTIVE INTERVIEW IN INTERVIEW ROOM
# =========================================================

if st.session_state.interview_started:

    st.session_state.page = "Interviews"

    page = "Interviews"


scenario_names = list(
    INTERVIEW_SCENARIOS.keys()
)


# =========================================================
# HOME DASHBOARD
# =========================================================

if (
    page == "Home"
    and not st.session_state.interview_started
):

    history = st.session_state.history

    completed = len(history)

    avg_score = (
        round(
            sum(
                x["score"]
                for x in history
            ) / completed,
            1,
        )
        if completed
        else 0
    )

    st.html(
        '<div class="dashboard-shell">'
    )

    # -----------------------------------------------------
    # HERO
    # -----------------------------------------------------

    st.html(
        """
        <div class="hero-dashboard">

            <div class="hero-kicker">
                YOUR VALUATION INTERVIEW PARTNER
            </div>

            <div class="hero-title">
                Practice like it’s a real interview.
            </div>

            <div class="hero-subtitle">
                InterviewSathi turns valuation preparation into a
                connected technical interview — not a random list
                of questions. Answer, think, get feedback, and move
                to the next level.
            </div>

            <div class="pill-row">
                <span class="pill">Equity Valuation</span>
                <span class="pill">Equity Allocation</span>
                <span class="pill">PPA</span>
                <span class="pill">Case Studies</span>
            </div>

        </div>
        """
    )

    st.html(
        '<div class="section-title">Your Progress</div>'
    )

    st.html(
        '<div class="section-subtitle">Your interview practice at a glance.</div>'
    )

    m1, m2, m3, m4 = st.columns(4)

    with m1:

        st.html(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    TOTAL INTERVIEWS
                </div>

                <div class="metric-value">
                    {completed}
                </div>

                <div class="metric-note">
                    Completed sessions
                </div>

            </div>
            """
        )

    with m2:

        st.html(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    AVERAGE SCORE
                </div>

                <div class="metric-value">
                    {avg_score}/10
                </div>

                <div class="metric-note">
                    Across completed interviews
                </div>

            </div>
            """
        )

    with m3:

        st.html(
            """
            <div class="metric-card">

                <div class="metric-label">
                    TOPIC AREAS
                </div>

                <div class="metric-value">
                    4
                </div>

                <div class="metric-note">
                    Core valuation areas
                </div>

            </div>
            """
        )

    with m4:

        strong = sum(
            1
            for x in history
            if x["score"] >= 7
        )

        st.html(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    STRONG SESSIONS
                </div>

                <div class="metric-value">
                    {strong}
                </div>

                <div class="metric-note">
                    Score ≥ 7/10
                </div>

            </div>
            """
        )

    st.html(
        '<div class="section-title">Start Your Interview</div>'
    )

    st.html(
        '<div class="section-subtitle">Choose an interview that matches your preparation goal.</div>'
    )

    cards = [

        (
            "📊",
            "Equity Valuation — Fundamentals",
            "Associate",
            "Start with EV vs Equity Value, multiples, WACC and CSRP.",
        ),

        (
            "🏢",
            "Equity Valuation — Private Company",
            "Senior Associate",
            "Move from methodology into private-company assumptions and judgment.",
        ),

        (
            "🧩",
            "Equity Allocation — Capital Structure",
            "Senior Associate",
            "Work through OPM, conversion rights, options and allocation logic.",
        ),

        (
            "🧾",
            "PPA — Intangible Assets",
            "Senior Associate",
            "Discuss Customer Relationships, Developed Technology and Trade Name.",
        ),

        (
            "📁",
            "Case Studies — Portfolio",
            "Senior Associate",
            "Work through a 30-investment portfolio and valuation judgments.",
        ),

        (
            "🚀",
            "Case Studies — Startup",
            "Assistant Manager",
            "Handle startup valuation, VC method and scenario-based thinking.",
        ),
    ]

    for row_start in range(
        0,
        len(cards),
        3,
    ):

        cols = st.columns(3)

        for col, (
            icon,
            title,
            level,
            desc,
        ) in zip(
            cols,
            cards[
                row_start:row_start + 3
            ],
        ):

            with col:

                st.html(
                    f"""
                    <div class="interview-card">

                        <div class="card-icon">
                            {icon}
                        </div>

                        <div class="card-title">
                            {title}
                        </div>

                        <div class="card-meta">
                            {level} · Connected interview
                        </div>

                        <div class="card-desc">
                            {desc}
                        </div>

                    </div>
                    """
                )

                if st.button(
                    "Start Interview →",
                    key=f"home_start_{title}",
                    use_container_width=True,
                    type="primary",
                ):

                    scenario_key = title

                    if title == "Case Studies — Portfolio":

                        scenario_key = (
                            "Portfolio Valuation — Senior"
                        )

                    if title == "Case Studies — Startup":

                        scenario_key = (
                            "Startup Valuation — Manager Case"
                        )

                    st.session_state.selected_scenario = (
                        scenario_key
                    )

                    scenario = INTERVIEW_SCENARIOS[
                        scenario_key
                    ]

                    st.session_state.selected_area = (
                        scenario["area"]
                    )

                    st.session_state.selected_level = (
                        scenario["level"]
                    )

                    selected_questions = (
                        get_scenario_questions(
                            scenario_key
                        )
                    )

                    st.session_state.number_of_questions = (
                        len(selected_questions)
                    )

                    st.session_state.selected_questions = (
                        selected_questions
                    )

                    st.session_state.current_index = 0

                    st.session_state.answers = {}

                    st.session_state.evaluations = {}

                    st.session_state.answer_submitted = False

                    st.session_state.interviewer_reaction = ""

                    st.session_state.interview_id = str(uuid.uuid4())

                    st.session_state.interview_started = True

                    st.session_state.interview_completed = False

                    st.session_state.usage_completed_tracked = False

                    st.session_state.voice_text_box_version = {}

                    st.session_state.page = "Interviews"

                    track_interview_started()

                    st.rerun()

    left, right = st.columns(
        [1.2, 1]
    )

    with left:

        st.html(
            '<div class="section-title">Recent Activity</div>'
        )

        if history:

            st.html(
                '<div class="recent-card">'
            )

            for item in history[-5:][::-1]:

                st.write(
                    f"**{item['scenario']}** · "
                    f"{item['score']}/10 · "
                    f"{item['questions']} questions"
                )

            st.html(
                '</div>'
            )

        else:

            st.info(
                "Your completed interviews will appear here."
            )

    with right:

        st.html(
            '<div class="section-title">Keep Going</div>'
        )

        st.html(
            """
            <div class="quote-card">

                <div class="quote-text">
                    “A strong valuation interview is not about
                    memorising formulas. It is about explaining
                    why your approach makes sense.”
                </div>

                <div class="quote-small">
                    InterviewSathi · Technical Practice
                </div>

            </div>
            """
        )

    st.html(
        '</div>'
    )


# =========================================================
# INTERVIEWS PAGE — SELECT INTERVIEW
# =========================================================

elif (
    page == "Interviews"
    and not st.session_state.interview_started
):

    st.html(
        '<div class="dashboard-shell">'
    )

    st.html(
        '<div class="section-title">Interviews</div>'
    )

    st.html(
        '<div class="section-subtitle">Pick a connected technical interview. The next question reacts to your previous answer.</div>'
    )

    selected_scenario = st.selectbox(
        "Interview Type",
        scenario_names,
        index=(
            scenario_names.index(
                st.session_state.selected_scenario
            )
            if st.session_state.selected_scenario
            in scenario_names
            else 0
        ),
    )

    scenario = INTERVIEW_SCENARIOS[
        selected_scenario
    ]

    scenario_questions = get_scenario_questions(
        selected_scenario
    )

    q_count = len(
        scenario_questions
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Area",
            scenario["area"],
        )

    with c2:

        st.metric(
            "Level",
            scenario["level"],
        )

    with c3:

        st.metric(
            "Questions",
            q_count,
        )

    st.html(
        f"""
        <div class="case-card">

            <b>👤 {scenario["interviewer"]}</b>
            · {scenario["interviewer_title"]}

            <br><br>

            {scenario["intro"]}

            <br><br>

            <span class="small-muted">
                Connected sequence:
                {" → ".join(scenario.get("topics", []))}
            </span>

        </div>
        """
    )

    if st.button(
        "🚀 Start Interview",
        use_container_width=True,
        type="primary",
    ):

        st.session_state.selected_scenario = (
            selected_scenario
        )

        st.session_state.selected_area = (
            scenario["area"]
        )

        st.session_state.selected_level = (
            scenario["level"]
        )

        st.session_state.number_of_questions = (
            q_count
        )

        st.session_state.selected_questions = (
            scenario_questions
        )

        st.session_state.current_index = 0

        st.session_state.answers = {}

        st.session_state.evaluations = {}

        st.session_state.answer_submitted = False

        st.session_state.interviewer_reaction = ""

        st.session_state.interview_id = str(uuid.uuid4())

        st.session_state.interview_started = True

        st.session_state.interview_completed = False

        st.session_state.usage_completed_tracked = False

        st.session_state.voice_text_box_version = {}

        track_interview_started()

        st.rerun()

    st.html(
        '</div>'
    )


# =========================================================
# ACTIVE INTERVIEW
# =========================================================

elif (
    page == "Interviews"
    and st.session_state.interview_started
    and not st.session_state.interview_completed
):

    questions = (
        st.session_state.selected_questions
    )

    current_index = (
        st.session_state.current_index
    )

    total_questions = len(
        questions
    )

    if total_questions == 0:

        st.error(
            "No interview questions were loaded."
        )

        st.stop()

    if current_index >= total_questions:

        current_index = total_questions - 1

        st.session_state.current_index = (
            current_index
        )

    current_question = questions[
        current_index
    ]

    scenario = INTERVIEW_SCENARIOS[
        st.session_state.selected_scenario
    ]

    st.html(
        '<div class="interview-shell">'
    )

    st.progress(
        (current_index + 1) / total_questions,
        text=(
            f"Question {current_index + 1} "
            f"of {total_questions} · "
            f"{scenario['area']}"
        ),
    )

    reaction = st.session_state.get(
        "interviewer_reaction",
        "",
    )

    note = (
        reaction
        if current_index > 0 and reaction
        else (
            scenario["intro"]
            if current_index == 0
            else "Good. Let’s go one level deeper."
        )
    )

    st.html(
        f"""
        <div class="interviewer-card">

            <span class="interviewer-avatar">
                👤
            </span>

            <span class="interviewer-name">
                {scenario['interviewer']}
            </span>

            <br>

            <span class="interviewer-role">
                {scenario['interviewer_title']}
            </span>

            <div class="interviewer-note">
                {note}
            </div>

        </div>
        """
    )

    st.html(
        f"""
        <div class="question-card">

            <div class="question-label">
                Technical Question ·
                {current_question.get("topic", "Valuation")}
            </div>

            <div class="question-text">
                {current_question["question"]}
            </div>

        </div>
        """
    )

    # -----------------------------------------------------
    # ANSWER INPUT
    # -----------------------------------------------------

    if not st.session_state.answer_submitted:

        st.markdown(
            "### 🎙️ Your Answer"
        )

        st.caption(
            "Speak naturally. You can review and edit the transcription before submitting."
        )

        spoken_text = speech_to_text(
            language="en",
            start_prompt="🎙️ Start Recording",
            stop_prompt="⏹️ Stop Recording",
            just_once=True,
            use_container_width=True,
            key=(
                f"voice_"
                f"{st.session_state.selected_scenario}_"
                f"{current_index}"
            ),
        )

        if spoken_text:

            st.session_state.answers[
                current_index
            ] = spoken_text

            current_version = (
                st.session_state.voice_text_box_version.get(
                    current_index,
                    0,
                )
            )

            st.session_state.voice_text_box_version[
                current_index
            ] = current_version + 1

            st.rerun()

    text_box_version = (
        st.session_state.voice_text_box_version.get(
            current_index,
            0,
        )
    )

    current_answer = st.text_area(
        "📝 Review & Edit",

        value=st.session_state.answers.get(
            current_index,
            "",
        ),

        height=190,

        placeholder=(
            "Type your answer or use the microphone above..."
        ),

        key=(
            f"answer_box_"
            f"{current_index}_"
            f"{text_box_version}"
        ),

        disabled=st.session_state.answer_submitted,
    )

    # -----------------------------------------------------
    # SUBMIT ANSWER
    # -----------------------------------------------------

    if not st.session_state.answer_submitted:

        if st.button(
            "✅ Submit Answer",
            use_container_width=True,
            type="primary",
        ):

            if not current_answer.strip():

                st.warning(
                    "Please provide an answer before submitting."
                )

            else:

                st.session_state.answers[
                    current_index
                ] = current_answer

                rule_evaluation = evaluate_answer(
                    current_question,
                    current_answer,
                )

                rule_score = (
                    rule_evaluation["score"]
                )

                next_topic = None

                if current_index < total_questions - 1:

                    next_topic = (
                        questions[
                            current_index + 1
                        ].get("topic")
                    )

                with st.spinner(
                    "🤖 Interviewer is evaluating your answer..."
                ):

                    ai_result = evaluate_with_gemini(
                        question=current_question["question"],
                        answer=current_answer,
                        level=st.session_state.selected_level,
                        area=st.session_state.selected_area,
                        rule_score=rule_score,
                        next_topic=next_topic,
                    )

                final_score = (
                    ai_result["score"]
                    if ai_result is not None
                    else rule_score
                )

                interviewer_reaction = ""

                if ai_result is not None:

                    interviewer_reaction = str(
                        ai_result.get(
                            "interviewer_reaction",
                            "",
                        )
                    ).strip()

                    generated_next = str(
                        ai_result.get(
                            "next_question",
                            "",
                        )
                    ).strip()

                    if (
                        generated_next
                        and current_index < total_questions - 1
                    ):

                        next_q = dict(
                            st.session_state.selected_questions[
                                current_index + 1
                            ]
                        )

                        next_q["question"] = (
                            generated_next
                        )

                        st.session_state.selected_questions[
                            current_index + 1
                        ] = next_q

                st.session_state.interviewer_reaction = (
                    interviewer_reaction
                )

                st.session_state.evaluations[
                    current_index
                ] = {

                    "score": final_score,

                    "rule_score": rule_score,

                    "feedback": (
                        rule_evaluation["feedback"]
                    ),

                    "matched_keywords": (
                        rule_evaluation[
                            "matched_keywords"
                        ]
                    ),

                    "missing_keywords": (
                        rule_evaluation[
                            "missing_keywords"
                        ]
                    ),

                    "improvement": (
                        rule_evaluation[
                            "improvement"
                        ]
                    ),

                    "length_feedback": (
                        rule_evaluation[
                            "length_feedback"
                        ]
                    ),

                    "ai_evaluation": ai_result,
                }

                st.session_state.answer_submitted = True

                track_event(
                    "answer_submitted",

                    scenario=(
                        st.session_state.selected_scenario
                    ),

                    question_number=current_index + 1,

                    questions_total=total_questions,
                )

                st.rerun()

    # -----------------------------------------------------
    # ANSWER FEEDBACK
    # -----------------------------------------------------

    else:

        evaluation = (
            st.session_state.evaluations[
                current_index
            ]
        )

        score = evaluation[
            "score"
        ]

        ai_result = evaluation.get(
            "ai_evaluation"
        )

        reaction_text = (
            (ai_result or {}).get("interviewer_reaction", "")
            or "Let’s examine the key technical reasoning in your answer."
        )

        feedback_text = (
            (ai_result or {}).get(
                "overall_feedback",
                evaluation["feedback"],
            )
        )

        st.markdown(f"### 🎯 Score: {score}/10")
        st.markdown("**Interviewer**")
        st.write(reaction_text)
        st.markdown("**Evaluation**")
        st.write(feedback_text)

        if ai_result:
            technical_accuracy = str(ai_result.get("technical_accuracy", "")).strip()
            if technical_accuracy:
                st.markdown("**Technical accuracy**")
                st.write(technical_accuracy)

            strengths = ai_result.get("strengths", [])
            if strengths:
                st.markdown("**What you did well**")
                for item in strengths:
                    st.markdown(f"- {item}")

            gaps = ai_result.get("areas_to_improve", [])
            if gaps:
                st.markdown("**Gaps to address**")
                for item in gaps:
                    st.markdown(f"- {item}")

            how_to_improve = str(ai_result.get("how_to_improve", "")).strip()
            if how_to_improve:
                st.markdown("**How to improve this answer**")
                st.write(how_to_improve)

            model_answer = str(ai_result.get("model_answer", "")).strip()
            if model_answer:
                with st.expander("📘 See a stronger sample answer"):
                    st.write(model_answer)
        else:
            st.caption("AI evaluation was unavailable for this response. The comments below are a basic keyword-based estimate, not a full technical review.")
            st.markdown("**Concepts detected**")
            st.write(", ".join(evaluation.get("matched_keywords", [])) or "No expected keywords were clearly detected.")
            st.markdown("**Potential gaps to check**")
            st.write(", ".join(evaluation.get("missing_keywords", [])) or "The basic checker did not detect missing keywords; technical accuracy has not been verified.")
            st.markdown("**Suggested next step**")
            st.write(evaluation.get("improvement", "Review the core definition, methodology and assumptions."))

        if current_index < total_questions - 1:

            if st.button(
                "➡️ Continue Interview",
                use_container_width=True,
                type="primary",
            ):

                st.session_state.current_index += 1

                st.session_state.answer_submitted = False

                st.session_state.interviewer_reaction = ""

                st.rerun()

        else:

            st.success(
                "You have completed all interview questions."
            )

            if st.button(
                "🏁 Finish & See Interviewer Report",
                use_container_width=True,
                type="primary",
            ):

                st.session_state.interview_completed = True

                if not st.session_state.usage_completed_tracked:

                    track_event(
                        "interview_completed",

                        scenario=(
                            st.session_state.selected_scenario
                        ),

                        area=(
                            st.session_state.selected_area
                        ),

                        level=(
                            st.session_state.selected_level
                        ),

                        questions=len(
                            st.session_state.evaluations
                        ),
                    )

                    st.session_state.usage_completed_tracked = True

                scores = [
                    x["score"]
                    for x in (
                        st.session_state.evaluations.values()
                    )
                ]

                overall = (
                    round(
                        sum(scores) / len(scores),
                        1,
                    )
                    if scores
                    else 0
                )

                st.session_state.history.append(
                    {
                        "scenario": (
                            st.session_state.selected_scenario
                        ),

                        "score": overall,

                        "questions": len(scores),
                    }
                )

                st.rerun()

    st.html(
        '</div>'
    )


# =========================================================
# FINAL REPORT
# =========================================================

elif (
    page == "Interviews"
    and st.session_state.interview_completed
):

    evaluations = (
        st.session_state.evaluations
    )

    scenario = INTERVIEW_SCENARIOS[
        st.session_state.selected_scenario
    ]

    st.html(
        '<div class="interview-shell">'
    )

    st.subheader(
        "🏆 Interviewer Report"
    )

    st.caption(
        f"{st.session_state.selected_scenario} · "
        f"{scenario['level']}"
    )

    if evaluations:

        scores = [
            item["score"]
            for item in evaluations.values()
        ]

        overall_score = round(
            sum(scores) / len(scores),
            1,
        )

        strong_answers = sum(
            1
            for score in scores
            if score >= 7
        )

        st.html(
            f"""
            <div class="final-card">

                <div class="small-muted">
                    OVERALL INTERVIEW SCORE
                </div>

                <div class="score-pill">
                    {overall_score}/10
                </div>

                <p>
                    Based on {len(scores)}
                    technical responses.
                </p>

            </div>
            """
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Overall Score",
                f"{overall_score}/10",
            )

        with col2:

            st.metric(
                "Questions",
                len(scores),
            )

        with col3:

            st.metric(
                "Strong Answers",
                strong_answers,
            )

        all_ai = [
            e.get("ai_evaluation")
            for e in evaluations.values()
            if e.get("ai_evaluation")
        ]

        strengths = []
        improvements = []

        for item in all_ai:

            strengths.extend(
                item.get(
                    "strengths",
                    [],
                )
            )

            improvements.extend(
                item.get(
                    "areas_to_improve",
                    [],
                )
            )

        if strengths:

            st.subheader(
                "🟢 What You Did Well"
            )

            for item in list(
                dict.fromkeys(strengths)
            )[:5]:

                st.write(
                    f"• {item}"
                )

        if improvements:

            st.subheader(
                "🎯 Focus Areas"
            )

            for item in list(
                dict.fromkeys(improvements)
            )[:5]:

                st.write(
                    f"• {item}"
                )

        st.subheader(
            "📋 Question-by-Question Review"
        )

        for index, evaluation in evaluations.items():

            question = (
                st.session_state.selected_questions[
                    index
                ]["question"]
            )

            score = evaluation[
                "score"
            ]

            with st.expander(
                f"Q{index + 1} — {score}/10"
            ):

                st.write(
                    f"**Question:** {question}"
                )

                st.write(
                    "**Your Answer:**"
                )

                st.write(
                    st.session_state.answers.get(
                        index,
                        "",
                    )
                )

                ai_result = evaluation.get(
                    "ai_evaluation"
                )

                if ai_result:

                    st.write(
                        "**Interviewer Feedback:**"
                    )

                    st.write(
                        ai_result.get(
                            "overall_feedback",
                            "",
                        )
                    )

                    st.write(
                        "**Model Answer:**"
                    )

                    st.info(
                        ai_result.get(
                            "model_answer",
                            "",
                        )
                    )

                else:

                    st.write(
                        "**Feedback:**"
                    )

                    st.write(
                        evaluation["feedback"]
                    )

    st.divider()

    if st.button(
        "🔄 Back to Dashboard",
        use_container_width=True,
    ):

        st.session_state.interview_started = False

        st.session_state.interview_completed = False

        st.session_state.selected_questions = []

        st.session_state.current_index = 0

        st.session_state.answers = {}

        st.session_state.evaluations = {}

        st.session_state.answer_submitted = False

        st.session_state.voice_text_box_version = {}

        st.session_state.interviewer_reaction = ""

        st.session_state.page = "Home"

        st.rerun()

    st.html(
        '</div>'
    )


# =========================================================
# ANALYTICS
# =========================================================

elif page == "Analytics":
    st.html('<div class="dashboard-shell">')
    st.html('<div class="section-title">Analytics</div>')
    st.html('<div class="section-subtitle">Anonymous product usage and interview funnel.</div>')

    try:
        admin_password = str(st.secrets.get("ADMIN_PASSWORD", ""))
    except Exception:
        admin_password = ""

    entered_password = st.text_input("Admin password", type="password", key="analytics_admin_password")

    if not admin_password:
        st.warning("Set ADMIN_PASSWORD in Streamlit Secrets to enable this page.")
    elif entered_password != admin_password:
        st.info("Enter the admin password to view usage.")
    else:
        if not supabase_configured():
            st.error("Persistent analytics are not configured. Add SUPABASE_URL and SUPABASE_KEY to Streamlit Secrets.")
        else:
            action_col1, action_col2 = st.columns([1, 2])
            with action_col1:
                if st.button("↻ Refresh analytics", key="refresh_analytics"):
                    st.rerun()
            with action_col2:
                if st.button("Run analytics write test", key="analytics_write_test"):
                    test_ok = track_event("analytics_test")
                    if test_ok:
                        st.success("Test event inserted. Refresh to confirm it can also be read.")
                    else:
                        st.error("Test insert failed: " + st.session_state.get("analytics_last_write_error", "Unknown error"))
            st.caption("The write test creates an analytics_test row; it does not count as an app open or interview.")

            rows, fetch_error, possibly_truncated = get_usage_events()
            if fetch_error:
                st.error(f"Could not read analytics from Supabase: {fetch_error}")
                st.caption("Check the key, table name, column names, and SELECT permissions/RLS policy.")
            else:
                # Normalize timestamps and remove malformed rows before calculating metrics.
                parsed = []
                for row in rows:
                    try:
                        dt = datetime.fromisoformat(str(row.get("timestamp_utc", "")).replace("Z", "+00:00"))
                        if dt.tzinfo is None:
                            dt = dt.replace(tzinfo=timezone.utc)
                        row["_dt"] = dt.astimezone(timezone.utc)
                        parsed.append(row)
                    except Exception:
                        continue

                if not parsed:
                    st.warning("Supabase returned zero readable event rows. This usually means no successful inserts yet, an incorrect table/schema, or API permissions/RLS blocking reads.")
                    st.write("**Quick checks**")
                    st.markdown("""
                    1. Run the `InterviewSathi_supabase_migration.sql` script in the Supabase SQL Editor.
                    2. In Streamlit Cloud → App → Settings → Secrets, verify `SUPABASE_URL`, `SUPABASE_KEY`, and `ADMIN_PASSWORD`.
                    3. `SUPABASE_KEY` must be a server-side secret/service-role key for this setup; never put it in client-side code or GitHub.
                    4. Click **Run analytics write test**, then refresh. If writing works but reading fails, check the key and SELECT permissions.
                    """)
                    if st.session_state.get("analytics_last_write_error"):
                        st.error("Last write error: " + st.session_state["analytics_last_write_error"])
                    elif st.session_state.get("analytics_last_write_ok"):
                        st.success("Last write succeeded at " + st.session_state["analytics_last_write_ok"] + ". If the table still reads empty, check SELECT permissions/key configuration.")
                    else:
                        st.caption("No write attempt has succeeded in this admin session yet. The public app may have a separate session, so use the write test above.")
                else:
                    oldest = min(r["_dt"].date() for r in parsed)
                    newest = max(r["_dt"].date() for r in parsed)
                    date_cols = st.columns([1, 1, 2])
                    with date_cols[0]:
                        date_from = st.date_input("From (UTC)", value=max(oldest, newest.replace(day=1)), min_value=oldest, max_value=newest, key="analytics_from")
                    with date_cols[1]:
                        date_to = st.date_input("To (UTC)", value=newest, min_value=oldest, max_value=newest, key="analytics_to")
                    with date_cols[2]:
                        st.caption("Metrics use event timestamps in UTC. Sessions are not the same as unique people.")

                    if date_from > date_to:
                        st.warning("The start date is after the end date. Choose a valid date range.")
                        filtered = []
                    else:
                        filtered = [r for r in parsed if date_from <= r["_dt"].date() <= date_to]

                    def event_rows(name):
                        return [r for r in filtered if r.get("event") == name]

                    app_open_events = event_rows("app_opened")
                    started = event_rows("interview_started")
                    completed = event_rows("interview_completed")
                    answered = event_rows("answer_submitted")
                    sessions = {r.get("visitor_id") for r in app_open_events if r.get("visitor_id")}
                    # Count distinct attempts when interview_id exists; legacy rows fall back to event rows.
                    started_ids = {r.get("interview_id") for r in started if r.get("interview_id")}
                    completed_ids = {r.get("interview_id") for r in completed if r.get("interview_id")}
                    legacy_starts = sum(1 for r in started if not r.get("interview_id"))
                    legacy_completions = sum(1 for r in completed if not r.get("interview_id"))
                    starts_count = len(started_ids) + legacy_starts
                    completions_count = len(completed_ids) + legacy_completions
                    rate = (completions_count / starts_count * 100) if starts_count else None

                    k1, k2, k3, k4 = st.columns(4)
                    k1.metric("Sessions with app-open event", len(sessions))
                    k2.metric("Interviews started", starts_count)
                    k3.metric("Interviews completed", completions_count)
                    k4.metric("Completion rate", f"{rate:.1f}%" if rate is not None else "N/A")
                    st.caption(f"Selected period: {date_from} to {date_to} UTC · {len(filtered):,} events loaded")

                    if possibly_truncated:
                        st.warning("The event query reached its 10,000-row limit. Metrics may be incomplete; use a narrower date range or add paginated queries before relying on totals.")

                    # Daily event counts, represented as a tidy dataframe for Streamlit charts.
                    daily = {}
                    for r in filtered:
                        day = r["_dt"].date().isoformat()
                        daily.setdefault(day, {"Date (UTC)": day, "App opens": 0, "Interviews started": 0, "Interviews completed": 0, "Answers submitted": 0})
                        label = {"app_opened": "App opens", "interview_started": "Interviews started", "interview_completed": "Interviews completed", "answer_submitted": "Answers submitted"}.get(r.get("event"))
                        if label:
                            daily[day][label] += 1
                    if daily:
                        st.subheader("Daily activity")
                        import pandas as pd
                        daily_df = pd.DataFrame([daily[k] for k in sorted(daily)])
                        st.line_chart(daily_df.set_index("Date (UTC)")[ ["App opens", "Interviews started", "Interviews completed"] ])
                        with st.expander("View daily activity table"):
                            st.dataframe(daily_df, use_container_width=True, hide_index=True)

                    left, right = st.columns(2)
                    with left:
                        st.subheader("Interviews by topic")
                        topic_counts = {}
                        for r in started:
                            label = r.get("area") or "Not recorded"
                            topic_counts[label] = topic_counts.get(label, 0) + 1
                        if topic_counts:
                            import pandas as pd
                            st.bar_chart(pd.DataFrame({"Interviews": topic_counts}).sort_values("Interviews", ascending=False))
                        else:
                            st.caption("No interview-start events in this period.")
                    with right:
                        st.subheader("Interviews by level")
                        level_counts = {}
                        for r in started:
                            label = r.get("level") or "Not recorded"
                            level_counts[label] = level_counts.get(label, 0) + 1
                        if level_counts:
                            import pandas as pd
                            st.bar_chart(pd.DataFrame({"Interviews": level_counts}).sort_values("Interviews", ascending=False))
                        else:
                            st.caption("No interview-start events in this period.")

                    st.subheader("Recent interview activity")
                    recent = []
                    for r in sorted(filtered, key=lambda x: x["_dt"], reverse=True)[:100]:
                        recent.append({
                            "Time (UTC)": r["_dt"].strftime("%Y-%m-%d %H:%M:%S"),
                            "Event": r.get("event", ""),
                            "Topic": r.get("area") or "",
                            "Level": r.get("level") or "",
                            "Scenario": r.get("scenario") or "",
                            "Question #": r.get("question_number") or "",
                            "Questions": r.get("questions") or "",
                            "Attempt ID": (str(r.get("interview_id") or "")[:8]),
                        })
                    st.dataframe(recent, use_container_width=True, hide_index=True)

                    with st.expander("Tracking health and interpretation"):
                        st.write(f"**Rows loaded:** {len(parsed):,}")
                        st.write(f"**app_opened events:** {len(app_open_events):,}")
                        st.write(f"**answer_submitted events:** {len(answered):,}")
                        st.write(f"**Distinct start IDs:** {len(started_ids):,}; **distinct completion IDs:** {len(completed_ids):,}")
                        if st.session_state.get("analytics_last_write_error"):
                            st.error("Most recent event write failed in this admin session: " + st.session_state["analytics_last_write_error"])
                        elif st.session_state.get("analytics_last_write_ok"):
                            st.success("Most recent event write succeeded at " + st.session_state["analytics_last_write_ok"])
                        else:
                            st.caption("No write test has been performed in this admin session. Open a fresh interview session to verify end-to-end writes.")
                        st.caption("Historical events created before interview_id was added cannot be reliably deduplicated by attempt. The dashboard falls back to event-row counts where IDs are absent.")

                    st.caption("Anonymous event tracking only. Session counts are based on visitor_id values that emitted app_opened during the selected period; browser restarts may create new session IDs.")
    st.html('</div>')


# =========================================================
# PERFORMANCE
# =========================================================

elif page == "Performance":

    history = (
        st.session_state.history
    )

    st.html(
        '<div class="dashboard-shell">'
    )

    st.html(
        '<div class="section-title">Performance</div>'
    )

    st.html(
        '<div class="section-subtitle">Your completed InterviewSathi sessions.</div>'
    )

    if not history:

        st.info(
            "Complete your first interview to start building your performance history."
        )

    else:

        scores = [
            x["score"]
            for x in history
        ]

        a, b, c = st.columns(3)

        with a:

            st.metric(
                "Interviews",
                len(history),
            )

        with b:

            st.metric(
                "Average Score",
                f"{round(sum(scores) / len(scores), 1)}/10",
            )

        with c:

            st.metric(
                "Latest Score",
                f"{scores[-1]}/10",
            )

        st.markdown(
            "### Recent Sessions"
        )

        for item in history[::-1]:

            st.html(
                f"""
                <div class="recent-card">

                    <b>
                        {item['scenario']}
                    </b>

                    <br>

                    <span class="small-muted">
                        {item['questions']} questions
                        · Score {item['score']}/10
                    </span>

                </div>

                <br>
                """
            )

    st.html(
        '</div>'
    )


# =========================================================
# SETTINGS
# =========================================================

elif page == "Settings":

    st.html(
        '<div class="dashboard-shell">'
    )

    st.html(
        '<div class="section-title">Settings</div>'
    )

    st.html(
        '<div class="section-subtitle">Simple preferences for the interview experience.</div>'
    )

    st.checkbox(
        "Show detailed technical feedback",
        value=True,
        disabled=True,
    )

    st.checkbox(
        "Use microphone when available",
        value=True,
        disabled=True,
    )

    st.info(
        "More personalization options can be added later as InterviewSathi grows."
    )

    st.html(
        '</div>'
    )