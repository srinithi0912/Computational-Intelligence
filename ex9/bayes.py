def bayes_theorem(p_b_a,p_a,p_b):
    p_a_b = (p_b_a * p_a)/p_b;
    return p_a_b;

p_b_a = float(input("Enter Probability of B given A (likelihood): "))
p_a = float(input("Enter the Probability of A (prior): "))
p_b = float(input("Enter the Probability of B (evidence): "))

res = bayes_theorem(p_b_a,p_a,p_b)
print(f"P(A|B) = {res:.3f}")
