<template>
  <v-app>
    <v-card>
      <v-data-table
        :headers="headers"
        :items="parameterChangesTableObject"
        item-key="oldValue"
      ></v-data-table>
    </v-card>
  </v-app>
</template>

<script lang='ts'>
import Vue from "vue";
import KeyValuePairs from "../Model/KeyValuePairs";

const keyValuePairsObject = new KeyValuePairs([
  { text: "Parameter/ value old", value: "oldValue" },
  { text: "Parameter/ value new", value: "newValue" },
]);

export default {
  name: "KeyValuePairs",
  // details: https://frontendsociety.com/using-a-typescript-interfaces-and-types-as-a-prop-type-in-vuejs-508ab3f83480
  props: {
    parameterChanges: {
      type: Array as () => Array<[string, string]>,
    },
  },
  computed: {
    parameterChangesTableObject: function (): object[] {
      return this.parameterChanges.map((x: [string, string]): object => {
        return { oldValue: x[0], newValue: x[1] };
      });
    },
    headers: {
      get: function (): Object[] {
        return keyValuePairsObject.headers;
      },
      set: function (headers: Object[]) {
        keyValuePairsObject.headers = headers;
      },
    },
  },
  beforeCreate: function () {
    // Vue is oberserving data in the data property.
    // Vue.observable has to be used to make an object outside of data reactive: https:///// v3.vuejs.org/guide/reactivity-fundamentals.html#declaring-reactive-state
    Vue.observable(keyValuePairsObject);
  },
};
</script>