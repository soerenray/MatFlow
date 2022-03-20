<template>
  <v-app>
    <div class="d-flex flex-row ma-4">
      <div style="min-width: 15%" class="mr-2">
        <v-card height="50px">
          <v-btn variant="text">Workflow-instances names:</v-btn>
        </v-card>
        <v-divider></v-divider>
        <v-card v-if="workflowInstancesName.length > 0">
          <div
            class="workflowInstanceName"
            v-for="workflowInstanceName in workflowInstancesName"
            :key="workflowInstanceName"
          >
            <v-col
              @click="
                setSelectedWorkflowInstanceNameAndResetConfigFileNameAndUpdatedConfigFiles(
                  workflowInstanceName
                )
              "
              style="background-color: white"
              v-if="selectedWorkflowInstanceName != workflowInstanceName"
            >
              {{ workflowInstanceName }}
            </v-col>
            <v-col
              v-if="selectedWorkflowInstanceName == workflowInstanceName"
              style="background-color: #a9cce3"
            >
              {{ workflowInstanceName }}
            </v-col>
            <v-divider></v-divider>
          </div>
        </v-card>
      </div>
      <div style="min-width: 15%" class="pr-2">
        <v-card height="50px">
          <v-btn variant="text">Config-file names:</v-btn>
        </v-card>
        <v-divider></v-divider>
        <v-card v-if="configFilesName.length > 0">
          <div
            class="configFileName"
            v-for="configFileName in configFilesName"
            :key="configFileName"
          >
            <v-col
              @click="
                setSelectedConfigFileNameAndRequestConfigFileFromBackendServer(
                  configFileName
                )
              "
              :style="{
                background: colorForConfigFileName(
                  updatedConfigFiles,
                  selectedConfigFileName,
                  configFileName
                ),
              }"
            >
              {{ configFileName }}
            </v-col>
            <v-divider></v-divider>
          </v-div>
        </v-card>
      </div>
      <edit-key-value-pairs
        v-on:changeAllKeyValuePairs="changeAllKeyValuePairs"
        v-on:update="pushUpdatedConfigFilesToBackendServer"
        v-on:reset="resetChoosenConfigFileObjects"
        :fileName="selectedConfigFileName"
        :keyValuePairsFromParent="keyValuePairs"
      ></edit-key-value-pairs>
    </div>
  </v-app>
</template>

<script lang='ts'>
// @ts-nocheck
import ChooseConfigFile from '@Model/ChooseConfigFile';
import ConfigFile from '@Classes/ConfigFile';
import BackendServerCommunicator from '@Controler/BackendServerCommunicator';
import EditKeyValuePairs from '@View/EditKeyValuePairs.vue';

export default {
  name: 'ChooseConfigFile',
  data() {
    return {
      backendServerCommunicatorObject: new BackendServerCommunicator(),
      chooseConfigFileObject: new ChooseConfigFile(),
    };
  },
  components: {
    EditKeyValuePairs,
  },
  methods: {
    changeAllKeyValuePairs(
      configFileName: string,
      newKeyValuePairs: Array<[string, string]>,
    ) {
      this.updateKeyValuePairs(
        // Gets the neccessary config file out of all config
        // files that were requested from the server
        this.getConfigFileFromUpdatedConfigFiles(
          this.updatedConfigFiles,
          configFileName,
        ).keyValuePairs,
        newKeyValuePairs,
      );
    },
    updateKeyValuePairs(
      oldKeyValuePairs: Array<[string, string]>,
      newKeyValuePairs: Array<[string, string]>,
    ) {
      oldKeyValuePairs.forEach(
        (keyValuePair: [string, string], index: number) => {
          /* eslint-disable no-param-reassign */
          [keyValuePair[0], keyValuePair[1]] = [
            newKeyValuePairs[index][0],
            newKeyValuePairs[index][1],
          ];
          /* eslint-enable no-param-reassign */
        },
      );
    },
    colorForConfigFileName(
      updatedConfigFiles: ConfigFile[],
      selectedConfigFileName: string,
      configFileName: string,
    ): string {
      if (selectedConfigFileName === configFileName) {
        return '#a9cce3';
      }
      if (
        this.isConfigFileNameInUpdatedConfigFiles(
          updatedConfigFiles,
          configFileName,
        )
      ) {
        return '#a3e4d7';
      }
      return '#FFFFFF';
    },
    isConfigFileNameInUpdatedConfigFiles(
      updatedConfigFiles: ConfigFile[],
      configFileName: string,
    ): boolean {
      if (updatedConfigFiles !== undefined) {
        return (
          updatedConfigFiles
            .map((configFile: ConfigFile) => configFile.configFileName)
            .indexOf(configFileName) !== -1
        );
      }
      return false;
    },
    getConfigFileFromUpdatedConfigFiles(
      updatedConfigFiles: ConfigFile[],
      configFileName: string,
    ): ConfigFile {
      const configFile = updatedConfigFiles.find(
        (updatedConfigFile: ConfigFile) => configFileName === updatedConfigFile.configFileName,
      );
      if (configFile === undefined) {
        throw new Error(`There is no configFile with name ${configFileName}`);
      }
      return configFile;
    },
    pushUpdatedConfigFilesToBackendServer() {
      this.backendServerCommunicatorObject.pushConfigFilesWithWorkflowInstanceName(
        this.updatedConfigFiles,
        this.selectedWorkflowInstanceName,
      );
    },
    async resetChoosenConfigFileObjects() {
      this.updatedConfigFiles = [];
      this.chooseConfigFileObject
        .workflowIntancesAndConfigFilesNames = await this.backendServerCommunicatorObject
          .pullWorkflowInstancesNameAndConfigFilesName();
      this.chosenConfigFile = await this.backendServerCommunicatorObject
        .pullConfigFileWithConfigFileNameWithWorkflowInstanceName(
          this.selectedWorkflowInstanceName,
          this.selectedConfigFileName,
        );
      this.updatedConfigFiles.push(this.chosenConfigFile);
    },
    setSelectedWorkflowInstanceNameAndResetConfigFileNameAndUpdatedConfigFiles(
      selectedWorkflowInstanceName: string,
    ) {
      this.selectedWorkflowInstanceName = selectedWorkflowInstanceName;
      this.selectedConfigFileName = '';
      this.updatedConfigFiles = [];
      this.chosenConfigFile = new ConfigFile();
    },
    async setSelectedConfigFileNameAndRequestConfigFileFromBackendServer(
      selectedConfigFileName: string,
    ) {
      this.selectedConfigFileName = selectedConfigFileName;
      if (
        !this.isConfigFileNameInUpdatedConfigFiles(
          this.updatedConfigFiles,
          this.selectedConfigFileName,
        )
      ) {
        this.chosenConfigFile = await this.backendServerCommunicatorObject
          .pullConfigFileWithConfigFileNameWithWorkflowInstanceName(
            this.selectedWorkflowInstanceName,
            this.selectedConfigFileName,
          );
        this.updatedConfigFiles.push(this.chosenConfigFile);
      } else {
        this.chosenConfigFile = this.getConfigFileFromUpdatedConfigFiles(
          this.updatedConfigFiles,
          this.selectedConfigFileName,
        );
      }
    },
  },
  computed: {
    keyValuePairs(): Array<[string, string]> {
      return this.chosenConfigFile.keyValuePairs;
    },
    workflowInstancesName(): string[] {
      return this.chooseConfigFileObject.workflowIntancesAndConfigFilesNames.map(
        (x) => x[0],
      );
    },
    configFilesName(): string[] {
      const indexOfSelectedWorkflowInstanceName = this.workflowInstancesName
        .indexOf(this.selectedWorkflowInstanceName);
      if (indexOfSelectedWorkflowInstanceName === -1) {
        return [];
      }
      return this.chooseConfigFileObject.workflowIntancesAndConfigFilesNames[
        indexOfSelectedWorkflowInstanceName
      ][1];
    },
    chosenConfigFile: {
      get(): ConfigFile {
        return this.chooseConfigFileObject.chosenConfigFile;
      },
      set(chosenConfigFile: ConfigFile) {
        this.chooseConfigFileObject.chosenConfigFile = chosenConfigFile;
      },
    },
    updatedConfigFiles: {
      get(): ConfigFile[] {
        return this.chooseConfigFileObject.updatedConfigFiles;
      },
      set(updatedConfigFiles: ConfigFile[]) {
        this.chooseConfigFileObject.updatedConfigFiles = updatedConfigFiles;
      },
    },
    selectedWorkflowInstanceName: {
      get(): string {
        return this.chooseConfigFileObject.selectedWorkflowInstanceName;
      },
      set(selectedWorkflowInstanceName: string) {
        this.chooseConfigFileObject.selectedWorkflowInstanceName = selectedWorkflowInstanceName;
      },
    },
    selectedConfigFileName: {
      get(): string {
        return this.chooseConfigFileObject.selectedConfigFileName;
      },
      set(selectedConfigFileName: string) {
        this.chooseConfigFileObject.selectedConfigFileName = selectedConfigFileName;
      },
    },
  },
  async created() {
    this.backendServerCommunicatorObject
      .pullWorkflowInstancesNameAndConfigFilesName()
      .then((res) => {
        res.forEach((elem) => {
          this.chooseConfigFileObject.workflowIntancesAndConfigFilesNames.push(
            elem,
          );
        });
      });
  },
};
</script>
