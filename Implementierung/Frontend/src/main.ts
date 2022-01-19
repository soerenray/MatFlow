import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import PlusIcon from 'vue-material-design-icons/Plus.vue';

Vue.component('plus-icon', PlusIcon);

Vue.config.productionTip = false

new Vue({
  vuetify,
  render: h => h(App)
}).$mount('#app')
