<template>
  <v-app>
    <v-card>
      <v-card-title> Create new template </v-card-title>
      <div style="padding-left: 20px">
        <v-row>
          <v-col>
            <v-text-field
              label="Name of the template"
              v-model='chosenTemplateName'
              hide-details="auto"
            ></v-text-field>
          </v-col>
          <v-col>
            <v-select
              :items="templatesName"
              v-model="chosenTemplateName"
              label="use predefined template"
            >
            </v-select>
          </v-col>
          <v-col>
            <v-file-input
              v-model="templateFolder"
              accept="application/zip"
              label="import folder"
            >
            </v-file-input>
          </v-col>
          <v-col>
            <v-radio-group>
              <v-radio :label="`Create template from empty document`"></v-radio>
            </v-radio-group>
          </v-col>
          <v-col>
            <v-row>
              <v-btn style="margin-top: 25px" color="blue">Edit</v-btn>
              <div style="padding-left: 80px; margin-top: 25px">
                <v-btn @click="pressSendButton" small color="#58D68D"><send-icon></send-icon></v-btn>
              </div>
            </v-row>
          </v-col>
          <v-col></v-col>
        </v-row>
      </div>
    </v-card>
  </v-app>
</template>

<script lang='ts'>
import Vue from "vue";
import CreateTemplate from "../Model/CreateTemplate";
import Template from "../Classes/Template";
import BackendServerCommunicator from "../Controler/BackendServerCommunicator";

const backendServerCommunicatorObject = new BackendServerCommunicator();
const createTemplateObject = new CreateTemplate();

export default {
  name: 'CreateTemplate',
  data: function () {
    return {};
  },
  methods: {
    pressSendButton() {
      this.pushTemplateObjectToBackend()
      this.resetView()
    },
    resetView() {
      backendServerCommunicatorObject.pullTemplatesName()
      createTemplateObject.setObjectToDefaultValues()
    },
    pushTemplateObjectToBackend() {
      backendServerCommunicatorObject.pushCreateTemplate(
        this.createTemplateObject()
      );
    },
    createTemplateObject(): Template {
      return new Template(
        this.templateBlueprintFile(),
        createTemplateObject.chosenTemplateName
      );
    },
    templateBlueprintFile(): File {
      if (createTemplateObject.templateFolder.name !== "emptyFile") {
        return createTemplateObject.templateFolder;
      } else if (createTemplateObject.templateFolder.name !== "emptyFile") {
        return createTemplateObject.templateFolder;
      }
      return new File([], "emptyFile", { type: "application/zip" });
    },
  },
  computed: {
    templatesName: {
      get: function () {
        return createTemplateObject.templatesName;
      },
      set: function (templatesName: string[]) {
        createTemplateObject.templatesName = templatesName;
      },
    },
    chosenTemplateName: {
      get: function (): string {
        return createTemplateObject.chosenTemplateName;
      },
      set: function (chosenTemplateName: string) {
        createTemplateObject.chosenTemplateName = chosenTemplateName;
      },
    },
    templateFolder: {
      get: function (): File {
        return createTemplateObject.templateFolder;
      },
      set: function (templateFolder: File) {
        createTemplateObject.templateFolder = templateFolder;
      },
    },
    dagFile: {
      get: function (): File {
        return createTemplateObject.dagFile;
      },
      set: function (dagFile: File) {
        createTemplateObject.dagFile = dagFile;
      },
    },
  },
  beforeCreate: function () {
    // Vue is oberserving data in the data property.
    // The object choosenConfigFileObject wouldn't update, when the parameters are
    // initialized in data
    // Vue.observable has to be used to make an object outside of data reactive: https:///// v3.vuejs.org/guide/reactivity-fundamentals.html#declaring-reactive-state
    Vue.observable(createTemplateObject);
    createTemplateObject.templatesName =
      backendServerCommunicatorObject.pullTemplatesName();
  },
};
</script>