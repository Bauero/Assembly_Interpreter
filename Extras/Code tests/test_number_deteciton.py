import pytest
from typing import Callable

# Import the functions to test
from program_code.helper_functions import (
    return_if_base_16_value,
    return_if_base_10_value,
    return_if_base_8_value,
    return_if_base_2_value,
)

@pytest.mark.parametrize("func, valid_cases, invalid_cases", [
    # Base 16 (Hexadecimal)
    (return_if_base_16_value,
     [("0ffh", "0ff"), ("123h", "123"), ("-0deadbeefh", "-0deadbeef"), ("0H", "0")],
     ["ffh", "123", "0x123h", "-0x123", "12gh", "abc", "0x1"]),
    
    # Base 10 (Decimal)
    (return_if_base_10_value,
     [("123", "123"), ("999d", "999"), ("-456D", "-456"), ("0d", "0"), ("-987", "-987")],
     ["d123", "-d", "123.5d", "12d3", "abc", "0x123"]),
    
    # Base 8 (Octal)
    (return_if_base_8_value,
     [("123o", "123"), ("777q", "777"), ("-10O", "-10"), ("777o", "777"), ("123q", "123")],
     ["08q", "123", "7778q", "0o89", "abc", "0x123"]),
    
    # Base 2 (Binary)
    (return_if_base_2_value,
     [("101b", "101"), ("1101B", "1101"), ("-1001b", "-1001"), ("-1B", "-1"), ("0b", "0")],
     ["b101", "-101", "102b", "12b", "abc", "0x101"]),
])
def test_number_validation(func: Callable[[str], str | None], valid_cases, invalid_cases):
    """Test the number validation functions"""
    
    # Check valid cases
    for input_value, expected_output in valid_cases:
        assert func(input_value) == expected_output, f"Failed for valid input: {input_value}"
    
    # Check invalid cases
    for input_value in invalid_cases:
        assert func(input_value) is None, f"Failed for invalid input: {input_value}"