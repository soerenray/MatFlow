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
              <v-text-field
                v-model="keyValuePairWithColor.keyName"
                solo
                dense
              ></v-text-field>
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
              <v-btn color="red" @click="revertAllChanges">
                Revert changes
              </v-btn>
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
interface keyValuePairWithColorInterface {
  _privateKeyName: string;
  isKeyInKeyValuPairsWithColorUnique: Function;
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
  methods: {
    changeAllKeyValuePairs() {
      let keyValuePairsWithoutColor = this.keyValuePairsWithColor.map(
        (
          keyValuePairWithColor: keyValuePairWithColorInterface
        ): [string, string] => {
          return [
            keyValuePairWithColor.keyName,
            keyValuePairWithColor.keyValue,
          ];
        }
      );
      this.$emit("editConfigFileEVENTS[0]", keyValuePairsWithoutColor);
    },
    revertAllChanges() {
        console.log("revert all changes in deitConfigFile")
      this.$emit("editConfigFileEVENTS[1]");
    },
    isKeyInKeyValuPairsWithColorUnique(key: string): boolean {
      return this.keyValuePairsWithColor
        .map(
          (keyValuePairWithColor: keyValuePairWithColorInterface): string => {
            return keyValuePairWithColor.keyName;
          }
        )
        .indexOf(key) === -1
        ? true
        : false;
    },
  },
  computed: {
    keyValuePairsWithColor: function (): keyValuePairWithColorInterface[] {
      let keyValuePairsWithColorArray = Array<keyValuePairWithColorInterface>();
      this.keyValuePairs.forEach((keyValuePair: [string, string]) => {
        keyValuePairsWithColorArray.push({
          _privateKeyName: keyValuePair[0],
          isKeyInKeyValuPairsWithColorUnique:
            this.isKeyInKeyValuPairsWithColorUnique,
          get keyName(): string {
            return this._privateKeyName;
          },
          set keyName(newKeyName: string) {
            if (this.isKeyInKeyValuPairsWithColorUnique(newKeyName)) {
              this._privateKeyName = newKeyName;
            }
          },
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