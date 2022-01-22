<template>
  <v-app>
    <v-row>
      <div style="width: 300px; padding-left: 20px; padding-top: 20px">
        <v-card height="50px">
          <v-btn text>Workflow-instances names:</v-btn>
        </v-card>
        <v-card>
          <div v-for="instance in workflowInstance" :key="instance.name">
            <v-col @click='selectedWorkflowInstanceName=instance.name' v-if="selectedWorkflowInstanceName!=instance.name">
                {{ instance.name }}
            </v-col>
            <v-col v-if="selectedWorkflowInstanceName==instance.name" style="background-color: #a9cce3">
                {{ instance.name }}
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
          <div v-for="configFile in configFiles" :key="configFile.name">
            <v-col
              @click="selectedConfigFileName = configFile.name"
              v-if="selectedConfigFileName != configFile.name"
            >
              {{ configFile.name }}
            </v-col>
            <v-col
              v-if="selectedConfigFileName == configFile.name"
              style="background-color: #a9cce3"
            >
              <!-- style="background-color: #a3e4d7" -->
              {{ configFile.name }}
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
      if (keyValuePairToChangeIndex !== undefined) {
        this.keyValuePairs[keyValuePairToChangeIndex][0] =
          newKeyValuePair.keyName;
        this.keyValuePairs[keyValuePairToChangeIndex][1] =
          newKeyValuePair.keyValue;
        console.log(this.keyValuePairs);
      }
    },
    changeAllKeyValuePairs(
      newKeyValuePairs: keyValuePairsWithColorInterface[]
    ) {
      newKeyValuePairs.forEach((newKeyValuePair) => {
        this.changeKeyValuePair(newKeyValuePair);
      });
    },
  },
  data: function () {
    return {
      workflowInstance: [
        { colored: true, name: "WorkflowInstance1" },
        { colored: false, name: "WorkflowInstance2" },
        { colored: false, name: "WorkflowInstance3" },
        { colored: false, name: "WorkflowInstance4" },
        { colored: false, name: "WorkflowInstance5" },
      ],
      configFiles: [
        { colored: false, name: "configFile1" },
        { colored: true, name: "configFile2" },
        { colored: true, name: "configFile3" },
        { colored: false, name: "configFile4" },
        { colored: true, name: "configFile5" },
        { colored: false, name: "configFile6" },
        { colored: false, name: "configFile7" },
        { colored: true, name: "configFile8" },
      ],
    };
  },
  computed: {
    keyValuePairs: function (): Array<[string, string]> {
      return chooseConfigFileObject.chosenConfigFile.keyValuePairs;
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
    // Vue is oberserving data in the $data property
    // Vue.observable has to be used to make an object outside of data reactive: https://v3.vuejs.org/guide/reactivity-fundamentals.html#declaring-reactive-state
    Vue.observable(chooseConfigFileObject);
    Vue.observable(chooseConfigFileObject.selectedWorkflowInstanceName)
  },
};
</script>