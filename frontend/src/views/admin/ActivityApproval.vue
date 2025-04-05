<template>
  <div class="activity-approval">
    <!-- 搜索区域 -->
    <div class="search-section">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="活动名称">
          <el-input v-model="searchForm.name" placeholder="请输入活动名称" />
        </el-form-item>
        <el-form-item label="申请人">
          <el-input v-model="searchForm.applicant_name" placeholder="请输入申请人姓名" />
        </el-form-item>
        <el-form-item label="审批状态" style="width: 190px">
          <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
            <el-option label="审核中" value="1" />
            <el-option label="审核通过" value="2" />
            <el-option label="审核不通过" value="3" />
          </el-select>
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
      <el-table-column prop="apply_time" label="申请时间" min-width="180">
        <template #default="scope">
          {{ formatDateTime(scope.row.apply_time) }}
        </template>
      </el-table-column>
      <el-table-column prop="event_time" label="活动举办时间" min-width="180">
        <template #default="scope">
          {{ formatDateTime(scope.row.event_time) }}
        </template>
      </el-table-column>
      <el-table-column prop="status" label="审批状态" min-width="100">
        <template #default="scope">
          <el-tag :type="getStatusType(scope.row.status)">
            {{ getStatusText(scope.row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" fixed="right" width="200">
        <template #default="scope">
          <el-button
            type="success"
            size="small"
            @click="handleApprove(scope.row)"
            :disabled="scope.row.status !== 1"
          >通过</el-button>
          <el-button
            type="danger"
            size="small"
            @click="handleReject(scope.row)"
            :disabled="scope.row.status !== 1"
          >不通过</el-button>
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
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '@/utils/request'

export default {
  name: 'ActivityApproval',
  setup() {
    // 搜索表单
    const searchForm = ref({
      name: '',
      applicant_name: '',
      status: ''
    })

    // 列表数据
    const activityList = ref([])
    const currentPage = ref(1)
    const pageSize = ref(10)
    const total = ref(0)

    // 获取活动列表
    const getActivityList = async () => {
      try {
        const params = {
          page: currentPage.value,
          page_size: pageSize.value,
          name: searchForm.value.name,
          applicant_name: searchForm.value.applicant_name,
          status: searchForm.value.status
        }
        const response = await request.get('/api/activities/list/', { params })
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

    // 状态相关方法
    const getStatusType = (status) => {
      const statusMap = {
        0: 'info',    // 默认
        1: 'warning', // 申请中
        2: 'success', // 已通过
        3: 'danger'   // 已拒绝
      }
      return statusMap[status] || 'info'
    }

    const getStatusText = (status) => {
      const statusMap = {
        0: '默认',
        1: '申请中',
        2: '已通过',
        3: '已拒绝'
      }
      return statusMap[status] || '未知'
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
        name: '',
        applicant_name: '',
        status: ''
      }
      handleSearch()
    }

    // 审批操作
    const handleApprove = async (row) => {
      try {
        await ElMessageBox.confirm('确认通过该活动申请吗？', '提示', {
          type: 'warning',
          confirmButtonText: '确定',
          cancelButtonText: '取消'
        })
        
        await request.post(`/api/activities/${row.id}/approve/`)
        ElMessage.success('审批通过成功')
        getActivityList()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('审批失败:', error)
          ElMessage.error(error.response?.data?.error || '审批失败')
        }
      }
    }

    const handleReject = async (row) => {
      try {
        await ElMessageBox.confirm('确认拒绝该活动申请吗？', '提示', {
          type: 'warning',
          confirmButtonText: '确定',
          cancelButtonText: '取消'
        })
        
        await request.post(`/api/activities/${row.id}/reject/`)
        ElMessage.success('已拒绝该活动申请')
        getActivityList()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('操作失败:', error)
          ElMessage.error(error.response?.data?.error || '操作失败')
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
      getActivityList()
    })

    return {
      searchForm,
      activityList,
      currentPage,
      pageSize,
      total,
      handleSearch,
      handleReset,
      handleApprove,
      handleReject,
      handleSizeChange,
      handleCurrentChange,
      getStatusType,
      getStatusText,
      formatDateTime
    }
  }
}
</script>

<style scoped>
.activity-approval {
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

.el-tag {
  margin-right: 8px;
}
</style> 