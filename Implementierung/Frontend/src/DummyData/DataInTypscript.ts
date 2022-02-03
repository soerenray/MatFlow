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
let wf2Conf1: ConfigFile = new ConfigFile('conf1', [['key1', 'val1']])
let wf2Conf2: ConfigFile = new ConfigFile('conf2', [['key1', 'val1'], ['key2', 'val2']])
let wf2Conf3: ConfigFile = new ConfigFile('conf3', [['key1', 'val1'], ['key2', 'val2'], ['key3', 'val3']])

function deepCopyConfigFile(configFile: ConfigFile): ConfigFile {
    return new ConfigFile(JSON.parse(JSON.stringify(configFile.configFileName)), JSON.parse(JSON.stringify(configFile.keyValuePairs)))
}

function getWfConf(wfConstName: string): ConfigFile {
    switch (wfConstName) {
        case "wf1conf1": return deepCopyConfigFile(wf1Conf1)
        case "wf1conf2": return deepCopyConfigFile(wf1Conf2)
        case "wf2conf1": return deepCopyConfigFile(wf2Conf1)
        case "wf2conf2": return deepCopyConfigFile(wf2Conf2)
        case "wf2conf3": return deepCopyConfigFile(wf2Conf3)
        default: return new ConfigFile()
    }
}

function setWfConf(wfConstName: string, configFile: ConfigFile) {
    switch (wfConstName) {
        case "wf1conf1": {
            wf1Conf1 = deepCopyConfigFile(configFile)
            break;
        }
        case "wf1conf2": {
            wf1Conf2 = deepCopyConfigFile(configFile)
            break
        }
        case "wf2conf1": {
            wf2Conf1 = deepCopyConfigFile(configFile)
            break
        }
        case "wf2conf2": {
            wf2Conf2 = deepCopyConfigFile(configFile)
            break
        }
        case "wf2conf3": {
            wf2Conf3 = deepCopyConfigFile(configFile)
            break
        }
    }

}

function deleteUser(user: User) {
    users = users.filter(userInUsers => { return user.userName !== userInUsers.userName })
}

function updateUser(user: User) {
    let userIndex = users.findIndex((userInUsers: User) => {
        return user.userName === userInUsers.userName
    })
    if (userIndex == -1) {
        return
    } else {
        users[userIndex] = user
    }
}

interface VersionsObject {
    workflowInstance1: Version[],
    workflowInstance2: Version[],
}

// pullVersionsWithWorkflowInstanceName
let versions: VersionsObject = {
    workflowInstance1: [new Version('1.1', 'changed value of key1', [["key1: Ipsom lorum", "key1: lorem ipsum"], ["key1: xy", "key2: xy"],
    ["key3: 5.0 5.0", "key3: 'text'"]]), new Version('1.1.1', 'reverted previous change', [["key1: Ipsom lorum", "key1: lorem ipsum"], ["key1: xy", "key2: xy"],
    ["key3: 5.0 5.0", "key3: 'text'"]])], workflowInstance2: [new Version('2.1', 'changed name of key3', [["key3: Foo bar", "key1: Foo bar"]]), new Version('2.2', 'fixed typo in key-value', [["key1: xy", "key1: xy"], ["key2: 42", "key2: 420"],
    ])]
}

// pullUsers
let users: User[] = [new User('name1', 'suspended', 'administrator'), new User('name2', 'pending', 'visitor')]

// pullServers
// wont be implemented at the moement (time pressure)
export { templateNames, workflowInstancesNameAndConfigFilesName, getWfConf, setWfConf, versions, users, deleteUser, updateUser }