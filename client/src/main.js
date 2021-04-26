import Vue from 'vue';
import lodash from 'lodash';
import App from './App.vue';
import router from './router';
import vuetify from './plugins/vuetify';
import store from './store';
import axios from './utils/request';
import '@/assets/global.scss';

Vue.config.productionTip = false;

Object.defineProperty(Vue.prototype, '$axios', { value: axios });
Object.defineProperty(Vue.prototype, '_', { value: lodash });

new Vue({
  router,
  vuetify,
  store,
  render: (h) => h(App),
}).$mount('#app');
