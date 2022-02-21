const path = require('path')
const basUrlSrc = "matflow/frontend/src"
const basUrlPublic = "matflow/frontend/public"

module.exports = {
  lintOnSave: true,
  pages: {
    index: {
      entry: basUrlSrc + '/main.ts',
      template: basUrlPublic + '/index.html'
    }
  },
  transpileDependencies: [
    'vuetify'
  ],
  configureWebpack: {
    resolve: {
      alias: {
        '@': path.resolve(__dirname, basUrlSrc),
        "@Classes": path.resolve(__dirname, basUrlSrc + '/Classes'),
        "@Controler": path.resolve(__dirname, basUrlSrc + '/Controler'),
        "@Memento": path.resolve(__dirname, basUrlSrc + '/Memento'),
        "@Model": path.resolve(__dirname, basUrlSrc + '/Model'),
        "@View": path.resolve(__dirname, basUrlSrc + '/View'),
      }
    }
  },
}