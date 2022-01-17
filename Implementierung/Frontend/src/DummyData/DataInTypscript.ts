import ConfigFile from '../Classes/ConfigFile'
import User from '../Classes/User'
import Server from '../Classes/Server'
import Version from '../Classes/Version'
import WorkflowInstance from '../Classes/WorkflowInstance'

// pullTemplates
let templateNames: string[] = [
    'template1',
    'template2',
    'template3',
]

// pullTemplateWithName
// not clear what the 'File' type is
// let template = new Template(template1File, 'tempalte1')

// pullWorkflowInstancesNameAndConfigFilesName
let workflowInstancesNameAndConfigFilesName: Array<[string, string[]]> = [
    ['workflowInstance1', [
        'conf1',
        'conf2'
    ]],
    ['workflowInstance2', [
        'conf1',
        'conf2',
        'conf3'
    ]]
]

// pullWorkflowInstancesName
let workflowInstancesName: string[] = ['workflowInstance1', 'workflowInstance2']


//pullConfigFileWithConfigFileNameWithWorkflowIsntanceName
let conf1: ConfigFile = new ConfigFile('conf1', [['key1', 'val1'], ['key2', 'val2']])

// pullVersionsWithWorkflowInstanceName
let versions: Version[] = [new Version('1.1', 'changed value of key1', [['key1', 'val2']]), new Version('1.1.1', 'reverted previous change', [['key1', 'val1']])]

// pullUsers
let users: User[] = [new User('name1', 'status1', 'privilege1'), new User('name2', 'status2', 'privilege2')]

// pullServers
// wont be implemented at the moement (time pressure)

export { templateNames, workflowInstancesNameAndConfigFilesName, workflowInstancesName, conf1, versions, users }