from abc import ABC
from typing import List, Any
from airflow.models import BaseOperator


class ConditionOperator(BaseOperator, ABC):
    """
    The condition operator for the alternating operator without n tasks.
    """
    def __init__(self, condition: bool, *args, **kwargs):
        self.condition = condition
        super(ConditionOperator, self).__init__(*args, **kwargs)

    def get_condition(self):
        return self.condition


class AlternatingOperator(BaseOperator):
    """
    This operator enables users to design directed CYCLIC graphs.
    With this operator, you can plug in a list of operators, e.g. tasks, that you want to run
    for n amount of times or until a certain condition is not met anymore.
    Note that if you wish to refrain from using n_tasks and would rather base the number of executions on a given state,
    you have to use ConditionOperator operators.
    If one of your operators requires the context parameter in its execute function to be filled, be sure to
    implement a get_context() method in your operator.
    """

    ui_color = "white"
    ui_fgcolor = "black"

    def __init__(self, operators: List[BaseOperator], n_tasks: int = -1, *args, **kwargs):
        """
        constructs a new alternating operator
        Args:
            operators(List[BaseOperator]: list of tasks/ operators to be executed
            optional: n_tasks(int): number of times the loop is to be executed
        """
        self.loop_condition = True
        self.operators = operators
        self.n_tasks = n_tasks
        if self.n_tasks < 1:
            self.loop_type = "conditional"
        else:
            self.loop_type = "numerical"

        if self.loop_type == "conditional":
            self.__validify_ops()
        super(AlternatingOperator, self).__init__(*args, **kwargs)

    def execute(self, context: Any):
        """
        executes all operators. context is not relevant but wanted due to overriding
        """
        if self.loop_type == "numerical":
            for i in range(self.n_tasks):
                self.__loop_execute()

        elif self.loop_type == "conditional":
            while self.loop_condition:
                self.__loop_execute()
                self.__get_loop_condition()

    def __loop_execute(self):
        for operator in self.operators:
            if hasattr(operator, 'get_context') and callable(
                    operator.get_context):
                operator.execute(operator.get_context())
            else:
                operator.execute("")

    def __validify_ops(self):
        for operator in self.operators:
            if not isinstance(operator, ConditionOperator):
                raise ValueError("All Operators must be ConditionOperators!")

    def __get_loop_condition(self):
        for operator in self.operators:
            status = operator.get_condition()
            if not status:
                self.loop_condition = False
                break
