<template>
  <v-app>
    <v-card>
      <v-card-title> Create new template </v-card-title>
      <div style="padding-left: 20px">
        <div v-if="selectedDrowpnItem == 'create workflow from template'">
          <v-row>
            <v-col>
              <v-text-field
                label="Name of the template"
                hide-details="auto"
              ></v-text-field>
            </v-col>
            <v-col>
              <v-select :items="templates" label="use predefined template">
              </v-select>
            </v-col>
            <v-col>
              <v-file-input label="import folder"> </v-file-input>
            </v-col>
            <v-col>
              <v-radio-group>
                <v-radio
                  :label="`Create template from empty document`"
                ></v-radio>
              </v-radio-group>
            </v-col>
            <v-col>
              <v-row>
                <v-btn color="blue">Edit</v-btn>
                <div style="padding-left: 80px">
                  <v-btn fab small color="#58D68D"><v-icon>add</v-icon></v-btn>
                </div>
              </v-row>
            </v-col>
            <v-col></v-col>
          </v-row>
        </div>
      </div>
      <div v-if="selectedDrowpnItem == 'import worfklow'">
        <v-file-input accept="image/*" label="Workflow-folder"></v-file-input>
      </div>
    </v-card>
  </v-app>
</template>

<script>
import CreateTemplate from "../Model/CreateTemplate";

let createTemplateObject = new CreateTemplate();

export default {
  data: function () {
    return {
      templates: createTemplateObject.templatesName,
      selectedDrowpnItem: "create workflow from template",
      dropwDown: ["import worfklow", "create workflow from template"],
    };
  },
};
</script>