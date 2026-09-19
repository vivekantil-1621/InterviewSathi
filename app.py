import streamlit as st
import random
import re
import json
from google import genai
from streamlit_mic_recorder import speech_to_text


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="InterviewSathi | AI Valuation Interview Practice",
    page_icon="🎯",
    layout="wide"
)
# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

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
        background: linear-gradient(
            135deg,
            #eef4ff,
            #f5efff
        );
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
        background: linear-gradient(
            135deg,
            #f5f8ff,
            #faf5ff
        );
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

    </style>
    """,
    unsafe_allow_html=True
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
                    "cost approach"
                ]
            },

            {
                "question": "What is the difference between Enterprise Value and Equity Value?",
                "keywords": [
                    "enterprise value",
                    "equity value",
                    "debt",
                    "cash"
                ]
            },

            {
                "question": "What is WACC and why is it used in valuation?",
                "keywords": [
                    "WACC",
                    "cost of debt",
                    "cost of equity",
                    "capital structure"
                ]
            },

            {
                "question": "What is CAPM and how is it used to calculate the cost of equity?",
                "keywords": [
                    "CAPM",
                    "risk free rate",
                    "beta",
                    "equity risk premium"
                ]
            },

            {
                "question": "What is Beta and what does it represent in valuation?",
                "keywords": [
                    "beta",
                    "systematic risk",
                    "market risk"
                ]
            },

            {
                "question": "What is the difference between Equity Risk Premium and Company Specific Risk Premium?",
                "keywords": [
                    "equity risk premium",
                    "company specific risk premium",
                    "CSRP",
                    "risk"
                ]
            },

            {
                "question": "What factors would you consider while selecting comparable companies?",
                "keywords": [
                    "industry",
                    "size",
                    "growth",
                    "profitability",
                    "business model"
                ]
            },

            {
                "question": "What is a precedent transaction analysis?",
                "keywords": [
                    "precedent transactions",
                    "transaction multiples",
                    "acquisition"
                ]
            },

            {
                "question": "What is a terminal value in a DCF valuation?",
                "keywords": [
                    "terminal value",
                    "DCF",
                    "perpetuity",
                    "exit multiple"
                ]
            },

            {
                "question": "What is the difference between an enterprise value multiple and an equity value multiple?",
                "keywords": [
                    "enterprise value",
                    "equity value",
                    "EV EBITDA",
                    "P E"
                ]
            }
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
                    "present value"
                ]
            },

            {
                "question": "How would you select an appropriate WACC for a private company?",
                "keywords": [
                    "risk free rate",
                    "beta",
                    "ERP",
                    "size premium",
                    "CSRP",
                    "capital structure"
                ]
            },

            {
                "question": "What factors would cause the WACC of a private company to be different from a public company?",
                "keywords": [
                    "size",
                    "liquidity",
                    "CSRP",
                    "capital structure",
                    "beta"
                ]
            },

            {
                "question": "How would you select an appropriate EBITDA multiple for a company?",
                "keywords": [
                    "growth",
                    "margin",
                    "size",
                    "industry",
                    "risk",
                    "comparable companies"
                ]
            },

            {
                "question": "What are the key differences between the Guideline Public Company method and Precedent Transaction method?",
                "keywords": [
                    "public companies",
                    "transactions",
                    "control premium",
                    "synergies",
                    "multiples"
                ]
            },

            {
                "question": "How would you value a company that has negative EBITDA?",
                "keywords": [
                    "revenue multiple",
                    "DCF",
                    "growth",
                    "business model",
                    "future profitability"
                ]
            },

            {
                "question": "How would you evaluate whether a Company Specific Risk Premium is appropriate?",
                "keywords": [
                    "CSRP",
                    "company specific risk",
                    "size",
                    "customer concentration",
                    "management",
                    "financial performance"
                ]
            },

            {
                "question": "How does an increase in WACC affect the value of a business?",
                "keywords": [
                    "WACC",
                    "discount rate",
                    "present value",
                    "valuation decreases"
                ]
            },

            {
                "question": "How would you perform a sensitivity analysis in a DCF?",
                "keywords": [
                    "WACC",
                    "terminal growth",
                    "sensitivity",
                    "valuation range"
                ]
            }
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
                    "risk"
                ]
            },

            {
                "question": "A company has significantly higher margins than its peer group. How would you assess whether this should affect the selected valuation multiple?",
                "keywords": [
                    "margin",
                    "peer group",
                    "growth",
                    "multiple",
                    "sustainability"
                ]
            },

            {
                "question": "A company has high customer concentration and dependence on two major customers. How would this affect your valuation?",
                "keywords": [
                    "customer concentration",
                    "risk",
                    "CSRP",
                    "cash flow",
                    "multiple"
                ]
            },

            {
                "question": "How would you determine whether management projections are reasonable for a DCF valuation?",
                "keywords": [
                    "historical performance",
                    "industry growth",
                    "margin",
                    "management assumptions",
                    "market data"
                ]
            },

            {
                "question": "How would you select the appropriate valuation multiple when comparable companies have a wide range of multiples?",
                "keywords": [
                    "growth",
                    "margin",
                    "size",
                    "risk",
                    "median",
                    "comparable companies"
                ]
            },

            {
                "question": "Explain how changes in working capital affect free cash flow in a DCF.",
                "keywords": [
                    "working capital",
                    "cash flow",
                    "increase",
                    "decrease",
                    "free cash flow"
                ]
            }
        ]
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
                    "preferred stock"
                ]
            },

            {
                "question": "What is the Current Value Method?",
                "keywords": [
                    "CVM",
                    "current value",
                    "liquidation",
                    "waterfall"
                ]
            },

            {
                "question": "What is the Option Pricing Method?",
                "keywords": [
                    "OPM",
                    "option",
                    "volatility",
                    "strike price"
                ]
            },

            {
                "question": "When would you use OPM instead of CVM?",
                "keywords": [
                    "OPM",
                    "CVM",
                    "complex capital structure",
                    "future outcomes"
                ]
            },

            {
                "question": "What are liquidation preferences?",
                "keywords": [
                    "liquidation preference",
                    "preferred stock",
                    "priority",
                    "liquidation"
                ]
            },

            {
                "question": "What are conversion rights in preferred stock?",
                "keywords": [
                    "conversion rights",
                    "preferred stock",
                    "common stock"
                ]
            },

            {
                "question": "What is a non-1:1 conversion ratio?",
                "keywords": [
                    "conversion ratio",
                    "preferred stock",
                    "common stock"
                ]
            }
        ],

        "Senior Associate": [

            {
                "question": "Walk me through an OPM allocation for a company with common and preferred shares.",
                "keywords": [
                    "OPM",
                    "breakpoints",
                    "waterfall",
                    "volatility",
                    "time to liquidity"
                ]
            },

            {
                "question": "What are the key inputs required for an OPM?",
                "keywords": [
                    "equity value",
                    "volatility",
                    "risk free rate",
                    "time to liquidity",
                    "strike price"
                ]
            },

            {
                "question": "How does volatility affect the value allocated under OPM?",
                "keywords": [
                    "volatility",
                    "option value",
                    "higher",
                    "value"
                ]
            },

            {
                "question": "How would you handle a preferred stock with a 1.5:1 conversion ratio?",
                "keywords": [
                    "conversion ratio",
                    "1.5",
                    "preferred",
                    "common"
                ]
            },

            {
                "question": "How are employee stock options considered in equity allocation?",
                "keywords": [
                    "stock options",
                    "exercise price",
                    "option",
                    "equity allocation"
                ]
            }
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
                    "options"
                ]
            },

            {
                "question": "How would you determine the breakpoints in an OPM?",
                "keywords": [
                    "breakpoints",
                    "liquidation preference",
                    "conversion",
                    "waterfall"
                ]
            },

            {
                "question": "How would you decide between OPM, PWERM and CVM for an equity allocation?",
                "keywords": [
                    "OPM",
                    "PWERM",
                    "CVM",
                    "scenario",
                    "capital structure"
                ]
            }
        ]
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
                    "liabilities"
                ]
            },

            {
                "question": "What are the major intangible assets commonly valued in a PPA?",
                "keywords": [
                    "customer relationships",
                    "developed technology",
                    "trade name"
                ]
            },

            {
                "question": "What is the Relief-from-Royalty method?",
                "keywords": [
                    "relief from royalty",
                    "royalty rate",
                    "trade name",
                    "present value"
                ]
            },

            {
                "question": "What is the Multi-Period Excess Earnings Method?",
                "keywords": [
                    "MPEEM",
                    "customer relationships",
                    "excess earnings",
                    "contributory asset charges"
                ]
            },

            {
                "question": "What valuation methods may be used for Developed Technology, and what factors influence the method selection?",
                "keywords": [
                    "developed technology",
                    "relief from royalty",
                    "income approach",
                    "cost approach",
                    "method selection"
                ]
            }
        ],

        "Senior Associate": [

            {
                "question": "Walk me through the valuation of Customer Relationships using MPEEM.",
                "keywords": [
                    "MPEEM",
                    "revenue",
                    "attrition",
                    "contributory asset charges",
                    "present value"
                ]
            },

            {
                "question": "What are contributory asset charges and why are they used in MPEEM?",
                "keywords": [
                    "contributory asset charges",
                    "CAC",
                    "double counting",
                    "customer relationships"
                ]
            },

            {
                "question": "How would you determine the useful life of Customer Relationships?",
                "keywords": [
                    "useful life",
                    "attrition",
                    "customer retention",
                    "economic life"
                ]
            },

            {
                "question": "How would you determine an appropriate royalty rate for a Trade Name?",
                "keywords": [
                    "royalty rate",
                    "comparable agreements",
                    "trade name",
                    "profitability"
                ]
            },

            {
                "question": "What is the With-and-Without Method?",
                "keywords": [
                    "with-and-without",
                    "cash flow",
                    "difference",
                    "intangible asset"
                ]
            }
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
                    "useful life"
                ]
            },

            {
                "question": "How would you assess whether the projected attrition rate for Customer Relationships is reasonable?",
                "keywords": [
                    "attrition",
                    "historical",
                    "customer retention",
                    "industry",
                    "benchmark"
                ]
            },

            {
                "question": "What factors would you consider when selecting the useful life of Developed Technology?",
                "keywords": [
                    "useful life",
                    "technology",
                    "obsolescence",
                    "replacement",
                    "economic life"
                ]
            },

            {
                "question": "How would you perform a valuation of a Trade Name using the Relief-from-Royalty method?",
                "keywords": [
                    "relief from royalty",
                    "royalty rate",
                    "revenue",
                    "tax",
                    "present value"
                ]
            }
        ]
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
                    "market approach"
                ]
            },

            {
                "question": "You are given a startup with limited historical financial information. What information would you request from management before starting the valuation?",
                "keywords": [
                    "financial statements",
                    "projections",
                    "cap table",
                    "business plan",
                    "revenue"
                ]
            },

            {
                "question": "A company has three classes of shares with different rights. Which equity allocation method would you consider?",
                "keywords": [
                    "OPM",
                    "CVM",
                    "liquidation preference",
                    "conversion rights"
                ]
            }
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
                    "reporting"
                ]
            },

            {
                "question": "You are valuing a startup with no meaningful historical earnings. What information would you request and which valuation approach would you consider?",
                "keywords": [
                    "projections",
                    "cap table",
                    "funding",
                    "revenue",
                    "DCF",
                    "market approach"
                ]
            },

            {
                "question": "How would you select the appropriate GPC multiple for a private company when the comparable companies have different growth rates and margins?",
                "keywords": [
                    "GPC",
                    "growth",
                    "margin",
                    "multiple",
                    "comparable"
                ]
            },

            {
                "question": "How would you determine an appropriate venture capital rate of return for a startup valuation?",
                "keywords": [
                    "venture capital",
                    "rate of return",
                    "risk",
                    "stage",
                    "expected return"
                ]
            }
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
                    "reporting"
                ]
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
                    "two years"
                ]
            },

            {
                "question": "A private company has a wide range of GPC multiples. What factors would you consider before selecting the final multiple?",
                "keywords": [
                    "GPC",
                    "growth",
                    "margin",
                    "size",
                    "risk",
                    "business model"
                ]
            },

            {
                "question": "You are asked to value a startup using a Venture Capital Method. Walk me through the key steps and assumptions.",
                "keywords": [
                    "venture capital method",
                    "exit value",
                    "exit multiple",
                    "rate of return",
                    "present value"
                ]
            }
        ]
    }
}


# =========================================================
# ALIASES FOR CONCEPT MATCHING
# =========================================================

ALIASES = {

    "income approach": [
        "income approach",
        "income method"
    ],

    "market approach": [
        "market approach",
        "market method"
    ],

    "cost approach": [
        "cost approach",
        "cost method"
    ],

    "company specific risk premium": [
        "company specific risk premium",
        "company-specific risk premium",
        "csrp"
    ],

    "equity risk premium": [
        "equity risk premium",
        "erp"
    ],

    "risk free rate": [
        "risk free rate",
        "risk-free rate",
        "riskfree rate"
    ],

    "customer relationships": [
        "customer relationships",
        "customer relationship"
    ],

    "developed technology": [
        "developed technology",
        "technology"
    ],

    "trade name": [
        "trade name",
        "tradename"
    ],

    "relief from royalty": [
        "relief from royalty",
        "relief-from-royalty"
    ],

    "contributory asset charges": [
        "contributory asset charges",
        "contributory asset charge",
        "cac"
    ],

    "liquidation preference": [
        "liquidation preference",
        "liquidation preferences"
    ],

    "conversion rights": [
        "conversion rights",
        "conversion right"
    ],

    "OPM": [
        "opm",
        "option pricing method"
    ],

    "CVM": [
        "cvm",
        "current value method"
    ],

    "PWERM": [
        "pwerm",
        "probability weighted expected return method"
    ]
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
            "length_feedback": "No answer provided."
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
        1
    )

    structure_score = 1 if (
        "." in answer
        or "\n" in answer
        or word_count >= 40
    ) else 0.5

    final_score = (
        keyword_score * 7
        + length_score * 2
        + structure_score * 1
    )

    final_score = round(
        min(final_score, 10),
        1
    )

    if final_score >= 8.5:

        feedback = (
            "Excellent answer. You covered the major concepts "
            "and demonstrated strong technical understanding."
        )

        improvement = (
            "Focus on making the answer even more concise "
            "and interview-ready."
        )

    elif final_score >= 7:

        feedback = (
            "Strong answer. You covered most of the important "
            "technical concepts."
        )

        improvement = (
            "Add more depth and practical reasoning to "
            "strengthen the answer."
        )

    elif final_score >= 5.5:

        feedback = (
            "Good foundation, but the answer could be more "
            "complete and structured."
        )

        improvement = (
            "Cover the missing concepts and explain why "
            "they matter in an actual valuation."
        )

    elif final_score >= 4:

        feedback = (
            "Partial answer. Some relevant concepts are present, "
            "but important technical areas are missing."
        )

        improvement = (
            "Structure the answer clearly and address "
            "the major valuation concepts."
        )

    else:

        feedback = (
            "The answer needs significant improvement "
            "from a technical perspective."
        )

        improvement = (
            "Start with the core definition, then explain "
            "the methodology and key assumptions."
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

        length_feedback = (
            "Answer has sufficient detail."
        )

    return {
        "score": final_score,
        "feedback": feedback,
        "matched_keywords": matched,
        "missing_keywords": missing,
        "improvement": improvement,
        "length_feedback": length_feedback
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
    next_topic=None
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

Existing rule-based score:
{rule_score}/10

IMPORTANT EVALUATION PRINCIPLES:

1. Evaluate the candidate according to the expected knowledge
   for their stated level.

2. Do NOT require every possible technical detail.

3. For an Associate, focus primarily on strong fundamentals,
   correct definitions, basic methodology and logical understanding.

4. For a Senior Associate, expect deeper technical knowledge,
   practical application and reasonable judgment.

5. For an Assistant Manager, expect technical depth,
   structured thinking, judgment and practical engagement experience.

6. Distinguish between:
   - Required concepts
   - Useful additional depth
   - Advanced technical details

7. Do NOT penalize a candidate heavily for omitting an advanced
   detail when the core answer is technically correct.

8. For example, when discussing Enterprise Value versus Equity
   Value, an Associate can reasonably explain the basic bridge
   using debt and cash. Preferred stock, minority interest and
   other detailed bridge adjustments may be treated as additional
   depth rather than mandatory omissions unless the question
   specifically requires a detailed bridge.

9. Do NOT give credit simply because a keyword appears.
   Judge whether the candidate demonstrates the concept correctly.

10. Do not invent errors that are not actually present.

11. Prefer practical valuation interview expectations over
    unnecessarily textbook-heavy answers.

Evaluate the answer on:

1. Technical accuracy
2. Completeness
3. Understanding of valuation concepts
4. Practical application
5. Logical reasoning
6. Interview communication
7. Appropriateness for the candidate's experience level

Important valuation concepts may include:

- Business Valuation
- Income Approach
- Market Approach
- Cost Approach
- DCF
- Guideline Public Companies
- Precedent Transactions
- WACC
- CAPM
- Beta
- Risk Free Rate
- Equity Risk Premium
- Size Premium
- Company Specific Risk Premium
- Enterprise Value
- Equity Value
- Equity Allocation
- CVM
- OPM
- PWERM
- Liquidation Preferences
- Conversion Rights
- Stock Options
- Purchase Price Allocation
- ASC 805
- Customer Relationships
- Developed Technology
- Trade Name
- MPEEM
- Relief-from-Royalty
- Contributory Asset Charges
- Portfolio Valuation
- Venture Capital Method

The score must be from 0 to 10.

INTERVIEW FLOW:
This is a connected interview, not a random quiz. Listen to the candidate's response and make the next question feel like a natural interviewer follow-up.

Next topic that must be covered (if provided):
{next_topic if next_topic else "No next question"}

If a next topic is provided, also create:
- interviewer_reaction: one short, natural sentence reacting to the candidate's answer.
- next_question: ONE concise technical question on the specified next topic.
- Use something from the candidate's answer in the wording when useful.
- If the answer is weak, probe the relevant gap, but stay on the specified next topic.
- Do not jump to a later topic.
- Do not ask a generic "tell me more" question.
- If no next topic is provided, return an empty next_question.

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

- score must be a number between 0 and 10
- overall_feedback should be professional interview feedback
- technical_accuracy should explain whether the technical concepts are correct
- strengths should contain 2 to 4 concise points
- areas_to_improve should contain 2 to 4 concise points
- how_to_improve should provide practical interview advice
- model_answer should be a professional answer that the candidate could give
  in an interview
- The model answer should be technically accurate
- Do not make the model answer unnecessarily long
- Do not mention the underlying evaluation technology
- Do not mention any AI model, provider, API or software name
"""

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        raw_text = response.text.strip()

        raw_text = re.sub(
            r"^```json\s*",
            "",
            raw_text,
            flags=re.IGNORECASE
        )

        raw_text = re.sub(
            r"^```\s*",
            "",
            raw_text
        )

        raw_text = re.sub(
            r"\s*```$",
            "",
            raw_text
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
                    result["score"]
                )
            ),
            1
        )

        return result

    except Exception as e:

        # Technical details stay in the server console.
        # They are NOT shown to candidates.
        print(
            "AI evaluation error:",
            str(e)
        )

        return None



# =========================================================
# INTERVIEW SCENARIOS
# =========================================================
# Curated sequences make the experience feel like an interview rather than
# a random question bank. The existing question bank remains the source of truth.

INTERVIEW_SCENARIOS = {
    "Equity Valuation — Fundamentals": {
        "area": "Equity Valuation",
        "level": "Associate",
        "interviewer": "Sarah",
        "interviewer_title": "Senior Valuation Manager",
        "intro": "You are interviewing for a valuation role. We will start with fundamentals and gradually move into practical valuation judgment.",
        "questions": [1, 9, 2, 5, 6],
        "topics": [
            "valuation approaches",
            "Enterprise Value versus Equity Value",
            "enterprise value multiples versus equity value multiples",
            "WACC and why it is used",
            "Equity Risk Premium versus Company Specific Risk Premium"
        ],
    },
    "Equity Valuation — Private Company": {
        "area": "Equity Valuation",
        "level": "Senior Associate",
        "interviewer": "Sarah",
        "interviewer_title": "Senior Valuation Manager",
        "intro": "Let's discuss a private company valuation. I will start with methodology and then probe your assumptions and judgment.",
        "questions": [0, 1, 2, 3, 6],
        "topics": ["DCF process", "private-company WACC", "WACC risk differences", "EBITDA multiple selection", "Company Specific Risk Premium"],
    },
    "Equity Valuation — Manager Case": {
        "area": "Equity Valuation",
        "level": "Assistant Manager",
        "interviewer": "David",
        "interviewer_title": "Valuation Director",
        "intro": "Assume you are leading a private-company valuation with limited information. I am interested in how you structure the problem and defend your judgment.",
        "questions": [0, 1, 2, 3, 4],
        "topics": ["private-company valuation approach", "margin versus peers", "customer concentration and valuation risk", "management projections", "selecting a multiple from a wide comparable range"],
    },
    "Equity Allocation — Capital Structure": {
        "area": "Equity Allocation",
        "level": "Senior Associate",
        "interviewer": "Michael",
        "interviewer_title": "Valuation Director",
        "intro": "We are valuing a company with preferred and common equity. We will move from the allocation framework into OPM assumptions and conversion rights.",
        "questions": [0, 1, 3, 4, 2],
        "topics": ["OPM allocation", "OPM inputs", "conversion ratios", "employee stock options", "OPM versus CVM and PWERM"],
    },
    "PPA — Intangible Assets": {
        "area": "PPA",
        "level": "Senior Associate",
        "interviewer": "Priya",
        "interviewer_title": "PPA Senior Manager",
        "intro": "Assume we have completed an acquisition and identified Customer Relationships, Developed Technology and Trade Name. Let's work through the valuation logic.",
        "questions": [0, 1, 2, 3, 4],
        "topics": ["PPA fundamentals", "major intangible assets", "Relief-from-Royalty", "MPEEM", "With-and-Without Method"],
    },
    "PPA — Acquisition Case": {
        "area": "PPA",
        "level": "Assistant Manager",
        "interviewer": "Priya",
        "interviewer_title": "PPA Senior Manager",
        "intro": "You are leading the PPA for an acquisition with significant intangible assets. I will test both methodology and the assumptions behind your valuation.",
        "questions": [0, 1, 2, 3],
        "topics": ["PPA acquisition approach", "customer relationship attrition", "developed technology useful life", "Trade Name Relief-from-Royalty valuation"],
    },
    "Portfolio Valuation — Senior": {
        "area": "Case Studies",
        "level": "Senior Associate",
        "interviewer": "Alex",
        "interviewer_title": "Portfolio Valuation Director",
        "intro": "You have been asked to support a portfolio valuation engagement. We will move from engagement planning into individual valuation judgments.",
        "questions": [0, 1, 2, 3],
        "topics": ["portfolio valuation engagement process", "startup information and valuation approach", "GPC multiple selection", "venture capital rate of return"],
    },
    "Startup Valuation — Manager Case": {
        "area": "Case Studies",
        "level": "Assistant Manager",
        "interviewer": "Alex",
        "interviewer_title": "Portfolio Valuation Director",
        "intro": "Let's work through a startup valuation where historical earnings are limited and multiple future outcomes are possible.",
        "questions": [1, 3, 2, 0],
        "topics": ["startup information request", "venture capital method", "GPC multiple selection", "basic business valuation approach"],
    },
}


def get_scenario_questions(scenario_name):
    scenario = INTERVIEW_SCENARIOS[scenario_name]
    bank_questions = QUESTION_BANK[scenario["area"]][scenario["level"]]
    questions = []
    topics = scenario.get("topics", [])

    for pos, bank_index in enumerate(scenario["questions"]):
        if bank_index < len(bank_questions):
            q = dict(bank_questions[bank_index])
            q["topic"] = topics[pos] if pos < len(topics) else "technical valuation"
            q["base_question"] = q["question"]
            questions.append(q)

    return questions


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
    "selected_scenario": "Equity Valuation — Fundamentals",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# =========================================================
# INTERVIEW SATHI DASHBOARD + INTERVIEW EXPERIENCE
# =========================================================

st.markdown("""
<style>
/* ---------- GLOBAL ---------- */
.block-container { padding-top: 1.2rem; padding-bottom: 3rem; }

/* ---------- DASHBOARD ---------- */
.dashboard-shell { max-width: 1250px; margin: 0 auto; }
.hero-dashboard {
    background: linear-gradient(135deg, #eef4ff 0%, #f6f0ff 100%);
    border: 1px solid #dfe7f5;
    border-radius: 24px;
    padding: 30px 34px;
    margin-bottom: 22px;
}
.hero-kicker { color:#6366f1; font-size:12px; font-weight:800; letter-spacing:.12em; }
.hero-title { color:#111827; font-size:38px; line-height:1.08; font-weight:850; margin-top:5px; }
.hero-subtitle { color:#475569; font-size:16px; line-height:1.6; margin-top:10px; max-width:760px; }
.pill-row { margin-top:18px; }
.pill {
    display:inline-block; background:white; border:1px solid #dbe3f0;
    border-radius:999px; padding:7px 12px; margin:3px 5px 3px 0;
    color:#334155; font-size:12px; font-weight:700;
}
.section-title { color:#0f172a; font-size:23px; font-weight:800; margin:18px 0 5px; }
.section-subtitle { color:#64748b; font-size:14px; margin-bottom:14px; }
.metric-card {
    background:white; border:1px solid #e2e8f0; border-radius:16px;
    padding:17px 18px; min-height:105px; box-shadow:0 4px 14px rgba(15,23,42,.04);
}
.metric-label { color:#64748b; font-size:12px; font-weight:700; }
.metric-value { color:#111827; font-size:27px; font-weight:850; margin-top:5px; }
.metric-note { color:#94a3b8; font-size:11px; margin-top:3px; }
.case-card {
    background:#f8fafc; border:1px solid #e2e8f0; border-radius:16px;
    padding:20px 22px; margin:12px 0 18px; line-height:1.55;
}

.interview-card {
    background:#fff; border:1px solid #e2e8f0; border-radius:18px;
    padding:19px; min-height:205px; box-shadow:0 4px 14px rgba(15,23,42,.04);
}
.card-icon {
    width:42px; height:42px; display:flex; align-items:center; justify-content:center;
    border-radius:12px; background:#eef2ff; font-size:21px; margin-bottom:12px;
}
.card-title { color:#111827; font-size:17px; font-weight:800; }
.card-meta { color:#64748b; font-size:12px; margin-top:5px; }
.card-desc { color:#475569; font-size:13px; line-height:1.45; margin:12px 0 13px; }
.recent-card {
    background:#f8fafc; border:1px solid #e2e8f0; border-radius:16px; padding:16px;
}
.quote-card {
    background:linear-gradient(135deg,#111827,#312e81); color:white;
    border-radius:18px; padding:20px; min-height:140px;
}
.quote-text { font-size:16px; line-height:1.55; font-weight:650; }
.quote-small { color:#cbd5e1; font-size:12px; margin-top:12px; }

/* ---------- INTERVIEW ROOM ---------- */
.interview-shell { max-width: 1100px; margin: 0 auto; }
.interviewer-card {
    background:linear-gradient(135deg,#111827 0%,#1e293b 100%);
    color:white; border-radius:18px; padding:22px 26px;
    margin:8px 0 18px; border:1px solid #334155;
}
.interviewer-avatar {
    display:inline-flex; width:46px; height:46px; border-radius:50%;
    align-items:center; justify-content:center; background:#334155;
    font-size:23px; margin-right:12px; vertical-align:middle;
}
.interviewer-name { font-size:19px; font-weight:750; }
.interviewer-role { color:#cbd5e1; font-size:13px; }
.interviewer-note { color:#e2e8f0; font-size:15px; margin-top:12px; line-height:1.55; }
.question-card {
    background:linear-gradient(135deg,#eef4ff 0%,#f7f3ff 100%);
    border:1px solid #dbe4ff; border-radius:18px; padding:24px 26px;
    margin:12px 0 20px;
}
.question-label { color:#6366f1; font-size:13px; font-weight:800; letter-spacing:.05em; text-transform:uppercase; }
.question-text { color:#0f172a; font-size:25px; line-height:1.35; font-weight:700; margin-top:8px; }
.reaction-card {
    background:#f8fafc; border-left:4px solid #6366f1; border-radius:10px;
    padding:14px 18px; margin:15px 0;
}
.score-pill { font-size:28px; font-weight:800; color:#312e81; }
.final-card {
    background:linear-gradient(135deg,#eef4ff 0%,#faf5ff 100%);
    border:1px solid #dbe4ff; border-radius:18px; padding:24px;
}
.small-muted { color:#64748b; font-size:13px; }

/* ---------- SIDEBAR ---------- */
.sidebar-brand { font-size:22px; font-weight:850; color:#172554; margin-bottom:3px; }
.sidebar-tag { color:#64748b; font-size:11px; line-height:1.45; margin-bottom:16px; }
</style>
""", unsafe_allow_html=True)

# ---------- SESSION STATE ----------
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
    "selected_scenario": "Equity Valuation — Fundamentals",
    "page": "Home",
    "history": [],
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------- SIDEBAR NAVIGATION ----------
with st.sidebar:
    st.markdown('<div class="sidebar-brand">🎯 InterviewSathi</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-tag">Better Practice.<br>Stronger Interviews.<br>Bigger Opportunities.</div>', unsafe_allow_html=True)

    page = st.radio(
        "",
        ["Home", "Interviews", "Performance", "Settings"],
        index=["Home", "Interviews", "Performance", "Settings"].index(st.session_state.page),
        label_visibility="collapsed"
    )
    st.session_state.page = page
    st.divider()
    st.caption("AI-style technical valuation practice")

# If an interview is active, always keep the user in the interview room.
if st.session_state.interview_started:
    st.session_state.page = "Interviews"
    page = "Interviews"

scenario_names = list(INTERVIEW_SCENARIOS.keys())

# ---------- HOME DASHBOARD ----------
if page == "Home" and not st.session_state.interview_started:
    history = st.session_state.history
    completed = len(history)
    avg_score = round(sum(x["score"] for x in history) / completed, 1) if completed else 0

    st.markdown('<div class="dashboard-shell">', unsafe_allow_html=True)
    st.markdown("""
    <div class="hero-dashboard">
        <div class="hero-kicker">YOUR VALUATION INTERVIEW PARTNER</div>
        <div class="hero-title">Practice like it’s a real interview.</div>
        <div class="hero-subtitle">
            InterviewSathi turns valuation preparation into a connected technical interview —
            not a random list of questions. Answer, think, get feedback, and move to the next level.
        </div>
        <div class="pill-row">
            <span class="pill">Equity Valuation</span>
            <span class="pill">Equity Allocation</span>
            <span class="pill">PPA</span>
            <span class="pill">Case Studies</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Your Progress</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Your interview practice at a glance.</div>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f'<div class="metric-card"><div class="metric-label">TOTAL INTERVIEWS</div><div class="metric-value">{completed}</div><div class="metric-note">Completed sessions</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-card"><div class="metric-label">AVERAGE SCORE</div><div class="metric-value">{avg_score}/10</div><div class="metric-note">Across completed interviews</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-card"><div class="metric-label">TOPIC AREAS</div><div class="metric-value">4</div><div class="metric-note">Core valuation areas</div></div>', unsafe_allow_html=True)
    with m4:
        strong = sum(1 for x in history if x["score"] >= 7)
        st.markdown(f'<div class="metric-card"><div class="metric-label">STRONG SESSIONS</div><div class="metric-value">{strong}</div><div class="metric-note">Score ≥ 7/10</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Start Your Interview</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Choose an interview that matches your preparation goal.</div>', unsafe_allow_html=True)

    cards = [
        ("📊", "Equity Valuation — Fundamentals", "Associate", "Start with EV vs Equity Value, multiples, WACC and CSRP."),
        ("🏢", "Equity Valuation — Private Company", "Senior Associate", "Move from methodology into private-company assumptions and judgment."),
        ("🧩", "Equity Allocation — Capital Structure", "Senior Associate", "Work through OPM, conversion rights, options and allocation logic."),
        ("🧾", "PPA — Intangible Assets", "Senior Associate", "Discuss Customer Relationships, Developed Technology and Trade Name."),
        ("📁", "Case Studies — Portfolio", "Senior Associate", "Work through a 30-investment portfolio and valuation judgments."),
        ("🚀", "Case Studies — Startup", "Assistant Manager", "Handle startup valuation, VC method and scenario-based thinking."),
    ]

    for row_start in range(0, len(cards), 3):
        cols = st.columns(3)
        for col, (icon, title, level, desc) in zip(cols, cards[row_start:row_start+3]):
            with col:
                st.markdown(f'<div class="interview-card"><div class="card-icon">{icon}</div><div class="card-title">{title}</div><div class="card-meta">{level} · Connected interview</div><div class="card-desc">{desc}</div></div>', unsafe_allow_html=True)
                if st.button("Start Interview →", key=f"home_start_{title}", use_container_width=True, type="primary"):
                    scenario_key = title
                    if title == "Case Studies — Portfolio": scenario_key = "Portfolio Valuation — Senior"
                    if title == "Case Studies — Startup": scenario_key = "Startup Valuation — Manager Case"
                    st.session_state.selected_scenario = scenario_key
                    scenario = INTERVIEW_SCENARIOS[scenario_key]
                    st.session_state.selected_area = scenario["area"]
                    st.session_state.selected_level = scenario["level"]
                    st.session_state.number_of_questions = len(get_scenario_questions(title))
                    st.session_state.selected_questions = get_scenario_questions(title)
                    st.session_state.current_index = 0
                    st.session_state.answers = {}
                    st.session_state.evaluations = {}
                    st.session_state.answer_submitted = False
                    st.session_state.interviewer_reaction = ""
                    st.session_state.interview_started = True
                    st.session_state.interview_completed = False
                    st.session_state.voice_text_box_version = {}
                    st.session_state.page = "Interviews"
                    st.rerun()

    left, right = st.columns([1.2, 1])
    with left:
        st.markdown('<div class="section-title">Recent Activity</div>', unsafe_allow_html=True)
        if history:
            st.markdown('<div class="recent-card">', unsafe_allow_html=True)
            for item in history[-5:][::-1]:
                st.write(f"**{item['scenario']}** · {item['score']}/10 · {item['questions']} questions")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Your completed interviews will appear here.")
    with right:
        st.markdown('<div class="section-title">Keep Going</div>', unsafe_allow_html=True)
        st.markdown('<div class="quote-card"><div class="quote-text">“A strong valuation interview is not about memorising formulas. It is about explaining why your approach makes sense.”</div><div class="quote-small">InterviewSathi · Technical Practice</div></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- INTERVIEWS PAGE ----------
elif page == "Interviews" and not st.session_state.interview_started:
    st.markdown('<div class="dashboard-shell">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Interviews</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Pick a connected technical interview. The next question reacts to your previous answer.</div>', unsafe_allow_html=True)

    selected_scenario = st.selectbox("Interview Type", scenario_names, index=scenario_names.index(st.session_state.selected_scenario) if st.session_state.selected_scenario in scenario_names else 0)
    scenario = INTERVIEW_SCENARIOS[selected_scenario]
    q_count = len(get_scenario_questions(selected_scenario))

    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Area", scenario["area"])
    with c2: st.metric("Level", scenario["level"])
    with c3: st.metric("Questions", q_count)

    st.markdown(f'<div class="case-card"><b>👤 {scenario["interviewer"]}</b> · {scenario["interviewer_title"]}<br><br>{scenario["intro"]}<br><br><span class="small-muted">Connected sequence: {" → ".join(scenario.get("topics", []))}</span></div>', unsafe_allow_html=True)

    if st.button("🚀 Start Interview", use_container_width=True, type="primary"):
        st.session_state.selected_scenario = selected_scenario
        st.session_state.selected_area = scenario["area"]
        st.session_state.selected_level = scenario["level"]
        st.session_state.number_of_questions = q_count
        st.session_state.selected_questions = get_scenario_questions(selected_scenario)
        st.session_state.current_index = 0
        st.session_state.answers = {}
        st.session_state.evaluations = {}
        st.session_state.answer_submitted = False
        st.session_state.interviewer_reaction = ""
        st.session_state.interview_started = True
        st.session_state.interview_completed = False
        st.session_state.voice_text_box_version = {}
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- ACTIVE INTERVIEW ----------
elif page == "Interviews" and st.session_state.interview_started and not st.session_state.interview_completed:
    questions = st.session_state.selected_questions
    current_index = st.session_state.current_index
    total_questions = len(questions)
    current_question = questions[current_index]
    scenario = INTERVIEW_SCENARIOS[st.session_state.selected_scenario]

    st.markdown('<div class="interview-shell">', unsafe_allow_html=True)
    st.progress((current_index + 1) / total_questions, text=f"Question {current_index + 1} of {total_questions} · {scenario['area']}")

    reaction = st.session_state.get("interviewer_reaction", "")
    note = reaction if current_index > 0 and reaction else (scenario["intro"] if current_index == 0 else "Good. Let’s go one level deeper.")
    st.markdown(f"""
    <div class="interviewer-card">
        <span class="interviewer-avatar">👤</span>
        <span class="interviewer-name">{scenario['interviewer']}</span><br>
        <span class="interviewer-role">{scenario['interviewer_title']}</span>
        <div class="interviewer-note">{note}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="question-card">
        <div class="question-label">Technical Question · {current_question.get('topic','Valuation')}</div>
        <div class="question-text">{current_question['question']}</div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.answer_submitted:
        st.markdown("### 🎙️ Your Answer")
        st.caption("Speak naturally. You can review and edit the transcription before submitting.")
        spoken_text = speech_to_text(
            language="en",
            start_prompt="🎙️ Start Recording",
            stop_prompt="⏹️ Stop Recording",
            just_once=True,
            use_container_width=True,
            key=f"voice_{st.session_state.selected_scenario}_{current_index}"
        )
        if spoken_text:
            st.session_state.answers[current_index] = spoken_text
            current_version = st.session_state.voice_text_box_version.get(current_index, 0)
            st.session_state.voice_text_box_version[current_index] = current_version + 1
            st.rerun()

    text_box_version = st.session_state.voice_text_box_version.get(current_index, 0)
    current_answer = st.text_area(
        "📝 Review & Edit",
        value=st.session_state.answers.get(current_index, ""),
        height=190,
        placeholder="Type your answer or use the microphone above...",
        key=f"answer_box_{current_index}_{text_box_version}"
    )

    if not st.session_state.answer_submitted:
        if st.button("✅ Submit Answer", use_container_width=True, type="primary"):
            if not current_answer.strip():
                st.warning("Please provide an answer before submitting.")
            else:
                st.session_state.answers[current_index] = current_answer
                rule_evaluation = evaluate_answer(current_question, current_answer)
                rule_score = rule_evaluation["score"]
                next_topic = None
                if current_index < total_questions - 1:
                    next_topic = questions[current_index + 1].get("topic")

                with st.spinner("🤖 Interviewer is evaluating your answer..."):
                    ai_result = evaluate_with_gemini(
                        question=current_question["question"],
                        answer=current_answer,
                        level=st.session_state.selected_level,
                        area=st.session_state.selected_area,
                        rule_score=rule_score,
                        next_topic=next_topic
                    )

                final_score = ai_result["score"] if ai_result is not None else rule_score
                interviewer_reaction = ""
                if ai_result is not None:
                    interviewer_reaction = str(ai_result.get("interviewer_reaction", "")).strip()
                    generated_next = str(ai_result.get("next_question", "")).strip()
                    if generated_next and current_index < total_questions - 1:
                        next_q = dict(st.session_state.selected_questions[current_index + 1])
                        next_q["question"] = generated_next
                        st.session_state.selected_questions[current_index + 1] = next_q

                st.session_state.interviewer_reaction = interviewer_reaction
                st.session_state.evaluations[current_index] = {
                    "score": final_score,
                    "rule_score": rule_score,
                    "feedback": rule_evaluation["feedback"],
                    "matched_keywords": rule_evaluation["matched_keywords"],
                    "missing_keywords": rule_evaluation["missing_keywords"],
                    "improvement": rule_evaluation["improvement"],
                    "length_feedback": rule_evaluation["length_feedback"],
                    "ai_evaluation": ai_result,
                }
                st.session_state.answer_submitted = True
                st.rerun()
    else:
        evaluation = st.session_state.evaluations[current_index]
        score = evaluation["score"]
        ai_result = evaluation.get("ai_evaluation")
        reaction_text = (ai_result or {}).get("interviewer_reaction", "") or evaluation["feedback"]
        feedback_text = (ai_result or {}).get("overall_feedback", evaluation["feedback"])
        st.markdown(f"<div class='reaction-card'><span class='score-pill'>🎯 {score}/10</span><br><br><b>Interviewer</b><br>{reaction_text}<br><br><b>Feedback</b><br>{feedback_text}</div>", unsafe_allow_html=True)

        if current_index < total_questions - 1:
            if st.button("➡️ Continue Interview", use_container_width=True, type="primary"):
                st.session_state.current_index += 1
                st.session_state.answer_submitted = False
                st.session_state.interviewer_reaction = ""
                st.rerun()
        else:
            st.success("You have completed all interview questions.")
            if st.button("🏁 Finish & See Interviewer Report", use_container_width=True, type="primary"):
                st.session_state.interview_completed = True
                scores = [x["score"] for x in st.session_state.evaluations.values()]
                overall = round(sum(scores) / len(scores), 1) if scores else 0
                st.session_state.history.append({
                    "scenario": st.session_state.selected_scenario,
                    "score": overall,
                    "questions": len(scores),
                })
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- FINAL REPORT ----------
elif page == "Interviews" and st.session_state.interview_completed:
    evaluations = st.session_state.evaluations
    scenario = INTERVIEW_SCENARIOS[st.session_state.selected_scenario]
    st.markdown('<div class="interview-shell">', unsafe_allow_html=True)
    st.subheader("🏆 Interviewer Report")
    st.caption(f"{st.session_state.selected_scenario} · {scenario['level']}")

    if evaluations:
        scores = [item["score"] for item in evaluations.values()]
        overall_score = round(sum(scores) / len(scores), 1)
        strong_answers = sum(1 for score in scores if score >= 7)
        st.markdown(f"""
        <div class="final-card">
            <div class="small-muted">OVERALL INTERVIEW SCORE</div>
            <div class="score-pill">{overall_score}/10</div>
            <p>Based on {len(scores)} technical responses.</p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Overall Score", f"{overall_score}/10")
        with col2: st.metric("Questions", len(scores))
        with col3: st.metric("Strong Answers", strong_answers)

        all_ai = [e.get("ai_evaluation") for e in evaluations.values() if e.get("ai_evaluation")]
        strengths, improvements = [], []
        for item in all_ai:
            strengths.extend(item.get("strengths", []))
            improvements.extend(item.get("areas_to_improve", []))
        if strengths:
            st.subheader("🟢 What You Did Well")
            for item in list(dict.fromkeys(strengths))[:5]: st.write(f"• {item}")
        if improvements:
            st.subheader("🎯 Focus Areas")
            for item in list(dict.fromkeys(improvements))[:5]: st.write(f"• {item}")

        st.subheader("📋 Question-by-Question Review")
        for index, evaluation in evaluations.items():
            question = st.session_state.selected_questions[index]["question"]
            score = evaluation["score"]
            with st.expander(f"Q{index + 1} — {score}/10"):
                st.write(f"**Question:** {question}")
                st.write("**Your Answer:**")
                st.write(st.session_state.answers.get(index, ""))
                ai_result = evaluation.get("ai_evaluation")
                if ai_result:
                    st.write("**Interviewer Feedback:**")
                    st.write(ai_result.get("overall_feedback", ""))
                    st.write("**Model Answer:**")
                    st.info(ai_result.get("model_answer", ""))
                else:
                    st.write("**Feedback:**")
                    st.write(evaluation["feedback"])

    st.divider()
    if st.button("🔄 Back to Dashboard", use_container_width=True):
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
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- PERFORMANCE ----------
elif page == "Performance":
    history = st.session_state.history
    st.markdown('<div class="dashboard-shell">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Performance</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Your completed InterviewSathi sessions.</div>', unsafe_allow_html=True)
    if not history:
        st.info("Complete your first interview to start building your performance history.")
    else:
        scores = [x["score"] for x in history]
        a,b,c = st.columns(3)
        with a: st.metric("Interviews", len(history))
        with b: st.metric("Average Score", f"{round(sum(scores)/len(scores),1)}/10")
        with c: st.metric("Latest Score", f"{scores[-1]}/10")
        st.markdown("### Recent Sessions")
        for item in history[::-1]:
            st.markdown(f"<div class='recent-card'><b>{item['scenario']}</b><br><span class='small-muted'>{item['questions']} questions · Score {item['score']}/10</span></div><br>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- SETTINGS ----------
elif page == "Settings":
    st.markdown('<div class="dashboard-shell">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Settings</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Simple preferences for the interview experience.</div>', unsafe_allow_html=True)
    st.checkbox("Show detailed technical feedback", value=True, disabled=True)
    st.checkbox("Use microphone when available", value=True, disabled=True)
    st.info("More personalization options can be added later as InterviewSathi grows.")
    st.markdown('</div>', unsafe_allow_html=True)
