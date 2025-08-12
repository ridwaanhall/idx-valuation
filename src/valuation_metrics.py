"""
Valuation Metrics Calculator

This module contains classes for calculating and analyzing different valuation ratios
including P/E, P/B, and PEG ratios with their respective benchmarks.
"""

from enum import Enum
from typing import Optional, Tuple
from dataclasses import dataclass


class ValuationStatus(Enum):
    """
    Enumeration for valuation status categories.
    """
    UNDERVALUED = "Undervalued"
    FAIRLY_VALUED = "Fairly Valued" 
    OVERVALUED = "Overvalued"
    INCONCLUSIVE = "Inconclusive"


@dataclass
class ValuationResult:
    """
    Data class to store the result of a valuation metric analysis.
    
    Attributes:
        metric_name (str): Name of the valuation metric (e.g., "P/E Ratio")
        current_value (float): Current value of the metric
        benchmark_value (float): Benchmark value for comparison
        status (ValuationStatus): Valuation status based on analysis
        confidence (str): Confidence level of the assessment
        reasoning (str): Explanation of the valuation conclusion
    """
    metric_name: str
    current_value: float
    benchmark_value: float
    status: ValuationStatus
    confidence: str
    reasoning: str


class PERAnalyzer:
    """
    Price-to-Earnings Ratio analyzer.
    
    Analyzes whether a stock is undervalued, fairly valued, or overvalued
    based on P/E ratio compared to historical and industry benchmarks.
    """
    
    def __init__(self, tolerance: float = 0.15):
        """
        Initialize P/E analyzer with tolerance level.
        
        Args:
            tolerance (float): Tolerance range for "fairly valued" assessment (default: 15%)
        """
        self.tolerance = tolerance
    
    def analyze(self, current_per: float, historical_per: float, industry_per: float) -> ValuationResult:
        """
        Analyze P/E ratio against benchmarks.
        
        Args:
            current_per (float): Current P/E ratio
            historical_per (float): Historical P/E ratio
            industry_per (float): Industry average P/E ratio
            
        Returns:
            ValuationResult: Analysis result with valuation status and reasoning
        """
        # Use the more conservative (higher) benchmark for safety
        benchmark = max(historical_per, industry_per)
        
        # Calculate percentage difference from benchmark
        difference_pct = (current_per - benchmark) / benchmark
        
        # Determine valuation status
        if difference_pct < -self.tolerance:
            status = ValuationStatus.UNDERVALUED
            confidence = "High" if abs(difference_pct) > 0.3 else "Moderate"
            reasoning = f"P/E ratio is {abs(difference_pct):.1%} below benchmark, suggesting undervaluation"
            
        elif difference_pct > self.tolerance:
            status = ValuationStatus.OVERVALUED
            confidence = "High" if difference_pct > 0.3 else "Moderate"
            reasoning = f"P/E ratio is {difference_pct:.1%} above benchmark, suggesting overvaluation"
            
        else:
            status = ValuationStatus.FAIRLY_VALUED
            confidence = "Moderate"
            reasoning = f"P/E ratio is within {self.tolerance:.0%} of benchmark, suggesting fair valuation"
        
        return ValuationResult(
            metric_name="P/E Ratio",
            current_value=current_per,
            benchmark_value=benchmark,
            status=status,
            confidence=confidence,
            reasoning=reasoning
        )


class PBVAnalyzer:
    """
    Price-to-Book Value ratio analyzer.
    
    Analyzes whether a stock is undervalued, fairly valued, or overvalued
    based on P/B ratio compared to historical and industry benchmarks.
    """
    
    def __init__(self, tolerance: float = 0.20):
        """
        Initialize P/B analyzer with tolerance level.
        
        Args:
            tolerance (float): Tolerance range for "fairly valued" assessment (default: 20%)
        """
        self.tolerance = tolerance
    
    def analyze(self, current_pbv: float, historical_pbv: float, industry_pbv: float) -> ValuationResult:
        """
        Analyze P/B ratio against benchmarks.
        
        Args:
            current_pbv (float): Current P/B ratio
            historical_pbv (float): Historical P/B ratio
            industry_pbv (float): Industry average P/B ratio
            
        Returns:
            ValuationResult: Analysis result with valuation status and reasoning
        """
        # Use the more conservative (higher) benchmark for safety
        benchmark = max(historical_pbv, industry_pbv)
        
        # Calculate percentage difference from benchmark
        difference_pct = (current_pbv - benchmark) / benchmark
        
        # Determine valuation status
        if difference_pct < -self.tolerance:
            status = ValuationStatus.UNDERVALUED
            confidence = "High" if abs(difference_pct) > 0.4 else "Moderate"
            reasoning = f"P/B ratio is {abs(difference_pct):.1%} below benchmark, suggesting undervaluation"
            
        elif difference_pct > self.tolerance:
            status = ValuationStatus.OVERVALUED
            confidence = "High" if difference_pct > 0.4 else "Moderate"
            reasoning = f"P/B ratio is {difference_pct:.1%} above benchmark, suggesting overvaluation"
            
        else:
            status = ValuationStatus.FAIRLY_VALUED
            confidence = "Moderate"
            reasoning = f"P/B ratio is within {self.tolerance:.0%} of benchmark, suggesting fair valuation"
        
        return ValuationResult(
            metric_name="P/B Ratio",
            current_value=current_pbv,
            benchmark_value=benchmark,
            status=status,
            confidence=confidence,
            reasoning=reasoning
        )


class PEGAnalyzer:
    """
    Price/Earnings-to-Growth ratio analyzer.
    
    Analyzes whether a stock is undervalued, fairly valued, or overvalued
    based on PEG ratio using standard benchmarks.
    """
    
    def analyze(self, peg_ratio: Optional[float]) -> ValuationResult:
        """
        Analyze PEG ratio against standard benchmarks.
        
        Standard PEG interpretation:
        - PEG < 1.0: Potentially undervalued
        - PEG = 1.0: Fairly valued
        - PEG > 1.0: Potentially overvalued
        
        Args:
            peg_ratio (float or None): Current PEG ratio (None if growth is zero)
            
        Returns:
            ValuationResult: Analysis result with valuation status and reasoning
        """
        if peg_ratio is None:
            return ValuationResult(
                metric_name="PEG Ratio",
                current_value=0.0,
                benchmark_value=1.0,
                status=ValuationStatus.INCONCLUSIVE,
                confidence="N/A",
                reasoning="Cannot calculate PEG ratio with zero or negative earnings growth"
            )
        
        benchmark = 1.0  # Standard PEG benchmark
        
        # Determine valuation status based on PEG ranges
        if peg_ratio < 0.5:
            status = ValuationStatus.UNDERVALUED
            confidence = "High"
            reasoning = f"PEG ratio of {peg_ratio:.2f} is significantly below 1.0, suggesting strong undervaluation"
            
        elif peg_ratio < 1.0:
            status = ValuationStatus.UNDERVALUED
            confidence = "Moderate"
            reasoning = f"PEG ratio of {peg_ratio:.2f} is below 1.0, suggesting potential undervaluation"
            
        elif peg_ratio <= 1.3:
            status = ValuationStatus.FAIRLY_VALUED
            confidence = "Moderate"
            reasoning = f"PEG ratio of {peg_ratio:.2f} is close to 1.0, suggesting fair valuation"
            
        elif peg_ratio <= 2.0:
            status = ValuationStatus.OVERVALUED
            confidence = "Moderate"
            reasoning = f"PEG ratio of {peg_ratio:.2f} is above 1.3, suggesting potential overvaluation"
            
        else:
            status = ValuationStatus.OVERVALUED
            confidence = "High"
            reasoning = f"PEG ratio of {peg_ratio:.2f} is significantly above 2.0, suggesting strong overvaluation"
        
        return ValuationResult(
            metric_name="PEG Ratio",
            current_value=peg_ratio,
            benchmark_value=benchmark,
            status=status,
            confidence=confidence,
            reasoning=reasoning
        )
