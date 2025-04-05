<template>
  <div class="login-container">
    <div class="login-content">
      <!-- 左侧欢迎语 -->
      <div class="welcome-section">
        <div class="logo">LOGO</div>
        <div class="welcome-text">
          <h1>Hi, 你好！</h1>
          <h2>欢迎进入校友信息管理系统</h2>
        </div>
      </div>

      <!-- 右侧角色选择 -->
      <div class="role-section">
        <div class="role-card admin" @click="handleRoleSelect('admin')">
          <span>我是校方管理员</span>
        </div>
        <div class="role-card liaison" @click="handleRoleSelect('liaison')">
          <span>我是校友联络人</span>
        </div>
        <div class="role-cards-row">
          <div class="role-card alumni" @click="handleRoleSelect('graduated_alumni')">
            <span>我是校友<br/>(毕业生)</span>
          </div>
          <div class="role-card alumni" @click="handleRoleSelect('alumni_student')">
            <span>我是校友<br/>(非毕业生)</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 登录对话框 -->
    <el-dialog 
      v-model="dialogVisible" 
      :title="getDialogTitle"
      width="400px"
      center
    >
      <el-form 
        ref="loginFormRef"
        :model="loginForm" 
        :rules="rules" 
        label-width="0"
      >
        <el-form-item prop="username">
          <el-input 
            v-model="loginForm.username" 
            :placeholder="getUsernamePlaceholder"
            :prefix-icon="User"
            clearable
          ></el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input 
            v-model="loginForm.password" 
            type="password" 
            placeholder="请输入密码"
            :prefix-icon="Lock"
            show-password
            clearable
          ></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button type="primary" style="width: 100%" @click="handleLogin">登录</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import request from '@/utils/request'

const router = useRouter()
const store = useStore()
const loginFormRef = ref(null)
const dialogVisible = ref(false)

const loginForm = ref({
  username: '',
  password: '',
  role: ''
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const getDialogTitle = computed(() => {
  const titles = {
    admin: '校方管理员登录',
    liaison: '校友联络人登录',
    graduated_alumni: '毕业校友登录',
    alumni_student: '在校校友登录'
  }
  return titles[loginForm.value.role] || '用户登录'
})

const getUsernamePlaceholder = computed(() => {
  if (loginForm.value.role === 'alumni_student') {
    return '请输入学号'
  }
  return '请输入用户名'
})

const handleRoleSelect = (role) => {
  loginForm.value.role = role
  dialogVisible.value = true
}

const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  try {
    await loginFormRef.value.validate()
    console.log('登录数据:', loginForm.value)  // 调试信息
    const response = await request.post('/api/users/login/', {
      username: loginForm.value.username,
      password: loginForm.value.password,
      role: loginForm.value.role
    })
    console.log('登录响应:', response.data)  // 调试信息
    store.commit('SET_TOKEN', response.data.token)
    store.commit('SET_USER', response.data.user)
    ElMessage.success('登录成功')
    router.push('/dashboard')
  } catch (error) {
    console.error('登录失败:', error)
    ElMessage.error(error.response?.data?.error || '登录失败，请检查用户名和密码')
  }
}
</script>

<style scoped>
.login-container {
  height: 100vh;
  width: 100vw;
  background: linear-gradient(135deg, #6aa1ff 0%, #3f7efd 100%);
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;
}

.login-container::before {
  content: '';
  position: absolute;
  width: 200%;
  height: 200%;
  background: url('/src/assets/bg-pattern.png') repeat;
  opacity: 0.1;
  animation: bg-move 20s linear infinite;
}

@keyframes bg-move {
  from { transform: translate(0, 0); }
  to { transform: translate(-50%, -50%); }
}

.login-content {
  width: 1200px;
  height: 600px;
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 20px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
  display: flex;
  position: relative;
  z-index: 1;
}

.welcome-section {
  flex: 1;
  padding: 50px;
  display: flex;
  flex-direction: column;
}

.logo {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 100px;
}

.welcome-text {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.welcome-text h1 {
  font-size: 48px;
  color: #333;
  margin-bottom: 20px;
}

.welcome-text h2 {
  font-size: 32px;
  color: #666;
}

.role-section {
  flex: 1;
  padding: 50px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 20px;
}

.role-card {
  height: 100px;
  background-color: #fff;
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.role-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.role-card span {
  font-size: 18px;
  color: #333;
  text-align: center;
}

.role-cards-row {
  display: flex;
  gap: 20px;
}

.role-cards-row .role-card {
  flex: 1;
}

.admin {
  background-color: #f0f2f5;
}

.liaison {
  background-color: #e1f3e8;
}

.alumni {
  background-color: #fde9ef;
}

:deep(.el-dialog) {
  border-radius: 15px;
}

:deep(.el-dialog__header) {
  text-align: center;
  margin-bottom: 20px;
}

:deep(.el-input__wrapper) {
  border-radius: 8px;
}
</style> 