def calculate_net_salary(base_salary: float, deductions: float = 0.0, bonuses: float = 0.0) -> float:
    """Professional payroll calculation"""
    gross = base_salary + bonuses
    tax = gross * 0.1  # Simplified
    net = gross - deductions - tax
    return round(net, 2)

def generate_payslip(employee_name: str, month: str, base: float, net: float):
    """Generate payslip string or PDF in full impl"""
    return f"Payslip for {employee_name} - {month}\nBase: {base}\nNet: {net}"