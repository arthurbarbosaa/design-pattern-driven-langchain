from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool

from src.llm import get_llm, get_runtime_model
from src.schemas import (
    CodeAnalysisResult,
    EvaluationResult,
    PatternDetectionResult,
    PatternRecommendationResult,
    RefactoredCodeResult,
)


# ========================
# CODE ANALYSIS
# ========================

@tool
def code_analysis_tool(code: str) -> dict:
    """
    Use this tool to understand the code before making any design decisions.

    It analyzes:
    - what the code does
    - how it is structured
    - potential design problems (code smells)

    This is usually the FIRST step in any reasoning process.
    """
    llm = get_llm()
    structured_llm = llm.with_structured_output(
        CodeAnalysisResult, include_raw=True)

    prompt = PromptTemplate(
        input_variables=["code"],
        template="""
You are a senior software architect performing a static code review.

Your task:
1. Summarize what the code does
2. Describe its structure (classes, functions, responsibilities)
3. Identify concrete code smells or design issues

Guidelines:
- Be precise and technical
- Do NOT suggest solutions yet
- Focus only on analysis
- Prefer bullet-like clarity internally, but return structured JSON

Code:
{code}
""",
    )

    chain = prompt | structured_llm
    result = chain.invoke({"code": code})

    parsed_result = result.get("parsed")
    runtime_model = get_runtime_model(result)
    print(f"tool=code_analysis_tool model={runtime_model}")

    if parsed_result is None:
        raise ValueError(
            "Tool code_analysis_tool did not produce parsed output")

    return parsed_result.model_dump()


# ========================
# PATTERN DETECTION
# ========================

@tool
def pattern_detection_tool(analysis: dict) -> dict:
    """
    Use this tool AFTER code analysis to identify:
    - existing design patterns
    - missing patterns that could solve detected problems
    """
    llm = get_llm()
    structured_llm = llm.with_structured_output(
        PatternDetectionResult, include_raw=True)

    prompt = PromptTemplate(
        input_variables=["analysis"],
        template="""
You are a software design expert specialized in design patterns.

Given a code analysis result:

1. Identify any design patterns already present in the system
2. Suggest design patterns that could improve the design

Guidelines:
- Base your reasoning strictly on the analysis input
- Do NOT invent patterns without evidence
- Suggested patterns must address specific code smells

Analysis:
{analysis}
""",
    )

    chain = prompt | structured_llm
    result = chain.invoke({"analysis": analysis})

    parsed_result = result.get("parsed")
    runtime_model = get_runtime_model(result)
    print(f"tool=pattern_detection_tool model={runtime_model}")

    if parsed_result is None:
        raise ValueError(
            "Tool pattern_detection_tool did not produce parsed output")

    return parsed_result.model_dump()


# ========================
# PATTERN RECOMMENDATION
# ========================

@tool
def pattern_recommendation_tool(detection_result: dict) -> dict:
    """
    Use this tool to decide the BEST pattern among the suggested ones.

    It must:
    - choose exactly one pattern
    - justify the choice
    - list alternatives
    """
    llm = get_llm()
    structured_llm = llm.with_structured_output(
        PatternRecommendationResult,
        include_raw=True,
    )

    prompt = PromptTemplate(
        input_variables=["detection_result"],
        template="""
You are a senior software architect making a design decision.

Based on the detected and suggested patterns:

1. Select exactly ONE best design pattern to apply
2. Justify why it is the best choice

Guidelines:
- Prioritize simplicity and maintainability
- Avoid over-engineering
- The chosen pattern must clearly solve the identified problems

Detection Result:
{detection_result}
""",
    )

    chain = prompt | structured_llm
    result = chain.invoke({"detection_result": detection_result})

    parsed_result = result.get("parsed")
    runtime_model = get_runtime_model(result)
    print(f"tool=pattern_recommendation_tool model={runtime_model}")

    if parsed_result is None:
        raise ValueError(
            "Tool pattern_recommendation_tool did not produce parsed output")

    return parsed_result.model_dump()


# ========================
# CODE GENERATION
# ========================

@tool
def code_generation_tool(pattern: str, code: str) -> dict:
    """
    Use this tool to refactor code by applying a specific design pattern.

    It must:
    - preserve original behavior
    - improve structure
    - apply the pattern correctly
    """
    llm = get_llm()
    structured_llm = llm.with_structured_output(
        RefactoredCodeResult, include_raw=True)

    prompt = PromptTemplate(
        input_variables=["pattern", "code"],
        template="""
You are a senior refactoring engineer.

Refactor the given code using the "{pattern}" design pattern.

Requirements:
- Preserve ALL existing behavior
- Improve structure and readability
- Properly implement the pattern (no fake usage)
- Reduce code smells if possible
- Keep code clean and minimal (avoid over-engineering)

Output rules:
- Return ONLY the full refactored source code
- Do NOT include explanations
- Do NOT use markdown formatting

Code:
{code}
""",
    )

    chain = prompt | structured_llm
    result = chain.invoke({"pattern": pattern, "code": code})

    parsed_result = result.get("parsed")
    runtime_model = get_runtime_model(result)
    print(f"tool=code_generation_tool model={runtime_model}")

    if parsed_result is None:
        raise ValueError(
            "Tool code_generation_tool did not produce parsed output")

    return parsed_result.model_dump()


# ========================
# EVALUATION
# ========================

@tool
def evaluation_tool(original_code: str, refactored_code: str) -> dict:
    """
    Use this tool to evaluate the quality of a refactoring.

    It compares:
    - improvements
    - drawbacks
    - overall quality score
    """
    llm = get_llm()
    structured_llm = llm.with_structured_output(
        EvaluationResult, include_raw=True)

    prompt = PromptTemplate(
        input_variables=["original_code", "refactored_code"],
        template="""
You are a software quality analyst.

Compare the original code and the refactored version.

Your tasks:
1. List concrete improvements (structure, readability, maintainability)
2. Identify possible drawbacks (complexity, over-engineering, unnecessary abstractions)

Guidelines:
- Be critical but fair
- Prefer objective arguments
- Avoid generic statements

=== Original Code ===
{original_code}

=== Refactored Code ===
{refactored_code}
""",
    )

    chain = prompt | structured_llm
    result = chain.invoke(
        {
            "original_code": original_code,
            "refactored_code": refactored_code,
        }
    )

    parsed_result = result.get("parsed")
    runtime_model = get_runtime_model(result)
    print(f"tool=evaluation_tool model={runtime_model}")

    if parsed_result is None:
        raise ValueError("Tool evaluation_tool did not produce parsed output")

    return parsed_result.model_dump()
