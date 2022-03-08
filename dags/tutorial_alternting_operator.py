import datetime
from typing import Any

from operators.alternating_operator import AlternatingOperator, ConditionOperator
from airflow import DAG


class PrintOperator(ConditionOperator):

    def __init__(self, n, *args, **kwargs):
        self.n = n
        self.condition = True
        self.out = ""
        self.context = "a"
        super(PrintOperator, self).__init__(condition=self.condition, *args, **kwargs)

    def execute(self, context: Any):
        if self.n == 0:
            self.condition = False
        else:
            self.n -= 1
            self.out += self.context
            print(context)

    def get_condition(self):
        return self.condition

    def get_context(self) -> str:
        return self.context


with DAG(
    "tutorial_matflow",
    default_args={},
    description="This tutorial describes how to use the alternating operator",
    tags=['matflow_example'],
    start_date= datetime.datetime(2022, 1, 1, 1, 1, 1),
    # only one time execution (due to operator limits)
    schedule_interval='@once'
)as dag:
    operators = [PrintOperator(n=4, task_id="1"), PrintOperator(n=1, task_id="2")]
    alt_op = AlternatingOperator(operators=operators, task_id="3")
    end_op = PrintOperator(n=1,  task_id="4")

    alt_op >> end_op

