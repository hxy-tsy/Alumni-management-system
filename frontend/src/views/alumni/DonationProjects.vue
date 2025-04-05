<template>
  <div class="donation-projects">
    <!-- 搜索区域 -->
    <div class="search-section">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="捐赠项目">
          <el-input v-model="searchForm.name" placeholder="请输入捐赠项目名称" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 捐赠项目列表 -->
    <el-table
      :data="projectList"
      style="width: 100%"
      border
      v-loading="loading"
    >
      <el-table-column prop="name" label="捐赠项目" min-width="150" />
      <el-table-column prop="type" label="捐赠类型" min-width="120" />
      <el-table-column prop="purpose" label="捐赠目的" min-width="200" show-overflow-tooltip />
      <el-table-column label="已完成捐赠目标" min-width="150">
        <template #default="scope">
          <el-progress
            :percentage="calculateProgress(scope.row)"
            :format="percentageFormat"
          />
          <div class="donation-amount">
            {{ formatAmount(scope.row.current_amount) }} / {{ formatAmount(scope.row.target_amount) }}
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="donor_count" label="捐赠人数" min-width="100" />
      <el-table-column prop="end_time" label="截止时间" min-width="180">
        <template #default="scope">
          {{ formatDateTime(scope.row.end_time) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" fixed="right" width="120">
        <template #default="scope">
          <el-button
            type="primary"
            size="small"
            @click="handleDonate(scope.row)"
            :disabled="scope.row.hasDonated"
          >
            {{ scope.row.hasDonated ? '已捐赠' : '我要捐赠' }}
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

    <!-- 捐赠对话框 -->
    <el-dialog
      v-model="donationVisible"
      title="捐赠"
      width="500px"
    >
      <el-form :model="donationForm" label-width="100px">
        <el-form-item label="捐赠项目">
          <span>{{ currentProject?.name }}</span>
        </el-form-item>
        <el-form-item label="捐赠类型">
          <span>{{ currentProject?.type }}</span>
        </el-form-item>
        <el-form-item label="捐赠金额">
          <el-input-number
            v-model="donationForm.amount"
            :min="1"
            :precision="2"
            :step="100"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="donationVisible = false">取消</el-button>
          <el-button type="primary" @click="submitDonation">确认捐赠</el-button>
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
  name: 'DonationProjects',
  setup() {
    // 搜索表单
    const searchForm = ref({
      name: ''
    })

    // 列表数据
    const projectList = ref([])
    const loading = ref(false)
    const currentPage = ref(1)
    const pageSize = ref(10)
    const total = ref(0)

    // 捐赠相关
    const donationVisible = ref(false)
    const currentProject = ref(null)
    const donationForm = ref({
      amount: 100
    })

    // 获取捐赠项目列表
    const getProjectList = async () => {
      loading.value = true
      try {
        const params = {
          page: currentPage.value,
          page_size: pageSize.value,
          name: searchForm.value.name
        }
        const response = await request.get('/api/donations/projects/', { params })
        if (response.data && response.data.results) {
          projectList.value = response.data.results
          total.value = response.data.count
        } else {
          projectList.value = []
          total.value = 0
        }
      } catch (error) {
        console.error('获取捐赠项目列表失败:', error)
        ElMessage.error('获取捐赠项目列表失败')
      } finally {
        loading.value = false
      }
    }

    // 格式化日期时间
    const formatDateTime = (datetime) => {
      if (!datetime) return ''
      const date = new Date(datetime)
      return date.toLocaleString()
    }

    // 格式化金额
    const formatAmount = (amount) => {
      return `￥${amount.toLocaleString()}`
    }

    // 计算进度
    const calculateProgress = (project) => {
      return Math.min(100, (project.current_amount / project.target_amount) * 100)
    }

    // 格式化百分比
    const percentageFormat = (percentage) => {
      return percentage.toFixed(1) + '%'
    }

    // 检查项目是否过期
    const isProjectExpired = (project) => {
      return new Date(project.end_time) < new Date()
    }

    // 搜索和重置
    const handleSearch = () => {
      currentPage.value = 1
      getProjectList()
    }

    const handleReset = () => {
      searchForm.value = {
        name: ''
      }
      handleSearch()
    }

    // 捐赠相关
    const handleDonate = (project) => {
      currentProject.value = project
      donationForm.value = {
        amount: 100
      }
      donationVisible.value = true
    }

    const submitDonation = async () => {
      try {
        await request.post(`/api/donations/projects/${currentProject.value.id}/donate/`, {
          amount: donationForm.value.amount
        })
        ElMessage.success('捐赠成功，感谢您的支持！')
        donationVisible.value = false
        
        // 更新项目状态
        currentProject.value.hasDonated = true
        currentProject.value.current_amount += donationForm.value.amount
        currentProject.value.donor_count += 1
        
        // 刷新列表
        getProjectList()
      } catch (error) {
        console.error('捐赠失败:', error)
        ElMessage.error(error.response?.data?.error || '捐赠失败')
      }
    }

    // 分页
    const handleSizeChange = (val) => {
      pageSize.value = val
      getProjectList()
    }

    const handleCurrentChange = (val) => {
      currentPage.value = val
      getProjectList()
    }

    onMounted(() => {
      getProjectList()
    })

    return {
      searchForm,
      projectList,
      loading,
      currentPage,
      pageSize,
      total,
      donationVisible,
      currentProject,
      donationForm,
      handleSearch,
      handleReset,
      handleDonate,
      submitDonation,
      handleSizeChange,
      handleCurrentChange,
      formatDateTime,
      formatAmount,
      calculateProgress,
      percentageFormat,
      isProjectExpired
    }
  }
}
</script>

<style scoped>
.donation-projects {
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

.donation-amount {
  margin-top: 5px;
  font-size: 12px;
  color: #606266;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}
</style> 