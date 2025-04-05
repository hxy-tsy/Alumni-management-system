<template>
  <div class="application-approval">
    <div class="content-card">
      <h1 class="title">校友会申请审批</h1>

      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="10" animated />
      </div>

      <div v-else-if="applications.length === 0" class="empty-container">
        <el-empty description="暂无待审批的申请" />
      </div>

      <div v-else class="applications-content">
        <el-table :data="applications" style="width: 100%" border>
          <el-table-column label="申请人" min-width="100">
            <template #default="scope">
              {{ formatName(scope.row.user) }}
            </template>
          </el-table-column>
          <el-table-column label="学号" min-width="120">
            <template #default="scope">
              {{ scope.row.profile?.student_id || scope.row.user?.student_id || '-' }}
            </template>
          </el-table-column>
          <el-table-column label="学院" min-width="150">
            <template #default="scope">
              {{ scope.row.user?.department || '-' }}
            </template>
          </el-table-column>
          <el-table-column label="班级" min-width="120">
            <template #default="scope">
              {{ scope.row.profile?.class_name || '-' }}
            </template>
          </el-table-column>
          <el-table-column label="申请时间" prop="join_date" min-width="120" />
          <el-table-column label="状态" min-width="100">
            <template #default="scope">
              <el-tag type="warning">{{ scope.row.status_display }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200">
            <template #default="scope">
              <el-button 
                type="success" 
                size="small" 
                @click="handleApprove(scope.row)"
                :loading="actionLoading === scope.row.id"
              >
                通过
              </el-button>
              <el-button 
                type="danger" 
                size="small" 
                @click="handleReject(scope.row)"
                :loading="actionLoading === scope.row.id"
              >
                拒绝
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '@/utils/request'

export default {
  name: 'ApplicationApproval',
  setup() {
    const loading = ref(true)
    const applications = ref([])
    const actionLoading = ref(null)

    // 获取待审批的申请列表
    const fetchApplications = async () => {
      try {
        loading.value = true
        const response = await request.get('/api/association/my-branch/applications/')
        applications.value = response.data
      } catch (error) {
        console.error('获取申请列表失败:', error)
        ElMessage.error('获取申请列表失败: ' + (error.response?.data?.error || error.message || '未知错误'))
      } finally {
        loading.value = false
      }
    }

    // 处理申请（通过或拒绝）
    const handleApplication = async (application, action) => {
      try {
        actionLoading.value = application.id
        
        await ElMessageBox.confirm(
          `确定要${action === 'approve' ? '通过' : '拒绝'}该申请吗？`,
          '确认操作',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
          }
        )
        
        const response = await request.put(`/api/association/my-branch/applications/${application.id}/`, {
          action: action
        })
        
        ElMessage.success(response.data.message || `申请已${action === 'approve' ? '通过' : '拒绝'}`)
        
        // 刷新申请列表
        fetchApplications()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('处理申请失败:', error)
          ElMessage.error('处理申请失败: ' + (error.response?.data?.error || error.message || '未知错误'))
        }
      } finally {
        actionLoading.value = null
      }
    }

    // 通过申请
    const handleApprove = (application) => {
      handleApplication(application, 'approve')
    }

    // 拒绝申请
    const handleReject = (application) => {
      handleApplication(application, 'reject')
    }

    // 格式化姓名
    const formatName = (user) => {
      if (!user) return '-'
      
      const firstName = user.first_name || ''
      const lastName = user.last_name || ''
      
      if (firstName || lastName) {
        return firstName + lastName
      }
      
      return user.username || '-'
    }

    onMounted(() => {
      fetchApplications()
    })

    return {
      loading,
      applications,
      actionLoading,
      handleApprove,
      handleReject,
      formatName
    }
  }
}
</script>

<style scoped>
.application-approval {
  padding: 20px;
}

.content-card {
  background: #fff;
  padding: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.title {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
}

.loading-container {
  padding: 20px;
}

.empty-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 0;
}

.applications-content {
  margin-top: 20px;
}
</style> 