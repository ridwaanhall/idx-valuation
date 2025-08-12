#!/usr/bin/env python3
"""
Stock Valuation Analyzer - Main Application

A comprehensive tool for evaluating stock valuations using P/E, P/B, and PEG ratios.
This script provides both interactive and programmatic interfaces for stock analysis.
"""

import sys
import os
from typing import Dict, Any

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.analyzer import StockValuationAnalyzer
from src.stock_data import StockData


def get_user_input() -> Dict[str, float]:
    """
    Interactive function to collect stock data from user input.
    
    Returns:
        Dict[str, float]: Dictionary containing all required stock parameters
    """
    print("=== STOCK VALUATION ANALYZER ===")
    print("Please enter the following stock information:")
    print()
    
    try:
        # Collect basic stock information
        current_price = float(input("Current Stock Price ($): "))
        eps = float(input("Earnings Per Share (EPS) ($): "))
        bvps = float(input("Book Value Per Share (BVPS) ($): "))
        eps_growth = float(input("EPS Growth Rate (%): "))
        
        print("\nBenchmark Information:")
        historical_per = float(input("Historical P/E Ratio: "))
        industry_per = float(input("Industry Average P/E Ratio: "))
        historical_pbv = float(input("Historical P/B Ratio: "))
        industry_pbv = float(input("Industry Average P/B Ratio: "))
        
        return {
            'current_price': current_price,
            'eps': eps,
            'bvps': bvps,
            'eps_growth': eps_growth,
            'historical_per': historical_per,
            'industry_per': industry_per,
            'historical_pbv': historical_pbv,
            'industry_pbv': industry_pbv
        }
        
    except ValueError as e:
        print(f"Error: Invalid input. Please enter numeric values only.")
        print(f"Details: {e}")
        return None
    except KeyboardInterrupt:
        print("\nAnalysis cancelled by user.")
        return None


def run_sample_analysis():
    """
    Run a sample analysis with predefined data for demonstration purposes.
    """
    print("=== RUNNING SAMPLE ANALYSIS ===")
    print("Using sample data for Apple Inc. (AAPL)")
    print()
    
    # Sample data - Apple Inc. example
    sample_data = {
        'current_price': 185.50,
        'eps': 6.15,
        'bvps': 4.25,
        'eps_growth': 8.5,
        'historical_per': 28.5,
        'industry_per': 25.0,
        'historical_pbv': 42.0,
        'industry_pbv': 3.8
    }
    
    analyzer = StockValuationAnalyzer()
    result = analyzer.quick_analysis(**sample_data)
    print(result)


def run_interactive_analysis():
    """
    Run interactive analysis with user-provided data.
    """
    user_data = get_user_input()
    
    if user_data is None:
        return
    
    print("\n" + "="*50)
    print("ANALYZING...")
    print("="*50)
    
    try:
        analyzer = StockValuationAnalyzer()
        result = analyzer.quick_analysis(**user_data)
        print(result)
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        print("Please check your input values and try again.")


def main():
    """
    Main application entry point.
    """
    if len(sys.argv) > 1:
        if sys.argv[1] == "--sample":
            run_sample_analysis()
        elif sys.argv[1] == "--help":
            print("Stock Valuation Analyzer")
            print("Usage:")
            print("  python main.py           - Interactive mode")
            print("  python main.py --sample  - Run sample analysis")
            print("  python main.py --help    - Show this help")
        else:
            print("Unknown option. Use --help for usage information.")
    else:
        run_interactive_analysis()


if __name__ == "__main__":
    main()
