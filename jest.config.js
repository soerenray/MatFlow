module.exports = {
  preset: '@vue/cli-plugin-unit-jest/presets/typescript-and-babel',
  // Required when testing the view. Very unperformant
  // transformIgnorePatterns: [
  //   '/nodes-modules/vue-material-design-icons/Plus.vue',
  //   '/nodes-modules/vue-material-design-icons/FileDocumentOutline.vue',
  //   '/nodes-modules/vue-material-design-icons/FileRestore.vue',
  //   '/nodes-modules/vue-material-design-icons/Delete.vue',
  //   '/nodes-modules/vue-material-design-icons/LockClock.vue',
  //   '/nodes-modules/vue-material-design-icons/Memory.vue',
  //   '/nodes-modules/vue-material-design-icons/Send.vue',
  //   '/nodes-modules/vue-material-design-icons/Send.vue'],
  transformIgnorePatterns: [],
  setupFiles: ["./Implementierung/Frontend/tests/unit/index.ts"],
  globals: {
    'ts-jest': {
      diagnostics: false
    }
  }
}
