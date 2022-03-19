<template>
  <v-app>
    <v-card>
      <v-card-title> Create new template </v-card-title>
      <div style="padding-left: 20px">
        <v-row>
          <v-col>
            <v-text-field
              id="nameOfTheTempalte"
              data-cy="nameOfTheTemplate"
              label="Name of the template"
              variant="contained"
              style="width: 300px"
              v-model="newTemplateName"
              hide-details="auto"
            ></v-text-field>
          </v-col>
          {{ chosenTemplateName }}
          <v-col>
            <v-select
              data-cy="selectTemplateNameFromDropdown"
              id="selectTemplateNameFromDropdown"
              :items="templatesName"
              variant="contained"
              style="width: 300px"
              v-model="chosenTemplateName"
              label="use predefined template"
            >
            </v-select>
          </v-col>
          <v-col>
            <v-file-input
              data-cy="fileInput"
              :loading="!isDagFileInBase64 && tempTextFile !== ''"
              @change="transformDagFileToBase64"
              id="fileInput"
              v-model="dagFileAsArray"
              variant="contained"
              style="width: 300px"
              :clearable="false"
              type="file"
              label="template-blueprint"
            >
            </v-file-input>
          </v-col>
          <v-col>
            <v-row style="padding-top: 25px">
              <v-dialog v-model="openEdit">
                <template v-slot:activator="{}">
                  <v-btn
                    data-cy="editTemplate"
                    color="blue"
                    @click="openEditAndWriteTotempTextFile"
                    >Edit</v-btn
                  >
                </template>
                <v-card style="width: 800px">
                  <v-card-title>Edit Dag-file</v-card-title>
                  <v-card-header>
                    <v-btn
                      data-cy="save"
                      @click="writeFromtempTextFileAndConvertToBase64"
                    >
                      Save
                    </v-btn>
                    <v-spacer></v-spacer>
                    <v-btn data-cy="close" @click="openEdit = false">
                      <v-icon> mdi-close </v-icon>
                    </v-btn>
                  </v-card-header>
                  <v-card-text>
                    <v-textarea
                      data-cy="textarea"
                      v-model="tempTextFile"
                      filled
                    ></v-textarea>
                  </v-card-text>
                </v-card>
              </v-dialog>
              <div style="padding-left: 25px">
                <v-btn
                  :disabled="!(isDagFileInBase64 && newTemplateName !== '')"
                  data-cy="sendTemplate"
                  @click="pressSendButton"
                  color="#58D68D"
                >
                  <v-icon> mdi-send </v-icon>
                </v-btn>
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
// @ts-nocheck
import CreateTemplate from '@Model/CreateTemplate';
import CreateTemplateCaretaker from '@Memento/CreateTemplateCaretaker';
import Template from '@Classes/Template';
import BackendServerCommunicator from '@Controler/BackendServerCommunicator';
import { fileToDataURLWithFunction } from '@Classes/base64Utility';

export default {
  name: 'CreateTemplate',
  data() {
    return {
      backendServerCommunicatorObject: new BackendServerCommunicator(),
      createTemplateObject: new CreateTemplate(),
      createTemplateCaretakerObject: new CreateTemplateCaretaker(),
    };
  },
  methods: {
    pullDagFileAndTransformDagFileToBase64() {
      console.log('hi');
      this.backendServerCommunicatorObject
        .pullDagFileByTemplateName(this.chosenTemplateName)
        .then((result) => {
          this.dagFile = result;
          this.transformDagFileToBase64();
        });
    },
    transformDagFileToBase64() {
      fileToDataURLWithFunction(
        this.dagFile,
        (input: ArrayBuffer, isConverted: boolean) => {
          this.dagFileInBase64 = input;
          this.isDagFileInBase64 = isConverted;
        },
      );
    },
    pressSendButton() {
      this.pushTemplateObjectToBackend();
      this.resetView();
    },
    async resetView() {
      await this.backendServerCommunicatorObject.pullTemplatesName();
      this.createTemplateObject.setCreateTemplateMemento(
        this.createTemplateCaretakerObject.createTemplateMementoObjects[0],
      );
      this.createTemplateObject.templatesName = await this.backendServerCommunicatorObject
        .pullTemplatesName();
    },
    pushTemplateObjectToBackend() {
      this.backendServerCommunicatorObject.pushCreateTemplate(
        this.createNewTemplateObject(this.dagFileInBase64, this.newTemplateName),
      );
    },
    createNewTemplateObject(
      templateBlueprintFile: File,
      templateName: string,
    ): Template {
      return new Template(templateBlueprintFile, templateName);
    },
    openEditAndWriteTotempTextFile() {
      this.openEdit = !this.openEdit;
      this.writeTotempTextFile();
    },
    writeTotempTextFile() {
      this.dagFile.text().then((text) => {
        this.tempTextFile = text;
      });
    },
    writeFromtempTextFileAndConvertToBase64() {
      this.dagFile = new File([this.tempTextFile], this.dagFile.name, {
        type: this.dagFile.type,
      });
      this.transformDagFileToBase64();
    },
  },
  computed: {
    newTemplateName: {
      get() {
        return this.createTemplateObject.newTemplateName;
      },
      set(newTemplateName: string) {
        this.createTemplateObject.newTemplateName = newTemplateName;
      },
    },
    templatesName: {
      get() {
        return this.createTemplateObject.templatesName;
      },
      set(templatesName: string[]) {
        this.createTemplateObject.templatesName = templatesName;
      },
    },
    chosenTemplateName: {
      get(): string {
        return this.createTemplateObject.chosenTemplateName;
      },
      set(chosenTemplateName: string) {
        this.createTemplateObject.chosenTemplateName = chosenTemplateName;
      },
    },
    dagFileAsArray: {
      get(): File[] {
        return [this.createTemplateObject.dagFile];
      },
      set(dagFileAsArray: File[]) {
        [this.createTemplateObject.dagFile] = dagFileAsArray;
      },
    },
    dagFile: {
      get(): File {
        return this.createTemplateObject.dagFile;
      },
      set(dagFile: File) {
        this.createTemplateObject.dagFile = dagFile;
      },
    },
    openEdit: {
      get(): boolean {
        return this.createTemplateObject.openEdit;
      },
      set(openEdit: File) {
        this.createTemplateObject.openEdit = openEdit;
      },
    },
    tempTextFile: {
      get(): string {
        return this.createTemplateObject.tempTextFile;
      },
      set(tempTextFile: string) {
        this.createTemplateObject.tempTextFile = tempTextFile;
      },
    },
    isDagFileInBase64: {
      get(): boolean {
        return this.createTemplateObject.isDagFileInBase64;
      },
      set(isDagFileInBase64: boolean) {
        this.createTemplateObject.isDagFileInBase64 = isDagFileInBase64;
      },
    },
    dagFileInBase64: {
      get(): ArrayBuffer {
        return this.createTemplateObject.dagFileInBase64;
      },
      set(dagFileInBase64: ArrayBuffer) {
        console.log('setting', dagFileInBase64);
        this.createTemplateObject.dagFileInBase64 = dagFileInBase64;
      },
    },
  },
  async created() {
    await this.backendServerCommunicatorObject
      .pullTemplatesName()
      .then((res) => {
        res.forEach((elem) => this.createTemplateObject.templatesName.push(elem));
      });
    // For now this is everything I want to recover
    this.createTemplateCaretakerObject.addCreateTemplateMementoObjectToArray(
      this.createTemplateObject.createTemplateMemento(),
    );
  },
  watch: {
    chosenTemplateName: {
      handler() {
        console.log('ho');
        this.pullDagFileAndTransformDagFileToBase64();
      },
    },
  },
};
</script>
