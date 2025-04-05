<template>
  <div class="activity-registration">
    <!-- 搜索区域 -->
    <div class="search-section">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="活动名称">
          <el-input v-model="searchForm.name" placeholder="请输入活动名称" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
          <el-button 
            type="warning" 
            @click="handleSmartRecommend"
            v-if="userInfo.is_graduated"
          >一键生成智能推荐</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 活动列表 -->
    <el-table
      :data="showRecommendOnly ? [recommendedActivity] : activityList"
      style="width: 100%"
      border
    >
      <el-table-column prop="name" label="活动名称" min-width="150" />
      <el-table-column prop="description" label="活动介绍" min-width="200" show-overflow-tooltip />
      <el-table-column prop="applicant_name" label="申请人姓名" min-width="120" />
      <el-table-column prop="phone" label="电话" min-width="120" />
      <el-table-column prop="organization" label="举办组织" min-width="150" />
      <el-table-column prop="venue" label="场地设施" min-width="150" />
      <el-table-column prop="event_time" label="活动举办时间" min-width="180">
        <template #default="scope">
          {{ formatDateTime(scope.row.event_time) }}
        </template>
      </el-table-column>
      <el-table-column prop="registration_count" label="报名人数" min-width="100" />
      <el-table-column label="操作" fixed="right" width="120">
        <template #default="scope">
          <el-button
            type="primary"
            size="small"
            :disabled="scope.row.is_registered"
            @click="handleRegister(scope.row)"
          >
            {{ scope.row.is_registered ? '已报名' : '报名' }}
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <div class="pagination" v-if="!showRecommendOnly">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '@/utils/request'

export default {
  name: 'ActivityRegistration',
  setup() {
    // 搜索表单
    const searchForm = ref({
      name: ''
    })

    // 用户信息
    const userInfo = ref({
      student_id: '',
      is_graduated: false
    })

    // 列表数据
    const activityList = ref([])
    const currentPage = ref(1)
    const pageSize = ref(10)
    const total = ref(0)

    // 推荐相关
    const showRecommendOnly = ref(false)
    const recommendedActivity = ref(null)

    // 获取用户信息
    const getUserInfo = async () => {
      try {
        const response = await request.get('/api/alumni/current/')
        userInfo.value = response.data
      } catch (error) {
        console.error('获取用户信息失败:', error)
      }
    }

    // 获取活动列表
    const getActivityList = async () => {
      try {
        const params = {
          page: currentPage.value,
          page_size: pageSize.value,
          name: searchForm.value.name
        }
        const response = await request.get('/api/activities/registration/list/', { params })
        if (response.data && response.data.results) {
          activityList.value = response.data.results
          total.value = response.data.count
        } else {
          activityList.value = []
          total.value = 0
        }
      } catch (error) {
        console.error('获取活动列表失败:', error)
        ElMessage.error('获取活动列表失败')
        activityList.value = []
        total.value = 0
      }
    }

    // 智能推荐
    const handleSmartRecommend = async () => {
      try {
        // 先获取所有活动
        const response = await request.get('/api/activities/registration/list/', {
          params: { page: 1, page_size: 1000 }
        })
        
        if (response.data && response.data.results && response.data.results.length > 0) {
          const activities = response.data.results
          const studentId = parseInt(userInfo.value.student_id)
          const index = studentId % activities.length
          recommendedActivity.value = activities[index]
          showRecommendOnly.value = true
          ElMessage.success('已为您智能推荐最适合的活动')
        } else {
          ElMessage.warning('暂无可推荐的活动')
        }
      } catch (error) {
        console.error('智能推荐失败:', error)
        ElMessage.error('智能推荐失败')
      }
    }

    // 格式化日期时间
    const formatDateTime = (datetime) => {
      if (!datetime) return ''
      const date = new Date(datetime)
      return date.toLocaleString()
    }

    // 搜索和重置
    const handleSearch = () => {
      showRecommendOnly.value = false
      currentPage.value = 1
      getActivityList()
    }

    const handleReset = () => {
      showRecommendOnly.value = false
      searchForm.value = {
        name: ''
      }
      handleSearch()
    }

    // 报名活动
    const handleRegister = async (activity) => {
      try {
        await ElMessageBox.confirm('确认报名该活动吗？', '提示', {
          type: 'warning',
          confirmButtonText: '确定',
          cancelButtonText: '取消'
        })
        
        await request.post(`/api/activities/${activity.id}/register/`)
        ElMessage.success('报名成功')
        if (showRecommendOnly.value) {
          recommendedActivity.value.is_registered = true
        } else {
          getActivityList()
        }
      } catch (error) {
        if (error !== 'cancel') {
          console.error('报名失败:', error)
          ElMessage.error(error.response?.data?.error || '报名失败')
        }
      }
    }

    // 分页
    const handleSizeChange = (val) => {
      pageSize.value = val
      getActivityList()
    }

    const handleCurrentChange = (val) => {
      currentPage.value = val
      getActivityList()
    }

    onMounted(() => {
      getUserInfo()
      getActivityList()
    })

    return {
      searchForm,
      userInfo,
      activityList,
      currentPage,
      pageSize,
      total,
      showRecommendOnly,
      recommendedActivity,
      handleSearch,
      handleReset,
      handleRegister,
      handleSizeChange,
      handleCurrentChange,
      handleSmartRecommend,
      formatDateTime
    }
  }
}
</script>

<style scoped>
.activity-registration {
  padding: 20px;
}

.search-section {
  background: #fff;
  padding: 20px;
  border-radius: 4px;
  margin-bottom: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.pagination {
  margin-top: 20px;
  text-align: right;
}
</style> 