# utils/cpf_validator.py
def is_valid_cpf(cpf: str) -> bool:
    # Remove non-digits and check length
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11:
        return False
    
    # Check if all digits are the same (invalid CPF)
    if cpf == cpf[0] * 11:
        return False
    
    # Calculate first check digit
    sum = 0
    for i in range(9):
        sum += int(cpf[i]) * (10 - i)
    digit1 = (sum * 10) % 11
    digit1 = 0 if digit1 >= 10 else digit1
    
    # Calculate second check digit
    sum = 0
    for i in range(10):
        sum += int(cpf[i]) * (11 - i)
    digit2 = (sum * 10) % 11
    digit2 = 0 if digit2 >= 10 else digit2
    
    # Verify check digits
    return digit1 == int(cpf[9]) and digit2 == int(cpf[10])
