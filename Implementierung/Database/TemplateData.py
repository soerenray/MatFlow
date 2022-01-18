import DatabaseTable
class TemplateData:
    __instance = None

    @staticmethod
    def get_instance():
        if TemplateData.__instance == None:
            TemplateData()
        return TemplateData.__instance

    def __init__(self):
        if TemplateData.__instance != None:
            #throw exception
        else:
            TemplateData.__instance = self


    def create_Template(template):
        """Create new template.

        Extended description of function.

        Args:
            template(Template): Template object to be used

        Returns:
            void

        """



    def get_Template_Name():
        """Return all template names.

        Extended description of function.

        Returns:
            str[]: list of all template names; empty list if none exist

        """



    def get_Template_By_Name(name):
        """Return a template.

        Search in Database for @name and construct a Template object if name exists.

        Args:
            name(str): name of template

        Returns:
            Template: Template object

        """
