const path = require('path')

module.exports = {
  lintOnSave: false,
  pages: {
    index: {
      entry: 'Implementierung/Frontend/src/main.ts',
      template: 'Implementierung/Frontend/public/index.html'
    }
  },
  transpileDependencies: [
    'vuetify'
  ],
  configureWebpack: {
    resolve: {
      alias: {
        '@': path.resolve(__dirname, 'Implementierung/Frontend/src/')
      }
    }
  },
  chainWebpack: config => {
    config
      .plugin('copy')
      .use(require('copy-webpack-plugin'), [[{
        from: path.resolve(__dirname, 'Implementierung/Frontend/public'),
        to: path.resolve(__dirname, 'dist'),
        toType: 'dir',
        ignore: ['.DS_Store']
      }]])
  }
}