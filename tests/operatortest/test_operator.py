import unittest
from typing import Any

from plugins.operators.alternating_operator import (
    AlternatingOperator,
    ConditionOperator,
)
from airflow.models import BaseOperator


class PrintOperator(BaseOperator):
    def __init__(self, n, *args, **kwargs):
        self.n = n
        super(PrintOperator, self).__init__(*args, **kwargs)

    def execute(self, context: Any):
        self.n -= 1


class PrintOperatorContext(BaseOperator):
    def __init__(self, n, *args, **kwargs):
        self.n = n
        super(PrintOperatorContext, self).__init__(*args, **kwargs)
        self.out = ""

    def execute(self, context: str):
        self.n -= 1
        self.out += context

    def get_context(self) -> str:
        return "a"


class Print2Operator(ConditionOperator):
    def __init__(self, n, *args, **kwargs):
        self.n = n
        self.condition = True
        super(Print2Operator, self).__init__(condition=self.condition, *args, **kwargs)

    def execute(self, context: Any):
        if self.n == 0:
            self.condition = False
        else:
            self.n -= 1

    def get_condition(self):
        return self.condition


class Print2OperatorContext(ConditionOperator):
    def __init__(self, n, *args, **kwargs):
        self.n = n
        self.condition = True
        self.out = ""
        super(Print2OperatorContext, self).__init__(
            condition=self.condition, *args, **kwargs
        )

    def execute(self, context: Any):
        if self.n == 0:
            self.condition = False
        else:
            self.n -= 1
            self.out += context

    def get_condition(self):
        return self.condition

    def get_context(self) -> str:
        return "a"


class OperatorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.operators = [
            PrintOperator(n=4, task_id="1"),
            PrintOperator(n=4, task_id="2"),
        ]
        self.operators2 = [
            Print2Operator(n=4, task_id="5"),
            Print2Operator(n=4, task_id="6"),
        ]

    def test_numerical(self):
        alternating = AlternatingOperator(
            operators=self.operators, n_tasks=4, task_id="3"
        )
        alternating.execute("")
        self.assertEqual(self.operators[0].n, 0)
        self.assertEqual(self.operators[1].n, 0)

    def test_conditional(self):
        alternating = AlternatingOperator(operators=self.operators2, task_id="4")
        alternating.execute("")
        self.assertEqual(self.operators2[0].n, 0)
        self.assertEqual(self.operators2[1].n, 0)

    def test_numerical_with_context(self):
        operators = [
            PrintOperatorContext(n=4, task_id="10"),
            PrintOperatorContext(n=4, task_id="9"),
        ]
        alternating = AlternatingOperator(operators=operators, n_tasks=4, task_id="3")
        alternating.execute("")
        self.assertEqual(operators[0].n, 0)
        self.assertEqual(operators[1].n, 0)
        self.assertEqual(operators[1].out, "aaaa")
        self.assertEqual(operators[0].out, "aaaa")

    def test_conditional_with_context(self):
        operators = [
            Print2OperatorContext(n=4, task_id="8"),
            Print2OperatorContext(n=4, task_id="9"),
        ]
        alternating = AlternatingOperator(operators=operators, task_id="7")
        alternating.execute("")
        self.assertEqual(operators[0].n, 0)
        self.assertEqual(operators[1].n, 0)
        self.assertEqual(operators[1].out, "aaaa")
        self.assertEqual(operators[0].out, "aaaa")

    def test_conditional_wrong_class(self):
        with self.assertRaises(ValueError):
            # no n tasks -> conditional -> wrong class type
            alternating = AlternatingOperator(operators=self.operators, task_id="6")
            alternating.execute("")


# Note: we could also test two operators where one has a get_context function and one does not.
# That is overkill because of the if statement inside the loop: the context is fetched when the method is implemented


if __name__ == "__main__":
    unittest.main()
