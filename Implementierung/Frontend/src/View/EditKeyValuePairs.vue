<template>
  <v-app>
    <div style="width: 700px; padding-top: 10px">
      <v-card>
        <v-card style="padding-bottom: 35px">
          <v-row>
            <div style="padding-left: 20px; padding-top: 5px">
              <v-btn @click="resetChoosenConfigFileObject" color="yellow"
                >Revert all files</v-btn
              >
            </div>
            <v-spacer></v-spacer>
            <div style="padding-right: 20px; padding-top: 5px">
              <v-btn @click="pushUpdatedConfigFilesToBackendServer" color="blue"
                >Save all files</v-btn
              >
            </div>
          </v-row>
        </v-card>
        <v-card>
          <v-row>
            <v-col>
              <v-btn text color="primary"> Key name </v-btn>
            </v-col>
            <v-spacer></v-spacer>
            <v-col style="padding-right: 290px">
              <v-btn text color="primary"> Value </v-btn>
            </v-col>
          </v-row>
          <v-row v-for="(keyValuePair, index) in keyValuePairs" :key="index">
            <div style="padding-top: 5px; padding-left: 20px">
              <v-text-field
                @input="changeAllKeyValuePairs"
                v-model="keyValuePair.keyName"
                solo
                dense
              ></v-text-field>
            </div>
            <v-spacer></v-spacer>
            <div style="padding-top: 5px; padding-right: 50px">
              <v-text-field
                @input="changeAllKeyValuePairs"
                v-model="keyValuePair.keyValue"
                style="width: 400px"
                dense
              ></v-text-field>
            </div>
          </v-row>
        </v-card>
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
      if (this.keyValuePairsFromParent === undefined) {
        throw Error("keyValuePairsFromParents is undefined");
      }
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