// No more errors for vue file import in ts
// https://stackoverflow.com/questions/42002394/importing-vue-components-in-typescript-file
declare module '*.vue' {
    import Vue from 'vue';

    export default Vue;
  }
