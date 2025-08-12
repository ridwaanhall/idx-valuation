"""
Stock Valuation Analyzer Main Class

This module contains the main StockValuationAnalyzer class that orchestrates
the complete valuation analysis using multiple metrics.
"""

from typing import List, Dict, Tuple
from collections import Counter

from .stock_data import StockData
from .valuation_metrics import (
    PERAnalyzer, PBVAnalyzer, PEGAnalyzer, 
    ValuationResult, ValuationStatus
)


class StockValuationAnalyzer:
    """
    Main class for comprehensive stock valuation analysis.
    
    This class coordinates the analysis of multiple valuation metrics
    and provides an overall valuation verdict with detailed explanations.
    """
    
    def __init__(self, per_tolerance: float = 0.15, pbv_tolerance: float = 0.20):
        """
        Initialize the stock valuation analyzer.
        
        Args:
            per_tolerance (float): Tolerance for P/E ratio analysis (default: 15%)
            pbv_tolerance (float): Tolerance for P/B ratio analysis (default: 20%)
        """
        self.per_analyzer = PERAnalyzer(tolerance=per_tolerance)
        self.pbv_analyzer = PBVAnalyzer(tolerance=pbv_tolerance)
        self.peg_analyzer = PEGAnalyzer()
    
    def analyze_stock(self, stock_data: StockData) -> Dict:
        """
        Perform comprehensive valuation analysis on stock data.
        
        Args:
            stock_data (StockData): Stock financial information
            
        Returns:
            Dict: Complete analysis results including individual metrics and overall verdict
        """
        # Calculate current ratios
        current_per = stock_data.get_current_per()
        current_pbv = stock_data.get_current_pbv()
        current_peg = stock_data.get_current_peg()
        
        # Perform individual metric analyses
        per_result = self.per_analyzer.analyze(
            current_per, 
            stock_data.historical_per, 
            stock_data.industry_per
        )
        
        pbv_result = self.pbv_analyzer.analyze(
            current_pbv,
            stock_data.historical_pbv,
            stock_data.industry_pbv
        )
        
        peg_result = self.peg_analyzer.analyze(current_peg)
        
        # Combine results for overall verdict
        results = [per_result, pbv_result, peg_result]
        overall_verdict = self._determine_overall_verdict(results)
        
        return {
            'stock_info': {
                'current_price': stock_data.current_price,
                'eps': stock_data.eps,
                'bvps': stock_data.bvps,
                'eps_growth': stock_data.eps_growth
            },
            'current_ratios': {
                'per': current_per,
                'pbv': current_pbv,
                'peg': current_peg
            },
            'individual_analyses': {
                'per_analysis': per_result,
                'pbv_analysis': pbv_result,
                'peg_analysis': peg_result
            },
            'overall_verdict': overall_verdict,
            'analysis_summary': self._generate_summary(stock_data, results, overall_verdict)
        }
    
    def _determine_overall_verdict(self, results: List[ValuationResult]) -> Dict:
        """
        Determine overall valuation verdict from individual metric results.
        
        Uses a weighted voting system considering confidence levels and
        the consistency of signals across different metrics.
        
        Args:
            results (List[ValuationResult]): Individual metric analysis results
            
        Returns:
            Dict: Overall verdict with status, confidence, and reasoning
        """
        # Filter out inconclusive results for voting
        valid_results = [r for r in results if r.status != ValuationStatus.INCONCLUSIVE]
        
        if not valid_results:
            return {
                'status': ValuationStatus.INCONCLUSIVE,
                'confidence': 'Low',
                'reasoning': 'Insufficient data for reliable valuation assessment'
            }
        
        # Count votes with confidence weighting
        status_votes = Counter()
        confidence_weights = {'High': 2, 'Moderate': 1, 'Low': 0.5}
        
        for result in valid_results:
            weight = confidence_weights.get(result.confidence, 1)
            status_votes[result.status] += weight
        
        # Determine winning status
        winning_status = status_votes.most_common(1)[0][0]
        total_weight = sum(status_votes.values())
        winning_weight = status_votes[winning_status]
        
        # Calculate overall confidence based on consensus
        consensus_strength = winning_weight / total_weight
        
        if consensus_strength >= 0.75:
            overall_confidence = 'High'
        elif consensus_strength >= 0.5:
            overall_confidence = 'Moderate'
        else:
            overall_confidence = 'Low'
        
        # Generate reasoning
        agreeing_metrics = [r.metric_name for r in valid_results if r.status == winning_status]
        disagreeing_metrics = [r.metric_name for r in valid_results if r.status != winning_status]
        
        if disagreeing_metrics:
            reasoning = (f"Mixed signals: {', '.join(agreeing_metrics)} suggest {winning_status.value.lower()}, "
                        f"while {', '.join(disagreeing_metrics)} suggest otherwise")
        else:
            reasoning = f"All metrics ({', '.join(agreeing_metrics)}) consistently suggest {winning_status.value.lower()}"
        
        return {
            'status': winning_status,
            'confidence': overall_confidence,
            'reasoning': reasoning,
            'consensus_strength': consensus_strength
        }
    
    def _generate_summary(self, stock_data: StockData, results: List[ValuationResult], 
                         overall_verdict: Dict) -> str:
        """
        Generate a comprehensive analysis summary.
        
        Args:
            stock_data (StockData): Original stock data
            results (List[ValuationResult]): Individual metric results
            overall_verdict (Dict): Overall valuation verdict
            
        Returns:
            str: Formatted summary text
        """
        summary_lines = [
            "=== STOCK VALUATION ANALYSIS SUMMARY ===",
            "",
            f"Stock Price: ${stock_data.current_price:.2f}",
            f"Earnings Per Share: ${stock_data.eps:.2f}",
            f"Book Value Per Share: ${stock_data.bvps:.2f}",
            f"Earnings Growth Rate: {stock_data.eps_growth}%",
            "",
            "CURRENT RATIOS:",
            f"  • P/E Ratio: {stock_data.get_current_per():.2f}",
            f"  • P/B Ratio: {stock_data.get_current_pbv():.2f}",
        ]
        
        peg = stock_data.get_current_peg()
        if peg is not None:
            summary_lines.append(f"  • PEG Ratio: {peg:.2f}")
        else:
            summary_lines.append("  • PEG Ratio: N/A (zero growth)")
        
        summary_lines.extend([
            "",
            "INDIVIDUAL METRIC ANALYSIS:",
        ])
        
        for result in results:
            summary_lines.extend([
                f"  {result.metric_name}:",
                f"    Status: {result.status.value}",
                f"    Confidence: {result.confidence}",
                f"    Current: {result.current_value:.2f} | Benchmark: {result.benchmark_value:.2f}",
                f"    Reasoning: {result.reasoning}",
                ""
            ])
        
        summary_lines.extend([
            "OVERALL VERDICT:",
            f"  Status: {overall_verdict['status'].value}",
            f"  Confidence: {overall_verdict['confidence']}",
            f"  Consensus Strength: {overall_verdict.get('consensus_strength', 0):.1%}",
            f"  Reasoning: {overall_verdict['reasoning']}",
            "",
            "=== END OF ANALYSIS ==="
        ])
        
        return "\n".join(summary_lines)
    
    def quick_analysis(self, current_price: float, eps: float, bvps: float, eps_growth: float,
                      historical_per: float, industry_per: float, historical_pbv: float, 
                      industry_pbv: float) -> str:
        """
        Perform quick analysis with direct input parameters.
        
        Convenience method that creates StockData object and returns formatted summary.
        
        Args:
            current_price (float): Current stock price
            eps (float): Earnings per share
            bvps (float): Book value per share
            eps_growth (float): Earnings growth rate (%)
            historical_per (float): Historical P/E ratio
            industry_per (float): Industry P/E ratio
            historical_pbv (float): Historical P/B ratio
            industry_pbv (float): Industry P/B ratio
            
        Returns:
            str: Formatted analysis summary
        """
        try:
            stock_data = StockData(
                current_price=current_price,
                eps=eps,
                bvps=bvps,
                eps_growth=eps_growth,
                historical_per=historical_per,
                industry_per=industry_per,
                historical_pbv=historical_pbv,
                industry_pbv=industry_pbv
            )
            
            analysis = self.analyze_stock(stock_data)
            return analysis['analysis_summary']
            
        except ValueError as e:
            return f"Error in analysis: {str(e)}"
