<template>
  <div class="my-activities">
    <div class="page-header">
      <h2>我的活动</h2>
    </div>

    <!-- 搜索栏 -->
    <div class="search-bar">
      <el-input
        v-model="searchQuery"
        placeholder="搜索活动名称"
        clearable
        @clear="handleSearch"
        style="width: 300px"
      >
        <template #append>
          <el-button @click="handleSearch">
            <el-icon><Search /></el-icon>
          </el-button>
        </template>
      </el-input>
    </div>

    <!-- 活动列表 -->
    <el-table :data="activities" style="width: 100%" v-loading="loading">
      <el-table-column prop="name" label="活动名称" />
      <el-table-column prop="description" label="活动介绍" show-overflow-tooltip />
      <el-table-column prop="organization" label="举办组织" />
      <el-table-column prop="venue" label="场地" />
      <el-table-column prop="event_time" label="活动时间">
        <template #default="scope">
          {{ formatDate(scope.row.event_time) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="280">
        <template #default="scope">
          <el-button
            type="danger"
            size="small"
            @click="handleCancelRegistration(scope.row)"
          >
            取消报名
          </el-button>
          <el-button
            type="primary"
            size="small"
            @click="handleReturnVisit(scope.row)"
          >
            返校预约
          </el-button>
          <el-button
            type="success"
            size="small"
            @click="handleFeedback(scope.row)"
          >
            活动反馈
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <div class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 30, 50]"
        layout="total, sizes, prev, pager, next"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <!-- 返校预约二维码对话框 -->
    <el-dialog
      v-model="qrCodeVisible"
      title="返校预约"
      width="400px"
      center
    >
      <div class="qr-code-container">
        <img src="/static/images/return-visit-qr.png" alt="返校预约二维码" style="width: 200px; height: 200px;">
        <p class="qr-code-tip">请扫描二维码进行返校预约</p>
      </div>
    </el-dialog>

    <!-- 活动反馈对话框 -->
    <el-dialog
      v-model="feedbackVisible"
      title="活动反馈"
      width="500px"
    >
      <el-form :model="feedbackForm" label-width="80px">
        <el-form-item label="活动评分">
          <el-rate
            v-model="feedbackForm.rating"
            :max="5"
            :allow-half="true"
            show-score
          />
        </el-form-item>
        <el-form-item label="评价内容">
          <el-input
            v-model="feedbackForm.comment"
            type="textarea"
            :rows="4"
            placeholder="请输入您的评价内容"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="feedbackVisible = false">取消</el-button>
          <el-button type="primary" @click="submitFeedback">提交</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { Search } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import request from '@/utils/request'

export default {
  name: 'MyActivities',
  components: {
    Search
  },
  setup() {
    const activities = ref([])
    const loading = ref(false)
    const currentPage = ref(1)
    const pageSize = ref(10)
    const total = ref(0)
    const searchQuery = ref('')
    
    // 返校预约相关
    const qrCodeVisible = ref(false)
    
    // 活动反馈相关
    const feedbackVisible = ref(false)
    const feedbackForm = ref({
      activity: null,
      rating: 5,
      comment: ''
    })
    
    // 格式化日期
    const formatDate = (dateStr) => {
      if (!dateStr) return ''
      const date = new Date(dateStr)
      return date.toLocaleString()
    }

    // 获取活动列表
    const fetchActivities = async () => {
      loading.value = true
      try {
        const response = await request.get('/api/activities/my-activities/', {
          params: {
            page: currentPage.value,
            page_size: pageSize.value,
            name: searchQuery.value
          }
        })
        activities.value = response.data.results
        total.value = response.data.count
      } catch (error) {
        console.error('获取活动列表失败:', error)
        ElMessage.error('获取活动列表失败')
      } finally {
        loading.value = false
      }
    }

    // 取消报名
    const handleCancelRegistration = async (activity) => {
      try {
        await request.post(`/api/activities/cancel-registration/${activity.id}/`)
        ElMessage.success('取消报名成功')
        fetchActivities()
      } catch (error) {
        console.error('取消报名失败:', error)
        ElMessage.error('取消报名失败')
      }
    }

    // 返校预约
    const handleReturnVisit = (activity) => {
      qrCodeVisible.value = true
    }

    // 活动反馈
    const handleFeedback = async (activity) => {
      try {
        // 先检查是否已经提交过反馈
        const response = await request.get(`/api/activities/feedback/${activity.id}/get/`)
        if (response.data && response.data.id) {
          ElMessage.warning('您已经提交过反馈')
          return
        }
      } catch (error) {
        // 如果是404错误，说明还没有提交过反馈
        if (error.response && error.response.status === 404) {
          feedbackForm.value.activity = activity.id
          feedbackVisible.value = true
        } else {
          console.error('检查反馈状态失败:', error)
          ElMessage.error('检查反馈状态失败')
        }
      }
    }

    // 提交反馈
    const submitFeedback = async () => {
      try {
        await request.post(`/api/activities/feedback/${feedbackForm.value.activity}/`, {
          rating: feedbackForm.value.rating,
          comment: feedbackForm.value.comment
        })
        ElMessage.success('反馈提交成功')
        feedbackVisible.value = false
        // 重置表单
        feedbackForm.value = {
          activity: null,
          rating: 5,
          comment: ''
        }
      } catch (error) {
        console.error('提交反馈失败:', error)
        ElMessage.error('提交反馈失败')
      }
    }

    // 搜索处理
    const handleSearch = () => {
      currentPage.value = 1
      fetchActivities()
    }

    // 分页处理
    const handleSizeChange = (val) => {
      pageSize.value = val
      fetchActivities()
    }

    const handleCurrentChange = (val) => {
      currentPage.value = val
      fetchActivities()
    }

    onMounted(() => {
      fetchActivities()
    })

    return {
      activities,
      loading,
      currentPage,
      pageSize,
      total,
      searchQuery,
      qrCodeVisible,
      feedbackVisible,
      feedbackForm,
      formatDate,
      handleSearch,
      handleSizeChange,
      handleCurrentChange,
      handleCancelRegistration,
      handleReturnVisit,
      handleFeedback,
      submitFeedback
    }
  }
}
</script>

<style scoped>
.my-activities {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  font-size: 24px;
  color: #303133;
}

.search-bar {
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.qr-code-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

.qr-code-tip {
  margin-top: 15px;
  color: #606266;
  font-size: 14px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}
</style> 