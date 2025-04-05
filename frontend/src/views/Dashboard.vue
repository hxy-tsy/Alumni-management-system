<template>
  <div class="dashboard">
    <!-- 顶部导航栏 -->
    <el-header class="header">
      <div class="logo">校友信息管理系统</div>
      <div class="user-info">
        <el-dropdown>
          <span class="user-name">
            {{ userInfo.username }}
            <el-icon><arrow-down /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </el-header>

    <el-container class="main-container">
      <!-- 侧边栏导航 -->
      <el-aside width="200px">
        <el-menu
          :default-active="activeMenu"
          class="side-menu"
          router
        >
          <!-- 管理员菜单 -->
          <template v-if="userInfo.role === 'admin'">
            <el-sub-menu index="alumni">
              <template #title>
                <el-icon><user /></el-icon>
                <span>校友信息</span>
              </template>
              <el-menu-item index="/dashboard/alumni-info">校友信息</el-menu-item>
              <el-menu-item index="/dashboard/alumni-applications">审批校友申请</el-menu-item>
              <el-menu-item index="/dashboard/alumni-statistics">校友画像</el-menu-item>
            </el-sub-menu>

            <el-sub-menu index="association">
              <template #title>
                <el-icon><office-building /></el-icon>
                <span>校友会</span>
              </template>
              <el-menu-item index="/dashboard/association-manage">总会管理</el-menu-item>
              <el-menu-item index="/dashboard/branch-manage">分会管理</el-menu-item>
            </el-sub-menu>

            <el-sub-menu index="activities">
              <template #title>
                <el-icon><calendar /></el-icon>
                <span>校友活动</span>
              </template>
              <el-menu-item index="/dashboard/activity-publish">活动发布</el-menu-item>
              <el-menu-item index="/dashboard/activity-approval">活动审批</el-menu-item>
<!--              <el-menu-item index="/dashboard/my-activities">我的活动</el-menu-item>-->
<!--              <el-menu-item index="/dashboard/feedback">回馈母校</el-menu-item>-->
            </el-sub-menu>

            <el-sub-menu index="message">
              <template #title>
                <el-icon><message /></el-icon>
                <span>群发工具</span>
              </template>
              <el-menu-item index="/dashboard/news-notice">通知</el-menu-item>
<!--              <el-menu-item index="/dashboard/activity-notice">活动通知</el-menu-item>-->
<!--              <el-menu-item index="/dashboard/holiday-greetings">节日祝福</el-menu-item>-->
            </el-sub-menu>
          </template>

          <!-- 非毕业校友菜单 -->
          <template v-if="isStudentAlumni">
            <el-sub-menu index="alumni">
              <template #title>
                <el-icon><user /></el-icon>
                <span>校友信息</span>
              </template>
              <el-menu-item index="/dashboard/my-info">校友信息</el-menu-item>
              <el-menu-item index="/dashboard/career-recommendations">毕业去向推荐</el-menu-item>
            </el-sub-menu>
          </template>

          <!-- 已毕业校友菜单 -->
          <template v-if="isGraduatedAlumni">
            <el-sub-menu index="alumni">
              <template #title>
                <el-icon><user /></el-icon>
                <span>校友信息</span>
              </template>
              <el-menu-item index="/dashboard/my-info">校友信息</el-menu-item>
            </el-sub-menu>

            <el-sub-menu index="association">
              <template #title>
                <el-icon><office-building /></el-icon>
                <span>校友会</span>
              </template>
              <el-menu-item index="/dashboard/join-association">加入校友会</el-menu-item>
              <el-menu-item index="/dashboard/my-association">我的校友会</el-menu-item>
            </el-sub-menu>

            <el-sub-menu index="activities">
              <template #title>
                <el-icon><calendar /></el-icon>
                <span>校友活动</span>
              </template>
              <el-menu-item index="/dashboard/activity-registration">活动报名</el-menu-item>
              <el-menu-item index="/dashboard/my-activities">我的活动</el-menu-item>
              <el-menu-item index="/dashboard/donation-projects">回馈母校</el-menu-item>
            </el-sub-menu>

            <el-sub-menu index="message" >
              <template #title>
                <el-icon><message /></el-icon>
                <span>消息通知</span>
              </template>
              <el-menu-item index="/dashboard/news-notice-graduate">通知</el-menu-item>
<!--              <el-menu-item index="/dashboard/activity-notice-graduate">活动通知</el-menu-item>-->
<!--              <el-menu-item index="/dashboard/holiday-greetings-graduate">节日祝福</el-menu-item>-->
            </el-sub-menu>
          </template>

          <!-- 校友联络人菜单 -->
          <template v-if="isLiaison">
            <el-sub-menu index="alumni">
              <template #title>
                <el-icon><user /></el-icon>
                <span>校友信息</span>
              </template>
              <el-menu-item index="/dashboard/alumni-info">校友信息</el-menu-item>
            </el-sub-menu>

            <el-sub-menu index="association">
              <template #title>
                <el-icon><office-building /></el-icon>
                <span>校友会</span>
              </template>
              <el-menu-item index="/dashboard/association-overview">校友会概况</el-menu-item>
              <el-menu-item index="/dashboard/association-members">校友会成员</el-menu-item>
<!--              <el-menu-item index="/dashboard/association-applications">审批校友会申请</el-menu-item>-->
              <el-menu-item index="/dashboard/council-overview">理事会概况</el-menu-item>
              <el-menu-item index="/dashboard/council-meeting">召开理事会</el-menu-item>
            </el-sub-menu>

            <el-sub-menu index="activities">
              <template #title>
                <el-icon><calendar /></el-icon>
                <span>校友活动</span>
              </template>
              <el-menu-item index="/dashboard/activity-recommendations">活动策划推荐</el-menu-item>
              <el-menu-item index="/dashboard/activity-publish">活动发布</el-menu-item>
              <el-menu-item index="/dashboard/my-activities">我的活动</el-menu-item>
            </el-sub-menu>

            <el-sub-menu index="message">
              <template #title>
                <el-icon><message /></el-icon>
                <span>群发工具</span>
              </template>
              <el-menu-item index="/dashboard/news-notice">通知</el-menu-item>
<!--              <el-menu-item index="/dashboard/activity-notice">活动通知</el-menu-item>-->
<!--              <el-menu-item index="/dashboard/holiday-greetings">节日祝福</el-menu-item>-->
            </el-sub-menu>
          </template>

          <!-- 其他角色的菜单可以在这里添加 -->
        </el-menu>
      </el-aside>

      <!-- 主要内容区域 -->
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter, useRoute } from 'vue-router'
import { ArrowDown, User, OfficeBuilding, Calendar, Message } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import request from '@/utils/request'

export default {
  name: 'Dashboard',
  components: {
    ArrowDown,
    User,
    OfficeBuilding,
    Calendar,
    Message
  },
  setup() {
    const store = useStore()
    const router = useRouter()
    const route = useRoute()

    const userInfo = computed(() => store.state.user || {})
    const activeMenu = computed(() => route.path)

    // 判断是否为非毕业校友
    const isStudentAlumni = computed(() => {
      return userInfo.value.role === 'alumni' && !userInfo.value.is_graduated
    })

    // 判断是否为已毕业校友
    const isGraduatedAlumni = computed(() => {
      return userInfo.value.role === 'graduated_alumni'
    })

    // 判断是否为校友联络人
    const isLiaison = computed(() => {
      return userInfo.value.role === 'liaison'
    })

    const handleLogout = () => {
      store.dispatch('logout')
      router.push('/login')
    }

    // 不再需要在Dashboard中检查状态，因为已经在登录时检查了

    return {
      userInfo,
      activeMenu,
      handleLogout,
      isStudentAlumni,
      isGraduatedAlumni,
      isLiaison
    }
  }
}
</script>

<style scoped>
.dashboard {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background-color: #304156;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.logo {
  font-size: 20px;
  font-weight: bold;
}

.user-name {
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.main-container {
  flex: 1;
  overflow: hidden;
}

.side-menu {
  height: 100%;
  border-right: none;
}

.el-main {
  padding: 20px;
  background-color: #f0f2f5;
}
</style> 