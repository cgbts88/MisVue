<template>
  <div class="test">
    <ul>
      <li v-for="(order, index) in orders.results.data" :key="index" style="display:block">
        {{ order.num }} - - {{ order.created_log.record_time }} - - {{ order.created_log.recorder }}
         - - {{ order.content }} - - {{ order.process_log.recorder }} - - {{ order.process_log.record_time }}
         - - {{ order.type }} - - {{ order.state }}
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios'
export default({
  el: '#test',
  data () {
    return {
      orders: {}
    }
  },
  mounted () {
    axios
      .get('http://127.0.0.1:8000/worktable/order/')
      .then(response => (this.orders = response.data))
      .catch(function (error) { // 请求失败处理
        console.log(error)
      })
  }
})
</script>
