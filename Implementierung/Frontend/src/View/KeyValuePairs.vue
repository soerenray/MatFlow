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
import KeyValuePairs from "../Model/KeyValuePairs";

export default {
  name: "KeyValuePairs",
  // details: https://frontendsociety.com/using-a-typescript-interfaces-and-types-as-a-prop-type-in-vuejs-508ab3f83480
  props: {
    parameterChanges: {
      type: Array as () => Array<[string, string]>,
    },
  },
  data: function () {
    return {
      headers: [
        { text: "Parameter/ value old", value: "oldValue" },
        { text: "Parameter/ value new", value: "newValue" },
      ],
    };
  },
  computed: {
    parameterChangesTableObject: function (): object[] {
      return this.parameterChanges.map((x: [string, string]): object => {
        return { oldValue: x[0], newValue: x[1] };
      });
    },
  },
};
</script>