<template>
  <div class="alumni-applications">
    <!-- 搜索栏 -->
    <div class="search-bar">
      <el-form :inline="true" :model="searchForm">
        <el-form-item label="姓名">
          <el-input v-model="searchForm.name" placeholder="请输入姓名"></el-input>
        </el-form-item>
        <el-form-item label="学号">
          <el-input v-model="searchForm.student_id" placeholder="请输入学号"></el-input>
        </el-form-item>
        <el-form-item label="学院">
          <el-input v-model="searchForm.department" placeholder="请输入学院"></el-input>
        </el-form-item>
        <el-form-item label="班级">
          <el-input v-model="searchForm.class_name" placeholder="请输入班级"></el-input>
        </el-form-item>
        <el-form-item label="审核状态">
          <el-select v-model="searchForm.application_status" placeholder="请选择状态" clearable style="width: 120px;">
            <el-option label="未申请" value="0"></el-option>
            <el-option label="审核中" value="1"></el-option>
            <el-option label="审批通过" value="2"></el-option>
            <el-option label="审批拒绝" value="3"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 数据表格 -->
    <el-table :data="applicationList" border style="width: 100%">
      <el-table-column prop="student_id" label="学号" width="120"></el-table-column>
      <el-table-column prop="user.username" label="姓名" width="120"></el-table-column>
      <el-table-column prop="user.phone" label="联系电话" width="120"></el-table-column>
      <el-table-column prop="user.department" label="学院"></el-table-column>
      <el-table-column prop="class_name" label="班级" width="120"></el-table-column>
      <el-table-column prop="graduation_date" label="毕业日期" width="120"></el-table-column>
      <el-table-column prop="current_company" label="毕业去向"></el-table-column>
<!--      <el-table-column prop="apply_date" label="申请时间" width="180">-->
<!--        <template #default="scope">-->
<!--          {{ formatDate(scope.row.apply_date) }}-->
<!--        </template>-->
<!--      </el-table-column>-->
      <el-table-column prop="status" label="审核状态" width="100">
        <template #default="scope">
          <el-tag :type="getStatusType(scope.row)">
            {{ getStatusText(scope.row) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="scope">
          <el-button 
            v-if="scope.row.status === 'pending'"
            type="success" 
            size="small" 
            @click="handleApprove(scope.row)"
          >通过</el-button>
          <el-button 
            v-if="scope.row.status === 'pending'"
            type="danger" 
            size="small" 
            @click="handleReject(scope.row)"
          >拒绝</el-button>
          <el-button 
            type="primary" 
            size="small" 
            @click="handleDetail(scope.row)"
            :disabled="scope.row.application_status === 0 || scope.row.application_status === 2"
          >详情</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <div class="pagination">
      <el-pagination
        :current-page="currentPage"
        :page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      ></el-pagination>
    </div>

    <!-- 详情对话框 -->
    <el-dialog 
      title="申请详情" 
      v-model="detailVisible" 
      width="800px"
    >
      <el-form :model="currentDetail" label-width="120px">
        <!-- 基本信息 -->
        <el-divider>基本信息</el-divider>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="姓名">
              <el-input v-model="currentDetail.user.username" disabled></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="学号">
              <el-input v-model="currentDetail.student_id" disabled></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="性别">
              <el-input :value="currentDetail.gender === 'male' ? '男' : '女'" disabled></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="民族">
              <el-input v-model="currentDetail.ethnicity" disabled></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="出生日期">
              <el-input v-model="currentDetail.birth_date" disabled></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话">
              <el-input v-model="currentDetail.user.phone" disabled></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 学习信息 -->
        <el-divider>学习信息</el-divider>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="学院">
              <el-input v-model="currentDetail.user.department" disabled></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="班级">
              <el-input v-model="currentDetail.class_name" disabled></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
<!--          <el-col :span="12">-->
<!--            <el-form-item label="学历">-->
<!--              <el-input :value="getEducationText(currentDetail.education_level)" disabled></el-input>-->
<!--            </el-form-item>-->
<!--          </el-col>-->
          <el-col :span="12">
            <el-form-item label="专业">
              <el-input v-model="currentDetail.major" disabled></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 就业信息 -->
        <el-divider>就业信息</el-divider>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="毕业日期">
              <el-input v-model="currentDetail.graduation_date" disabled></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="毕业去向">
              <el-input v-model="currentDetail.current_company" disabled></el-input>
            </el-form-item>
          </el-col>
        </el-row>
<!--        <el-row :gutter="20">-->
<!--          <el-col :span="12">-->
<!--            <el-form-item label="职位">-->
<!--              <el-input v-model="currentDetail.position" disabled></el-input>-->
<!--            </el-form-item>-->
<!--          </el-col>-->
<!--          <el-col :span="12">-->
<!--            <el-form-item label="工作城市">-->
<!--              <el-input v-model="currentDetail.work_city" disabled></el-input>-->
<!--            </el-form-item>-->
<!--          </el-col>-->
<!--        </el-row>-->
        <el-row>
          <el-col :span="24">
            <el-form-item label="通讯地址">
              <el-input v-model="currentDetail.address" disabled></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 审批结果 -->
        <el-divider>审批结果</el-divider>
        <el-form-item label="审批结果">
          <el-radio-group v-model="approvalResult">
            <el-radio :label="true">通过</el-radio>
            <el-radio :label="false">不通过</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="detailVisible = false">取消</el-button>
          <el-button type="primary" @click="submitApproval">提交审批</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '@/utils/request'

export default {
  name: 'AlumniApplications',
  setup() {
    const applicationList = ref([])
    const currentPage = ref(1)
    const pageSize = ref(10)
    const total = ref(0)
    const detailVisible = ref(false)
    const currentDetail = ref({})
    const approvalResult = ref(true)  // 默认选中"通过"

    const searchForm = reactive({
      name: '',
      student_id: '',
      department: '',
      class_name: '',
      application_status: '',
    })

    // 获取申请列表
    const getApplicationList = async () => {
      try {
        const response = await request.get('/api/alumni/list/', {
          params: {
            // application_status: 1,  // 只获取审核中的申请
            ...searchForm
          }
        })
        applicationList.value = response.data
        total.value = response.data.count
      } catch (error) {
        console.error('获取申请列表失败:', error)
        ElMessage.error('获取申请列表失败')
      }
    }

    // 格式化日期
    const formatDate = (date) => {
      if (!date) return ''
      return new Date(date).toLocaleString()
    }

    // 获取状态类型
    const getStatusType = (row) => {
      if (row.application_status === 1) return 'warning'
      if (row.application_status === 2) return 'success'
      if (row.application_status === 3) return 'danger'
      return 'info'
    }

    // 获取状态文本
    const getStatusText = (row) => {
      const statusMap = {
        0: '未申请',
        1: '审核中',
        2: '审核通过',
        3: '审核不通过'
      }
      return statusMap[row.application_status] || '未知状态'
    }

    // 获取学历文本
    const getEducationText = (level) => {
      const educationMap = {
        'bachelor': '学士',
        'master': '硕士',
        'doctor': '博士'
      }
      return educationMap[level] || level
    }

    // 审批通过
    const handleApprove = async (row) => {
      try {
        await ElMessageBox.confirm('确认通过该申请吗？', '提示', {
          type: 'warning'
        })
        await request.post(`/applications/${row.id}/approve/`)
        ElMessage.success('审批通过成功')
        getApplicationList()
      } catch (error) {
        console.error('审批失败:', error)
        ElMessage.error('审批失败')
      }
    }

    // 审批拒绝
    const handleReject = async (row) => {
      try {
        await ElMessageBox.confirm('确认拒绝该申请吗？', '提示', {
          type: 'warning'
        })
        await request.post(`/applications/${row.id}/reject/`)
        ElMessage.success('已拒绝申请')
        getApplicationList()
      } catch (error) {
        console.error('操作失败:', error)
        ElMessage.error('操作失败')
      }
    }

    // 查看详情
    const handleDetail = (row) => {
      currentDetail.value = { ...row }  // 创建副本以避免直接修改
      approvalResult.value = true  // 重置审批结果为通过
      detailVisible.value = true
    }

    // 搜索
    const handleSearch = () => {
      currentPage.value = 1
      getApplicationList()
    }

    // 重置搜索
    const resetSearch = () => {
      Object.keys(searchForm).forEach(key => {
        searchForm[key] = ''
      })
      handleSearch()
    }

    // 分页大小变化
    const handleSizeChange = (val) => {
      pageSize.value = val
      getApplicationList()
    }

    // 页码变化
    const handleCurrentChange = (val) => {
      currentPage.value = val
      getApplicationList()
    }

    // 提交审批
    const submitApproval = async () => {
      try {
        const url = `/api/alumni/${currentDetail.value.id}/${approvalResult.value ? 'approve' : 'reject'}/`
        await request.post(url)
        ElMessage.success(`审批${approvalResult.value ? '通过' : '拒绝'}成功`)
        detailVisible.value = false
        getApplicationList()  // 刷新列表
      } catch (error) {
        console.error('审批提交失败:', error)
        ElMessage.error('审批提交失败')
      }
    }

    onMounted(() => {
      getApplicationList()
    })

    return {
      applicationList,
      currentPage,
      pageSize,
      total,
      searchForm,
      detailVisible,
      currentDetail,
      formatDate,
      getStatusType,
      getStatusText,
      handleApprove,
      handleReject,
      handleDetail,
      handleSearch,
      resetSearch,
      handleSizeChange,
      handleCurrentChange,
      approvalResult,
      getEducationText,
      submitApproval
    }
  }
}
</script>

<style scoped>
.alumni-applications {
  padding: 20px;
}

.search-bar {
  margin-bottom: 20px;
  padding: 20px;
  background-color: #fff;
  border-radius: 4px;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}

.el-divider {
  margin: 20px 0;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style> 