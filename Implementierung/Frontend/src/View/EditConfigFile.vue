<template>
  <v-app>
    <div style="width: 700px">
      <v-card>
        <v-row>
          <div>
            <v-btn text color="primary"> Key name </v-btn>
          </div>
          <v-spacer></v-spacer>
          <div style="padding-top: 15px; padding-right: 290px">
            <v-btn text color="primary"> Value </v-btn>
          </div>
        </v-row>
        <v-card
          v-for="{ name, value, color1, color2 } in keyValuePairsWithColor"
          :key="name"
        >
          <v-row>
            <div style="padding-top: 15px; padding-left: 20px">
              <v-text-field v-model="name" solo dense></v-text-field>
            </div>
            <v-spacer></v-spacer>
            <div style="padding-top: 15px; padding-right: 50px">
              <v-text-field
                v-model="value"
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
export default {
  // details: https://frontendsociety.com/using-a-typescript-interfaces-and-types-as-a-prop-type-in-vuejs-508ab3f83480
  props: {
    keyValuePairs: {
      type: Array as () => Array<[string, string]>,
    },
  },
  data() {
    return {};
  },
  methods: {
      changeKeyValuePair(keyValuePair: object) {
          this.$emit('changeKeyValuePair', keyValuePair)
      },
      changeAllKeyValuePairs() {
          this.$emit('changeAllKeyValuePairs', this.keyValuePairsWithColor)
      }
  },
  computed: {
    keyValuePairsWithColor: function (): object[] {
      this.keyValuePairs.forEach((keyValuePair: object) => {
        Object.assign(
          keyValuePair,
          { originalKeyName: keyValuePair.name },
          { color1: "#000000" },
          { color2: "#000000" }
        );
        console.log(keyValuePair)
      });
      return this.keyValuePairs;
    },
  },
};
</script>