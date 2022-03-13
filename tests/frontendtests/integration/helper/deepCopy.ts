import ConfigFile from "@Classes/ConfigFile"
import Server from "@Classes/Server"
import User from "@Classes/User"
import Version from "@Classes/Version"
import { config } from "cypress/types/bluebird"

function deepCopyJS(elem: any): any {
    return JSON.parse(JSON.stringify(elem))
}

function deepCopyUser(user: User): User {
    return new User(deepCopyJS(user.userName), deepCopyJS(user.userStatus), deepCopyJS(user.userPrivilege))
}

function deepCopyUsers(users: User[]): User[] {
    let tempUsers: User[] = []
    users.forEach(user => {
        tempUsers.push(deepCopyUser(user))
    })
    return tempUsers
}

function deepCopyServer(server: Server): Server {
    return new Server(deepCopyJS(server.serverAddress), deepCopyJS(server.serverStatus), deepCopyJS(server.containerLimit),
        deepCopyJS(server.selectedForExecution), deepCopyJS(server.serverName), deepCopyStringTupleArray(server.serverResources))
}

function deepCopyStringTuple(stringTupel: [string, string]): [string, string] {
    return [deepCopyString(stringTupel[0]), deepCopyString(stringTupel[1])]
}

function deepCopyStringTupleArray(stringTupels: Array<[string, string]>): Array<[string, string]> {
    let tempStringTupleArray: Array<[string, string]> = []
    stringTupels.forEach(stringTuple => {
        tempStringTupleArray.push(deepCopyStringTuple(stringTuple))
    })
    return tempStringTupleArray
}


function deepCopyServers(servers: Server[]): Server[] {
    let tempServers: Server[] = []
    servers.forEach(server => {
        tempServers.push(deepCopyServer(server))
    })
    return tempServers
}

function deepCopyVersion(version: Version): Version {
    return new Version(deepCopyJS(version.versionNumber), deepCopyJS(version.versionNote), deepCopyStringTupleArray(version.parameterChanges))
}

function deepCopyVersions(versions: Version[]): Version[] {
    let tempVersions: Version[] = []
    versions.forEach(version => {
        tempVersions.push(deepCopyVersion(version))
    })
    return tempVersions
}

function deepCopyConfigFile(configFile: ConfigFile): ConfigFile {
    return new ConfigFile(deepCopyJS(configFile.configFileName), deepCopyStringTupleArray(configFile.keyValuePairs))
}

function deepCopyConfigFiles(configFiles: ConfigFile[]): ConfigFile[] {
    let tempConfigFiles: ConfigFile[] = []
    configFiles.forEach(configFile => {
        tempConfigFiles.push(deepCopyConfigFile(configFile))
    })
    return tempConfigFiles
}

function deepCopyString(string: string): string {
    return JSON.parse(JSON.stringify(string))
}

function deepCopyStrings(strings: string[]): string[] {
    let tempStrings: string[] = []
    strings.forEach(string => {
        tempStrings.push(deepCopyString(string))
    })
    return tempStrings
}

function deepCopyWorkflowInstancesNameAndConfigFilesName(workflowInstancesNameAndConfigFilesName: Array<[string, string[]]>): Array<[string, string[]]> {
    let tempCopyWorkflowInstancesNameAndConfigFilesName: Array<[string, string[]]> = []
    workflowInstancesNameAndConfigFilesName.forEach(elem => {
        tempCopyWorkflowInstancesNameAndConfigFilesName.push([deepCopyString(elem[0]), deepCopyStrings(elem[1])])
    })
    return tempCopyWorkflowInstancesNameAndConfigFilesName
}


function deepCopyworkflowInstanceNameAndConfigFiles(workflowInstanceNameAndConfigFiles: Array<[ConfigFile[], string]>): Array<[ConfigFile[], string]> {
    let tempworkflowInstanceNameAndConfigFiles: Array<[ConfigFile[], string]> = []
    workflowInstanceNameAndConfigFiles.forEach(elem => {
        tempworkflowInstanceNameAndConfigFiles.push([deepCopyConfigFiles(elem[0]), deepCopyString(elem[1])])
    })
    return tempworkflowInstanceNameAndConfigFiles
}



export {
    deepCopyUsers, deepCopyServers, deepCopyStrings, deepCopyVersions, deepCopyWorkflowInstancesNameAndConfigFilesName, deepCopyworkflowInstanceNameAndConfigFiles,
    deepCopyConfigFile
}