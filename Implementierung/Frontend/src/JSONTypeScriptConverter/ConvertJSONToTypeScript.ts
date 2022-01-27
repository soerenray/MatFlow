import ConfigFile from '../Classes/ConfigFile'
import User from '../Classes/User'
import Server from '../Classes/Server'
import Template from '../Classes/Template'
import WorkflowInstance from '../Classes/WorkflowInstance'

class ConvertJSONTOTypeScript{
    public templateToTS(json: object): Template { return }
    public workflowInstanceToTS(json: object): WorkflowInstance { return }
    public usersToTS(json: object): User[] { return }
    public serversToTS(json: object): Server[]  { return }
    public configFileToTS(json: object): ConfigFile { return }
}