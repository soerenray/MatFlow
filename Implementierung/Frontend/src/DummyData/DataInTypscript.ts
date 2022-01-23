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



//pullConfigFileWithConfigFileNameWithWorkflowIsntanceName
let wf1Conf1: ConfigFile = new ConfigFile('conf1', [['key1', 'val1'], ['key2', 'val2']])
let wf1Conf2: ConfigFile = new ConfigFile('conf2', [['key1', 'val1'], ['key2', 'val2'], ['key3', 'val3']])
let wf2Conf1: ConfigFile = new ConfigFile('conf3', [['key1', 'val1']])
let wf2Conf2: ConfigFile = new ConfigFile('conf1', [['key1', 'val1'], ['key2', 'val2']])
let wf2Conf3: ConfigFile = new ConfigFile('conf2', [['key1', 'val1'], ['key2', 'val2'], ['key3', 'val3']])

// pullVersionsWithWorkflowInstanceName
let versions: Version[] = [new Version('1.1', 'changed value of key1', [["key1: Ipsom lorum", "key1: lorem ipsum"], ["key1: xy", "key2: xy"],
["key3: 5.0 5.0", "key3: 'text'"]]), new Version('1.1.1', 'reverted previous change', [["key1: Ipsom lorum", "key1: lorem ipsum"], ["key1: xy", "key2: xy"],
["key3: 5.0 5.0", "key3: 'text'"]])]

// pullUsers
let users: User[] = [new User('name1', 'status1', 'privilege1'), new User('name2', 'status2', 'privilege2')]

// pullServers
// wont be implemented at the moement (time pressure)
export { templateNames, workflowInstancesNameAndConfigFilesName, wf1Conf1, wf1Conf2, wf2Conf1, wf2Conf2, wf2Conf3, versions, users }