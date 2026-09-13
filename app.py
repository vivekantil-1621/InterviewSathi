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
    page_title="InterviewSathi",
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
    rule_score
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
    "model_answer": ""
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

    # -----------------------------------------------------
    # Voice transcription state
    # -----------------------------------------------------

    "voice_text_box_version": {}

}


for key, value in defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🎯 InterviewSathi</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-style Valuation Interview Practice'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("⚙️ Interview Setup")

    selected_area = st.selectbox(
        "Interview Area",
        list(QUESTION_BANK.keys()),
        index=list(
            QUESTION_BANK.keys()
        ).index(
            st.session_state.selected_area
        )
    )

    selected_level = st.selectbox(
        "Candidate Level",
        [
            "Associate",
            "Senior Associate",
            "Assistant Manager"
        ],
        index=[
            "Associate",
            "Senior Associate",
            "Assistant Manager"
        ].index(
            st.session_state.selected_level
        )
    )

    max_questions = len(
        QUESTION_BANK[
            selected_area
        ][
            selected_level
        ]
    )

    number_of_questions = st.slider(
        "Number of Questions",
        min_value=1,
        max_value=min(
            10,
            max_questions
        ),
        value=min(
            st.session_state.number_of_questions,
            max_questions
        )
    )

    st.divider()

    st.caption(
        "Professional technical evaluation "
        "with standard fallback assessment."
    )


# =========================================================
# START SCREEN
# =========================================================

if not st.session_state.interview_started:

    st.subheader(
        "🚀 Start Your Interview"
    )

    st.write(
        "Practice technical valuation questions "
        "and receive professional interview feedback."
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Area",
            selected_area
        )

    with col2:

        st.metric(
            "Level",
            selected_level
        )

    with col3:

        st.metric(
            "Questions",
            number_of_questions
        )

    st.write("")

    if st.button(
        "🚀 Start Interview",
        use_container_width=True
    ):

        questions = QUESTION_BANK[
            selected_area
        ][
            selected_level
        ]

        selected_questions = random.sample(
            questions,
            min(
                number_of_questions,
                len(questions)
            )
        )

        st.session_state.selected_questions = (
            selected_questions
        )

        st.session_state.selected_area = (
            selected_area
        )

        st.session_state.selected_level = (
            selected_level
        )

        st.session_state.number_of_questions = (
            number_of_questions
        )

        st.session_state.current_index = 0

        st.session_state.answers = {}

        st.session_state.evaluations = {}

        st.session_state.answer_submitted = False

        st.session_state.interview_started = True

        st.session_state.interview_completed = False

        st.session_state.voice_text_box_version = {}

        st.rerun()


# =========================================================
# ACTIVE INTERVIEW
# =========================================================

elif (
    st.session_state.interview_started
    and not st.session_state.interview_completed
):

    questions = st.session_state.selected_questions

    current_index = st.session_state.current_index

    total_questions = len(questions)

    current_question = questions[
        current_index
    ]


    # -----------------------------------------------------
    # PROGRESS
    # -----------------------------------------------------

    st.progress(
        (current_index + 1)
        / total_questions
    )

    st.caption(
        f"Question {current_index + 1} "
        f"of {total_questions}"
    )


    # -----------------------------------------------------
    # QUESTION
    # -----------------------------------------------------

    st.markdown(
        f"""
        <div class="question-box">

        <h3>
        Q{current_index + 1}.
        {current_question["question"]}
        </h3>

        </div>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # ANSWER INPUT
    # =====================================================

    existing_answer = st.session_state.answers.get(
        current_index,
        ""
    )


    # -----------------------------------------------------
    # VOICE INPUT
    # -----------------------------------------------------

    if not st.session_state.answer_submitted:

        st.markdown(
            "### 🎙️ Answer by Voice"
        )

        st.caption(
            "Click Start Recording, speak your complete answer, "
            "then click Stop Recording."
        )

        spoken_text = speech_to_text(
            language="en",
            start_prompt="🎙️ Start Recording",
            stop_prompt="⏹️ Stop Recording",
            just_once=True,
            use_container_width=True,
            key=f"voice_{current_index}"
        )

        # -------------------------------------------------
        # NEW TRANSCRIPTION RECEIVED
        # -------------------------------------------------

        if spoken_text:

            st.session_state.answers[
                current_index
            ] = spoken_text

            current_version = (
                st.session_state.voice_text_box_version.get(
                    current_index,
                    0
                )
            )

            st.session_state.voice_text_box_version[
                current_index
            ] = current_version + 1

            st.rerun()


    # -----------------------------------------------------
    # TEXT BOX VERSION
    # -----------------------------------------------------

    text_box_version = (
        st.session_state.voice_text_box_version.get(
            current_index,
            0
        )
    )


    # -----------------------------------------------------
    # ANSWER TEXT BOX
    # -----------------------------------------------------

    current_answer = st.text_area(
        "📝 Your Answer — Review & Edit",
        value=st.session_state.answers.get(
            current_index,
            ""
        ),
        height=220,
        placeholder=(
            "Speak using the microphone above, "
            "or type your answer here..."
        ),
        key=(
            f"answer_box_"
            f"{current_index}_"
            f"{text_box_version}"
        )
    )


    # -----------------------------------------------------
    # SUBMIT ANSWER
    # -----------------------------------------------------

    if not st.session_state.answer_submitted:

        if st.button(
            "✅ Submit Answer",
            use_container_width=True
        ):

            if not current_answer.strip():

                st.warning(
                    "Please provide an answer before submitting."
                )

            else:

                # -----------------------------------------
                # SAVE LATEST EDITED ANSWER
                # -----------------------------------------

                st.session_state.answers[
                    current_index
                ] = current_answer


                # -----------------------------------------
                # RULE BASED SCORE
                # -----------------------------------------

                rule_evaluation = evaluate_answer(
                    current_question,
                    current_answer
                )

                rule_score = rule_evaluation[
                    "score"
                ]


                # -----------------------------------------
                # AI EVALUATION
                # -----------------------------------------

                with st.spinner(
                    "🤖 Evaluating your answer..."
                ):

                    ai_result = (
                        evaluate_with_gemini(
                            question=current_question[
                                "question"
                            ],
                            answer=current_answer,
                            level=st.session_state[
                                "selected_level"
                            ],
                            area=st.session_state[
                                "selected_area"
                            ],
                            rule_score=rule_score
                        )
                    )


                # -----------------------------------------
                # FINAL SCORE
                # -----------------------------------------

                if ai_result is not None:

                    final_score = ai_result[
                        "score"
                    ]

                else:

                    final_score = rule_score


                # -----------------------------------------
                # SAVE EVALUATION
                # -----------------------------------------

                st.session_state.evaluations[
                    current_index
                ] = {

                    "score": final_score,

                    "rule_score": rule_score,

                    "feedback": rule_evaluation[
                        "feedback"
                    ],

                    "matched_keywords":
                        rule_evaluation[
                            "matched_keywords"
                        ],

                    "missing_keywords":
                        rule_evaluation[
                            "missing_keywords"
                        ],

                    "improvement":
                        rule_evaluation[
                            "improvement"
                        ],

                    "length_feedback":
                        rule_evaluation[
                            "length_feedback"
                        ],

                    "ai_evaluation":
                        ai_result
                }


                st.session_state.answer_submitted = True

                st.rerun()


    # =====================================================
    # EVALUATION
    # =====================================================

    else:

        evaluation = st.session_state.evaluations[
            current_index
        ]

        score = evaluation[
            "score"
        ]

        ai_result = evaluation.get(
            "ai_evaluation"
        )


        # -------------------------------------------------
        # SCORE
        # -------------------------------------------------

        st.markdown(
            f"""
            <div class="score-box">

            <h2>
            🎯 Score: {score}/10
            </h2>

            </div>
            """,
            unsafe_allow_html=True
        )


        # -------------------------------------------------
        # AI FEEDBACK
        # -------------------------------------------------

        if ai_result is not None:

            st.markdown(
                '<div class="ai-box">',
                unsafe_allow_html=True
            )

            st.subheader(
                "🤖 AI Interviewer Evaluation"
            )

            st.write(
                ai_result.get(
                    "overall_feedback",
                    ""
                )
            )

            st.divider()

            st.markdown(
                "### 🎯 Technical Accuracy"
            )

            st.write(
                ai_result.get(
                    "technical_accuracy",
                    ""
                )
            )

            st.markdown(
                "### 🟢 Strengths"
            )

            strengths = ai_result.get(
                "strengths",
                []
            )

            if strengths:

                for item in strengths:

                    st.write(
                        f"• {item}"
                    )

            st.markdown(
                "### 🔴 Areas to Improve"
            )

            improvements = ai_result.get(
                "areas_to_improve",
                []
            )

            if improvements:

                for item in improvements:

                    st.write(
                        f"• {item}"
                    )

            st.markdown(
                "### 💡 How to Improve"
            )

            st.write(
                ai_result.get(
                    "how_to_improve",
                    ""
                )
            )

            st.markdown(
                "### 📚 Professional Model Answer"
            )

            st.info(
                ai_result.get(
                    "model_answer",
                    ""
                )
            )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )


        # -------------------------------------------------
        # FALLBACK MESSAGE
        # -------------------------------------------------

        else:

            st.warning(
                "AI evaluation is temporarily unavailable, "
                "so a standard technical evaluation has been used."
            )

            st.subheader(
                "📝 Interviewer Evaluation"
            )

            st.write(
                evaluation[
                    "feedback"
                ]
            )

            st.write(
                evaluation[
                    "improvement"
                ]
            )


        # -------------------------------------------------
        # RULE BASED DETAILS
        # -----------------------------------------------------

        st.divider()

        st.subheader(
            "🔍 Concept Coverage"
        )

        matched = evaluation[
            "matched_keywords"
        ]

        missing = evaluation[
            "missing_keywords"
        ]

        col1, col2 = st.columns(2)

        with col1:

            st.markdown(
                "### 🟢 Covered Concepts"
            )

            if matched:

                for item in matched:

                    st.write(
                        f"✅ {item}"
                    )

            else:

                st.write(
                    "No major concepts detected."
                )

        with col2:

            st.markdown(
                "### 🔴 Missing Concepts"
            )

            if missing:

                for item in missing:

                    st.write(
                        f"⚠️ {item}"
                    )

            else:

                st.write(
                    "Excellent concept coverage."
                )


        st.markdown(
            "### 📌 Answer Depth"
        )

        st.write(
            evaluation[
                "length_feedback"
            ]
        )


        # -------------------------------------------------
        # NEXT QUESTION
        # -----------------------------------------------------

        if current_index < total_questions - 1:

            if st.button(
                "➡️ Next Question",
                use_container_width=True
            ):

                st.session_state.current_index += 1

                st.session_state.answer_submitted = False

                st.rerun()

        else:

            if st.button(
                "🏁 Finish Interview",
                use_container_width=True
            ):

                st.session_state.interview_completed = True

                st.rerun()


# =========================================================
# FINAL RESULTS
# =========================================================

elif st.session_state.interview_completed:

    st.subheader(
        "🏆 Interview Results"
    )

    evaluations = (
        st.session_state.evaluations
    )

    if evaluations:

        scores = [
            item["score"]
            for item in evaluations.values()
        ]

        overall_score = round(
            sum(scores) / len(scores),
            1
        )

        strong_answers = sum(
            1
            for score in scores
            if score >= 7
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Overall Score",
                f"{overall_score}/10"
            )

        with col2:

            st.metric(
                "Questions",
                len(scores)
            )

        with col3:

            st.metric(
                "Strong Answers",
                strong_answers
            )

        st.divider()

        st.subheader(
            "📊 Question-wise Results"
        )

        for index, evaluation in evaluations.items():

            question = (
                st.session_state.selected_questions[
                    index
                ][
                    "question"
                ]
            )

            score = evaluation[
                "score"
            ]

            with st.expander(
                f"Q{index + 1} — {score}/10"
            ):

                st.write(
                    question
                )

                st.write(
                    "**Your Answer:**"
                )

                st.write(
                    st.session_state.answers.get(
                        index,
                        ""
                    )
                )

                ai_result = evaluation.get(
                    "ai_evaluation"
                )

                if ai_result:

                    st.write(
                        "**AI Feedback:**"
                    )

                    st.write(
                        ai_result.get(
                            "overall_feedback",
                            ""
                        )
                    )

                    st.write(
                        "**Model Answer:**"
                    )

                    st.info(
                        ai_result.get(
                            "model_answer",
                            ""
                        )
                    )

                else:

                    st.write(
                        "**Feedback:**"
                    )

                    st.write(
                        evaluation[
                            "feedback"
                        ]
                    )

        st.divider()


    # -----------------------------------------------------
    # NEW INTERVIEW
    # -----------------------------------------------------

    if st.button(
        "🔄 Start New Interview",
        use_container_width=True
    ):

        st.session_state.interview_started = False

        st.session_state.interview_completed = False

        st.session_state.selected_questions = []

        st.session_state.current_index = 0

        st.session_state.answers = {}

        st.session_state.evaluations = {}

        st.session_state.answer_submitted = False

        st.session_state.voice_text_box_version = {}

        st.rerun()