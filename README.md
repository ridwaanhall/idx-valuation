# 📊 Stock Valuation Analyzer - Indonesian Market

A comprehensive Python application for evaluating whether Indonesian stocks are undervalued, fairly valued, or overvalued using three key financial ratios:

- **P/E Ratio (Price-to-Earnings)** - Compares current P/E with historical and industry benchmarks
- **P/B Ratio (Price-to-Book Value)** - Analyzes price relative to book value per share
- **PEG Ratio (Price/Earnings-to-Growth)** - Evaluates valuation considering earnings growth

Specifically designed for Indonesian Stock Exchange (IDX) with IDR currency formatting.

## 🚀 Features

- **Object-Oriented Design** - Clean, modular architecture
- **Individual Method Selection** - Choose specific valuation methods (PER, PBV, PEG, or All)
- **Comprehensive Analysis** - Multiple valuation metrics with confidence levels
- **Input Validation** - Robust error handling and data validation
- **Flexible Interface** - Interactive mode, programmatic API, and examples
- **Detailed Reporting** - Clear explanations and reasoning for each assessment
- **No External Dependencies** - Uses only Python standard library

## 📁 Project Structure

```txt
idx-valuation/
├── src/
│   ├── __init__.py           # Package initialization
│   ├── stock_data.py         # StockData class and validation
│   ├── valuation_metrics.py  # Individual metric analyzers
│   └── analyzer.py           # Main StockValuationAnalyzer class
├── main.py                   # Interactive application
├── examples.py               # Usage examples and demonstrations
├── requirements.txt          # Project dependencies
└── README.md                # This file
```

## 🛠️ Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/ridwaanhall/idx-valuation
   cd idx-valuation
   ```

2. **Create virtual environment:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **No additional packages required** - Uses Python standard library only

## 💻 Usage

### Interactive Mode

Run the main application and select which valuation method to use:

```bash
python main.py
```

You'll be prompted to choose from:

1. **PER** - Price-to-Earnings Ratio Analysis only
2. **PBV** - Price-to-Book Value Analysis only  
3. **PEG** - Price/Earnings-to-Growth Analysis only
4. **All** - Complete analysis using all methods

### Sample Analysis

Run with sample data (Bank Central Asia) and choose method:

```bash
python main.py --sample
```

### Individual Method Usage

Use specific valuation methods programmatically:

```python
from src.analyzer import StockValuationAnalyzer

analyzer = StockValuationAnalyzer()

# P/E Ratio Analysis Only
per_result = analyzer.analyze_per_only(
    current_price=9250.0,    # IDR
    eps=1150.0,              # IDR
    historical_per=8.5,
    industry_per=9.2
)

# P/B Ratio Analysis Only
pbv_result = analyzer.analyze_pbv_only(
    current_price=9250.0,    # IDR
    bvps=2850.0,             # IDR
    historical_pbv=3.2,
    industry_pbv=2.8
)

# PEG Ratio Analysis Only
peg_result = analyzer.analyze_peg_only(
    current_price=9250.0,    # IDR
    eps=1150.0,              # IDR
    eps_growth=12.5
)

print(per_result)  # Individual method results
```

### Complete Analysis

```python
from src.analyzer import StockValuationAnalyzer

# Create analyzer instance
analyzer = StockValuationAnalyzer()

# Quick analysis with all methods
result = analyzer.quick_analysis(
    current_price=9250.0,    # IDR
    eps=1150.0,              # IDR
    bvps=2850.0,             # IDR
    eps_growth=12.5,         # %
    historical_per=8.5,
    industry_per=9.2,
    historical_pbv=3.2,
    industry_pbv=2.8
)

print(result)
```

### Detailed Analysis

```python
from src.analyzer import StockValuationAnalyzer
from src.stock_data import StockData

# Create stock data object
stock_data = StockData(
    current_price=12500.0,   # IDR
    eps=950.0,               # IDR
    bvps=4200.0,             # IDR
    eps_growth=15.0,         # %
    historical_per=12.5,
    industry_per=14.2,
    historical_pbv=2.8,
    industry_pbv=3.1
)

# Perform detailed analysis
analyzer = StockValuationAnalyzer()
analysis = analyzer.analyze_stock(stock_data)

# Access individual components
print("Current Ratios:", analysis['current_ratios'])
print("Overall Verdict:", analysis['overall_verdict'])
```

## 📊 Input Parameters

| Parameter | Description | Type | Example |
|-----------|-------------|------|---------|
| `current_price` | Current market price per share | float | 9250.0 |
| `eps` | Earnings Per Share (annual) | float | 1150.0 |
| `bvps` | Book Value Per Share | float | 2850.0 |
| `eps_growth` | Earnings growth rate (%) | float | 12.5 |
| `historical_per` | Historical P/E ratio | float | 8.5 |
| `industry_per` | Industry average P/E ratio | float | 9.2 |
| `historical_pbv` | Historical P/B ratio | float | 3.2 |
| `industry_pbv` | Industry average P/B ratio | float | 2.8 |

*All price values are in Indonesian Rupiah (IDR)*

## 📈 Valuation Logic

### P/E Ratio Analysis

- Compares current P/E with historical and industry benchmarks
- Uses the higher (more conservative) benchmark
- Default tolerance: ±15 %

### P/B Ratio Analysis  

- Evaluates price relative to book value
- Compares with historical and industry averages
- Default tolerance: ±20%

### PEG Ratio Analysis

- Standard benchmarks:
  - PEG < 1.0: Potentially undervalued
  - PEG ≈ 1.0: Fairly valued
  - PEG > 1.0: Potentially overvalued

### Overall Verdict

- Weighted voting system across all metrics
- Considers confidence levels and consensus strength
- Provides clear reasoning for the final assessment

## 🔍 Examples

Run the examples script to see various scenarios:

```bash
python examples.py
```

This includes:

- Technology stock (high growth)
- Value stock (low growth)  
- Overvalued stock
- Zero growth stock
- Detailed analysis breakdown
- Error handling demonstration

## 🎯 Sample Output

```txt
=== STOCK VALUATION ANALYSIS SUMMARY ===

Stock Price: $185.50
Earnings Per Share: $6.15
Book Value Per Share: $4.25
Earnings Growth Rate: 8.5%

CURRENT RATIOS:
  • P/E Ratio: 30.16
  • P/B Ratio: 43.65
  • PEG Ratio: 3.55

INDIVIDUAL METRIC ANALYSIS:
  P/E Ratio:
    Status: Overvalued
    Confidence: Moderate
    Current: 30.16 | Benchmark: 28.50
    Reasoning: P/E ratio is 5.8% above benchmark, suggesting overvaluation

  P/B Ratio:
    Status: Overvalued  
    Confidence: High
    Current: 43.65 | Benchmark: 42.00
    Reasoning: P/B ratio is 3.9% above benchmark, suggesting overvaluation

  PEG Ratio:
    Status: Overvalued
    Confidence: High
    Current: 3.55 | Benchmark: 1.00
    Reasoning: PEG ratio of 3.55 is significantly above 2.0, suggesting strong overvaluation

OVERALL VERDICT:
  Status: Overvalued
  Confidence: High
  Consensus Strength: 100.0%
  Reasoning: All metrics (P/E Ratio, P/B Ratio, PEG Ratio) consistently suggest overvalued

=== END OF ANALYSIS ===
```

## ⚙️ Configuration

You can customize the tolerance levels for P/E and P/B analysis:

```python
# Custom tolerance levels
analyzer = StockValuationAnalyzer(
    per_tolerance=0.10,  # 10% tolerance for P/E
    pbv_tolerance=0.25   # 25% tolerance for P/B
)
```

## 🧪 Testing

The project includes comprehensive examples and error handling demonstrations. Run:

```bash
python examples.py
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📧 Support

For questions or issues, please open an issue in the repository or contact the development team.
A Python tool to assess whether a stock is undervalued or overpriced based on technical and fundamental indicators.
