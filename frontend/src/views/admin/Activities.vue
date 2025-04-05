<!-- frontend/src/views/admin/Greetings.vue -->
<template>
  <div class="greetings">
    <!-- 搜索区域 -->
    <div class="search-section">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="短信内容">
          <el-input v-model="searchForm.content" placeholder="请输入短信内容" />
        </el-form-item>
        <el-form-item label="短信类型">
          <el-select v-model="searchForm.type" placeholder="请选择活动类型" clearable style="width: 150px;">
            <el-option label="新闻通知" value="news" />
            <el-option label="活动通知" value="activity" />
            <el-option label="节日祝福" value="greeting" />
          </el-select>
        </el-form-item>
        <el-form-item label="发送状态">
          <el-select v-model="searchForm.status" placeholder="请选择发送状态" clearable style="width: 150px;">
            <el-option label="成功" :value="0" />
            <el-option label="失败" :value="1" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 操作按钮区域 -->
    <div class="operation-section">
      <el-button type="primary" @click="handleAdd">新增</el-button>
      <el-button type="danger" :disabled="!selectedIds.length" @click="handleBatchDelete">
        批量删除
      </el-button>
      <el-upload
        class="upload-demo"
        action="/api/notifications/greetings/import/"
        :headers="headers"
        :on-success="handleImportSuccess"
        :on-error="handleImportError"
        :show-file-list="false"
      >
        <el-button type="primary">导入</el-button>
      </el-upload>
      <el-button type="primary" @click="handleExport">导出</el-button>
    </div>

    <!-- 数据表格 -->
    <el-table
      :data="greetingsList"
      style="width: 100%"
      @selection-change="handleSelectionChange"
      border
    >
      <el-table-column type="selection" width="55" />
      <el-table-column prop="title" label="标题" min-width="150" />
      <el-table-column prop="type_display" label="短信类型" min-width="150" />
      <el-table-column prop="content" label="内容" min-width="200" show-overflow-tooltip />
      <el-table-column prop="status_display" label="发送状态" width="100" />
      <el-table-column label="接收者" min-width="200" show-overflow-tooltip>
        <template #default="scope">
          {{ scope.row.receivers_info.map(user => user.username).join(', ') }}
        </template>
      </el-table-column>
      <el-table-column prop="send_time" label="发送时间" width="180">
        <template #default="scope">
          {{ formatDateTime(scope.row.send_time) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="150" fixed="right">
        <template #default="scope">
          <el-button type="primary" size="small" @click="handleEdit(scope.row)">
            编辑
          </el-button>
          <el-button type="danger" size="small" @click="handleDelete(scope.row)">
            删除
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

    <!-- 新增/编辑对话框 -->
    <el-dialog
      :title="dialogType === 'add' ? '新增活动通知' : '编辑活动通知'"
      v-model="dialogVisible"
      width="500px"
    >
      <el-form :model="greetingForm" :rules="rules" ref="greetingFormRef" label-width="100px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="greetingForm.title" />
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <el-input v-model="greetingForm.content" type="textarea" :rows="4" />
        </el-form-item>
        <el-form-item label="短信类型" prop="type">
          <el-select v-model="greetingForm.type" placeholder="请选择短信类型">
            <el-option label="新闻通知" value="news" />
            <el-option label="活动通知" value="activity" />
            <el-option label="节日祝福" value="greeting" />
          </el-select>
        </el-form-item>
        <el-form-item label="接收者" prop="receivers">
          <div class="select-all-wrapper">
            <el-checkbox v-model="selectAll" @change="handleSelectAllChange">全选</el-checkbox>
          </div>
          <el-select
            v-model="greetingForm.receivers"
            multiple
            filterable
            placeholder="请选择接收者"
            style="width: 100%"
          >
            <el-option
              v-for="alumni in alumniList"
              :key="alumni.id"
              :label="`${alumni.name}(${alumni.student_id})`"
              :value="alumni.id"
            />
          </el-select>
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
import { ref, onMounted, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '@/utils/request'
import { useStore } from 'vuex'

export default {
  name: 'Greetings',
  setup() {
    const store = useStore()
    const headers = {
      Authorization: `Bearer ${store.state.token}`
    }

    // 搜索表单
    const searchForm = ref({
      content: '',
      type: '',
      status: ''
    })

    // 列表数据
    const greetingsList = ref([])
    const currentPage = ref(1)
    const pageSize = ref(10)
    const total = ref(0)
    const selectedIds = ref([])

    // 对话框相关
    const dialogVisible = ref(false)
    const dialogType = ref('add')
    const greetingForm = ref({
      title: '',
      content: '',
      type: '',
      receivers: []
    })
    const greetingFormRef = ref(null)
    const rules = {
      title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
      content: [{ required: true, message: '请输入内容', trigger: 'blur' }],
      type: [{ required: true, message: '请选择短信类型', trigger: 'blur' }],
      receivers: [{ required: true, message: '请选择接收者', trigger: 'change' }]
    }

    // 用户选择相关
    const userOptions = ref([])
    const loading = ref(false)

    // 校友列表相关
    const alumniList = ref([])
    const selectAll = ref(false)

    // 获取列表数据
    const getGreetingsList = async () => {
      try {
        const params = {
          page: currentPage.value,
          page_size: pageSize.value,
          content: searchForm.value.content,
          type: searchForm.value.type,
          status: searchForm.value.status
        }
        if (searchForm.value.status !== '') {  // 只有当状态不为空时才添加到参数中
          params.status = searchForm.value.status
        }
        const response = await request.get('/api/notifications/greetings/', { params })
        greetingsList.value = response.data.results
        total.value = response.data.count
      } catch (error) {
        console.error('获取节日祝福列表失败:', error)
        ElMessage.error('获取列表失败')
      }
    }

    // 远程搜索用户
    const remoteSearchUsers = async (query) => {
      if (query) {
        loading.value = true
        try {
          const response = await request.get('/api/users/search/', {
            params: { query }
          })
          userOptions.value = response.data
        } catch (error) {
          console.error('搜索用户失败:', error)
        }
        loading.value = false
      } else {
        userOptions.value = []
      }
    }

    // 格式化日期时间
    const formatDateTime = (datetime) => {
      if (!datetime) return ''
      return new Date(datetime).toLocaleString()
    }

    // 搜索和重置
    const handleSearch = () => {
      currentPage.value = 1
      getGreetingsList()
    }

    const handleReset = () => {
      searchForm.value = {
        content: '',
        type: '',
        status: ''
      }
      handleSearch()
    }

    // 表格选择
    const handleSelectionChange = (val) => {
      selectedIds.value = val.map(item => item.id)
    }

    // 获取已毕业校友列表
    const getAlumniList = async () => {
      try {
        const response = await request.get('/api/notifications/graduated-alumni/')
        alumniList.value = response.data
      } catch (error) {
        console.error('获取校友列表失败:', error)
        ElMessage.error('获取校友列表失败')
      }
    }

    // 处理全选/取消全选
    const handleSelectAllChange = (val) => {
      if (val) {
        greetingForm.value.receivers = alumniList.value.map(alumni => alumni.id)
      } else {
        greetingForm.value.receivers = []
      }
    }

    // 监听接收者选择变化，更新全选状态
    watch(() => greetingForm.value.receivers, (newVal) => {
      selectAll.value = newVal.length === alumniList.value.length
    })

    // 新增/编辑
    const handleAdd = () => {
      dialogType.value = 'add'
      greetingForm.value = {
        title: '',
        content: '',
        type: 'greeting',
        receivers: []
      }
      selectAll.value = false
      getAlumniList()  // 获取校友列表
      dialogVisible.value = true
    }

    const handleEdit = (row) => {
      dialogType.value = 'edit'
      greetingForm.value = {
        id: row.id,
        title: row.title,
        content: row.content,
        type: row.type,
        receivers: row.receivers || []
      }
      getAlumniList()  // 获取校友列表
      dialogVisible.value = true
    }

    const handleSubmit = async () => {
      if (!greetingFormRef.value) return

      await greetingFormRef.value.validate(async (valid) => {
        if (valid) {
          try {
            if (dialogType.value === 'add') {
              await request.post('/api/notifications/greetings/', greetingForm.value)
              ElMessage.success('添加成功')
            } else {
              await request.put(`/api/notifications/greetings/${greetingForm.value.id}/`, greetingForm.value)
              ElMessage.success('修改成功')
            }
            dialogVisible.value = false
            getGreetingsList()
          } catch (error) {
            console.error('操作失败:', error)
            ElMessage.error('操作失败')
          }
        }
      })
    }

    // 删除
    const handleDelete = async (row) => {
      try {
        await ElMessageBox.confirm('确认删除该条节日祝福吗？', '提示', {
          type: 'warning'
        })
        await request.delete(`/api/notifications/greetings/${row.id}/`)
        ElMessage.success('删除成功')
        getGreetingsList()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除失败:', error)
          ElMessage.error('删除失败')
        }
      }
    }

    // 批量删除
    const handleBatchDelete = async () => {
      if (!selectedIds.value.length) {
        ElMessage.warning('请选择要删除的项目')
        return
      }

      try {
        await ElMessageBox.confirm('确认删除选中的节日祝福吗？', '提示', {
          type: 'warning'
        })
        await request.post('/api/notifications/greetings/batch-delete/', {
          ids: selectedIds.value
        })
        ElMessage.success('批量删除成功')
        getGreetingsList()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('批量删除失败:', error)
          ElMessage.error('批量删除失败')
        }
      }
    }

    // 导入导出
    const handleImportSuccess = (response) => {
      ElMessage.success(`导入成功：${response.success_count} 条记录`)
      if (response.error_count > 0) {
        ElMessage.warning(`${response.error_count} 条记录导入失败`)
        console.error('导入错误:', response.errors)
      }
      getGreetingsList()
    }

    const handleImportError = () => {
      ElMessage.error('导入失败')
    }

    const handleExport = async () => {
      try {
        const params = {
          content: searchForm.value.content,
          status: searchForm.value.status
        }
        const response = await request.get('/api/notifications/greetings/export/', {
          params,
          responseType: 'blob'
        })

        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `greetings_${new Date().getTime()}.xlsx`)
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        window.URL.revokeObjectURL(url)
      } catch (error) {
        console.error('导出失败:', error)
        ElMessage.error('导出失败')
      }
    }

    // 分页
    const handleSizeChange = (val) => {
      pageSize.value = val
      getGreetingsList()
    }

    const handleCurrentChange = (val) => {
      currentPage.value = val
      getGreetingsList()
    }

    onMounted(() => {
      getGreetingsList()
    })

    return {
      headers,
      searchForm,
      greetingsList,
      currentPage,
      pageSize,
      total,
      selectedIds,
      dialogVisible,
      dialogType,
      greetingForm,
      greetingFormRef,
      rules,
      userOptions,
      loading,
      alumniList,
      selectAll,
      handleSearch,
      handleReset,
      handleSelectionChange,
      handleAdd,
      handleEdit,
      handleDelete,
      handleBatchDelete,
      handleImportSuccess,
      handleImportError,
      handleExport,
      handleSizeChange,
      handleCurrentChange,
      formatDateTime,
      remoteSearchUsers,
      handleSubmit,
      getAlumniList,
      handleSelectAllChange
    }
  }
}
</script>

<style scoped>
.greetings {
  padding: 20px;
}

.search-section {
  background: #fff;
  padding: 20px;
  border-radius: 4px;
  margin-bottom: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.operation-section {
  margin-bottom: 20px;
}

.operation-section .el-button {
  margin-right: 10px;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}

.upload-demo {
  display: inline-block;
  margin-right: 10px;
}

.select-all-wrapper {
  margin-bottom: 8px;
}
</style>