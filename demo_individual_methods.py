#!/usr/bin/env python3
"""
Comprehensive demo of the Stock Valuation Analyzer's individual method selection feature.

This script demonstrates:
1. Individual method analysis (PER, PBV, PEG)
2. Complete analysis with all methods
3. Different stock scenarios
4. Method-specific input requirements
"""

import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.analyzer import StockValuationAnalyzer


def demo_individual_methods():
    """Demonstrate individual method selection capabilities."""
    print("="*80)
    print("STOCK VALUATION ANALYZER - INDIVIDUAL METHOD SELECTION DEMO")
    print("="*80)
    print()
    
    analyzer = StockValuationAnalyzer()
    
    # Sample stock data for different scenarios
    scenarios = [
        {
            'name': 'Apple Inc. (AAPL)',
            'data': {
                'current_price': 185.50,
                'eps': 6.15,
                'bvps': 4.25,
                'eps_growth': 8.5,
                'historical_per': 28.5,
                'industry_per': 25.0,
                'historical_pbv': 42.0,
                'industry_pbv': 3.8
            }
        },
        {
            'name': 'Value Stock Example',
            'data': {
                'current_price': 45.20,
                'eps': 3.80,
                'bvps': 18.50,
                'eps_growth': 4.2,
                'historical_per': 15.5,
                'industry_per': 18.0,
                'historical_pbv': 2.8,
                'industry_pbv': 3.2
            }
        }
    ]
    
    methods = [
        ('PER', 'per'),
        ('PBV', 'pbv'), 
        ('PEG', 'peg'),
        ('Complete Analysis', 'all')
    ]
    
    for scenario in scenarios:
        print(f"📊 ANALYZING: {scenario['name']}")
        print("="*60)
        
        for method_name, method_code in methods:
            print(f"\n🔍 {method_name} Analysis:")
            print("-" * 40)
            
            try:
                if method_code == 'per':
                    result = analyzer.analyze_per_only(
                        current_price=scenario['data']['current_price'],
                        eps=scenario['data']['eps'],
                        historical_per=scenario['data']['historical_per'],
                        industry_per=scenario['data']['industry_per']
                    )
                elif method_code == 'pbv':
                    result = analyzer.analyze_pbv_only(
                        current_price=scenario['data']['current_price'],
                        bvps=scenario['data']['bvps'],
                        historical_pbv=scenario['data']['historical_pbv'],
                        industry_pbv=scenario['data']['industry_pbv']
                    )
                elif method_code == 'peg':
                    result = analyzer.analyze_peg_only(
                        current_price=scenario['data']['current_price'],
                        eps=scenario['data']['eps'],
                        eps_growth=scenario['data']['eps_growth']
                    )
                elif method_code == 'all':
                    result = analyzer.quick_analysis(**scenario['data'])
                
                print(result)
                
            except Exception as e:
                print(f"Error in {method_name} analysis: {e}")
        
        print("\n" + "="*80)
        print()


def demo_benefits():
    """Demonstrate the benefits of individual method selection."""
    print("🎯 BENEFITS OF INDIVIDUAL METHOD SELECTION:")
    print("="*60)
    print()
    
    benefits = [
        "✅ Focused Analysis: Get specific insights from one valuation method",
        "✅ Reduced Input: Only provide data needed for selected method",
        "✅ Quick Assessment: Fast analysis when you need specific metric",
        "✅ Educational: Learn how each method works independently",
        "✅ Flexibility: Choose method based on available data",
        "✅ Comparison: Easily compare different methods for same stock"
    ]
    
    for benefit in benefits:
        print(benefit)
    
    print()
    print("🎓 WHEN TO USE EACH METHOD:")
    print("-" * 30)
    print("📈 PER Analysis: When you want to compare valuation multiples")
    print("📚 PBV Analysis: For asset-heavy companies or book value focus")
    print("🚀 PEG Analysis: For growth stocks or when considering earnings growth")
    print("🔄 Complete Analysis: For comprehensive valuation assessment")
    print()


def main():
    """Run the comprehensive demo."""
    demo_benefits()
    demo_individual_methods()
    
    print("="*80)
    print("✨ DEMO COMPLETED SUCCESSFULLY!")
    print("="*80)
    print()
    print("To use interactively, run: python main.py")
    print("To test with sample data, run: python main.py --sample")


if __name__ == "__main__":
    main()
