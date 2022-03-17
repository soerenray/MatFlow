from airflow.plugins_manager import AirflowPlugin

# Importing base classes that we need to derive
from airflow.models.baseoperator import BaseOperatorLink
from airflow.hooks.base_hook import BaseHook
from airflow.models import BaseOperator
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.executors.base_executor import BaseExecutor

# Will show up under airflow.hooks.test_plugin.PluginHook
class PluginHook(BaseHook):
    pass

# Will show up under airflow.operators.test_plugin.PluginOperatorflask_admin
class PluginOperator(BaseOperator):
    pass

# Will show up under airflow.sensors.test_plugin.PluginSensorOperator
class PluginSensorOperator(BaseSensorOperator):
    pass

# Will show up under airflow.executors.test_plugin.PluginExecutor
class PluginExecutor(BaseExecutor):
    pass

# Will show up under airflow.macros.test_plugin.plugin_macro
def plugin_macro():
    pass

appbuilder_mitem = {"name": "Frontend homepage",
                    "category": "Frontend",
                    "category_icon": "fa-th",
                    "href": "http://localhost:8081/LogIn"}

# Defining the plugin class
class AirflowTestPlugin(AirflowPlugin):
    name = "frontend_Link"
    operators = [PluginOperator]
    sensors = [PluginSensorOperator]
    hooks = [PluginHook]
    executors = [PluginExecutor]
    macros = [plugin_macro]
    appbuilder_menu_items = [appbuilder_mitem]