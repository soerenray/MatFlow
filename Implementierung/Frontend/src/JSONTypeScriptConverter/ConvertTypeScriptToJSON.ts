import ConfigFile from '../Classes/ConfigFile'
import User from '../Classes/User'
import Server from '../Classes/Server'
import Version from '../Classes/Version'
import Template from '../Classes/Template'
import WorkflowInstance from '../Classes/WorkflowInstance'

class ConvertTypeScriptTOJson{
    public userToJSON(user: User): object { return }
    public serverToJSON(server: Server): object { return }
    public configFilesToJSON( configFiles: ConfigFile[]): object { return }
    public templateToJSON(template: Template): object { return }
}