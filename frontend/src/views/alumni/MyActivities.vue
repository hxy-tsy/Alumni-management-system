<template>
  <div class="my-activities">
    <!-- 搜索区域 -->
    <div class="search-section">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="活动名称">
          <el-input v-model="searchForm.name" placeholder="请输入活动名称" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 活动列表 -->
    <el-table
      :data="activityList"
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
      <el-table-column label="操作" fixed="right" width="280">
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
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
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
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '@/utils/request'

export default {
  name: 'MyActivities',
  setup() {
    // 搜索表单
    const searchForm = ref({
      name: ''
    })

    // 列表数据
    const activityList = ref([])
    const currentPage = ref(1)
    const pageSize = ref(10)
    const total = ref(0)

    // 返校预约相关
    const qrCodeVisible = ref(false)
    
    // 活动反馈相关
    const feedbackVisible = ref(false)
    const feedbackForm = ref({
      activity: null,
      rating: 5,
      comment: ''
    })

    // 获取我的活动列表
    const getActivityList = async () => {
      try {
        const params = {
          page: currentPage.value,
          page_size: pageSize.value,
          name: searchForm.value.name
        }
        const response = await request.get('/api/activities/my-activities/', { params })
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

    // 格式化日期时间
    const formatDateTime = (datetime) => {
      if (!datetime) return ''
      const date = new Date(datetime)
      return date.toLocaleString()
    }

    // 搜索和重置
    const handleSearch = () => {
      currentPage.value = 1
      getActivityList()
    }

    const handleReset = () => {
      searchForm.value = {
        name: ''
      }
      handleSearch()
    }

    // 取消报名
    const handleCancelRegistration = async (activity) => {
      try {
        await ElMessageBox.confirm('确认取消报名该活动吗？', '提示', {
          type: 'warning',
          confirmButtonText: '确定',
          cancelButtonText: '取消'
        })
        
        await request.post(`/api/activities/cancel-registration/${activity.id}/`)
        ElMessage.success('取消报名成功')
        getActivityList()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('取消报名失败:', error)
          ElMessage.error(error.response?.data?.error || '取消报名失败')
        }
      }
    }

    // 返校预约
    const handleReturnVisit = () => {
      qrCodeVisible.value = true
    }

    // 活动反馈
    const handleFeedback = async (activity) => {
      try {
        // 获取现有反馈（如果有的话）
        const response = await request.get(`/api/activities/feedback/${activity.id}/get/`)
        feedbackForm.value = {
          activity: activity.id,
          rating: response.data.rating || 5,
          comment: response.data.comment || ''
        }
        feedbackVisible.value = true
      } catch (error) {
        console.error('获取反馈状态失败:', error)
        ElMessage.error('获取反馈状态失败')
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
        ElMessage.error(error.response?.data?.error || '提交反馈失败')
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
      getActivityList()
    })

    return {
      searchForm,
      activityList,
      currentPage,
      pageSize,
      total,
      qrCodeVisible,
      feedbackVisible,
      feedbackForm,
      handleSearch,
      handleReset,
      handleCancelRegistration,
      handleReturnVisit,
      handleFeedback,
      submitFeedback,
      handleSizeChange,
      handleCurrentChange,
      formatDateTime
    }
  }
}
</script>

<style scoped>
.my-activities {
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