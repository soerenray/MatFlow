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


    def create_Template(selftemplate):

        return


    def get_Template_Name():



    def get_Template_By_Name(name):
