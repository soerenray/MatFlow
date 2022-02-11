<template>
  <v-app>
    <div style="width: 700px">
      <v-card>
        <v-row>
          <v-col>
            <v-row style="padding-top: 10px">
              <div>
                <v-btn text color="primary"> Key name </v-btn>
              </div>
              <v-spacer></v-spacer>
              <div style="padding-right: 290px">
                <v-btn text color="primary"> Value </v-btn>
              </div>
            </v-row>
          </v-col>
          <v-col>
            <v-card
              style="background-color: #f7f9f9"
              width="700px"
              height="50px"
            >
              <v-row>
                <div style="padding-left: 20px; padding-top: 5px">
                  <v-btn @click="resetChoosenConfigFileObject" color="yellow"
                    >Pull from Server</v-btn
                  >
                </div>
                <v-spacer></v-spacer>
                <div style="padding-right: 20px; padding-top: 5px">
                  <v-btn
                    @click="pushUpdatedConfigFilesToBackendServer"
                    color="blue"
                    >Push to Server</v-btn
                  >
                </div>
              </v-row>
            </v-card>
          </v-col>
          <v-col>
            <v-card v-for="(keyValuePair, index) in keyValuePairs" :key="index">
              <v-row>
                <div style="padding-top: 15px; padding-left: 20px">
                  <v-text-field
                    @input="changeAllKeyValuePairs"
                    v-model="keyValuePair.keyName"
                    solo
                    dense
                  ></v-text-field>
                </div>
                <v-spacer></v-spacer>
                <div style="padding-top: 15px; padding-right: 50px">
                  <v-text-field
                    @input="changeAllKeyValuePairs"
                    v-model="keyValuePair.keyValue"
                    style="width: 400px"
                    dense
                  ></v-text-field>
                </div>
              </v-row>
            </v-card>
          </v-col>
        </v-row>
      </v-card>
    </div>
  </v-app>
</template>

<script lang='ts'>
import Vue from "vue";
import EditKeyValuePairs from "../Model/EditKeyValuePairs";

let editKeyValuePairsObject = new EditKeyValuePairs();

interface KeyValuePair {
  _keyName: string;
  keyValuePairInstance: any;
  keyName: string;
  keyValue: string;
}

export default {
  name: "EditKeyValuePairs",
  // details: https://frontendsociety.com/using-a-typescript-interfaces-and-types-as-a-prop-type-in-vuejs-508ab3f83480
  props: {
    keyValuePairsFromParent: {
      type: Array as () => Array<[string, string]>,
    },
    // Vue type-syntax
    fileName: String,
  },
  methods: {
    resetChoosenConfigFileObject() {
      this.$emit("reset");
    },
    pushUpdatedConfigFilesToBackendServer() {
      this.changeAllKeyValuePairs();
      this.$emit("update", this.fileName);
    },
    changeAllKeyValuePairs() {
      this.$emit(
        "changeAllKeyValuePairs",
        this.fileName,
        this.getKeyValuePairsAsTupleArray(this.keyValuePairs)
      );
    },
    getKeyValuePairsAsTupleArray(
      keyValuePairs: Array<KeyValuePair>
    ): Array<[string, string]> {
      return keyValuePairs.map(
        (keyValuePair: KeyValuePair): [string, string] => {
          return [keyValuePair.keyName, keyValuePair.keyValue];
        }
      );
    },
    initialiseKeyValuePairs() {
      editKeyValuePairsObject.keyValuePairs = [];
      if (this.fileName !== "") {
        this.keyValuePairsFromParent.forEach(
          (keyValuePairFromParent: [string, string]) => {
            editKeyValuePairsObject.addKeyValuePair(keyValuePairFromParent);
          }
        );
      }
    },
  },
  computed: {
    keyValuePairs: {
      get(): Array<KeyValuePair> {
        return editKeyValuePairsObject.keyValuePairs;
      },
      set(keyValuePairs: Array<KeyValuePair>) {
        editKeyValuePairsObject.keyValuePairs = keyValuePairs;
      },
    },
  },
  watch: {
    fileName: function () {
      this.initialiseKeyValuePairs();
    },
    keyValuePairsFromParent: function () {
      this.initialiseKeyValuePairs();
    },
  },
  beforeCreate: function () {
    Vue.observable(editKeyValuePairsObject);
  },
  created: function () {
    this.initialiseKeyValuePairs();
  },
};
</script>