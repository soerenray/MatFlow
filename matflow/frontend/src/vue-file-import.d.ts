// prevent vue releated errors

declare module '*.vue' {
    import Vue from 'vue';

    export default Vue;
 }
