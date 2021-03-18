import Axios from 'axios'

// 创建axios实例
const service = Axios.create({
  baseURL: process.env.BABEL_ENV, // api 的 base_url
  timeout: 60000 // 请求超时时间
})

// 能过拦截处理csrf问题，这里的正则和匹配下标可能需要根据实际情况小改动
service.interceptors.request.use((
  config) => {
  config.headers['Content-Type'] = 'application/json'
  return config
})

service.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    return Promise.reject(error)
  }
)

export default service
