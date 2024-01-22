from django.db import models


class Question(models.Model):
    problem = models.TextField()
    rationale = models.TextField()
    options = models.TextField()
    correct = models.CharField(max_length=1)
    annotated_formula = models.TextField()
    linear_formula = models.TextField()
    category = models.CharField(max_length=50)
    difficulty_score = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = "api_question"

    def calculate_answer(self):
        pass
        # Implement the logic to calculate the answer based on the expression
        # You can use a library like sympy for symbolic mathematics
        # Example:
        # from sympy import symbols, Eq, solve
        # n1, n4, const_100 = symbols('n1 n4 const_100')
        # expression = subtract(multiply(add(const_100, 20), divide(add(const_100, 5), const_100)), const_100)
        # answer = solve(expression.subs([(n1, value_1991), (n4, value_1993), (const_100, 100)]), const_100)
        # return answer

    def __str__(self):
        return self.problem
