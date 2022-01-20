<template>
  <v-app>
    <v-container>
      <v-col align="center">
        <v-card width="1000px">
          <v-data-table
            :headers="headers"
            :items="versionTableObject"
            item-key="name"
            :search="search"
          >
            <template v-slot:[`item.workspace`]="{}"
              ><v-btn icon><file-restore-icon></file-restore-icon></v-btn
            ></template>
            <template v-slot:[`item.veraenderteParameter`]="{}"
              ><v-btn icon>
                <v-dialog v-model="dialoge" max-width="600px">
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn icon v-bind="attrs" v-on="on">
                      <file-document-outline-icon></file-document-outline-icon>
                    </v-btn>
                  </template>
                  <v-card>
                    <v-data-table
                      :headers="headers2"
                      :items="parameterChanges"
                      item-key="oldValue"
                    ></v-data-table>
                  </v-card>
                </v-dialog> </v-btn
            ></template>
            <template v-slot:top>
              <v-text-field
                v-model="search"
                label="Search notes"
                class="mx-4"
              ></v-text-field>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-container>
  </v-app>
</template>

<script lang='ts'>
import Version from "../Classes/Version";
import VersionControl from "../Model/VersionControl";

interface VersionsTableObject {
  versionNumber: string;
  versionNote: string;
}

let versionControlObject = new VersionControl();

export default {
  data: function () {
    return {
      search: "",
      dialoge: "",
      headers2: [
        { text: "Parameter/ value old", value: "oldValue" },
        { text: "Parameter/ value new", value: "newValue" },
      ],
      headers: [
        { text: "Version number", value: "versionNumber" },
        { text: "Version notes", value: "versionNote" },
        { text: "Changed parameters", value: "veraenderteParameter" },
        { text: "Load into current workspace", value: "workspace" },
      ],
      parameterChanges: [
        { oldValue: "key1: Ipsom lorum", newValue: "key1: lorem ipsum" },
        { oldValue: "key1: xy", newValue: "key2: xy" },
        { oldValue: "key3: 5.0 5.0", newValue: "key3: 'text'" },
      ],
    };
  },
  computed: {
    versionTableObject: {
      get: function (): Array<VersionsTableObject> {
        return versionControlObject.versions.map<VersionsTableObject>(
          (version: Version): VersionsTableObject => {
            return {
              versionNumber: version.versionNumber,
              versionNote: version.versionNote,
            };
          }
        );
      },
    },
  },
};
</script>