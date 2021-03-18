import request from './index'

export function getOrders () {
  return request({
    url: 'worktable/order/',
    method: 'get'
  })
}
