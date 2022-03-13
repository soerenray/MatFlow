import ConfigFile from '@Classes/ConfigFile';
import Server from '@Classes/Server';
import User from '@Classes/User';
import Version from '@Classes/Version';

// @ts-ignore
/* eslint-disable */

function deepCopyJS(elem: any): any {
  return JSON.parse(JSON.stringify(elem));
}

function deepCopyUser(user: User): User {
  return new User(deepCopyJS(user.userName), deepCopyJS(user.userStatus), deepCopyJS(user.userPrivilege));
}

function deepCopyUsers(users: User[]): User[] {
  const tempUsers: User[] = [];
  users.forEach((user) => {
    tempUsers.push(deepCopyUser(user));
  });
  return tempUsers;
}

function deepCopyServer(server: Server): Server {
  return new Server(
    deepCopyJS(server.serverAddress),
    deepCopyJS(server.serverStatus),
    deepCopyJS(server.containerLimit),
    deepCopyJS(server.selectedForExecution),
    deepCopyJS(server.serverName),
    deepCopyStringTupleArray(server.serverResources),
  );
}

function deepCopyStringTuple(stringTupel: [string, string]): [string, string] {
  return [deepCopyString(stringTupel[0]), deepCopyString(stringTupel[1])];
}

function deepCopyStringTupleArray(stringTupels: Array<[string, string]>): Array<[string, string]> {
  const tempStringTupleArray: Array<[string, string]> = [];
  stringTupels.forEach((stringTuple) => {
    tempStringTupleArray.push(deepCopyStringTuple(stringTuple));
  });
  return tempStringTupleArray;
}

function deepCopyServers(servers: Server[]): Server[] {
  const tempServers: Server[] = [];
  servers.forEach((server) => {
    tempServers.push(deepCopyServer(server));
  });
  return tempServers;
}

function deepCopyVersion(version: Version): Version {
  return new Version(deepCopyJS(version.versionNumber), deepCopyJS(version.versionNote), deepCopyStringTupleArray(version.parameterChanges));
}

function deepCopyVersions(versions: Version[]): Version[] {
  const tempVersions: Version[] = [];
  versions.forEach((version) => {
    tempVersions.push(deepCopyVersion(version));
  });
  return tempVersions;
}

function deepCopyConfigFile(configFile: ConfigFile): ConfigFile {
  return new ConfigFile(deepCopyJS(configFile.configFileName), deepCopyStringTupleArray(configFile.keyValuePairs));
}

function deepCopyConfigFiles(configFiles: ConfigFile[]): ConfigFile[] {
  const tempConfigFiles: ConfigFile[] = [];
  configFiles.forEach((configFile) => {
    tempConfigFiles.push(deepCopyConfigFile(configFile));
  });
  return tempConfigFiles;
}

function deepCopyString(string: string): string {
  return JSON.parse(JSON.stringify(string));
}

function deepCopyStrings(strings: string[]): string[] {
  const tempStrings: string[] = [];
  strings.forEach((string) => {
    tempStrings.push(deepCopyString(string));
  });
  return tempStrings;
}

function deepCopyWorkflowInstancesNameAndConfigFilesName(workflowInstancesNameAndConfigFilesName: Array<[string, string[]]>): Array<[string, string[]]> {
  const tempCopyWorkflowInstancesNameAndConfigFilesName: Array<[string, string[]]> = [];
  workflowInstancesNameAndConfigFilesName.forEach((elem) => {
    tempCopyWorkflowInstancesNameAndConfigFilesName.push([deepCopyString(elem[0]), deepCopyStrings(elem[1])]);
  });
  return tempCopyWorkflowInstancesNameAndConfigFilesName;
}

function deepCopyworkflowInstanceNameAndConfigFiles(workflowInstanceNameAndConfigFiles: Array<[ConfigFile[], string]>): Array<[ConfigFile[], string]> {
  const tempworkflowInstanceNameAndConfigFiles: Array<[ConfigFile[], string]> = [];
  workflowInstanceNameAndConfigFiles.forEach((elem) => {
    tempworkflowInstanceNameAndConfigFiles.push([deepCopyConfigFiles(elem[0]), deepCopyString(elem[1])]);
  });
  return tempworkflowInstanceNameAndConfigFiles;
}

export {
  deepCopyUsers, deepCopyServers, deepCopyStrings, deepCopyVersions, deepCopyWorkflowInstancesNameAndConfigFilesName, deepCopyworkflowInstanceNameAndConfigFiles,
  deepCopyConfigFile,
};
