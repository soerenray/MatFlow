import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
//Search icons: https://materialdesignicons.com/
import PlusIcon from 'vue-material-design-icons/Plus.vue';
import FileDocumentOutlineIcon from 'vue-material-design-icons/FileDocumentOutline.vue'
import FileRestoreIcon from 'vue-material-design-icons/FileRestore.vue'

Vue.component('plus-icon', PlusIcon);
Vue.component('file-document-outline-icon', FileDocumentOutlineIcon)
Vue.component('file-restore-icon', FileRestoreIcon )

Vue.config.productionTip = false

new Vue({
  vuetify,
  render: h => h(App)
}).$mount('#app')
