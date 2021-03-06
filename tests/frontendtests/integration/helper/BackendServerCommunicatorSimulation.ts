// This class simulates the BackendServerCommunicator and gives the option to set value
// where the BackendServerCommunicator only pulls values

// @ts-nocheck
/* eslint-disable */

import ConfigFile from '@Classes/ConfigFile';
import User from '@Classes/User';
import Server from '@Classes/Server';
import Version from '@Classes/Version';
import Template from '@Classes/Template';
import WorkflowInstance from '@Classes/WorkflowInstance';
import BackendServerCommunicator from '@Controler/BackendServerCommunicator';

import {
  deepCopyUsers, deepCopyServers, deepCopyStrings, deepCopyVersions,
  deepCopyWorkflowInstancesNameAndConfigFilesName,
  deepCopyworkflowInstanceNameAndConfigFiles, deepCopyConfigFile,
} from './deepCopy';

class BackendServerCommunicatorSimulation extends BackendServerCommunicator {
  private _users: User[] = []

  private _servers: Server[] = []

  private _configFile: ConfigFile = new ConfigFile()

  private _versions: Version[] = []

  private _templatesName: string[] = []

  private _workflowInstancesNameAndConfigFilesName: Array<[string, string[]]> = []

  private _workflowInstanceNameAndConfigFiles: Array<[ConfigFile[], string]> = []

  public get users(): User[] {
    return deepCopyUsers(this._users);
  }

  public set users(users: User[]) {
    this._users = deepCopyUsers(users);
  }

  public get servers(): Server[] {
    return deepCopyServers(this._servers);
  }

  public set servers(servers: Server[]) {
    this._servers = deepCopyServers(servers);
  }

  public get configFile(): ConfigFile {
    return deepCopyConfigFile(this._configFile);
  }

  public set configFile(configFile: ConfigFile) {
    this._configFile = deepCopyConfigFile(configFile);
  }

  public get templatesName(): string[] {
    return deepCopyStrings(this._templatesName);
  }

  public set templatesName(templatesName: string[]) {
    this._templatesName = deepCopyStrings(templatesName);
  }

  public get versions(): Version[] {
    return deepCopyVersions(this._versions);
  }

  public set versions(versions: Version[]) {
    this._versions = deepCopyVersions(versions);
  }

  public get workflowInstancesNameAndConfigFilesName(): Array<[string, string[]]> {
    return deepCopyWorkflowInstancesNameAndConfigFilesName(this
      ._workflowInstancesNameAndConfigFilesName);
  }

  public set workflowInstancesNameAndConfigFilesName(workflowInstancesNameAndConfigFilesName:
    Array<[string, string[]]>) {
    this._workflowInstancesNameAndConfigFilesName = deepCopyWorkflowInstancesNameAndConfigFilesName(workflowInstancesNameAndConfigFilesName);
  }

  public get workflowInstanceNameAndConfigFiles(): Array<[ConfigFile[], string]> {
    return deepCopyworkflowInstanceNameAndConfigFiles(this._workflowInstanceNameAndConfigFiles);
  }

  public set workflowInstanceNameAndConfigFiles(workflowInstanceNameAndConfigFiles:
    Array<[ConfigFile[], string]>) {
    this._workflowInstanceNameAndConfigFiles = deepCopyworkflowInstanceNameAndConfigFiles(workflowInstanceNameAndConfigFiles);
  }

  // push requests should make no impact
  public pushLogIn(userName: string, userPassword: string): void { }

  public pushCreateTemplate(template: Template): void { }

  public pushCreateWorkflowInstanceFromTemplate(workflowInstanceObject: WorkflowInstance): void { }

  public pushExistingWorkflowInstance(workflowInstanceAsZip: File): void { }

  public pushReplaceActiveVersionOfWorkflowInstance(workflowInstanceName: string, versionNumber: string): void { }

  public pushConfigFileWithConfigFileNameWithWorkflowInstanceName(configFiles: ConfigFile[], workflowInstanceName: string): void { }

  public pushUser(user: User): void { }

  public pushServer(server: Server): void { }

  public pushDeleteUser(user: User): void { }
}

export default BackendServerCommunicatorSimulation;
