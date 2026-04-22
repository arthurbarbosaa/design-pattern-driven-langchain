from pydantic import BaseModel, Field
from typing import List


class CodeAnalysisResult(BaseModel):
    summary: str = Field(description="Summary of the code functionality")
    structure: str = Field(description="Description of the code structure")
    smells: List[str] = Field(description="List of identified code smells")


class PatternDetectionResult(BaseModel):
    detected_patterns: List[str] = Field(
        description="Design patterns already present in the code")
    suggested_patterns: List[str] = Field(
        description="Design patterns that could be applied")


class PatternRecommendationResult(BaseModel):
    pattern: str = Field(description="The recommended design pattern to apply")
    reasoning: str = Field(description="Reasoning behind this recommendation")
    alternatives: List[str] = Field(
        description="Alternative patterns considered")


class RefactoredCodeResult(BaseModel):
    refactored_code: str = Field(
        description="The full source code after applying the design pattern")


class EvaluationResult(BaseModel):
    improvements: List[str] = Field(
        description="List of improvements achieved")
    drawbacks: List[str] = Field(
        description="List of potential drawbacks of the refactoring")
