<template>
  <div class="join-association">
    <!-- 搜索区域 -->
    <div class="search-section">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="校友会名称">
          <el-input v-model="searchForm.name" placeholder="请输入校友会名称" />
        </el-form-item>
        <el-form-item label="校友会类型">
          <el-select v-model="searchForm.type" placeholder="请选择校友会类型" clearable style="width: 165px">
            <el-option label="全部类型" value="" />
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

    <!-- 校友会列表展示区域 -->
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
                <el-button type="primary" size="small" @click="handleView(branch)">查看</el-button>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 查看对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="校友会详情"
      width="50%"
    >
      <div class="association-detail">
        <h2 class="detail-title">{{ currentBranch.name }}</h2>
        
        <div class="detail-image-container">
          <el-image 
            :src="getImageUrl(currentBranch.image)" 
            fit="cover"
            class="detail-image"
          />
        </div>
        
        <div class="detail-info">
          <p><strong>校友会类型：</strong>{{ getTypeDisplay(currentBranch.type) }}</p>
          <p><strong>成立时间：</strong>{{ currentBranch.founding_date }}</p>
          <p><strong>简介：</strong></p>
          <p class="detail-description">{{ currentBranch.description }}</p>
        </div>
        
        <div class="detail-actions">
          <el-button 
            type="primary" 
            @click="handleApply" 
            :disabled="isApplied(currentBranch.id)"
            :loading="applyLoading"
          >
            {{ getApplyButtonText(currentBranch.id) }}
          </el-button>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import request from '@/utils/request'

export default {
  name: 'JoinAssociation',
  setup() {
    // 搜索表单
    const searchForm = ref({
      name: '',
      type: ''
    })

    // 校友会列表
    const branchList = ref([])
    
    // 对话框相关
    const dialogVisible = ref(false)
    const currentBranch = ref({})
    
    // 申请状态
    const applicationStatus = ref({})
    const applyLoading = ref(false)

    // 获取图片URL
    const getImageUrl = (image) => {
      if (!image) {
        return new URL('/src/assets/images/default-association.jpg', import.meta.url).href
      }
      return `${import.meta.env.VITE_API_URL}${image}`
    }

    // 获取校友会列表
    const fetchBranchList = async () => {
      try {
        const params = {}
        
        if (searchForm.value.name) {
          params.name = searchForm.value.name
        }
        
        if (searchForm.value.type) {
          params.type = searchForm.value.type
        }
        
        const response = await request.get('/api/association/branches/', { params })
        console.log('获取到的校友会数据:', response.data)
        branchList.value = response.data
        
        // 获取申请状态
        await checkApplicationStatus()
      } catch (error) {
        console.error('获取校友会列表失败:', error)
        ElMessage.error('获取校友会列表失败: ' + (error.response?.data?.error || error.message || '未知错误'))
      }
    }
    
    // 检查申请状态
    const checkApplicationStatus = async () => {
      try {
        // 获取我已加入或申请的校友会
        const response = await request.get('/api/association/my-joined/')
        if (response.data && response.data.length > 0) {
          const statusMap = {}
          response.data.forEach(item => {
            statusMap[item.association_name] = item.status
          })
          applicationStatus.value = statusMap
        }
      } catch (error) {
        console.error('获取申请状态失败:', error)
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

    // 查看校友会详情
    const handleView = (branch) => {
      currentBranch.value = branch
      dialogVisible.value = true
    }

    // 判断是否已申请或已加入
    const isApplied = (branchId) => {
      const status = applicationStatus.value[currentBranch.value.name]
      return status === 1 || status === 2  // 申请中(1)或已通过(2)时禁用按钮
    }
    
    // 获取申请按钮文本
    const getApplyButtonText = (branchId) => {
      const status = applicationStatus.value[currentBranch.value.name]
      if (status === 1) return '申请审核中'
      if (status === 2) return '已加入'
      if (status === 3) return '重新申请'
      return '申请加入'
    }

    // 申请加入校友会
    const handleApply = async () => {
      if (isApplied(currentBranch.value.id)) {
        ElMessage.warning('您已经申请或加入了该校友会')
        return
      }
      
      try {
        applyLoading.value = true
        const response = await request.post(`/api/association/branches/${currentBranch.value.id}/apply/`)
        ElMessage.success(response.data.message || '申请已提交，请等待审批')
        
        // 更新申请状态
        applicationStatus.value[currentBranch.value.name] = 1  // 申请中
      } catch (error) {
        console.error('申请加入校友会失败:', error)
        ElMessage.error('申请加入校友会失败: ' + (error.response?.data?.error || error.message || '未知错误'))
      } finally {
        applyLoading.value = false
      }
    }

    // 获取校友会类型显示文本
    const getTypeDisplay = (type) => {
      const typeMap = {
        'general': '总会',
        'college': '学院校友会',
        'local': '地方校友会',
        'overseas': '海外校友会',
        'industry': '行业校友会'
      }
      return typeMap[type] || type
    }

    onMounted(() => {
      fetchBranchList()
    })

    return {
      searchForm,
      branchList,
      dialogVisible,
      currentBranch,
      applyLoading,
      handleSearch,
      handleReset,
      handleView,
      handleApply,
      isApplied,
      getApplyButtonText,
      getTypeDisplay,
      getImageUrl
    }
  }
}
</script>

<style scoped>
.join-association {
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
}

.branch-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.branch-image {
  width: 100%;
  height: 200px;
  display: block;
}

.branch-info {
  padding: 14px;
}

.branch-info h3 {
  margin: 0;
  font-size: 16px;
  color: #333;
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
}

.association-detail {
  padding: 0 20px;
}

.detail-title {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}

.detail-image-container {
  width: 100%;
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.detail-image {
  width: 100%;
  max-width: 500px;
  height: 250px;
  object-fit: cover;
  border-radius: 4px;
}

.detail-info {
  margin-bottom: 20px;
}

.detail-description {
  white-space: pre-wrap;
  line-height: 1.6;
  color: #666;
}

.detail-actions {
  display: flex;
  justify-content: center;
  margin: 20px 0;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}
</style> 