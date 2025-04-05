<template>
  <div class="association-members">
    <!-- 搜索区域 -->
    <div class="search-section">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="学号">
          <el-input v-model="searchForm.student_id" placeholder="请输入学号" />
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="searchForm.name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="学院">
          <el-input v-model="searchForm.department" placeholder="请输入学院" />
        </el-form-item>
        <el-form-item label="班级">
          <el-input v-model="searchForm.class_name" placeholder="请输入班级" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 操作按钮区域 -->
    <div class="action-buttons">
      <el-button type="success" @click="handleExport">导出</el-button>
      <el-button type="danger" @click="handleBatchDelete">批量删除</el-button>
    </div>

    <!-- 成员列表区域 -->
    <div class="members-table">
      <el-table
        :data="membersList"
        style="width: 100%"
        border
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column label="学号" min-width="120">
          <template #default="scope">
            {{ scope.row.profile?.student_id || scope.row.user?.student_id || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="姓名" min-width="100">
          <template #default="scope">
            {{ formatName(scope.row.user) }}
          </template>
        </el-table-column>
        <el-table-column label="电话" min-width="120">
          <template #default="scope">
            {{ scope.row.user?.phone || '-' }}
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
        <el-table-column label="毕业时间" min-width="120">
          <template #default="scope">
            {{ scope.row.profile?.graduation_date || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="毕业去向" min-width="150">
          <template #default="scope">
            {{ scope.row.profile?.current_company || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="审核状态" min-width="100">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" fixed="right" width="250">
          <template #default="scope">
            <el-button
              v-if="scope.row.status === 1 || scope.row.status === 3"
              type="success"
              size="small"
              @click="handleApprove(scope.row)"
              :loading="approveLoading === scope.row.id"
            >
              通过
            </el-button>
            <el-button
              v-if="scope.row.status === 1"
              type="info"
              size="small"
              @click="handleReject(scope.row)"
              :loading="rejectLoading === scope.row.id"
            >
              不通过
            </el-button>
            <el-button 
              type="danger" 
              size="small" 
              @click="handleDelete(scope.row)"
              :disabled="scope.row.status !== 2"
              v-if="scope.row.status === 1 || scope.row.status === 2"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-container">
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
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '@/utils/request'
import store from '@/store'

export default {
  name: 'AssociationMembers',
  setup() {
    // 搜索表单
    const searchForm = ref({
      student_id: '',
      name: '',
      department: '',
      class_name: ''
    })

    // 分页相关
    const currentPage = ref(1)
    const pageSize = ref(10)
    const total = ref(0)

    // 成员列表
    const membersList = ref([])
    const selectedMembers = ref([])
    const approveLoading = ref(null)
    const rejectLoading = ref(null)

    // 获取认证头信息
    const getAuthHeaders = () => {
      const token = store.state.token || localStorage.getItem('token') || ''
      return {
        Authorization: token ? `Bearer ${token}` : ''
      }
    }

    // 获取状态类型
    const getStatusType = (status) => {
      switch (status) {
        case 1:
          return 'warning'  // 审核中
        case 2:
          return 'success'  // 已通过
        case 3:
          return 'danger'   // 已拒绝
        default:
          return 'info'     // 默认状态
      }
    }

    // 获取状态文本
    const getStatusText = (status) => {
      switch (status) {
        case 1:
          return '审核中'
        case 2:
          return '已通过'
        case 3:
          return '已拒绝'
        default:
          return '默认'
      }
    }

    // 获取成员列表
    const fetchMembersList = async () => {
      try {
        const params = {
          page: currentPage.value,
          page_size: pageSize.value,
          ...searchForm.value
        }

        const response = await request.get('/api/association/my-branch/members/', { params })
        console.log('获取到的成员数据:', response.data)
        
        if (response.data.results && response.data.results.length > 0) {
          console.log('第一个成员数据示例:', response.data.results[0])
          
          // 处理数据，确保所有字段都存在
          membersList.value = response.data.results.map(processMemberData)
        } else {
          membersList.value = []
        }
        
        total.value = response.data.count || 0
      } catch (error) {
        console.error('获取成员列表失败:', error)
        ElMessage.error('获取成员列表失败: ' + (error.response?.data?.error || error.message || '未知错误'))
      }
    }

    // 处理成员数据，确保所有字段都存在
    const processMemberData = (member) => {
      // 确保 user 对象存在
      if (!member.user) {
        member.user = {}
      }
      
      // 确保 profile 对象存在
      if (!member.profile) {
        member.profile = {}
      }
      
      // 确保电话字段存在
      if (!member.user.phone) {
        member.user.phone = '-'
      }
      
      // 确保学院字段存在
      if (!member.user.department) {
        member.user.department = '-'
      }
      
      // 如果 profile 中没有学号，但 user 中有，则使用 user 中的
      if (!member.profile.student_id && member.user.student_id) {
        member.profile.student_id = member.user.student_id
      }
      
      return member
    }

    // 通过申请
    const handleApprove = async (row) => {
      try {
        approveLoading.value = row.id
        
        await ElMessageBox.confirm(
          '确定要通过该成员的申请吗？',
          '确认操作',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
          }
        )
        
        const response = await request.put(`/api/association/my-branch/applications/${row.id}/`, {
          action: 'approve'
        })
        
        ElMessage.success(response.data.message || '申请已通过')
        
        // 刷新列表
        fetchMembersList()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('处理申请失败:', error)
          ElMessage.error('处理申请失败: ' + (error.response?.data?.error || error.message || '未知错误'))
        }
      } finally {
        approveLoading.value = null
      }
    }

    // 拒绝申请
    const handleReject = async (row) => {
      try {
        rejectLoading.value = row.id
        
        await ElMessageBox.confirm(
          '确定要拒绝该成员的申请吗？',
          '确认操作',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
          }
        )
        
        const response = await request.put(`/api/association/my-branch/applications/${row.id}/`, {
          action: 'reject'
        })
        
        ElMessage.success(response.data.message || '已拒绝申请')
        
        // 刷新列表
        fetchMembersList()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('处理申请失败:', error)
          ElMessage.error('处理申请失败: ' + (error.response?.data?.error || error.message || '未知错误'))
        }
      } finally {
        rejectLoading.value = null
      }
    }

    // 搜索
    const handleSearch = () => {
      currentPage.value = 1
      fetchMembersList()
    }

    // 重置搜索
    const handleReset = () => {
      searchForm.value = {
        student_id: '',
        name: '',
        department: '',
        class_name: ''
      }
      currentPage.value = 1
      fetchMembersList()
    }

    // 分页大小变化
    const handleSizeChange = (val) => {
      pageSize.value = val
      fetchMembersList()
    }

    // 当前页变化
    const handleCurrentChange = (val) => {
      currentPage.value = val
      fetchMembersList()
    }

    // 选择变化
    const handleSelectionChange = (val) => {
      selectedMembers.value = val
    }

    // 删除成员
    const handleDelete = async (row) => {
      try {
        // 如果状态不是已通过，则不允许删除
        if (row.status !== 2) {
          ElMessage.warning('只能删除已通过审核的成员')
          return
        }

        await ElMessageBox.confirm(
          `确定要删除成员 ${formatName(row.user)} 吗？`,
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
          }
        )

        await request.delete(`/api/association/my-branch/members/${row.id}/delete/`)
        ElMessage.success('删除成功')

        // 刷新列表
        fetchMembersList()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除成员失败:', error)
          ElMessage.error('删除成员失败: ' + (error.response?.data?.error || error.message || '未知错误'))
        }
      }
    }

    // 批量删除成员
    const handleBatchDelete = async () => {
      if (selectedMembers.value.length === 0) {
        ElMessage.warning('请选择要删除的成员')
        return
      }

      // 检查是否所有选中的成员都是已通过状态
      const hasInvalidStatus = selectedMembers.value.some(member => member.status !== 2)
      if (hasInvalidStatus) {
        ElMessage.warning('只能删除已通过审核的成员')
        return
      }

      try {
        await ElMessageBox.confirm(
          `确定要删除选中的 ${selectedMembers.value.length} 名成员吗？`,
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
          }
        )

        const ids = selectedMembers.value.map(member => member.id)
        await request.post('/api/association/my-branch/members/batch-delete/', { ids })
        ElMessage.success('批量删除成功')

        // 刷新列表
        fetchMembersList()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('批量删除失败:', error)
          ElMessage.error('批量删除失败: ' + (error.response?.data?.error || error.message || '未知错误'))
        }
      }
    }

    // 导出
    const handleExport = async () => {
      try {
        const response = await request.get('/api/association/my-branch/members/export/', {
          params: searchForm.value,
          responseType: 'blob'
        })
        
        const blob = new Blob([response.data], { type: 'application/vnd.ms-excel' })
        const link = document.createElement('a')
        link.href = URL.createObjectURL(blob)
        link.download = '校友会成员列表.xlsx'
        link.click()
        URL.revokeObjectURL(link.href)
        
        ElMessage.success('导出成功')
      } catch (error) {
        console.error('导出失败:', error)
        ElMessage.error('导出失败: ' + (error.response?.data?.error || error.message || '未知错误'))
      }
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
      fetchMembersList()
    })

    return {
      searchForm,
      currentPage,
      pageSize,
      total,
      membersList,
      selectedMembers,
      approveLoading,
      rejectLoading,
      handleSearch,
      handleReset,
      handleSizeChange,
      handleCurrentChange,
      handleSelectionChange,
      handleDelete,
      handleBatchDelete,
      handleExport,
      handleApprove,
      handleReject,
      formatName,
      getStatusType,
      getStatusText
    }
  }
}
</script>

<style scoped>
.association-members {
  padding: 20px;
}

.search-section {
  background: #fff;
  padding: 20px;
  border-radius: 4px;
  margin-bottom: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.action-buttons {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
}

.members-table {
  background: #fff;
  padding: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>