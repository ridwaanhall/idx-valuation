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
    
    def analyze_single_method(self, stock_data: StockData, method: str) -> Dict:
        """
        Perform analysis using a single valuation method.
        
        Args:
            stock_data (StockData): Stock financial information
            method (str): Method to use ('per', 'pbv', 'peg')
            
        Returns:
            Dict: Analysis results for the selected method
        """
        # Calculate current ratios
        current_per = stock_data.get_current_per()
        current_pbv = stock_data.get_current_pbv()
        current_peg = stock_data.get_current_peg()
        
        # Perform selected metric analysis
        if method == 'per':
            result = self.per_analyzer.analyze(
                current_per, 
                stock_data.historical_per, 
                stock_data.industry_per
            )
            current_ratios = {'per': current_per}
            
        elif method == 'pbv':
            result = self.pbv_analyzer.analyze(
                current_pbv,
                stock_data.historical_pbv,
                stock_data.industry_pbv
            )
            current_ratios = {'pbv': current_pbv}
            
        elif method == 'peg':
            result = self.peg_analyzer.analyze(current_peg)
            current_ratios = {'peg': current_peg}
            
        else:
            raise ValueError(f"Unknown method: {method}")
        
        return {
            'stock_info': {
                'current_price': stock_data.current_price,
                'eps': stock_data.eps,
                'bvps': stock_data.bvps,
                'eps_growth': stock_data.eps_growth
            },
            'current_ratios': current_ratios,
            'analysis_result': result,
            'analysis_summary': self._generate_single_method_summary(stock_data, result, method)
        }
    
    def _generate_single_method_summary(self, stock_data: StockData, result: ValuationResult, method: str) -> str:
        """
        Generate a summary for single method analysis.
        
        Args:
            stock_data (StockData): Original stock data
            result (ValuationResult): Single method analysis result
            method (str): Analysis method used
            
        Returns:
            str: Formatted summary text
        """
        summary_lines = [
            f"=== {method.upper()} VALUATION ANALYSIS ===",
            "",
            f"Stock Price: ${stock_data.current_price:.2f}",
        ]
        
        # Add relevant stock info based on method
        if method in ['per', 'peg']:
            summary_lines.append(f"Earnings Per Share: ${stock_data.eps:.2f}")
        if method == 'pbv':
            summary_lines.append(f"Book Value Per Share: ${stock_data.bvps:.2f}")
        if method == 'peg':
            summary_lines.append(f"Earnings Growth Rate: {stock_data.eps_growth}%")
        
        summary_lines.extend([
            "",
            "CURRENT RATIO:",
        ])
        
        # Add current ratio based on method
        if method == 'per':
            summary_lines.append(f"  • P/E Ratio: {stock_data.get_current_per():.2f}")
        elif method == 'pbv':
            summary_lines.append(f"  • P/B Ratio: {stock_data.get_current_pbv():.2f}")
        elif method == 'peg':
            peg = stock_data.get_current_peg()
            if peg is not None:
                summary_lines.append(f"  • PEG Ratio: {peg:.2f}")
            else:
                summary_lines.append("  • PEG Ratio: N/A (zero growth)")
        
        summary_lines.extend([
            "",
            "ANALYSIS RESULT:",
            f"  Status: {result.status.value}",
            f"  Confidence: {result.confidence}",
            f"  Current Value: {result.current_value:.2f}",
            f"  Benchmark Value: {result.benchmark_value:.2f}",
            f"  Reasoning: {result.reasoning}",
            "",
            "=== END OF ANALYSIS ==="
        ])
        
        return "\n".join(summary_lines)
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
            f"  Status: {overall_verdict}",
            "",
            "=== END OF ANALYSIS ==="
        ])
        
        return "\n".join(summary_lines)
    
    def quick_single_analysis(self, method: str, current_price: float, eps: float = 0.0, 
                             bvps: float = 0.0, eps_growth: float = 0.0,
                             historical_per: float = 0.0, industry_per: float = 0.0, 
                             historical_pbv: float = 0.0, industry_pbv: float = 0.0) -> str:
        """
        Perform quick analysis with a single method using direct input parameters.
        
        Args:
            method (str): Valuation method ('per', 'pbv', 'peg')
            current_price (float): Current stock price
            eps (float): Earnings per share (required for PER and PEG)
            bvps (float): Book value per share (required for PBV)
            eps_growth (float): Earnings growth rate (required for PEG)
            historical_per (float): Historical P/E ratio (required for PER)
            industry_per (float): Industry P/E ratio (required for PER)
            historical_pbv (float): Historical P/B ratio (required for PBV)
            industry_pbv (float): Industry P/B ratio (required for PBV)
            
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
            
            analysis = self.analyze_single_method(stock_data, method)
            return analysis['analysis_summary']
            
        except ValueError as e:
            return f"Error in {method.upper()} analysis: {str(e)}"
    
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
    
    def _determine_overall_verdict(self, results: Dict) -> str:
        """
        Determine overall verdict based on individual method results.
        
        Args:
            results (Dict): Dictionary containing individual analysis results
            
        Returns:
            str: Overall verdict (UNDERVALUED, FAIRLY VALUED, OVERVALUED)
        """
        verdicts = []
        
        if 'per_analysis' in results and results['per_analysis']['verdict'] != 'N/A':
            verdicts.append(results['per_analysis']['verdict'])
        if 'pbv_analysis' in results and results['pbv_analysis']['verdict'] != 'N/A':
            verdicts.append(results['pbv_analysis']['verdict'])
        if 'peg_analysis' in results and results['peg_analysis']['verdict'] != 'N/A':
            verdicts.append(results['peg_analysis']['verdict'])
        
        if not verdicts:
            return "INSUFFICIENT DATA"
        
        # Count verdicts
        undervalued_count = verdicts.count('UNDERVALUED')
        overvalued_count = verdicts.count('OVERVALUED')
        fairly_valued_count = verdicts.count('FAIRLY VALUED')
        
        # Determine overall verdict based on majority
        if undervalued_count > overvalued_count and undervalued_count > fairly_valued_count:
            return 'UNDERVALUED'
        elif overvalued_count > undervalued_count and overvalued_count > fairly_valued_count:
            return 'OVERVALUED'
        else:
            return 'FAIRLY VALUED'
    
    def analyze_per_only(self, current_price: float, eps: float, historical_per: float, 
                        industry_per: float) -> str:
        """
        Analyze only P/E ratio with minimal required parameters.
        
        Args:
            current_price (float): Current stock price
            eps (float): Earnings per share
            historical_per (float): Historical P/E ratio
            industry_per (float): Industry P/E ratio
            
        Returns:
            str: Formatted P/E analysis summary
        """
        try:
            # Validate only PER-specific inputs
            if current_price <= 0:
                raise ValueError("Current price must be positive")
            if eps <= 0:
                raise ValueError("Earnings Per Share (EPS) must be positive")
            if historical_per <= 0:
                raise ValueError("Historical P/E ratio must be positive")
            if industry_per <= 0:
                raise ValueError("Industry P/E ratio must be positive")
                
            # Calculate current P/E ratio
            current_per = current_price / eps
            
            # Perform P/E analysis
            result = self.per_analyzer.analyze(current_per, historical_per, industry_per)
            
            # Generate summary
            summary_lines = [
                "=== P/E RATIO VALUATION ANALYSIS ===",
                "",
                f"Stock Price: ${current_price:.2f}",
                f"Earnings Per Share: ${eps:.2f}",
                f"Current P/E Ratio: {current_per:.2f}",
                f"Historical P/E Ratio: {historical_per:.2f}",
                f"Industry P/E Ratio: {industry_per:.2f}",
                "",
                f"Analysis: {result.reasoning}",
                f"Verdict: {result.status.value}",
                ""
            ]
            
            return "\n".join(summary_lines)
            
        except ValueError as e:
            return f"Error in P/E analysis: {str(e)}"
    
    def analyze_pbv_only(self, current_price: float, bvps: float, historical_pbv: float, 
                        industry_pbv: float) -> str:
        """
        Analyze only P/B ratio with minimal required parameters.
        
        Args:
            current_price (float): Current stock price
            bvps (float): Book value per share
            historical_pbv (float): Historical P/B ratio
            industry_pbv (float): Industry P/B ratio
            
        Returns:
            str: Formatted P/B analysis summary
        """
        try:
            # Validate only PBV-specific inputs
            if current_price <= 0:
                raise ValueError("Current price must be positive")
            if bvps <= 0:
                raise ValueError("Book Value Per Share (BVPS) must be positive")
            if historical_pbv <= 0:
                raise ValueError("Historical P/B ratio must be positive")
            if industry_pbv <= 0:
                raise ValueError("Industry P/B ratio must be positive")
                
            # Calculate current P/B ratio
            current_pbv = current_price / bvps
            
            # Perform P/B analysis
            result = self.pbv_analyzer.analyze(current_pbv, historical_pbv, industry_pbv)
            
            # Generate summary
            summary_lines = [
                "=== P/B RATIO VALUATION ANALYSIS ===",
                "",
                f"Stock Price: ${current_price:.2f}",
                f"Book Value Per Share: ${bvps:.2f}",
                f"Current P/B Ratio: {current_pbv:.2f}",
                f"Historical P/B Ratio: {historical_pbv:.2f}",
                f"Industry P/B Ratio: {industry_pbv:.2f}",
                "",
                f"Analysis: {result.reasoning}",
                f"Verdict: {result.status.value}",
                ""
            ]
            
            return "\n".join(summary_lines)
            
        except ValueError as e:
            return f"Error in P/B analysis: {str(e)}"
    
    def analyze_peg_only(self, current_price: float, eps: float, eps_growth: float) -> str:
        """
        Analyze only PEG ratio with minimal required parameters.
        
        Args:
            current_price (float): Current stock price
            eps (float): Earnings per share
            eps_growth (float): Earnings growth rate (%)
            
        Returns:
            str: Formatted PEG analysis summary
        """
        try:
            # Validate only PEG-specific inputs
            if current_price <= 0:
                raise ValueError("Current price must be positive")
            if eps <= 0:
                raise ValueError("Earnings Per Share (EPS) must be positive")
            if eps_growth <= 0:
                raise ValueError("Earnings growth rate must be positive")
                
            # Calculate current P/E ratio and then PEG ratio
            current_per = current_price / eps
            current_peg = current_per / eps_growth
            
            # Perform PEG analysis
            result = self.peg_analyzer.analyze(current_peg)
            
            # Generate summary
            summary_lines = [
                "=== PEG RATIO VALUATION ANALYSIS ===",
                "",
                f"Stock Price: ${current_price:.2f}",
                f"Earnings Per Share: ${eps:.2f}",
                f"Earnings Growth Rate: {eps_growth}%",
                f"Current P/E Ratio: {current_per:.2f}",
                f"Current PEG Ratio: {current_peg:.2f}",
                "",
                f"Analysis: {result.reasoning}",
                f"Verdict: {result.status.value}",
                ""
            ]
            
            return "\n".join(summary_lines)
            
        except ValueError as e:
            return f"Error in PEG analysis: {str(e)}"
