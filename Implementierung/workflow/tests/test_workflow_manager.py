from unittest import TestCase
from workflow.workflow_manager import WorkflowManager


class TestWorkflowManager(TestCase):
    def setUp(self):
        self.w_man = WorkflowManager.get_instance()
        other_w_man = WorkflowManager.get_instance()
        self.assertEqual(self.w_man, other_w_man)


class TestCreateNewVersion(TestWorkflowManager):
    pass


class TestGetVersionsFromWorkflowInstance(TestWorkflowManager):
    pass