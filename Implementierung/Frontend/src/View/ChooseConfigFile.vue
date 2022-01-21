<template>
  <v-app>
    <v-row>
      <div style="width: 300px; padding-left: 20px; padding-top: 20px">
        <v-card height="50px">
          <v-btn text>Workflow-instances names:</v-btn>
        </v-card>
        <v-card>
          <div v-for="instance in workflowInstance" :key="instance.name">
            <v-col v-if="!instance.colored">
              <v-btn large text>
                {{ instance.name }}
              </v-btn>
            </v-col>
            <v-col v-if="instance.colored" style="background-color: #A9CCE3">
              <v-btn large text>
                {{ instance.name }}
              </v-btn>
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
            <v-col v-if="!configFile.colored">
              <v-btn large text>
                {{ configFile.name }}
              </v-btn>
            </v-col>
            <v-col v-if="configFile.colored" style="background-color: #A3E4D7">
              <v-btn large text>
                {{ configFile.name }}
              </v-btn>
            </v-col>
            <v-divider></v-divider>
          </div>
        </v-card>
      </div>
      <div style="padding-left: 40 px; padding-top: 20px">
        <v-card style="background-color: #F7F9F9" width="700px" height="50px">
          <v-row>
            <div style="padding-left: 20px; padding-top: 5px">
              <v-btn color="yellow">revert all files</v-btn>
            </div>
            <v-spacer></v-spacer>
            <div style="padding-right: 20px; padding-top: 5px">
              <v-btn color="blue">Create new version</v-btn>
            </div>
          </v-row>
        </v-card>
        <edit-confifile :keyValuePairs="configFileValues"></edit-confifile>
        <v-card>
          <v-row>
            <div
              style="
                padding-top: 10px;
                padding-bottom: 10px;
                padding-left: 20px;
              "
            >
              <v-btn color="red"> Revert changes </v-btn>
            </div>
            <v-spacer></v-spacer>
            <div
              style="
                padding-top: 10px;
                padding-bottom: 10px;
                padding-right: 20px;
              "
            >
              <v-btn color="#28B463"> Apply changes </v-btn>
            </div>
          </v-row>
        </v-card>
      </div>
    </v-row>
  </v-app>
</template>
<script lang='ts'>
import EditConfifile from "./EditConfigFile.vue";
import ChooseConfigFile from '../Model/ChooseConfigFile'

let chooseConfigFileObject = new ChooseConfigFile()

export default {
  components: {
    EditConfifile,
  },
  methods: {
      changeKeyValuePair(newKeyValuePair: object) {
          let keyValuePairToChange = this.configFileValues.find((keyValuePair: object) => {
              keyValuePair.name === newKeyValuePair.originalKeyName
          })
          if(keyValuePairToChange !== undefined) {
              keyValuePairToChange.name = newKeyValuePair.name
              keyValuePairToChange.value = newKeyValuePair.value
          }
      },
      changeAllKeyValuePairs(newKeyValuePairs: object[]) {
          newKeyValuePairs.forEach(newKeyValuePair => {
              this.changeKeyValuePair(newKeyValuePair)
          });
      }
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
      configFileValues: [
        {
          name: "Key1",
          value: "lorem ipsum",
        },
        {
          name: "Key2",
          value: "[val1,val2,val3,val4]",
        },
        {
          name: "Key3",
          value: "50. 50. 50.",
        },
        {
          name: "Key4",
          value: "Value 1 #It could also be Value 2",
        },
        {
          name: "Key5",
          value: "function() {}",
        },
      ],
    };
  },
};
</script>