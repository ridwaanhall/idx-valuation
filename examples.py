#!/usr/bin/env python3
"""
Example Usage of Stock Valuation Analyzer

This script demonstrates various ways to use the stock valuation analyzer
with different types of stocks and scenarios.
"""

import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.analyzer import StockValuationAnalyzer
from src.stock_data import StockData


def example_tech_stock():
    """
    Example analysis of a technology stock (high growth, high P/E).
    """
    print("=== EXAMPLE 1: TECHNOLOGY STOCK ===")
    print("Company: High-growth tech company")
    print()
    
    analyzer = StockValuationAnalyzer()
    
    # Tech stock example - high growth, high ratios
    result = analyzer.quick_analysis(
        current_price=250.00,    # Current stock price
        eps=8.50,                # Earnings per share
        bvps=15.00,              # Book value per share
        eps_growth=25.0,         # 25% earnings growth
        historical_per=35.0,     # Historical P/E ratio
        industry_per=30.0,       # Industry average P/E
        historical_pbv=18.0,     # Historical P/B ratio
        industry_pbv=15.0        # Industry average P/B
    )
    
    print(result)
    print("\n" + "="*80 + "\n")


def example_value_stock():
    """
    Example analysis of a value stock (low growth, low P/E).
    """
    print("=== EXAMPLE 2: VALUE STOCK ===")
    print("Company: Mature value company")
    print()
    
    analyzer = StockValuationAnalyzer()
    
    # Value stock example - low growth, low ratios
    result = analyzer.quick_analysis(
        current_price=45.00,     # Current stock price
        eps=4.20,                # Earnings per share
        bvps=28.00,              # Book value per share
        eps_growth=3.5,          # 3.5% earnings growth
        historical_per=12.0,     # Historical P/E ratio
        industry_per=14.0,       # Industry average P/E
        historical_pbv=1.8,      # Historical P/B ratio
        industry_pbv=2.2         # Industry average P/B
    )
    
    print(result)
    print("\n" + "="*80 + "\n")


def example_overvalued_stock():
    """
    Example analysis of a potentially overvalued stock.
    """
    print("=== EXAMPLE 3: POTENTIALLY OVERVALUED STOCK ===")
    print("Company: Overhyped stock with high ratios")
    print()
    
    analyzer = StockValuationAnalyzer()
    
    # Overvalued stock example - high ratios relative to benchmarks
    result = analyzer.quick_analysis(
        current_price=180.00,    # Current stock price
        eps=2.50,                # Earnings per share
        bvps=8.00,               # Book value per share
        eps_growth=5.0,          # 5% earnings growth
        historical_per=45.0,     # Historical P/E ratio
        industry_per=25.0,       # Industry average P/E
        historical_pbv=15.0,     # Historical P/B ratio
        industry_pbv=12.0        # Industry average P/B
    )
    
    print(result)
    print("\n" + "="*80 + "\n")


def example_zero_growth_stock():
    """
    Example analysis of a stock with zero earnings growth.
    """
    print("=== EXAMPLE 4: ZERO GROWTH STOCK ===")
    print("Company: Mature company with no growth")
    print()
    
    analyzer = StockValuationAnalyzer()
    
    # Zero growth stock example - PEG cannot be calculated
    result = analyzer.quick_analysis(
        current_price=65.00,     # Current stock price
        eps=5.20,                # Earnings per share
        bvps=45.00,              # Book value per share
        eps_growth=0.0,          # 0% earnings growth
        historical_per=15.0,     # Historical P/E ratio
        industry_per=13.0,       # Industry average P/E
        historical_pbv=1.5,      # Historical P/B ratio
        industry_pbv=1.8         # Industry average P/B
    )
    
    print(result)
    print("\n" + "="*80 + "\n")


def example_detailed_analysis():
    """
    Example showing detailed analysis with access to individual components.
    """
    print("=== EXAMPLE 5: DETAILED ANALYSIS ===")
    print("Company: Detailed breakdown of analysis components")
    print()
    
    # Create stock data
    stock_data = StockData(
        current_price=120.00,
        eps=7.50,
        bvps=22.00,
        eps_growth=12.0,
        historical_per=18.0,
        industry_per=20.0,
        historical_pbv=5.5,
        industry_pbv=4.8
    )
    
    # Perform detailed analysis
    analyzer = StockValuationAnalyzer()
    analysis = analyzer.analyze_stock(stock_data)
    
    # Print detailed breakdown
    print("STOCK INFORMATION:")
    for key, value in analysis['stock_info'].items():
        print(f"  {key}: {value}")
    
    print("\nCURRENT RATIOS:")
    for key, value in analysis['current_ratios'].items():
        if value is not None:
            print(f"  {key.upper()}: {value:.2f}")
        else:
            print(f"  {key.upper()}: N/A")
    
    print("\nINDIVIDUAL METRIC ANALYSIS:")
    for metric_name, result in analysis['individual_analyses'].items():
        print(f"\n  {result.metric_name}:")
        print(f"    Current Value: {result.current_value:.2f}")
        print(f"    Benchmark: {result.benchmark_value:.2f}")
        print(f"    Status: {result.status.value}")
        print(f"    Confidence: {result.confidence}")
        print(f"    Reasoning: {result.reasoning}")
    
    print(f"\nOVERALL VERDICT:")
    verdict = analysis['overall_verdict']
    print(f"  Status: {verdict['status'].value}")
    print(f"  Confidence: {verdict['confidence']}")
    print(f"  Reasoning: {verdict['reasoning']}")
    
    print("\n" + "="*80 + "\n")


def demonstrate_error_handling():
    """
    Demonstrate error handling with invalid inputs.
    """
    print("=== EXAMPLE 6: ERROR HANDLING ===")
    print("Demonstrating validation and error handling")
    print()
    
    analyzer = StockValuationAnalyzer()
    
    # Test with invalid data
    print("Testing with negative stock price:")
    try:
        result = analyzer.quick_analysis(
            current_price=-50.00,  # Invalid: negative price
            eps=5.00,
            bvps=20.00,
            eps_growth=10.0,
            historical_per=15.0,
            industry_per=18.0,
            historical_pbv=2.5,
            industry_pbv=3.0
        )
        print(result)
    except Exception as e:
        print(f"Expected error caught: {e}")
    
    print("\nTesting with zero EPS:")
    try:
        result = analyzer.quick_analysis(
            current_price=100.00,
            eps=0.00,              # Invalid: zero EPS
            bvps=20.00,
            eps_growth=10.0,
            historical_per=15.0,
            industry_per=18.0,
            historical_pbv=2.5,
            industry_pbv=3.0
        )
        print(result)
    except Exception as e:
        print(f"Expected error caught: {e}")
    
    print("\n" + "="*80 + "\n")


def main():
    """
    Run all examples.
    """
    print("STOCK VALUATION ANALYZER - EXAMPLES")
    print("="*80)
    print()
    
    # Run all examples
    example_tech_stock()
    example_value_stock()
    example_overvalued_stock()
    example_zero_growth_stock()
    example_detailed_analysis()
    demonstrate_error_handling()
    
    print("All examples completed!")


if __name__ == "__main__":
    main()
