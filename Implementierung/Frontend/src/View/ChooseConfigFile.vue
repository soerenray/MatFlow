<template>
  <v-app>
    <v-row>
      <div style="width: 300px; padding-left: 20px; padding-top: 20px">
        <v-card height="50px">
          <v-btn text>Workflow-instances names:</v-btn>
        </v-card>
        <v-card>
          <div
            v-for="workflowInstanceName in workflowInstancesName"
            :key="workflowInstanceName"
          >
            <v-col
              @click="
                setSelectedWorkflowInstanceNameAndResetConfigFileNameAndUpdatedConfigFiles(
                  workflowInstanceName
                )
              "
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
      <div style="width: 300px; padding-top: 20px">
        <v-card height="50px">
          <v-btn text>Config-file names:</v-btn>
        </v-card>
        <v-card>
          <div v-for="configFileName in configFilesName" :key="configFileName">
            <v-col
              @click="
                setSelectedConfigFileNameAndRequestConfigFileFromBackendServer(
                  configFileName
                )
              "
              :style="{ background: colorForConfigFileName(configFileName) }"
            >
              {{ configFileName }}
            </v-col>
            <v-divider></v-divider>
          </div>
        </v-card>
      </div>
      <div style="padding-left: 40 px; padding-top: 20px">
        <edit-key-value-pairs
          ref="editConfigFile"
          v-on:changeAllKeyValuePairs="changeAllKeyValuePairs"
          v-on:update="
            pushUpdatedConfigFilesToBackendServer
          "
          v-on:reset="resetChoosenConfigFileObject"
          :fileName="selectedConfigFileName"
          :keyValuePairsFromParent="keyValuePairs"
        ></edit-key-value-pairs>
      </div>
    </v-row>
  </v-app>
</template>

<script lang='ts'>
import Vue from "vue";

import EditKeyValuePairs from "./EditKeyValuePairs.vue";
import ChooseConfigFile from "../Model/ChooseConfigFile";
import ConfigFile from "../Classes/ConfigFile";
import BackendServerCommunicator from "../Controler/BackendServerCommunicator";

const backendServerCommunicatorObject = new BackendServerCommunicator();
const chooseConfigFileObject = new ChooseConfigFile();

export default {
  name: "ChooseConfigFile",
  components: {
    EditKeyValuePairs,
  },
  methods: {
    changeAllKeyValuePairs(configFileName: string, newKeyValuePairs: Array<[string, string]>) {
      this.getConfigFileFromUpdatedConfigFiles(configFileName).keyValuePairs.forEach(
        (keyValuePair: [string, string], index: number) => {
          keyValuePair[0] = newKeyValuePairs[index][0];
          keyValuePair[1] = newKeyValuePairs[index][1];
        }
      );
    },
    colorForConfigFileName: function (configFileName: string): string {
      if (this.selectedConfigFileName === configFileName) {
        return "#a9cce3";
      } else if (this.isConfigFileNameInUpdatedConfigFiles(configFileName)) {
        return "#a3e4d7";
      }
      return "#FFFFFF";
    },
    isConfigFileNameInUpdatedConfigFiles(configFileName: string): boolean {
      return this.updatedConfigFiles
        .map(function (configFile: ConfigFile) {
          return configFile.configFileName;
        })
        .indexOf(configFileName) === -1
        ? false
        : true;
    },
    getConfigFileFromUpdatedConfigFiles(configFileName: string): ConfigFile {
      let configFile = this.updatedConfigFiles.find(
        (configFile: ConfigFile) => {
          return configFileName === configFile.configFileName;
        }
      );
      if (configFile === undefined) {
        return new ConfigFile();
      }
      return configFile;
    },
    pushUpdatedConfigFilesToBackendServer(configFileName: string) {
      backendServerCommunicatorObject.pushConfigFilesWithWorkflowInstanceName(
        this.updatedConfigFiles,
        this.selectedWorkflowInstanceName
      );
    },
    resetChoosenConfigFileObject() {
      chooseConfigFileObject.workflowIntancesAndConfigFilesNames =
        backendServerCommunicatorObject.pullWorkflowInstancesNameAndConfigFilesName();
      this.updatedConfigFiles = [];
      this.chosenConfigFile =
        this.pullConfigFileWithConfigFileNameWithWorkflowInstanceName(
          this.selectedWorkflowInstanceName,
          this.selectedConfigFileName
        );
      this.updatedConfigFiles.push(this.chosenConfigFile);
    },
    pullConfigFileWithConfigFileNameWithWorkflowInstanceName(
      workflowInstanceName: string,
      configFileName: string
    ): ConfigFile {
      return backendServerCommunicatorObject.pullConfigFileWithConfigFileNameWithWorkflowInstanceName(
        workflowInstanceName,
        configFileName
      );
    },
    setSelectedWorkflowInstanceNameAndResetConfigFileNameAndUpdatedConfigFiles(
      selectedWorkflowInstanceName: string
    ) {
      this.selectedWorkflowInstanceName = selectedWorkflowInstanceName;
      this.selectedConfigFileName = "";
      this.updatedConfigFiles = [];
      this.chosenConfigFile = new ConfigFile();
    },
    setSelectedConfigFileNameAndRequestConfigFileFromBackendServer(
      selectedConfigFileName: string
    ) {
      this.selectedConfigFileName = selectedConfigFileName;
      if (
        !this.isConfigFileNameInUpdatedConfigFiles(this.selectedConfigFileName)
      ) {
        this.chosenConfigFile =
          backendServerCommunicatorObject.pullConfigFileWithConfigFileNameWithWorkflowInstanceName(
            this.selectedWorkflowInstanceName,
            this.selectedConfigFileName
          );
        this.updatedConfigFiles.push(this.chosenConfigFile);
      } else {
        this.chosenConfigFile = this.getConfigFileFromUpdatedConfigFiles(
          this.selectedConfigFileName
        );
      }
    },
  },
  computed: {
    keyValuePairs: function (): Array<[string, string]> {
      return this.chosenConfigFile.keyValuePairs;
    },
    workflowInstancesName: function (): string[] {
      return chooseConfigFileObject.workflowIntancesAndConfigFilesNames.map(
        (x) => x[0]
      );
    },
    configFilesName: function (): string[] {
      let indexOfSelectedWorkflowInstanceName =
        this.workflowInstancesName.indexOf(this.selectedWorkflowInstanceName);
      if (indexOfSelectedWorkflowInstanceName === -1) {
        return [];
      }
      return chooseConfigFileObject.workflowIntancesAndConfigFilesNames[
        indexOfSelectedWorkflowInstanceName
      ][1];
    },
    chosenConfigFile: {
      get: function (): ConfigFile {
        return chooseConfigFileObject.chosenConfigFile;
      },
      set: function (chosenConfigFile: ConfigFile) {
        chooseConfigFileObject.chosenConfigFile = chosenConfigFile;
      },
    },
    updatedConfigFiles: {
      get: function (): ConfigFile[] {
        return chooseConfigFileObject.updatedConfigFiles;
      },
      set: function (updatedConfigFiles: ConfigFile[]) {
        chooseConfigFileObject.updatedConfigFiles = updatedConfigFiles;
      },
    },
    selectedWorkflowInstanceName: {
      get: function (): string {
        return chooseConfigFileObject.selectedWorkflowInstanceName;
      },
      set: function (selectedWorkflowInstanceName: string) {
        chooseConfigFileObject.selectedWorkflowInstanceName =
          selectedWorkflowInstanceName;
      },
    },
    selectedConfigFileName: {
      get: function (): string {
        return chooseConfigFileObject.selectedConfigFileName;
      },
      set: function (selectedConfigFileName: string) {
        chooseConfigFileObject.selectedConfigFileName = selectedConfigFileName;
      },
    },
  },
  beforeCreate: function () {
    // Vue is oberserving data in the data property.
    // The object choosenConfigFileObject wouldn't update, when the parameters are
    // initialized in data
    // Vue.observable has to be used to make an object outside of data reactive: https:///// v3.vuejs.org/guide/reactivity-fundamentals.html#declaring-reactive-state
    Vue.observable(chooseConfigFileObject);
    chooseConfigFileObject.workflowIntancesAndConfigFilesNames =
      backendServerCommunicatorObject.pullWorkflowInstancesNameAndConfigFilesName();
  },
};
</script>