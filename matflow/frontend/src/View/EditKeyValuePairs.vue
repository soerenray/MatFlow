<template>
  <v-card>
    <div class="d-flex flex-row">
      <div style="width: 300px" class="pl-2 mr-10">
        <div>
          <v-btn
            data-cy="revertAllFiles"
            @click="resetChoosenConfigFileObject"
            color="yellow"
            >Revert all files</v-btn
          >
        </div>
        <div>
          <v-btn variant="text" color="blue"> Key name </v-btn>
        </div>
        <div>
          <div
            data-cy="keyEntry"
            v-for="keyValuePair in keyValuePairs"
            :key="keyValuePair.name"
          >
            <v-text-field
              @input="changeAllKeyValuePairs"
              v-model="keyValuePair.keyName"
              variant="contained"
            ></v-text-field>
          </div>
        </div>
      </div>
      <div style="width: 300px" class="pr-2">
        <div class="d-flex flex-row">
          <v-spacer></v-spacer>
          <v-btn
            data-cy="saveAllFiles"
            @click="pushUpdatedConfigFilesToBackendServer"
            color="blue"
            >Save all files</v-btn
          >
        </div>
        <div>
          <v-btn variant="text" color="blue"> Value </v-btn>
        </div>
        <div
          data-cy="valueEntry"
          v-for="keyValuePair in keyValuePairs"
          :key="keyValuePair.name"
        >
          <v-text-field
            @input="changeAllKeyValuePairs"
            v-model="keyValuePair.keyValue"
            variant="contained"
            dense
          ></v-text-field>
        </div>
      </div>
    </div>
  </v-card>
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
        (keyValuePair: KeyValuePair): [string, string] => [
          keyValuePair.keyName,
          keyValuePair.keyValue,
        ],
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
