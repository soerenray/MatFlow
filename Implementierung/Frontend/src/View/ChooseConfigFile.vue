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
                selectedWorkflowInstanceNameAndDeselectConfigFileName(
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
              @click="selectedConfigFileName = configFileName"
              v-if="selectedConfigFileName != configFileName"
            >
              {{ configFileName }}
            </v-col>
            <v-col
              v-if="selectedConfigFileName == configFileName"
              style="background-color: #a9cce3"
            >
              <!-- style="background-color: #a3e4d7" -->
              {{ configFileName }}
            </v-col>
            <v-divider></v-divider>
          </div>
        </v-card>
      </div>
      <div style="padding-left: 40 px; padding-top: 20px">
        <edit-confifile
          v-on:changeAllKeyValuePairs="changeAllKeyValuePairs"
          :keyValuePairs="keyValuePairs"
        ></edit-confifile>
      </div>
    </v-row>
  </v-app>
</template>

<script lang='ts'>
import Vue from "vue";

import EditConfifile from "./EditConfigFile.vue";
import ChooseConfigFile from "../Model/ChooseConfigFile";
import ConfigFile from "../Classes/ConfigFile";
import BackendServerCommunicator from "../Controler/BackendServerCommunicator";

let chooseConfigFileObject = new ChooseConfigFile();

interface keyValuePairsWithColorInterface {
  originalKeyName: string;
  keyName: string;
  keyValue: string;
  color1: string;
  color2: string;
}

export default {
  components: {
    EditConfifile,
  },
  methods: {
    changeKeyValuePair(newKeyValuePair: keyValuePairsWithColorInterface) {
      let keyValuePairToChangeIndex = this.keyValuePairs
        .map((keyValuePair: [string, string]) => {
          return keyValuePair[0];
        })
        .indexOf(newKeyValuePair.originalKeyName);
      this.keyValuePairs[keyValuePairToChangeIndex][0] =
        newKeyValuePair.keyName;
      this.keyValuePairs[keyValuePairToChangeIndex][1] =
        newKeyValuePair.keyValue;
    },
    changeAllKeyValuePairs(
      newKeyValuePairs: keyValuePairsWithColorInterface[]
    ) {
      newKeyValuePairs.forEach((newKeyValuePair) => {
        this.changeKeyValuePair(newKeyValuePair);
      });
    },
    selectedWorkflowInstanceNameAndDeselectConfigFileName(
      selectedWorkflowInstanceName: string
    ) {
      this.selectedWorkflowInstanceName = selectedWorkflowInstanceName;
      this.selectedConfigFileName = "";
    },
  },
  data: function () {
    return {};
  },
  computed: {
    keyValuePairs: function (): Array<[string, string]> {
      return chooseConfigFileObject.chosenConfigFile.keyValuePairs;
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
    choosenConfigFile: {
      get: function (): ChooseConfigFile {
        BackendServerCommunicator.pullConfigFileWithConfigFileNameWithWorkflowInstanceName(
          this.selectedWorkflowInstanceName,
          this.selectedConfigFileName
        );
      },
      set: function (chosenConfigFile: ConfigFile) {},
    },
    // choosenConfigFile: function(): ConfigFile {
    // return BackendServerCommunicator.pullConfigFileWithConfigFileNameWithWorkflowInstanceName(this.selectedWorkflowInstanceName, this.selectedConfigFileName)
    // },
  },
  beforeCreate: function () {
    // Vue is oberserving data in the $data property
    // Vue.observable has to be used to make an object outside of data reactive: https://v3.vuejs.org/guide/reactivity-fundamentals.html#declaring-reactive-state
    Vue.observable(chooseConfigFileObject);
  },
};
</script>