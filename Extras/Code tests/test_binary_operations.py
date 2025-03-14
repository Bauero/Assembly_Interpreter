import pytest
from program_code.helper_functions import binary_addition, binary_or, binary_xor # Replace 'your_module' with the actual module name

@pytest.mark.parametrize(
    "bit_no, n1, n2, carry, expected_output, expected_carry, expected_aux_carry",
    [
        # Simple addition (no carry)
        (8, list("00000000"), list("00000000"), 0, list("00000000"), 0, 0),  # 0 + 0 = 0
        (8, list("00000001"), list("00000001"), 0, list("00000010"), 0, 0),  # 1 + 1 = 2
        (8, list("00001111"), list("00000001"), 0, list("00010000"), 0, 1),  # 15 + 1 = 16 (auxiliary carry)

        # Addition with carry
        (8, list("11111111"), list("00000001"), 0, list("00000000"), 1, 1),  # 255 + 1 = 256 (carry)
        (8, list("10000000"), list("10000000"), 0, list("00000000"), 1, 0),  # 128 + 128 = 256 (carry)

        # Cases with initial carry
        (8, list("00000001"), list("00000001"), 1, list("00000011"), 0, 0),  # 1 + 1 + 1 = 3
        (8, list("01111111"), list("00000001"), 1, list("10000001"), 0, 1),  # 127 + 1 + 1 = 129 (auxiliary carry)
    ]
)
def test_binary_addition_8bit(bit_no, n1, n2, carry, expected_output, expected_carry, expected_aux_carry):
    result, final_carry, final_aux_carry = binary_addition(bit_no, n1, n2, carry)
    
    assert result == expected_output, f"Expected output: {expected_output}, but got {result}"
    assert final_carry == expected_carry, f"Expected carry: {expected_carry}, but got {final_carry}"
    assert final_aux_carry == expected_aux_carry, f"Expected auxiliary carry: {expected_aux_carry}, but got {final_aux_carry}"

@pytest.mark.parametrize(
    "bit_no, n1, n2, carry, expected_output, expected_carry, expected_aux_carry",
    [
        # Simple addition (no carry)
        (16, list("0000000000000000"), list("0000000000000000"), 0, list("0000000000000000"), 0, 0),
        (16, list("0000000000000001"), list("0000000000000001"), 0, list("0000000000000010"), 0, 0),
        (16, list("0000000011111111"), list("0000000000000001"), 0, list("0000000100000000"), 0, 1),  # Auxiliary carry

        # Addition with carry
        (16, list("1111111111111111"), list("0000000000000001"), 0, list("0000000000000000"), 1, 1),  # Overflow
        (16, list("1000000000000000"), list("1000000000000000"), 0, list("0000000000000000"), 1, 0),  # 32768 + 32768

        # Cases with initial carry
        (16, list("0000000000000001"), list("0000000000000001"), 1, list("0000000000000011"), 0, 0),
        (16, list("0111111111111111"), list("0000000000000001"), 1, list("1000000000000001"), 0, 1),
    ]
)
def test_binary_addition_16bit(bit_no, n1, n2, carry, expected_output, expected_carry, expected_aux_carry):
    result, final_carry, final_aux_carry = binary_addition(bit_no, n1, n2, carry)
    
    assert result == expected_output, f"Expected output: {expected_output}, but got {result}"
    assert final_carry == expected_carry, f"Expected carry: {expected_carry}, but got {final_carry}"
    assert final_aux_carry == expected_aux_carry, f"Expected auxiliary carry: {expected_aux_carry}, but got {final_aux_carry}"

@pytest.mark.parametrize(
    "bit_no, n1, n2, expected_output, expected_carry, expected_auxiliary_carry",
    [
        # 8-bit OR tests
        (8, list("00000000"), list("00000000"), list("00000000"), 0, 0),
        (8, list("00000000"), list("11111111"), list("11111111"), 0, 0),
        (8, list("10101010"), list("01010101"), list("11111111"), 0, 0),
        (8, list("11001100"), list("00110011"), list("11111111"), 0, 0),
        (8, list("00001111"), list("11110000"), list("11111111"), 0, 1),  # Auxiliary carry at bit 4

        # 16-bit OR tests
        (16, list("0000000000000000"), list("0000000000000000"), list("0000000000000000"), 0, 0),
        (16, list("0000000000000000"), list("1111111111111111"), list("1111111111111111"), 0, 0),
        (16, list("1010101010101010"), list("0101010101010101"), list("1111111111111111"), 0, 0),
        (16, list("1100110011001100"), list("0011001100110011"), list("1111111111111111"), 0, 0),
        (16, list("0000000011111111"), list("1111111100000000"), list("1111111111111111"), 0, 1),  # Auxiliary carry at bit 4
    ]
)
def test_binary_or(bit_no, n1, n2, expected_output, expected_carry, expected_auxiliary_carry):
    result, carry, aux_carry = binary_or(bit_no, n1, n2)  # Assuming function is defined
    assert result == expected_output, f"Expected output {expected_output}, got {result}"
    assert carry == expected_carry, f"Expected carry {expected_carry}, got {carry}"
    assert aux_carry == expected_auxiliary_carry, f"Expected auxiliary carry {expected_auxiliary_carry}, got {aux_carry}"

@pytest.mark.parametrize(
    "bit_no, n1, n2, expected_output, expected_carry, expected_auxiliary_carry",
    [
        # 8-bit XOR tests
        (8, list("00000000"), list("00000000"), list("00000000"), 0, 0),
        (8, list("00000000"), list("11111111"), list("11111111"), 0, 0),
        (8, list("10101010"), list("01010101"), list("11111111"), 0, 0),
        (8, list("11001100"), list("00110011"), list("11111111"), 0, 0),
        (8, list("00001111"), list("11110000"), list("11111111"), 0, 1),  # Auxiliary carry at bit 4

        # 16-bit XOR tests
        (16, list("0000000000000000"), list("0000000000000000"), list("0000000000000000"), 0, 0),
        (16, list("0000000000000000"), list("1111111111111111"), list("1111111111111111"), 0, 0),
        (16, list("1010101010101010"), list("0101010101010101"), list("1111111111111111"), 0, 0),
        (16, list("1100110011001100"), list("0011001100110011"), list("1111111111111111"), 0, 0),
        (16, list("0000000011111111"), list("1111111100000000"), list("1111111111111111"), 0, 1),  # Auxiliary carry at bit 4
    ]
)
def test_binary_xor(bit_no, n1, n2, expected_output, expected_carry, expected_auxiliary_carry):
    result, carry, aux_carry = binary_xor(bit_no, n1, n2)  # Assuming function is defined
    assert result == expected_output, f"Expected output {expected_output}, got {result}"
    assert carry == expected_carry, f"Expected carry {expected_carry}, got {carry}"
    assert aux_carry == expected_auxiliary_carry, f"Expected auxiliary carry {expected_auxiliary_carry}, got {aux_carry}"