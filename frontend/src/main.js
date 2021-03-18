import Vue from 'vue'
// import axios from 'axios'
// import VueAxios from 'vue-axios'
// import ElementUI from 'element-ui'
import App from './App'
import router from './router'

Vue.config.productionTip = false
// Vue.use(ElementUI)
// Vue.use(VueAxios, axios)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
