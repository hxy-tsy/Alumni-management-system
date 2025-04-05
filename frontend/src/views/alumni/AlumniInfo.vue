<template>
  <div class="alumni-info">
    <!-- 搜索栏 -->
    <div class="search-bar">
      <el-form :inline="true" :model="searchForm">
        <el-form-item label="学号">
          <el-input v-model="searchForm.student_id" placeholder="请输入学号"></el-input>
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="searchForm.name" placeholder="请输入姓名"></el-input>
        </el-form-item>
<!--        <el-form-item label="学院">-->
<!--          <el-input v-model="searchForm.department" placeholder="请输入学院"></el-input>-->
<!--        </el-form-item>-->
        <el-form-item label="MBTI">
          <el-input placeholder="请输入MBTI"></el-input>
        </el-form-item>
        <el-form-item label="班级">
          <el-input v-model="searchForm.class_name" placeholder="请输入班级"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 工具栏 -->
    <div class="toolbar" v-if="isAdmin">
      <el-button type="primary" @click="handleAdd">新增</el-button>
      <el-button type="success" @click="handleImport">导入</el-button>
      <el-button type="warning" @click="handleExport">导出</el-button>
      <el-button type="danger" @click="handleBatchDelete">批量删除</el-button>
    </div>

    <!-- 数据表格 -->
    <el-table 
      :data="alumniList" 
      border 
      style="width: 100%"
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" width="55" v-if="isAdmin"></el-table-column>
      <el-table-column prop="student_id" label="学号" width="120"></el-table-column>
      <el-table-column prop="user.username" label="姓名" width="100">
        <template #default="scope">
          <span>{{ scope.row.user.username }}{{ isCurrentUser(scope.row) ? '(我)' : '' }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="user.phone" label="电话" width="120"></el-table-column>
      <el-table-column prop="birth_date" label="出生日期" width="120"></el-table-column>
      <el-table-column prop="user.department" label="学院"></el-table-column>
      <el-table-column prop="class_name" label="班级" width="120"></el-table-column>
      <el-table-column prop="graduation_date" label="毕业日期" width="120"></el-table-column>
      <el-table-column prop="current_company" label="毕业去向"></el-table-column>
      <el-table-column prop="internship" label="实习经历"></el-table-column>
      <el-table-column prop="advantage" label="个人优势"></el-table-column>
      <el-table-column prop="mbti" label="MBTI"></el-table-column>
      <el-table-column prop="gender" label="性别" width="80">
        <template #default="scope">
          <span>{{ scope.row.gender === 'male' ? '男' : '女' }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="150" fixed="right" v-if="showOperationColumn">
        <template #default="scope">
          <template v-if="isAdmin">
            <el-button type="primary" size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button type="danger" size="small" @click="handleDelete(scope.row)">删除</el-button>
          </template>
          <template v-if="isCurrentUser(scope.row) && !isGraduatedAlumni">
            <el-button 
              type="success" 
              size="small" 
              @click="handleGraduationApplication(scope.row)"
              :disabled="scope.row.application_status === 1"
            >
              {{ getGraduationButtonText(scope.row) }}
            </el-button>
          </template>
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

    <!-- 新增/编辑对话框 -->
    <el-dialog 
      :title="dialogTitle" 
      v-model="dialogVisible" 
      width="1000px"
      :close-on-click-modal="false"
    >
      <el-form 
        :model="formData" 
        :rules="isGraduationApplication ? graduationRules : rules" 
        ref="formRef" 
        label-width="100px"
        class="alumni-form"
      >
        <div class="form-wrapper">
          <div class="form-content">
            <!-- 基本信息 -->
            <div class="section-title">基本信息</div>
            <el-row :gutter="20">
              <el-col :span="8">
                <el-form-item label="姓名" prop="user.username">
                  <el-input 
                    v-model="formData.user.username" 
                    placeholder="请输入姓名" 
                    :disabled="dialogTitle === '编辑校友'"
                  ></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="学号" prop="student_id">
                  <el-input 
                    v-model="formData.student_id" 
                    placeholder="请输入学号" 
                    :disabled="dialogTitle === '编辑校友'"
                  ></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="民族" prop="ethnicity">
                  <el-select 
                    v-model="formData.ethnicity" 
                    placeholder="请选择民族" 
                    style="width: 100%" 
                    :disabled="dialogTitle === '编辑校友'"
                  >
                    <el-option
                      v-for="item in ethnicityOptions"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value"
                    ></el-option>
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>

            <el-row :gutter="20">
              <el-col :span="8">
                <el-form-item label="性别" prop="gender">
                  <el-select 
                    v-model="formData.gender" 
                    placeholder="请选择性别" 
                    style="width: 100%" 
                    :disabled="dialogTitle === '编辑校友'"
                  >
                    <el-option label="男" value="male"></el-option>
                    <el-option label="女" value="female"></el-option>
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="出生年月" prop="birth_date">
                  <el-date-picker
                    v-model="formData.birth_date"
                    type="date"
                    placeholder="选择日期"
                    style="width: 100%"
                  ></el-date-picker>
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="联系方式" prop="user.phone">
                  <el-input v-model="formData.user.phone" placeholder="请输入联系方式"></el-input>
                </el-form-item>
              </el-col>
            </el-row>

            <el-row :gutter="20">
              <el-col :span="8">
                <el-form-item label="通讯地址" prop="address">
                  <el-cascader
                    v-model="formData.address"
                    :options="addressOptions"
                    placeholder="请选择省/市/区"
                    style="width: 100%"
                  ></el-cascader>
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-input v-model="formData.internship" label="实习经历" placeholder="请输入实习经历"></el-input>
              </el-col>
              <el-col :span="8">
                <el-input v-model="formData.advantage" label="个人优势" placeholder="请输入个人优势"></el-input>
              </el-col>
            </el-row>

            <!-- 教育背景信息 -->
            <div class="section-title">教育背景信息</div>
            <el-row :gutter="20">
              <el-col :span="8">
                <el-form-item label="学院" prop="user.department">
                  <el-select 
                    v-model="formData.user.department" 
                    placeholder="请选择学院" 
                    style="width: 100%"
                    @change="handleDepartmentChange"
                  >
                    <el-option
                      v-for="item in departmentOptions"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value"
                    ></el-option>
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="班级" prop="class_name">
                  <el-select 
                    v-model="formData.class_name" 
                    placeholder="请选择班级" 
                    style="width: 100%"
                  >
                    <el-option
                      v-for="item in classOptions"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value"
                    ></el-option>
                  </el-select>
                </el-form-item>
              </el-col>

              <el-col :span="8">
                <el-form-item label="毕业去向" prop="current_company">
                  <el-select v-model="formData.current_company" placeholder="请选择去向" style="width: 100%">
                    <el-option label="升学" value="升学"></el-option>
                    <el-option label="公务员" value="公务员"></el-option>
                    <el-option label="互联网企业" value="互联网企业"></el-option>
                    <el-option label="金融企业" value="金融企业"></el-option>
                    <el-option label="央国企" value="央国企"></el-option>
                    <el-option label="银行" value="银行"></el-option>
                    <!-- 其他去向选项... -->
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>

            <el-row :gutter="20">
              <el-col :span="8">
                <el-form-item label="毕业日期" prop="graduation_date">
                  <el-date-picker
                    v-model="formData.graduation_date"
                    type="date"
                    placeholder="选择日期"
                    style="width: 100%"
                  ></el-date-picker>
                </el-form-item>
              </el-col>
            </el-row>
          </div>
          
          <div class="avatar-section">
            <div class="avatar-upload">
              <el-upload
                class="avatar-uploader"
                action="/api/alumni/upload/"
                :show-file-list="false"
                :headers="authHeaders"
                :on-success="handleAvatarSuccess"
                :before-upload="beforeAvatarUpload"
              >
                <img v-if="formData.avatar" :src="getImageUrl(formData.avatar)" class="avatar">
                <div v-else class="upload-placeholder">
                  <el-icon><Plus /></el-icon>
                  <div class="upload-text">上传头像</div>
                  <div class="upload-hint">只支持.jpg格式</div>
                </div>
              </el-upload>
            </div>
          </div>
        </div>
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
import { ref, reactive, onMounted, nextTick, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '@/utils/request'
import { useStore } from 'vuex'

export default {
  name: 'AlumniInfo',
  setup() {
    const store = useStore()
    const authHeaders = computed(() => ({
      'Authorization': `Bearer ${store.state.token}`
    }))

    // 列表数据
    const alumniList = ref([])
    const total = ref(0)
    const currentPage = ref(1)
    const pageSize = ref(10)
    const selectedRows = ref([])

    // 搜索表单
    const searchForm = reactive({
      student_id: '',
      name: '',
      department: '',
      class_name: ''
    })

    // 新增/编辑表单
    const dialogVisible = ref(false)
    const dialogTitle = ref('新增校友')
    const formRef = ref(null)
    const formData = ref({
      user: {
        username: '',
        phone: '',
        department: '',
      },
      student_id: '',
      gender: '',
      ethnicity: '',
      birth_date: '',
      address: [],
      class_name: '',
      current_company: '',
      graduation_date: '',
      avatar: '',
      internship:'',
      advantage:'',
    })

    // 表单验证规则
    const rules = {
      'user.username': [{ required: true, message: '请输入姓名', trigger: 'blur' }],
      'student_id': [{ required: true, message: '请输入学号', trigger: 'blur' }],
      'user.phone': [{ required: true, message: '请输入电话', trigger: 'blur' }],
      'user.department': [{ required: true, message: '请选择学院', trigger: 'change' }],
      'class_name': [{ required: true, message: '请选择班级', trigger: 'change' }],
      'ethnicity': [{ required: true, message: '请选择民族', trigger: 'change' }],
      'gender': [{ required: true, message: '请选择性别', trigger: 'change' }]
    }

    // 是否为毕业申请
    const isGraduationApplication = ref(false)

    // 毕业申请的验证规则
    const graduationRules = {
      ...rules,
      'graduation_date': [{ required: true, message: '请选择毕业日期', trigger: 'change' }],
      'current_company': [{ required: true, message: '请选择毕业去向', trigger: 'change' }]
    }

    // 判断是否为管理员
    const isAdmin = computed(() => {
      return store.state.user.role === 'admin'
    })

    // 判断是否为当前用户
    const isCurrentUser = (row) => {
      return row.user.id === store.state.user.id
    }

    // 判断是否为已毕业校友
    const isGraduatedAlumni = computed(() => {
      return store.state.user.role === 'graduated_alumni'
    })

    // 判断是否显示操作列
    const showOperationColumn = computed(() => {
      return isAdmin.value || (!isGraduatedAlumni.value && store.state.user.role === 'alumni')
    })

    // 获取校友列表
    const getAlumniList = async () => {
      try {
        console.log('开始获取校友列表') // 调试信息
        
        // 构建查询参数
        const params = {
          student_id: searchForm.student_id || '',
          name: searchForm.name || '',
          department: searchForm.department || '',
          class_name: searchForm.class_name || ''
        }
        const response = await request.get('/api/alumni/list/', { params })
        alumniList.value = response.data
        console.log(alumniList.value)
      } catch (error) {
        console.error('获取校友列表失败:', error)
        ElMessage.error('获取校友列表失败')
      }
    }

    // 搜索
    const handleSearch = () => {
      getAlumniList()
    }

    // 重置搜索
    const resetSearch = () => {
      searchForm.student_id = ''
      searchForm.name = ''
      searchForm.department = ''
      searchForm.class_name = ''
      getAlumniList()
    }

    // 选择变化
    const handleSelectionChange = (val) => {
      selectedRows.value = val
    }

    // 新增
    const handleAdd = () => {
      dialogTitle.value = '新增校友'
      formData.value = {
        user: {
          username: '',
          phone: '',
          department: '',
          role: 'alumni',  // 添加角色字段
          password: '123456'  // 添加默认密码
        },
        student_id: '',
        ethnicity: '',
        gender: '',
        birth_date: '',
        address: [],
        class_name: '',
        current_company: '',
        graduation_date: '',
        avatar: ''
      }
      // 确保在数据设置完成后再显示对话框
      nextTick(() => {
        dialogVisible.value = true
      })
    }

    // 编辑
    const handleEdit = (row) => {
      dialogTitle.value = '编辑校友'
      console.log('编辑的行数据:', row)  // 调试信息
      
      // 处理地址数据
      let addressArray = []
      if (row.address) {
        try {
          const addressParts = row.address.split(/[省市区]/).filter(Boolean)
          console.log('地址分割结果:', addressParts)
          
          const findAddressValues = (options, parts, current = []) => {
            if (parts.length === 0 || options.length === 0) return current
            
            const part = parts[0]
            const option = options.find(opt => 
              opt.label.includes(part) || part.includes(opt.label)
            )
            
            if (!option) return current
            
            const newCurrent = [...current, option.value]
            if (parts.length === 1 || !option.children) return newCurrent
            
            return findAddressValues(option.children, parts.slice(1), newCurrent)
          }
          
          addressArray = findAddressValues(addressOptions.value, addressParts)
        } catch (e) {
          console.log('地址格式转换失败:', e)
        }
      }

      // 先设置学院，触发班级选项的加载
      const department = row.user.department
      handleDepartmentChange(department)

      formData.value = {
        id: row.id,
        user: {
          username: row.user.username,
          phone: row.user.phone,
          department: department,
          role: 'alumni',
          password: '123456'
        },
        student_id: row.student_id,
        ethnicity: row.ethnicity || '',
        gender: row.gender || '',
        birth_date: row.birth_date,
        address: addressArray,
        current_company: row.current_company,
        graduation_date: row.graduation_date,
        avatar: row.avatar,
      }

      // 确保在数据设置完成后再显示对话框
      nextTick(() => {
        // 等待班级选项加载完成后再设置班级值
        nextTick(() => {
          formData.value.class_name = row.class_name
        })
        dialogVisible.value = true
      })
    }

    // 删除
    const handleDelete = async (row) => {
      try {
        await ElMessageBox.confirm('确认删除该校友信息吗？', '提示', {
          type: 'warning'
        })
        await request.delete(`/api/alumni/${row.id}/`)
        ElMessage.success('删除成功')
        getAlumniList()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除失败:', error)
          ElMessage.error('删除失败')
        }
      }
    }

    // 批量删除
    const handleBatchDelete = async () => {
      if (selectedRows.value.length === 0) {
        ElMessage.warning('请选择要删除的校友')
        return
      }
      
      try {
        await ElMessageBox.confirm('确认删除选中的校友信息吗？', '提示', {
          type: 'warning'
        })
        await request.post('/api/alumni/batch-delete/', {
          ids: selectedRows.value.map(row => row.id)
        })
        ElMessage.success('删除成功')
        getAlumniList()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除失败:', error)
          ElMessage.error('删除失败')
        }
      }
    }

    // 提交表单
    const handleSubmit = async () => {
      if (!formRef.value) return
      
      try {
        await formRef.value.validate()
        const submitData = { ...formData.value }
        
        // 处理日期格式
        if (submitData.birth_date) {
          submitData.birth_date = new Date(submitData.birth_date).toISOString().split('T')[0]
        }
        if (submitData.graduation_date) {
          submitData.graduation_date = new Date(submitData.graduation_date).toISOString().split('T')[0]
        }

        // 处理头像字段，如果没有上传头像则设置为 null
        if (!submitData.avatar) {
          submitData.avatar = null
        }

        // 处理地址数据
        if (Array.isArray(submitData.address)) {
          const getAddressLabel = (values) => {
            let result = ''
            let options = addressOptions.value
            
            for (const value of values) {
              const option = options.find(opt => opt.value === value)
              if (!option) break
              result += option.label
              options = option.children || []
            }
            return result
          }
          submitData.address = getAddressLabel(submitData.address)
        }

        if (isGraduationApplication.value) {
          // 毕业申请
          await request.put(`/api/alumni/${submitData.id}/apply-graduation/`, {
            graduation_date: submitData.graduation_date,
            current_company: submitData.current_company
          })
          ElMessage.success('毕业申请提交成功，请等待管理员审核')
        } else if (dialogTitle.value === '新增校友') {
          // 新增校友
          await request.post('/api/alumni/add/', submitData)  // 修改为新的URL
          ElMessage.success('新增成功')
        } else {
          // 编辑校友
          await request.put(`/api/alumni/${submitData.id}/`, submitData)
          ElMessage.success('编辑成功')
        }

        dialogVisible.value = false
        isGraduationApplication.value = false  // 重置状态
        getAlumniList()  // 刷新列表
      } catch (error) {
        console.error('提交失败:', error)
        ElMessage.error('提交失败: ' + (error.response?.data?.error || error.message || '未知错误'))
      }
    }

    // 分页大小变化
    const handleSizeChange = (val) => {
      pageSize.value = val
      getAlumniList()
    }

    // 页码变化
    const handleCurrentChange = (val) => {
      currentPage.value = val
      getAlumniList()
    }

    // 头像上传相关方法
    const handleAvatarSuccess = (res, file) => {
      console.log('上传成功，响应数据:', res)  // 调试信息
      if (res.url) {
        formData.value.avatar = res.url
      } else {
        ElMessage.error('上传失败：未获取到文件URL')
      }
    }

    const beforeAvatarUpload = (file) => {
      const isJPG = file.type === 'image/jpeg'
      const isLt2M = file.size / 1024 / 1024 < 2

      if (!isJPG) {
        ElMessage.error('上传头像图片只能是 JPG 格式!')
      }
      if (!isLt2M) {
        ElMessage.error('上传头像图片大小不能超过 2MB!')
      }
      return isJPG && isLt2M
    }

    // 地址选项数据
    const addressOptions = ref([
      {
        value: '北京市',
        label: '北京市',
        children: [
          {
            value: '北京市',
            label: '北京市',
            children: [
              { value: '东城区', label: '东城区' },
              { value: '西城区', label: '西城区' },
              { value: '朝阳区', label: '朝阳区' },
              { value: '海淀区', label: '海淀区' }
            ]
          }
        ]
      },
      {
        value: '浙江省',
        label: '浙江省',
        children: [
          {
            value: '杭州市',
            label: '杭州市',
            children: [
              { value: '西湖区', label: '西湖区' },
              { value: '上城区', label: '上城区' },
              { value: '下城区', label: '下城区' },
              { value: '滨江区', label: '滨江区' }
            ]
          },
          {
            value: '宁波市',
            label: '宁波市',
            children: [
              { value: '海曙区', label: '海曙区' },
              { value: '江北区', label: '江北区' },
              { value: '北仑区', label: '北仑区' }
            ]
          }
        ]
      }
      // ... 其他省份
    ])

    // 民族选项数据
    const ethnicityOptions = ref([
      { label: '汉族', value: '汉族' },
      { label: '满族', value: '满族' },
      { label: '回族', value: '回族' },
      { label: '藏族', value: '藏族' },
      { label: '维吾尔族', value: '维吾尔族' },
      { label: '苗族', value: '苗族' },
      { label: '壮族', value: '壮族' },
      // ... 其他民族
    ])

    // 学院及对应班级数据
    const departmentOptions = ref([
      {
        label: '计算机学院',
        value: '计算机学院',
        classes: [
          { label: '计算机科学与技术1班', value: '计科1班' },
          { label: '计算机科学与技术2班', value: '计科2班' },
          { label: '软件工程1班', value: '软工1班' },
          { label: '软件工程2班', value: '软工2班' },
          { label: '人工智能1班', value: 'AI1班' }
        ]
      },
      {
        label: '信息工程学院',
        value: '信息工程学院',
        classes: [
          { label: '通信工程1班', value: '通信1班' },
          { label: '电子信息1班', value: '电信1班' },
          { label: '物联网工程1班', value: '物联网1班' }
        ]
      },
      {
        label: '经济管理学院',
        value: '经济管理学院',
        classes: [
          { label: '工商管理1班', value: '工管1班' },
          { label: '会计学1班', value: '会计1班' },
          { label: '金融学1班', value: '金融1班' }
        ]
      }
      // ... 其他学院
    ])

    // 当前选中学院的班级选项
    const classOptions = ref([])

    // 监听学院选择变化
    const handleDepartmentChange = (value) => {
      console.log('学院变化:', value)  // 调试信息
      // 根据选择的学院查找对应的班级选项
      const selectedDept = departmentOptions.value.find(dept => dept.value === value)
      classOptions.value = selectedDept ? selectedDept.classes : []
      // 清空已选班级
      formData.value.class_name = ''
      console.log('更新后的班级选项:', classOptions.value)  // 调试信息
    }

    // 导入
    const handleImport = () => {
      const input = document.createElement('input')
      input.type = 'file'
      input.accept = '.xlsx,.xls'
      input.onchange = async (e) => {
        const file = e.target.files[0]
        if (!file) return
        
        const formData = new FormData()
        formData.append('file', file)
        
        try {
          const response = await request.post('/api/alumni/import/', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })
          ElMessage.success(response.data.message)
          if (response.data.errors && response.data.errors.length > 0) {
            console.log('导入错误:', response.data.errors)
          }
          getAlumniList()  // 刷新列表
        } catch (error) {
          ElMessage.error('导入失败：' + (error.response?.data?.error || '未知错误'))
        }
      }
      input.click()
    }

    // 导出
    const handleExport = async () => {
      try {
        const response = await request.get('/api/alumni/export/', {
          responseType: 'blob'
        })
        
        // 创建下载链接
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `校友信息_${new Date().toLocaleDateString()}.xlsx`)
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        window.URL.revokeObjectURL(url)
        
        ElMessage.success('导出成功')
      } catch (error) {
        ElMessage.error('导出失败：' + (error.response?.data?.error || '未知错误'))
      }
    }

    // 处理毕业申请
    const handleGraduationApplication = (row) => {
      isGraduationApplication.value = true
      dialogTitle.value = '申请毕业'
       // 处理班级选项
      handleDepartmentChange(row.user.department)
      // 设置表单数据
      formData.value = {
        id: row.id,
        user: {
          id: row.user.id,
          username: row.user.username,
          phone: row.user.phone,
          department: row.user.department,
          role: 'alumni'
        },
        student_id: row.student_id,
        ethnicity: row.ethnicity || '',
        gender: row.gender || '',
        birth_date: row.birth_date,
        address: row.address ? row.address.split(/[省市区]/).filter(Boolean) : [],
        class_name: row.class_name,
        current_company: row.current_company || '',
        graduation_date: row.graduation_date || '',
        avatar: row.avatar,
        graduation_status: 'pending'  // 添加毕业状态
      }

      // 显示对话框
      nextTick(() => {
        // 等待班级选项加载完成后再设置班级值
        nextTick(() => {
          formData.value.class_name = row.class_name
        })
        dialogVisible.value = true
      })
    }

    const getGraduationButtonText = (row) => {
      switch(row.application_status) {
        case 1:
          return '审核中';
        case 2:
          return '审核通过';
        case 3:
          return '审核不通过';
        default:
          return '申请毕业';
      }
    }
    // 获取图片URL
    const getImageUrl = (image) => {
      if (!image) {
        return new URL('/src/assets/images/default-association.jpg', import.meta.url).href
      }
      return `${import.meta.env.VITE_API_URL}${image}`
    }

    onMounted(() => {
      console.log('组件挂载，开始获取数据') // 调试信息
      getAlumniList()
    })

    return {
      alumniList,
      total,
      currentPage,
      pageSize,
      selectedRows,
      searchForm,
      dialogVisible,
      dialogTitle,
      formRef,
      formData,
      rules,
      handleSearch,
      resetSearch,
      handleSelectionChange,
      handleAdd,
      handleEdit,
      handleDelete,
      handleBatchDelete,
      handleSubmit,
      handleSizeChange,
      handleCurrentChange,
      handleAvatarSuccess,
      beforeAvatarUpload,
      addressOptions,
      ethnicityOptions,
      departmentOptions,
      classOptions,
      handleDepartmentChange,
      authHeaders,
      store,
      handleImport,
      handleExport,
      isAdmin,
      isCurrentUser,
      isGraduationApplication,
      graduationRules,
      handleGraduationApplication,
      getGraduationButtonText,
      isGraduatedAlumni,
      showOperationColumn,
      getImageUrl
    }
  }
}
</script>

<style scoped>
.alumni-info {
  padding: 20px;
}

.search-bar {
  margin-bottom: 20px;
  padding: 20px;
  background-color: #fff;
  border-radius: 4px;
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

.section-title {
  font-size: 16px;
  font-weight: bold;
  margin: 20px 0;
  padding-left: 10px;
  border-left: 4px solid #409EFF;
}

.form-wrapper {
  display: flex;
  gap: 20px;
}

.form-content {
  flex: 1;
}

.avatar-section {
  width: 200px;
  padding-top: 20px;
}

.avatar-upload {
  width: 150px;
}

.alumni-form {
  overflow: visible;
}

.avatar-uploader {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  overflow: hidden;
}

.avatar-uploader:hover {
  border-color: #409EFF;
}

.avatar {
  width: 150px;
  height: 150px;
  display: block;
}

.upload-placeholder {
  width: 150px;
  height: 150px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #fafafa;
}

.upload-text {
  margin-top: 10px;
  color: #666;
}

.upload-hint {
  font-size: 12px;
  color: #999;
  margin-top: 5px;
}
</style> 