<template>
  <div class="activity-publish">
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

    <!-- 工具栏 -->
    <div class="toolbar">
      <el-button type="primary" @click="handleAdd">新增</el-button>
      <el-button type="danger" @click="handleBatchDelete">批量删除</el-button>
      <el-button type="success" @click="handleImport">导入</el-button>
      <el-button type="warning" @click="handleExport">导出</el-button>
    </div>

    <!-- 活动列表 -->
    <el-table
      :data="activityList"
      style="width: 100%"
      @selection-change="handleSelectionChange"
      border
    >
      <el-table-column type="selection" width="55" />
      <el-table-column prop="name" label="活动名称" min-width="150" >
        <template #default="scope">
          {{scope.row.name}}
        </template>
      </el-table-column>
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
      <el-table-column label="操作" fixed="right" width="250">
        <template #default="scope">
          <el-button
            type="primary"
            size="small"
            @click="handleEdit(scope.row)"
            :disabled="scope.row.status === 2"
          >编辑</el-button>
          <el-button
            type="danger"
            size="small"
            @click="handleDelete(scope.row)"
            :disabled="scope.row.status === 2"
          >删除</el-button>
          <el-button
            type="warning"
            size="small"
            @click="handleReapply(scope.row)"
            :disabled="scope.row.status !== 3"
          >重新申请</el-button>
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

    <!-- 新增/编辑对话框 -->
    <el-dialog
      :title="dialogTitle"
      v-model="dialogVisible"
      width="650px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="formRef"
        :model="formData"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="活动名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入活动名称" />
        </el-form-item>
        <el-form-item label="活动介绍" prop="description">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="4"
            placeholder="请输入活动介绍"
          />
        </el-form-item>
        <el-form-item label="申请人姓名" prop="applicant_name">
          <el-input v-model="formData.applicant_name" placeholder="请输入申请人姓名" />
        </el-form-item>
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="formData.phone" placeholder="请输入联系电话" />
        </el-form-item>
        <el-form-item label="举办组织" prop="organization">
          <el-input v-model="formData.organization" placeholder="请输入举办组织" />
        </el-form-item>
        <el-form-item label="场地设施" prop="venue">
          <el-input v-model="formData.venue" placeholder="请输入场地设施" />
        </el-form-item>
        <el-form-item label="活动时间" prop="event_time">
          <el-date-picker
            v-model="formData.event_time"
            type="datetime"
            placeholder="选择活动时间"
            style="width: 100%"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
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
  name: 'ActivityPublish',
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
    const selectedRows = ref([])

    // 对话框数据
    const dialogVisible = ref(false)
    const dialogTitle = ref('新增活动')
    const formRef = ref(null)
    const formData = ref({
      name: '',
      description: '',
      applicant_name: '',
      phone: '',
      organization: '',
      venue: '',
      event_time: ''
    })

    // 表单验证规则
    const rules = {
      name: [{ required: true, message: '请输入活动名称', trigger: 'blur' }],
      description: [{ required: true, message: '请输入活动介绍', trigger: 'blur' }],
      applicant_name: [{ required: true, message: '请输入申请人姓名', trigger: 'blur' }],
      phone: [{ required: true, message: '请输入联系电话', trigger: 'blur' }],
      organization: [{ required: true, message: '请输入举办组织', trigger: 'blur' }],
      venue: [{ required: true, message: '请输入场地设施', trigger: 'blur' }],
      event_time: [{ required: true, message: '请选择活动时间', trigger: 'change' }]
    }

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
        console.log('活动列表响应:', response)  // 添加详细的日志
        if (response.data && response.data.results) {
          activityList.value = response.data.results
          total.value = response.data.count
        } else {
          activityList.value = []
          total.value = 0
          console.warn('未获取到活动数据')
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
        organization: '',
        status: ''
      }
      handleSearch()
    }

    // 表格选择
    const handleSelectionChange = (val) => {
      selectedRows.value = val
    }

    // 新增活动
    const handleAdd = () => {
      dialogTitle.value = '新增活动'
      formData.value = {
        name: '',
        description: '',
        applicant_name: '',
        phone: '',
        organization: '',
        venue: '',
        event_time: ''
      }
      dialogVisible.value = true
    }

    // 编辑活动
    const handleEdit = (row) => {
      dialogTitle.value = '编辑活动'
      formData.value = {
        ...row,
        event_time: row.event_time ? new Date(row.event_time) : null
      }
      dialogVisible.value = true
    }

    // 删除活动
    const handleDelete = async (row) => {
      try {
        await ElMessageBox.confirm('确认删除该活动吗？', '提示', {
          type: 'warning',
          confirmButtonText: '确定',
          cancelButtonText: '取消'
        })
        await request.delete(`/api/activities/${row.id}/`)
        ElMessage.success('删除成功')
        getActivityList()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除失败:', error)
          if (error.response?.data?.error) {
            ElMessage.error(error.response.data.error)
          } else {
            ElMessage.error('删除失败')
          }
        }
      }
    }

    // 批量删除
    const handleBatchDelete = async () => {
      if (selectedRows.value.length === 0) {
        ElMessage.warning('请选择要删除的活动')
        return
      }

      try {
        await ElMessageBox.confirm('确认删除选中的活动吗？', '提示', {
          type: 'warning',
          confirmButtonText: '确定',
          cancelButtonText: '取消'
        })
        
        await request.post('/api/activities/batch-delete/', {
          ids: selectedRows.value.map(row => row.id)
        })
        
        ElMessage.success('批量删除成功')
        getActivityList()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('批量删除失败:', error)
          if (error.response?.data?.error) {
            ElMessage.error(error.response.data.error)
          } else {
            ElMessage.error('批量删除失败')
          }
        }
      }
    }

    // 导入导出
    const handleImport = () => {
      const input = document.createElement('input')
      input.type = 'file'
      input.accept = '.xlsx,.xls'
      input.onchange = async (e) => {
        const file = e.target.files[0]
        if (!file) return
        
        // 检查文件类型
        if (!file.name.endsWith('.xlsx') && !file.name.endsWith('.xls')) {
          ElMessage.error('请上传Excel文件（.xlsx或.xls格式）')
          return
        }

        try {
          const formData = new FormData()
          formData.append('file', file)

          const response = await request.post('/api/activities/import/', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })

          if (response.data.success_count > 0) {
            ElMessage.success(`成功导入 ${response.data.success_count} 条记录`)
          }
          
          if (response.data.error_count > 0) {
            ElMessageBox.alert(
              response.data.errors.join('\n'),
              '导入出现以下错误',
              {
                type: 'warning'
              }
            )
          }
          
          // 刷新列表
          getActivityList()
        } catch (error) {
          console.error('导入失败:', error)
          ElMessage.error(error.response?.data?.error || '导入失败')
        }
      }
      input.click()
    }

    const handleExport = async () => {
      try {
        // 获取当前的筛选条件
        const params = {
          name: searchForm.value.name,
          applicant_name: searchForm.value.applicant_name,
          status: searchForm.value.status
        }

        // 发送导出请求
        const response = await request.get('/api/activities/export/', {
          params,
          responseType: 'blob'  // 指定响应类型为blob
        })

        // 创建下载链接
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `activities_${new Date().getTime()}.xlsx`)
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        window.URL.revokeObjectURL(url)

        ElMessage.success('导出成功')
      } catch (error) {
        console.error('导出失败:', error)
        ElMessage.error('导出失败')
      }
    }

    // 提交表单
    const handleSubmit = async () => {
      if (!formRef.value) return
      
      try {
        await formRef.value.validate()
        const submitData = { ...formData.value }
        
        if (submitData.event_time) {
          submitData.event_time = new Date(submitData.event_time).toISOString()
        }

        if (dialogTitle.value === '新增活动') {
          const response = await request.post('/api/activities/add/', submitData)
          ElMessage.success('新增成功')
          dialogVisible.value = false
          getActivityList()
        } else {
          const response = await request.put(`/api/activities/${submitData.id}/`, submitData)
          ElMessage.success('编辑成功')
          dialogVisible.value = false
          getActivityList()
        }
      } catch (error) {
        console.error('提交失败:', error)
        if (error.response?.data?.error) {
          ElMessage.error(error.response.data.error)
        } else if (error.response?.data?.non_field_errors) {
          ElMessage.error(error.response.data.non_field_errors[0])
        } else if (typeof error.response?.data === 'string') {
          ElMessage.error(error.response.data)
        } else {
          ElMessage.error('提交失败，请检查输入信息')
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

    // 重新申请
    const handleReapply = async (row) => {
      try {
        await ElMessageBox.confirm('确认重新申请该活动吗？', '提示', {
          type: 'warning',
          confirmButtonText: '确定',
          cancelButtonText: '取消'
        })
        
        await request.post(`/api/activities/${row.id}/reapply/`)
        ElMessage.success('重新申请成功')
        getActivityList()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('重新申请失败:', error)
          ElMessage.error(error.response?.data?.error || '重新申请失败')
        }
      }
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
      selectedRows,
      dialogVisible,
      dialogTitle,
      formRef,
      formData,
      rules,
      handleSearch,
      handleReset,
      handleSelectionChange,
      handleAdd,
      handleEdit,
      handleDelete,
      handleBatchDelete,
      handleImport,
      handleExport,
      handleSubmit,
      handleSizeChange,
      handleCurrentChange,
      handleReapply,
      getStatusType,
      getStatusText,
      formatDateTime
    }
  }
}
</script>

<style scoped>
.activity-publish {
  padding: 20px;
}

.search-section {
  background: #fff;
  padding: 20px;
  border-radius: 4px;
  margin-bottom: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.toolbar {
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}

.dialog-footer {
  text-align: right;
}

.el-tag {
  margin-right: 8px;
}
</style> 