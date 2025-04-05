import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'
import store from '@/store'

const request = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
    timeout: 5000,
    withCredentials: false,
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
})

// 请求拦截器
request.interceptors.request.use(
    config => {
        const token = store.state.token
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`
        }
        return config
    },
    error => {
        return Promise.reject(error)
    }
)

// 响应拦截器
request.interceptors.response.use(
    response => {
        console.log('请求成功，响应数据:', response.data) // 调试信息
        return response
    },
    error => {
        console.error('请求失败:', error) // 调试信息
        if (error.response) {
            switch (error.response.status) {
                case 401:
                    store.commit('CLEAR_USER')
                    router.push('/login')
                    ElMessage.error('用户名或密码错误')
                    break
                case 403:
                    ElMessage.error('没有权限访问')
                    break
                default:
                    ElMessage.error(error.response?.data?.error || '请求失败')
            }
        } else {
            ElMessage.error('网络错误，请检查服务器连接')
        }
        return Promise.reject(error)
    }
)

export default request