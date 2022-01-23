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
        <edit-config-file
          v-on:changeAllKeyValuePairs="changeAllKeyValuePairs"
          :fileName="selectedConfigFileName"
          :keyValuePairsFromParent="keyValuePairs"
        ></edit-config-file>
      </div>
    </v-row>
  </v-app>
</template>

<script lang='ts'>
import Vue from "vue";

import EditConfigFile from "./EditConfigFile.vue";
import ChooseConfigFile from "../Model/ChooseConfigFile";
import ConfigFile from "../Classes/ConfigFile";
import BackendServerCommunicator from "../Controler/BackendServerCommunicator";

let chooseConfigFileObject = new ChooseConfigFile();

export default {
  components: {
    EditConfigFile,
  },
  methods: {
    changeKeyValuePair(newKeyValuePair: [string, string], index: number) {
      this.keyValuePairs[index][0] = newKeyValuePair[0];
      this.keyValuePairs[index][1] = newKeyValuePair[1];
    },
    changeAllKeyValuePairs(newKeyValuePairs: Array<[string, string]>) {
      newKeyValuePairs.forEach(
        (newKeyValuePair: [string, string], index: number) => {
          this.changeKeyValuePair(newKeyValuePair, index);
        }
      );
      this.addConfigFileToUpdatedConfigFiles(this.chosenConfigFile);
    },
    addConfigFileToUpdatedConfigFiles(configFile: ConfigFile) {
      let isConfigFileInUpdatedConfigFiles =
        this.isConfigFileNameInUpdatedConfigFiles(configFile.configFileName);
      if (!isConfigFileInUpdatedConfigFiles) {
        this.updatedConfigFiles.push(configFile);
      }
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
    updatedConfigFilesToBackendServer() {
      BackendServerCommunicator.pushConfigFilesWithWorkflowInstanceName(
        chooseConfigFileObject.updatedConfigFiles,
        this.selectedWorkflowInstanceName
      );
    },
    setSelectedWorkflowInstanceNameAndResetConfigFileNameAndUpdatedConfigFiles(
      selectedWorkflowInstanceName: string
    ) {
      this.selectedWorkflowInstanceName = selectedWorkflowInstanceName;
      this.selectedConfigFileName = "";
      this.updatedConfigFiles = [];
    },
    setSelectedConfigFileNameAndRequestConfigFileFromBackendServer(
      selectedConfigFileName: string
    ) {
      this.selectedConfigFileName = selectedConfigFileName;
      this.chosenConfigFile =
        BackendServerCommunicator.pullConfigFileWithConfigFileNameWithWorkflowInstanceName(
          this.selectedWorkflowInstanceName,
          this.selectedConfigFileName
        );
      // Vue does not behave reactive on array's. Therefore the component edit-config-file would not // update properly, when the chosenConfigFile changes
      this.$forceUpdate();
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
      // The class ChoosenConfigFile has only one config file. Therefore it has to be checked if the configFile is udpated already
      set: function (chosenConfigFile: ConfigFile) {
        if (
          this.isConfigFileNameInUpdatedConfigFiles(
            chosenConfigFile.configFileName
          )
        ) {
          chooseConfigFileObject.chosenConfigFile =
            this.getConfigFileFromUpdatedConfigFiles(
              chosenConfigFile.configFileName
            );
        } else {
          chooseConfigFileObject.chosenConfigFile = chosenConfigFile;
        }
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
    // Vue is oberserving data in the $data property.
    // The object choosenConfigFileObject wouldn't update, when the parameters are
    // initialized in data
    // Vue.observable has to be used to make an object outside of data reactive: https:///// v3.vuejs.org/guide/reactivity-fundamentals.html#declaring-reactive-state
    Vue.observable(chooseConfigFileObject);
    chooseConfigFileObject.workflowIntancesAndConfigFilesNames =
      BackendServerCommunicator.pullWorkflowInstancesNameAndConfigFilesName();
  },
};
</script>