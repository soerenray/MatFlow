const { defineConfig } = require('@vue/cli-service');
const path = require('path');

const basUrlSrc = './src';

module.exports = defineConfig({
  transpileDependencies: true,

  // pluginOptions: {
  //   vuetify: {
  //     // https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vuetify-loader
  //   },
  // },
  configureWebpack: {
    resolve: {
      alias: {
        '@': path.resolve(__dirname, basUrlSrc),
        '@plugins': path.resolve(__dirname, `${basUrlSrc}/plugins`),
        '@Classes': path.resolve(__dirname, `${basUrlSrc}/Classes`),
        '@Controler': path.resolve(__dirname, `${basUrlSrc}/Controler`),
        '@Memento': path.resolve(__dirname, `${basUrlSrc}/Memento`),
        '@Model': path.resolve(__dirname, `${basUrlSrc}/Model`),
        '@View': path.resolve(__dirname, `${basUrlSrc}/View`),
      },
    },
  },

  pluginOptions: {
    vuetify: {
      // https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vuetify-loader
    },
  },
});
