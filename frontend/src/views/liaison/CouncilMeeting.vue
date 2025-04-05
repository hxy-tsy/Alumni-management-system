<template>
  <div class="council-meeting">
    <!-- 搜索区域 -->
    <div class="search-section">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="理事会名称">
          <el-input v-model="searchForm.name" placeholder="请输入理事会名称" />
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
      <el-button type="danger" :disabled="!selectedRows.length" @click="handleBatchDelete">批量删除</el-button>
<!--      <el-upload-->
<!--        class="upload-button"-->
<!--        action="/api/council/meetings/import/"-->
<!--        :show-file-list="false"-->
<!--        :before-upload="beforeUpload"-->
<!--        :on-success="handleImportSuccess"-->
<!--        :on-error="handleImportError"-->
<!--      >-->
      <el-button type="primary" @click="handleImport">导入</el-button>
<!--      </el-upload>-->
      <el-button type="primary" @click="handleExport">导出</el-button>
    </div>

    <!-- 理事会列表 -->
    <el-table
      :data="meetingList"
      style="width: 100%"
      border
      v-loading="loading"
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" width="55" />
      <el-table-column prop="name" label="理事会名称" min-width="150" />
      <el-table-column prop="content" label="内容" min-width="200" show-overflow-tooltip />
      <el-table-column prop="location" label="地点" min-width="120" />
      <el-table-column label="邀请人员" min-width="150" show-overflow-tooltip>
        <template #default="scope">
          {{ scope.row.invitees_info ? scope.row.invitees_info.map(user => user.name || user.username).join(', ') : '' }}
        </template>
      </el-table-column>
      <el-table-column prop="meeting_time" label="召开时间" min-width="180">
        <template #default="scope">
          {{ formatDateTime(scope.row.meeting_time) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" fixed="right" width="200">
        <template #default="scope">
          <el-button
            type="primary"
            size="small"
            @click="handleSendInvitation(scope.row)"
            :disabled="scope.row.invitation_sent"
          >
            {{ scope.row.invitation_sent ? '已发送' : '发送邀请' }}
          </el-button>
          <el-button
            type="primary"
            size="small"
            @click="handleEdit(scope.row)"
          >
            编辑
          </el-button>
          <el-button
            type="danger"
            size="small"
            @click="handleWithdraw(scope.row)"
            :disabled="!scope.row.invitation_sent"
          >
            撤回
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
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="理事会名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入理事会名称" />
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <el-input
            v-model="form.content"
            type="textarea"
            :rows="4"
            placeholder="请输入理事会内容"
          />
        </el-form-item>
        <el-form-item label="地点" prop="location">
          <el-input v-model="form.location" placeholder="请输入召开地点" />
        </el-form-item>
        <el-form-item label="邀请人员" prop="invitees">
          <div class="select-all-wrapper">
            <el-checkbox v-model="selectAll" @change="handleSelectAllChange">全选</el-checkbox>
          </div>
          <el-select
            v-model="form.invitees"
            multiple
            filterable
            placeholder="请选择邀请人员"
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
        <el-form-item label="召开时间" prop="meeting_time">
          <el-date-picker
            v-model="form.meeting_time"
            type="datetime"
            placeholder="请选择召开时间"
            style="width: 100%"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '@/utils/request'

export default {
  name: 'CouncilMeeting',
  setup() {
    // 搜索表单
    const searchForm = ref({
      name: ''
    })

    // 列表数据
    const meetingList = ref([])
    const loading = ref(false)
    const currentPage = ref(1)
    const pageSize = ref(10)
    const total = ref(0)
    const selectedRows = ref([])

    // 对话框相关
    const dialogVisible = ref(false)
    const dialogTitle = ref('新增理事会')
    const formRef = ref(null)
    const form = ref({
      name: '',
      content: '',
      location: '',
      invitees: [],
      meeting_time: ''
    })

    // 表单验证规则
    const rules = {
      name: [{ required: true, message: '请输入理事会名称', trigger: 'blur' }],
      content: [{ required: true, message: '请输入理事会内容', trigger: 'blur' }],
      location: [{ required: true, message: '请输入召开地点', trigger: 'blur' }],
      invitees: [{ required: true, message: '请选择邀请人员', trigger: 'change' }],
      meeting_time: [{ required: true, message: '请选择召开时间', trigger: 'change' }]
    }

    // 已毕业校友列表
    const alumniList = ref([])
    const alumniLoading = ref(false)
    const selectAll = ref(false)

    // 获取理事会列表
    const getMeetingList = async () => {
      loading.value = true
      try {
        const params = {
          page: currentPage.value,
          page_size: pageSize.value,
          name: searchForm.value.name
        }
        const response = await request.get('/api/council/meetings/', { params })
        meetingList.value = response.data.results
        total.value = response.data.count
      } catch (error) {
        console.error('获取理事会列表失败:', error)
        ElMessage.error('获取理事会列表失败')
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

    // 搜索和重置
    const handleSearch = () => {
      currentPage.value = 1
      getMeetingList()
    }

    const handleReset = () => {
      searchForm.value.name = ''
      handleSearch()
    }

    // 获取已毕业校友列表
    const fetchGraduatedAlumni = async () => {
      try {
        alumniLoading.value = true
        const response = await request.get('/api/council/graduated-alumni/')
        alumniList.value = response.data
      } catch (error) {
        console.error('获取校友列表失败：' + (error.response?.data?.error || error.message))
        ElMessage.error('获取校友列表失败')
      } finally {
        alumniLoading.value = false
      }
    }

    // 处理全选/取消全选
    const handleSelectAllChange = (val) => {
      if (val) {
        form.value.invitees = alumniList.value.map(alumni => alumni.id)
      } else {
        form.value.invitees = []
      }
    }

    // 监听接收者选择变化，更新全选状态
    watch(() => form.value.invitees, (newVal) => {
      selectAll.value = newVal.length === alumniList.value.length && alumniList.value.length > 0
    })

    // 新增/编辑理事会
    const handleAdd = () => {
      dialogTitle.value = '新增理事会'
      form.value = {
        name: '',
        content: '',
        location: '',
        invitees: [],
        meeting_time: ''
      }
      selectAll.value = false
      dialogVisible.value = true
      fetchGraduatedAlumni()
    }

    const handleEdit = (row) => {
      dialogTitle.value = '编辑理事会'
      form.value = { ...row }
      dialogVisible.value = true
      fetchGraduatedAlumni().then(() => {
        form.value.invitees = row.invitees || []
        selectAll.value = form.value.invitees.length === alumniList.value.length && alumniList.value.length > 0
      })
    }

    const submitForm = async () => {
      if (!formRef.value) return
      
      await formRef.value.validate(async (valid) => {
        if (valid) {
          try {
            if (dialogTitle.value === '新增理事会') {
              await request.post('/api/council/meetings/', form.value)
              ElMessage.success('新增成功')
            } else {
              await request.put(`/api/council/meetings/${form.value.id}/`, form.value)
              ElMessage.success('编辑成功')
            }
            dialogVisible.value = false
            getMeetingList()
          } catch (error) {
            console.error('保存失败:', error)
            ElMessage.error('保存失败')
          }
        }
      })
    }

    // 批量删除
    const handleSelectionChange = (rows) => {
      selectedRows.value = rows
    }

    const handleBatchDelete = () => {
      if (!selectedRows.value.length) return
      
      ElMessageBox.confirm('确定要删除选中的理事会吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          const ids = selectedRows.value.map(row => row.id)
          await request.post('/api/council/meetings/batch-delete/', { ids })
          ElMessage.success('删除成功')
          getMeetingList()
        } catch (error) {
          console.error('删除失败:', error)
          ElMessage.error('删除失败')
        }
      })
    }

    // 发送邀请
    const handleSendInvitation = async (row) => {
      try {
        await request.post(`/api/council/meetings/${row.id}/send-invitation/`)
        row.invitation_sent = true
        ElMessage.success('邀请发送成功')
      } catch (error) {
        console.error('发送邀请失败:', error)
        ElMessage.error('发送邀请失败')
      }
    }

    // 撤回邀请
    const handleWithdraw = async (row) => {
      try {
        await request.post(`/api/council/meetings/${row.id}/withdraw-invitation/`)
        row.invitation_sent = false
        ElMessage.success('撤回成功')
      } catch (error) {
        console.error('撤回失败:', error)
        ElMessage.error('撤回失败')
      }
    }

    // 导入导出
    const beforeUpload = (file) => {
      const isExcel = file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' ||
                     file.type === 'application/vnd.ms-excel'
      if (!isExcel) {
        ElMessage.error('只能上传 Excel 文件!')
        return false
      }
      return true
    }

    const handleImportSuccess = (response) => {
      ElMessage.success(`成功导入 ${response.success_count} 条数据`)
      getMeetingList()
    }

    const handleImportError = () => {
      ElMessage.error('导入失败')
    }

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

          const response = await request.post('/api/council/meetings/import/', formData, {
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
          getMeetingList()
        } catch (error) {
          console.error('导入失败:', error)
          ElMessage.error(error.response?.data?.error || '导入失败')
        }
      }
      input.click()
    }
    const handleExport = async () => {
      try {
        const response = await request.get('/api/council/meetings/export/', {
          params: { name: searchForm.value.name },
          responseType: 'blob'
        })
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `理事会列表_${new Date().getTime()}.xlsx`)
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
      } catch (error) {
        console.error('导出失败:', error)
        ElMessage.error('导出失败')
      }
    }

    // 分页
    const handleSizeChange = (val) => {
      pageSize.value = val
      getMeetingList()
    }

    const handleCurrentChange = (val) => {
      currentPage.value = val
      getMeetingList()
    }

    onMounted(() => {
      getMeetingList()
    })

    return {
      searchForm,
      meetingList,
      loading,
      currentPage,
      pageSize,
      total,
      selectedRows,
      dialogVisible,
      dialogTitle,
      formRef,
      form,
      rules,
      alumniList,
      alumniLoading,
      selectAll,
      handleSearch,
      handleReset,
      handleAdd,
      handleEdit,
      submitForm,
      handleSelectionChange,
      handleBatchDelete,
      handleSendInvitation,
      handleWithdraw,
      beforeUpload,
      handleImportSuccess,
      handleImportError,
      handleImport,
      handleExport,
      handleSizeChange,
      handleCurrentChange,
      formatDateTime,
      fetchGraduatedAlumni,
      handleSelectAllChange
    }
  }
}
</script>

<style scoped>
.council-meeting {
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

.upload-button {
  display: inline-block;
  margin-right: 10px;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

.select-all-wrapper {
  margin-bottom: 8px;
}
</style> 