<template>
  <div class="branch-manage">
    <!-- 搜索区域 -->
    <div class="search-section">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="校友会名称">
          <el-input v-model="searchForm.name" placeholder="请输入校友会名称" />
        </el-form-item>
        <el-form-item label="校友会类型">
          <el-select v-model="searchForm.type" placeholder="请选择校友会类型" clearable style="width: 120px;">
            <el-option label="学院校友会" value="college" />
            <el-option label="地方校友会" value="local" />
            <el-option label="海外校友会" value="overseas" />
            <el-option label="行业校友会" value="industry" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 分会列表展示区域 -->
    <div class="branch-list">
      <el-row :gutter="20">
        <el-col v-for="branch in branchList" :key="branch.id" :span="8">
          <el-card class="branch-card" :body-style="{ padding: '0px' }">
            <el-image 
              :src="getImageUrl(branch.image)" 
              fit="contain"
              class="branch-image"
            />
            <div class="branch-info">
              <h3>{{ branch.name }}</h3>
              <p class="description">{{ branch.description }}</p>
              <div class="card-footer">
                <el-button type="primary" size="small" @click="handleEdit(branch)">编辑</el-button>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="70%"
    >
      <el-tabs v-model="activeTab">
        <el-tab-pane label="基本信息" name="basic">
          <el-form :model="editForm" label-width="100px">
            <el-form-item label="分会名称">
              <el-input v-model="editForm.name" />
            </el-form-item>
            <el-form-item label="分会类型">
              <el-select v-model="editForm.type">
                <el-option label="学院校友会" value="college" />
                <el-option label="地方校友会" value="local" />
                <el-option label="海外校友会" value="overseas" />
                <el-option label="行业校友会" value="industry" />
              </el-select>
            </el-form-item>
            <el-form-item label="成立时间">
              <el-date-picker
                v-model="editForm.founding_date"
                type="date"
                placeholder="选择日期"
              />
            </el-form-item>
            <el-form-item label="分会简介">
              <el-input
                v-model="editForm.description"
                type="textarea"
                :rows="4"
              />
            </el-form-item>
            <el-form-item label="图片">
              <el-upload
                class="upload-demo"
                action="/api/association/upload/"
                :headers="getAuthHeaders()"
                :on-success="handleImageSuccess"
                :before-upload="beforeUpload"
                :show-file-list="false"
              >
                <img v-if="editForm.image" :src="getImageUrl(editForm.image)" class="preview-image" />
                <el-button v-else type="primary">点击上传</el-button>
              </el-upload>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="成员信息" name="members">
          <div class="members-container">
            <el-table :data="members" style="width: 100%" border>
              <el-table-column label="姓名" min-width="100">
                <template #default="scope">
                  {{ scope.row.user.first_name }}{{ scope.row.user.last_name || scope.row.user.username }}
                </template>
              </el-table-column>
              <el-table-column label="角色" prop="role_display" min-width="80" />
              <el-table-column label="学号" min-width="120">
                <template #default="scope">
                  {{ scope.row.profile?.student_id || '-' }}
                </template>
              </el-table-column>
              <el-table-column label="学院" min-width="150">
                <template #default="scope">
                  {{ scope.row.profile?.department || '-' }}
                </template>
              </el-table-column>
              <el-table-column label="班级" min-width="120">
                <template #default="scope">
                  {{ scope.row.profile?.class_name || '-' }}
                </template>
              </el-table-column>
              <el-table-column label="毕业日期" min-width="120">
                <template #default="scope">
                  {{ scope.row.profile?.graduation_date || '-' }}
                </template>
              </el-table-column>
              <el-table-column label="工作单位" min-width="150">
                <template #default="scope">
                  {{ scope.row.profile?.current_company || '-' }}
                </template>
              </el-table-column>
              <el-table-column label="电话" min-width="120">
                <template #default="scope">
                  {{ scope.row.profile?.phone || '-' }}
                </template>
              </el-table-column>
<!--              <el-table-column label="工作城市" min-width="120">-->
<!--                <template #default="scope">-->
<!--                  {{ scope.row.profile?.work_city || '-' }}-->
<!--                </template>-->
<!--              </el-table-column>-->
<!--              <el-table-column label="联系地址" min-width="150">-->
<!--                <template #default="scope">-->
<!--                  {{ scope.row.profile?.address || '-' }}-->
<!--                </template>-->
<!--              </el-table-column>-->
<!--              <el-table-column label="加入日期" prop="join_date" min-width="120" />-->
            </el-table>
          </div>
        </el-tab-pane>
      </el-tabs>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSave">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import request from '@/utils/request'
import store from '@/store'

export default {
  name: 'AssociationBranchManage',
  setup() {
    // 搜索表单
    const searchForm = ref({
      name: '',
      type: ''
    })

    // 分会列表
    const branchList = ref([])

    const dialogVisible = ref(false)
    const dialogTitle = ref('')
    const editForm = ref({})
    const activeTab = ref('basic')
    
    // 成员信息
    const members = computed(() => {
      return editForm.value.members_info || []
    })

    // 获取完整的图片URL
    const getImageUrl = (imageUrl) => {
      if (!imageUrl) return '/src/assets/images/default-association.jpg'
      if (imageUrl.startsWith('http')) return imageUrl
      // 使用环境变量中的后端基础URL
      const baseUrl = import.meta.env.VITE_API_BASE_URL || ''
      const fullUrl = baseUrl + imageUrl
      console.log('Image URL:', {
        original: imageUrl,
        baseUrl: baseUrl,
        fullUrl: fullUrl
      })
      return fullUrl
    }

    // 获取认证头信息
    const getAuthHeaders = () => {
      const token = store.state.token || localStorage.getItem('token') || ''
      return {
        Authorization: token ? `Bearer ${token}` : ''
      }
    }

    // 获取分会列表
    const fetchBranchList = async () => {
      try {
        let url = '/api/association/branches/'
        const params = {}
        
        if (searchForm.value.name) {
          params.name = searchForm.value.name
        }
        
        if (searchForm.value.type) {
          params.type = searchForm.value.type
        }
        
        console.log('获取分会列表，参数:', params)
        const response = await request.get(url, { params })
        console.log('获取分会列表成功:', response.data)
        
        if (response.data && Array.isArray(response.data)) {
          branchList.value = response.data
        } else {
          console.warn('返回的分会数据格式不正确:', response.data)
          branchList.value = []
        }

      } catch (error) {
        console.error('获取分会列表失败:', error)
        ElMessage.error('获取分会列表失败: ' + (error.response?.data?.error || error.message || '未知错误'))
        
        // 显示默认数据
        branchList.value = [
          {
            id: 1,
            name: '计算机学院校友会',
            type: 'college',
            description: '计算机学院校友会成立于2000年，致力于促进计算机学院校友之间的交流与合作。',
            founding_date: '2000-09-01',
            image: '/src/assets/images/branch1.jpg'
          },
          {
            id: 2,
            name: '北京校友会',
            type: 'local',
            description: '北京校友会是最早成立的地方校友会之一，汇聚了在京工作生活的广大校友。',
            founding_date: '1995-05-15',
            image: '/src/assets/images/branch2.jpg'
          },
          {
            id: 3,
            name: '金融行业校友会',
            type: 'industry',
            description: '金融行业校友会联结了在金融领域工作的校友，促进行业交流与发展。',
            founding_date: '2010-03-20',
            image: '/src/assets/images/branch3.jpg'
          }
        ]
      }
    }

    // 搜索处理
    const handleSearch = () => {
      fetchBranchList()
    }

    // 重置搜索
    const handleReset = () => {
      searchForm.value = {
        name: '',
        type: ''
      }
      fetchBranchList()
    }

    // 编辑分会
    const handleEdit = (branch) => {
      console.log('编辑分会:', branch)
      editForm.value = { ...branch }
      dialogTitle.value = '编辑分会信息'
      dialogVisible.value = true
      activeTab.value = 'basic'
    }

    // 保存编辑
    const handleSave = async () => {
      try {
        // 准备要发送的数据
        const formData = {
          name: editForm.value.name,
          description: editForm.value.description
        }
        
        // 处理日期格式
        if (editForm.value.founding_date) {
          if (editForm.value.founding_date instanceof Date) {
            const date = editForm.value.founding_date
            const year = date.getFullYear()
            const month = String(date.getMonth() + 1).padStart(2, '0')
            const day = String(date.getDate()).padStart(2, '0')
            formData.founding_date = `${year}-${month}-${day}`
          } else {
            formData.founding_date = editForm.value.founding_date
          }
        }
        
        // 保留leader字段
        if (editForm.value.leader) {
          formData.leader = editForm.value.leader
        }
        
        // 处理图片字段
        if (editForm.value.image) {
          formData.image = editForm.value.image
          // 打印图片信息进行调试
          console.log('发送图片信息:', {
            imageType: typeof editForm.value.image,
            imageValue: editForm.value.image
          })
        }
        
        console.log('保存分会信息:', formData)
        const response = await request.put(`/api/association/branches/${editForm.value.id}/`, formData)
        console.log('保存成功，响应:', response)
        ElMessage.success('保存成功')
        dialogVisible.value = false
        fetchBranchList() // 重新加载数据
      } catch (error) {
        console.error('保存失败:', error)
        if (error.response && error.response.data) {
          console.error('错误详情:', error.response.data)
        }
        ElMessage.error('保存失败: ' + (error.response?.data?.error || error.message || '未知错误'))
      }
    }

    // 图片上传相关
    const beforeUpload = (file) => {
      const isImage = file.type.startsWith('image/')
      const isLt2M = file.size / 1024 / 1024 < 2

      if (!isImage) {
        ElMessage.error('只能上传图片文件!')
        return false
      }
      if (!isLt2M) {
        ElMessage.error('图片大小不能超过 2MB!')
        return false
      }
      return true
    }

    const handleImageSuccess = (response) => {
      console.log('图片上传成功:', response)
      if (response && response.url) {
        // 存储完整的图片URL
        editForm.value.image = response.url
        console.log('更新编辑表单的图片URL:', editForm.value.image)
      } else {
        console.error('图片上传返回格式不正确:', response)
        ElMessage.error('图片上传失败: 返回格式不正确')
      }
    }

    onMounted(() => {
      fetchBranchList()
    })

    return {
      searchForm,
      branchList,
      dialogVisible,
      dialogTitle,
      editForm,
      activeTab,
      members,
      getAuthHeaders,
      handleSearch,
      handleReset,
      handleEdit,
      handleSave,
      handleImageSuccess,
      beforeUpload,
      getImageUrl
    }
  }
}
</script>

<style scoped>
.branch-manage {
  padding: 20px;
}

.search-section {
  background: #fff;
  padding: 20px;
  border-radius: 4px;
  margin-bottom: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.branch-list {
  margin-top: 20px;
}

.branch-card {
  margin-bottom: 20px;
  transition: all 0.3s;
  background-color: #fff;  /* 添加白色背景 */
}

.branch-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.branch-image {
  width: 100%;
  height: 200px;
  object-fit: contain;
  display: block;
  background-color: #f5f7fa;
  padding: 10px;  /* 添加内边距 */
  box-sizing: border-box;  /* 确保padding不会增加元素实际大小 */
}

.branch-info {
  padding: 14px;
  background-color: #fff;  /* 确保信息区域有白色背景 */
}

.branch-info h3 {
  margin: 0;
  font-size: 16px;
  color: #333;
  margin-bottom: 10px;  /* 添加标题下方间距 */
}

.description {
  font-size: 14px;
  color: #666;
  margin: 10px 0;
  height: 60px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.card-footer {
  display: flex;
  justify-content: flex-end;
  padding-top: 10px;
  border-top: 1px solid #eee;  /* 添加顶部分隔线 */
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

.el-form-item {
  margin-bottom: 20px;
}

.preview-image {
  width: 200px;
  height: 200px;
  object-fit: contain;
  border-radius: 4px;
  margin-bottom: 10px;
  background-color: #f5f7fa;
  border: 1px solid #e0e0e0;
  padding: 10px;  /* 添加内边距 */
  box-sizing: border-box;
}

.members-container {
  margin-top: 10px;
  max-height: 500px;
  overflow-y: auto;
}
</style> 