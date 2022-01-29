<template>
  <v-app>
    <v-card>
      <v-card-title> Create new template </v-card-title>
      <div style="padding-left: 20px">
        <v-row>
          <v-col>
            <v-text-field
              label="Name of the template"
              hide-details="auto"
            ></v-text-field>
          </v-col>
          <v-col>
            <v-select
              :items="templates"
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
              <v-btn color="blue">Edit</v-btn>
              <div style="padding-left: 80px">
                <v-btn fab small color="#58D68D"><plus-icon></plus-icon></v-btn>
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
import CreateTemplate from "../Model/CreateTemplate";

let createTemplateObject = new CreateTemplate();

export default {
  data: function () {
    return {
      templates: createTemplateObject.templatesName,
    };
  },
  computed: {
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
};
</script>