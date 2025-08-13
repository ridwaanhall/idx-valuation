#!/usr/bin/env python3
"""
Test script for individual valuation methods.

This script demonstrates how to use each valuation method independently.
"""

import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.analyzer import StockValuationAnalyzer


def test_per_only():
    """Test P/E ratio analysis only."""
    print("="*60)
    print("TESTING P/E RATIO ANALYSIS ONLY")
    print("="*60)
    
    analyzer = StockValuationAnalyzer()
    
    # Test data for P/E analysis only
    result = analyzer.analyze_per_only(
        current_price=185.50,
        eps=6.15,
        historical_per=28.5,
        industry_per=25.0
    )
    
    print(result)
    print()


def test_pbv_only():
    """Test P/B ratio analysis only."""
    print("="*60)
    print("TESTING P/B RATIO ANALYSIS ONLY")
    print("="*60)
    
    analyzer = StockValuationAnalyzer()
    
    # Test data for P/B analysis only
    result = analyzer.analyze_pbv_only(
        current_price=185.50,
        bvps=4.25,
        historical_pbv=42.0,
        industry_pbv=35.0
    )
    
    print(result)
    print()


def test_peg_only():
    """Test PEG ratio analysis only."""
    print("="*60)
    print("TESTING PEG RATIO ANALYSIS ONLY")
    print("="*60)
    
    analyzer = StockValuationAnalyzer()
    
    # Test data for PEG analysis only
    result = analyzer.analyze_peg_only(
        current_price=185.50,
        eps=6.15,
        eps_growth=8.5
    )
    
    print(result)
    print()


def test_all_methods():
    """Test complete analysis with all methods."""
    print("="*60)
    print("TESTING COMPLETE ANALYSIS (ALL METHODS)")
    print("="*60)
    
    analyzer = StockValuationAnalyzer()
    
    # Complete test data
    result = analyzer.quick_analysis(
        current_price=185.50,
        eps=6.15,
        bvps=4.25,
        eps_growth=8.5,
        historical_per=28.5,
        industry_per=25.0,
        historical_pbv=42.0,
        industry_pbv=3.8
    )
    
    print(result)
    print()


def main():
    """Run all test scenarios."""
    print("STOCK VALUATION ANALYZER - INDIVIDUAL METHOD TESTING")
    print("This script demonstrates each valuation method working independently.")
    print()
    
    # Test individual methods
    test_per_only()
    test_pbv_only()
    test_peg_only()
    
    # Test complete analysis for comparison
    test_all_methods()
    
    print("="*60)
    print("TESTING COMPLETE")
    print("="*60)


if __name__ == "__main__":
    main()
