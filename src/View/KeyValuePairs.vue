<template>
  <v-app>
    <v-table>
      <thead data-cy="tableHeader">
        <tr>
          <th class="mr-5">{{ headers[0].text }}</th>
          <th>{{ headers[1].text }}</th>
        </tr>
      </thead>
      <tbody data-cy="tableBody">
        <tr
          v-for="parameterChange in parameterChangesTableObject"
          :key="parameterChange.oldValue"
        >
          <td class="mr-5">{{ parameterChange.oldValue }}</td>
          <td>{{ parameterChange.newValue }}</td>
        </tr>
      </tbody>
    </v-table>
  </v-app>
</template>

<script lang='ts'>
// @ts-nocheck
import KeyValuePairs from '@Model/KeyValuePairs';

export default {
  name: 'KeyValuePairs',
  data() {
    return {
      keyValuePairsObject: new KeyValuePairs([
        { text: 'old value', value: 'oldValue' },
        { text: 'new value', value: 'newValue' },
      ]),
    };
  },
  // details: https://frontendsociety.com/using-a-typescript-interfaces-and-types-as-a-prop-type-in-vuejs-508ab3f83480
  props: {
    parameterChanges: {
      type: Array as () => Array<[string, string]>,
    },
  },
  computed: {
    parameterChangesTableObject(): object[] {
      return this.parameterChanges.map((x: [string, string]):
      object => ({ oldValue: x[0], newValue: x[1] }));
    },
    headers: {
      get(): object[] {
        return this.keyValuePairsObject.headers;
      },
      set(headers: object[]) {
        this.keyValuePairsObject.headers = headers;
      },
    },
  },
};
</script>
