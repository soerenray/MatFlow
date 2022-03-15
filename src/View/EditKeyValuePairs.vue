<template>
  <v-app>
    <div style="width: 700px; padding-top: 10px">
      <v-card>
        <v-card style="padding-bottom: 35px; height: 40px">
          <v-row>
            <div style="padding-left: 20px; padding-top: 10px">
              <v-btn data-cy='revertAllFiles' @click="resetChoosenConfigFileObject" color="yellow"
                >Revert all files</v-btn
              >
            </div>
            <v-spacer></v-spacer>
            <div style="padding-right: 20px; padding-top: 10px">
              <v-btn data-cy='saveAllFiles' @click=
              "pushUpdatedConfigFilesToBackendServer" color="blue"
                >Save all files</v-btn
              >
            </div>
          </v-row>
        </v-card>
        <v-divider></v-divider>
        <v-card>
          <v-row>
            <v-col style="padding-left: 20px">
              <v-btn variant="text" color="blue"> Key name </v-btn>
            </v-col>
            <v-spacer></v-spacer>
            <v-col style="padding-right: 340px">
              <v-btn variant="text" color="blue"> Value </v-btn>
            </v-col>
          </v-row>
          <v-row v-for="keyValuePair in keyValuePairs" :key="keyValuePair.name">
            <div data-cy="keyEntry" style="padding-left: 20px">
              <v-text-field
                @input="changeAllKeyValuePairs"
                v-model="keyValuePair.keyName"
                style="width: 200px"
                variant="contained"
              ></v-text-field>
            </div>
            <v-spacer></v-spacer>
            <div data-cy="valueEntry" style="padding-right: 50px">
              <v-text-field
                @input="changeAllKeyValuePairs"
                v-model="keyValuePair.keyValue"
                variant="contained"
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
// @ts-nocheck
import EditKeyValuePairs from '@Model/EditKeyValuePairs';

interface KeyValuePair {
  _keyName: string;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  keyValuePairInstance: any;
  keyName: string;
  keyValue: string;
}

export default {
  name: 'EditKeyValuePairs',
  // details: https://frontendsociety.com/using-a-typescript-interfaces-and-types-as-a-prop-type-in-vuejs-508ab3f83480
  data() {
    return {
      editKeyValuePairsObject: new EditKeyValuePairs(),
    };
  },
  props: {
    // keyValuePairs: [],
    keyValuePairsFromParent: {
      type: Array as () => Array<[string, string]>,
    },
    // Vue type-syntax
    fileName: String,
  },
  methods: {
    resetChoosenConfigFileObject() {
      this.$emit('reset');
    },
    pushUpdatedConfigFilesToBackendServer() {
      this.changeAllKeyValuePairs();
      this.$emit('update', this.fileName);
    },
    changeAllKeyValuePairs() {
      this.$emit(
        'changeAllKeyValuePairs',
        this.fileName,
        this.getKeyValuePairsAsTupleArray(this.keyValuePairs),
      );
    },
    getKeyValuePairsAsTupleArray(
      keyValuePairs: Array<KeyValuePair>,
    ): Array<[string, string]> {
      return keyValuePairs.map(
        (keyValuePair: KeyValuePair): [string, string] => [keyValuePair.keyName,
          keyValuePair.keyValue],
      );
    },
    initialiseKeyValuePairs() {
      this.editKeyValuePairsObject.keyValuePairs = [];
      if (this.keyValuePairsFromParent === undefined) {
        throw Error('keyValuePairsFromParents is undefined');
      }
      if (this.fileName !== '') {
        this.keyValuePairsFromParent.forEach(
          (keyValuePairFromParent: [string, string]) => {
            this.editKeyValuePairsObject.addKeyValuePair(
              keyValuePairFromParent,
            );
          },
        );
      }
    },
  },
  computed: {
    // Setter, getter resulted in a vue internal bug
    keyValuePairs(): Array<KeyValuePair> {
      if (!this.editKeyValuePairsObject) {
        return [];
      }
      return this.editKeyValuePairsObject.keyValuePairs;
    },
  },
  watch: {
    fileName() {
      this.initialiseKeyValuePairs();
    },
    keyValuePairsFromParent() {
      this.initialiseKeyValuePairs();
    },
  },
  created() {
    this.initialiseKeyValuePairs();
  },
};
</script>
