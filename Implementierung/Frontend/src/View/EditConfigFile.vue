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
        <v-card style="background-color: #f7f9f9" width="700px" height="50px">
          <v-row>
            <div style="padding-left: 20px; padding-top: 5px">
              <v-btn color="yellow">revert all files</v-btn>
            </div>
            <v-spacer></v-spacer>
            <div style="padding-right: 20px; padding-top: 5px">
              <v-btn color="blue">Create new version</v-btn>
            </div>
          </v-row>
        </v-card>
        <v-card
          v-for="keyValuePairWithColor in keyValuePairsWithColor"
          :key="keyValuePairWithColor.keyName"
        >
          <v-row>
            <div style="padding-top: 15px; padding-left: 20px">
              <v-text-field v-model="keyValuePairWithColor.keyName" solo dense></v-text-field>
            </div>
            <v-spacer></v-spacer>
            <div style="padding-top: 15px; padding-right: 50px">
              <v-text-field
                v-model="keyValuePairWithColor.keyValue"
                style="width: 400px"
                dense
              ></v-text-field>
            </div>
          </v-row>
        </v-card>
        <v-card>
          <v-row>
            <div
              style="
                padding-top: 10px;
                padding-bottom: 10px;
                padding-left: 20px;
              "
            >
              <v-btn color="red"> Revert changes </v-btn>
            </div>
            <v-spacer></v-spacer>
            <div
              style="
                padding-top: 10px;
                padding-bottom: 10px;
                padding-right: 20px;
              "
            >
              <v-btn color="#28B463" @click="changeAllKeyValuePairs">
                Apply changes
              </v-btn>
            </div>
          </v-row>
        </v-card>
      </v-card>
    </div>
  </v-app>
</template>

<script lang='ts'>
interface keyValuePairsWithColorInterface {
  originalKeyName: string;
  keyName: string;
  keyValue: string;
  color1: string;
  color2: string;
}

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
    changeKeyValuePair(keyValuePair: keyValuePairsWithColorInterface) {
      this.$emit("changeKeyValuePair", keyValuePair);
    },
    changeAllKeyValuePairs() {
      this.$emit("changeAllKeyValuePairs", this.keyValuePairsWithColor);
    },
  },
  computed: {
    keyValuePairsWithColor: function (): keyValuePairsWithColorInterface[] {
      let keyValuePairsWithColorArray =
        Array<keyValuePairsWithColorInterface>();
      this.keyValuePairs.forEach((keyValuePair: [string, string]) => {
        keyValuePairsWithColorArray.push({
          originalKeyName: keyValuePair[0],
          keyName: keyValuePair[0],
          keyValue: keyValuePair[1],
          color1: "#000000",
          color2: "#000000",
        });
      });
      return keyValuePairsWithColorArray;
    },
  },
};
</script>