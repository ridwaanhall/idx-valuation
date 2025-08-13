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


def select_valuation_method() -> str:
    """
    Interactive function to let user select which valuation method to use.
    
    Returns:
        str: Selected method ('per', 'pbv', 'peg', 'all')
    """
    print("=== STOCK VALUATION ANALYZER ===")
    print("Available Valuation Methods:")
    print("1. PER (Price-to-Earnings Ratio) Analysis")
    print("2. PBV (Price-to-Book Value) Analysis") 
    print("3. PEG (Price/Earnings-to-Growth) Analysis")
    print("4. Complete Analysis (All Methods)")
    print()
    
    while True:
        try:
            choice = input("Select method (1-4): ").strip()
            
            if choice == '1':
                return 'per'
            elif choice == '2':
                return 'pbv'
            elif choice == '3':
                return 'peg'
            elif choice == '4':
                return 'all'
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")
                
        except KeyboardInterrupt:
            print("\nSelection cancelled by user.")
            return None


def get_user_input(method: str) -> Dict[str, float]:
    """
    Interactive function to collect stock data from user input based on selected method.
    
    Args:
        method (str): Selected valuation method ('per', 'pbv', 'peg', 'all')
    
    Returns:
        Dict[str, float]: Dictionary containing required stock parameters for selected method
    """
    print(f"\nEntering data for {method.upper()} analysis:")
    print("Please enter the following stock information:")
    print()
    
    try:
        # Collect basic stock information (always needed)
        current_price = float(input("Current Stock Price ($): "))
        
        data = {'current_price': current_price}
        
        if method in ['per', 'peg', 'all']:
            eps = float(input("Earnings Per Share (EPS) ($): "))
            data['eps'] = eps
            
        if method in ['pbv', 'all']:
            bvps = float(input("Book Value Per Share (BVPS) ($): "))
            data['bvps'] = bvps
            
        if method in ['peg', 'all']:
            eps_growth = float(input("EPS Growth Rate (%): "))
            data['eps_growth'] = eps_growth
            
        # Collect benchmark information based on method
        if method in ['per', 'all']:
            print("\nP/E Benchmark Information:")
            historical_per = float(input("Historical P/E Ratio: "))
            industry_per = float(input("Industry Average P/E Ratio: "))
            data.update({
                'historical_per': historical_per,
                'industry_per': industry_per
            })
            
        if method in ['pbv', 'all']:
            print("\nP/B Benchmark Information:")
            historical_pbv = float(input("Historical P/B Ratio: "))
            industry_pbv = float(input("Industry Average P/B Ratio: "))
            data.update({
                'historical_pbv': historical_pbv,
                'industry_pbv': industry_pbv
            })
        
        # Fill in missing values with defaults for methods that don't need them
        defaults = {
            'eps': 0.0,
            'bvps': 0.0,
            'eps_growth': 0.0,
            'historical_per': 0.0,
            'industry_per': 0.0,
            'historical_pbv': 0.0,
            'industry_pbv': 0.0
        }
        
        for key, default_value in defaults.items():
            if key not in data:
                data[key] = default_value
        
        return data
        
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
    
    # Let user choose method for sample analysis too
    method = select_valuation_method()
    if method is None:
        return
    
    print(f"Using sample data for Apple Inc. (AAPL) with {method.upper()} analysis")
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
    
    if method == 'all':
        result = analyzer.quick_analysis(**sample_data)
    else:
        result = analyzer.quick_single_analysis(method, **sample_data)
    
    print(result)


def run_interactive_analysis():
    """
    Run interactive analysis with user-provided data.
    """
    # Let user select method first
    method = select_valuation_method()
    if method is None:
        return
    
    # Get input data based on selected method
    user_data = get_user_input(method)
    
    if user_data is None:
        return
    
    print("\n" + "="*50)
    print("ANALYZING...")
    print("="*50)
    
    try:
        analyzer = StockValuationAnalyzer()
        
        if method == 'all':
            result = analyzer.quick_analysis(**user_data)
        else:
            result = analyzer.quick_single_analysis(method, **user_data)
        
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
            print("  python main.py           - Interactive mode (choose method)")
            print("  python main.py --sample  - Run sample analysis (choose method)")
            print("  python main.py --help    - Show this help")
            print()
            print("Available Methods:")
            print("  1. PER - Price-to-Earnings Ratio Analysis")
            print("  2. PBV - Price-to-Book Value Analysis")
            print("  3. PEG - Price/Earnings-to-Growth Analysis")
            print("  4. All - Complete analysis using all methods")
        else:
            print("Unknown option. Use --help for usage information.")
    else:
        run_interactive_analysis()


if __name__ == "__main__":
    main()
