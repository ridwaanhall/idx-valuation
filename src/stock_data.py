"""
Stock Data Model

This module contains the StockData class that represents stock information
and input validation for valuation analysis.
"""

from typing import Optional
from dataclasses import dataclass


@dataclass
class StockData:
    """
    Data class to store stock financial information for valuation analysis.
    
    This class encapsulates all the financial metrics required for stock valuation
    and provides input validation to ensure data integrity.
    
    Attributes:
        current_price (float): Current market price per share
        eps (float): Earnings Per Share (annual)
        bvps (float): Book Value Per Share
        eps_growth (float): Earnings growth rate (as percentage, e.g., 15.5 for 15.5%)
        historical_per (float): Historical P/E ratio for the stock
        industry_per (float): Industry average P/E ratio
        historical_pbv (float): Historical P/B ratio for the stock
        industry_pbv (float): Industry average P/B ratio
    """
    
    current_price: float
    eps: float
    bvps: float
    eps_growth: float
    historical_per: float
    industry_per: float
    historical_pbv: float
    industry_pbv: float
    
    def __post_init__(self):
        """
        Validate input data after initialization.
        
        Raises:
            ValueError: If any input values are invalid
        """
        self._validate_inputs()
    
    def _validate_inputs(self) -> None:
        """
        Validate all input parameters for logical consistency.
        
        Ensures that:
        - All financial values are positive (except EPS growth which can be negative)
        - Current price is greater than zero
        - Book value per share is positive
        - Ratios are within reasonable ranges
        
        Raises:
            ValueError: If validation fails
        """
        # Check for positive values where required
        if self.current_price <= 0:
            raise ValueError("Current price must be greater than zero")
        
        if self.eps <= 0:
            raise ValueError("Earnings Per Share (EPS) must be positive for P/E calculation")
        
        if self.bvps <= 0:
            raise ValueError("Book Value Per Share (BVPS) must be positive")
        
        # EPS growth can be negative (declining earnings)
        if not isinstance(self.eps_growth, (int, float)):
            raise ValueError("EPS growth must be a numeric value")
        
        # Check ratio values are reasonable
        if self.historical_per <= 0 or self.industry_per <= 0:
            raise ValueError("P/E ratios must be positive")
        
        if self.historical_pbv <= 0 or self.industry_pbv <= 0:
            raise ValueError("P/B ratios must be positive")
        
        # Sanity checks for extreme values
        if self.historical_per > 1000 or self.industry_per > 1000:
            raise ValueError("P/E ratios seem unreasonably high (>1000)")
        
        if self.historical_pbv > 100 or self.industry_pbv > 100:
            raise ValueError("P/B ratios seem unreasonably high (>100)")
    
    def get_current_per(self) -> float:
        """
        Calculate the current Price-to-Earnings ratio.
        
        Returns:
            float: Current P/E ratio (Price / EPS)
        """
        return self.current_price / self.eps
    
    def get_current_pbv(self) -> float:
        """
        Calculate the current Price-to-Book Value ratio.
        
        Returns:
            float: Current P/B ratio (Price / Book Value per Share)
        """
        return self.current_price / self.bvps
    
    def get_current_peg(self) -> Optional[float]:
        """
        Calculate the current Price/Earnings-to-Growth ratio.
        
        Returns:
            float or None: Current PEG ratio (P/E / Growth Rate) or None if growth is zero
        """
        if self.eps_growth == 0:
            return None  # Cannot calculate PEG with zero growth
        
        current_per = self.get_current_per()
        return current_per / self.eps_growth
    
    def __str__(self) -> str:
        """
        String representation of the stock data.
        
        Returns:
            str: Formatted string showing key stock metrics
        """
        return (f"Stock Data - Price: ${self.current_price:.2f}, "
                f"EPS: ${self.eps:.2f}, BVPS: ${self.bvps:.2f}, "
                f"Growth: {self.eps_growth}%")
