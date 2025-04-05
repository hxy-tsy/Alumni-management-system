<template>
  <div class="my-association">
    <div class="content-card">
      <h1 class="title">我的校友会</h1>

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

      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="5" animated />
      </div>

      <div v-else-if="associationList.length === 0" class="empty-container">
        <el-empty description="您尚未加入任何校友会" />
      </div>

      <div v-else class="association-table">
        <el-table :data="associationList" style="width: 100%" border>
          <el-table-column label="校友会名称" prop="association_name" min-width="150" />
          <el-table-column label="类型" min-width="120">
            <template #default="scope">
              {{ scope.row.association_type_display }}
            </template>
          </el-table-column>
          <el-table-column label="会长" prop="leader_name" min-width="100" />
          <el-table-column label="创立时间" min-width="120">
            <template #default="scope">
              {{ formatDate(scope.row.founding_date) }}
            </template>
          </el-table-column>
          <el-table-column label="加入时间" min-width="120">
            <template #default="scope">
              {{ formatDate(scope.row.join_date) }}
            </template>
          </el-table-column>
          <el-table-column label="状态" min-width="100">
            <template #default="scope">
              <el-tag :type="getStatusType(scope.row.status)">
                {{ scope.row.status_display }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="100" fixed="right">
            <template #default="scope">
              <el-button
                v-if="scope.row.status === 2"
                type="danger"
                size="small"
                @click="handleQuit(scope.row)"
                :loading="quitLoading === scope.row.id"
              >
                退出
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '@/utils/request'

export default {
  name: 'MyAssociation',
  setup() {
    const loading = ref(true)
    const associationList = ref([])
    const quitLoading = ref(null)
    
    // 搜索表单
    const searchForm = ref({
      name: '',
      type: ''
    })

    // 过滤后的列表
    const filteredAssociationList = computed(() => {
      return associationList.value.filter(item => {
        const nameMatch = !searchForm.value.name || 
          item.association_name.toLowerCase().includes(searchForm.value.name.toLowerCase())
        const typeMatch = !searchForm.value.type || 
          item.association_type === searchForm.value.type
        return nameMatch && typeMatch
      })
    })

    // 搜索处理
    const handleSearch = () => {
      // 直接使用计算属性进行过滤，无需额外操作
    }

    // 重置搜索
    const handleReset = () => {
      searchForm.value = {
        name: '',
        type: ''
      }
    }

    // 获取我的校友会列表
    const fetchAssociationList = async () => {
      try {
        loading.value = true
        const response = await request.get('/api/association/my-joined/')
        associationList.value = response.data
      } catch (error) {
        console.error('获取校友会列表失败:', error)
        ElMessage.error('获取校友会列表失败: ' + (error.response?.data?.error || error.message || '未知错误'))
      } finally {
        loading.value = false
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

    // 格式化日期
    const formatDate = (date) => {
      if (!date) return '-'
      return new Date(date).toLocaleDateString('zh-CN')
    }

    // 退出校友会
    const handleQuit = async (row) => {
      try {
        await ElMessageBox.confirm(
          `确定要退出 ${row.association_name} 吗？`,
          '确认退出',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
          }
        )

        quitLoading.value = row.id
        await request.delete(`/api/association/quit/${row.id}/`)
        ElMessage.success('已退出校友会')

        // 刷新列表
        fetchAssociationList()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('退出校友会失败:', error)
          ElMessage.error('退出校友会失败: ' + (error.response?.data?.error || error.message || '未知错误'))
        }
      } finally {
        quitLoading.value = null
      }
    }

    onMounted(() => {
      fetchAssociationList()
    })

    return {
      loading,
      searchForm,
      associationList: filteredAssociationList, // 使用过滤后的列表
      quitLoading,
      getStatusType,
      formatDate,
      handleQuit,
      handleSearch,
      handleReset
    }
  }
}
</script>

<style scoped>
.my-association {
  padding: 20px;
}

.content-card {
  background: #fff;
  padding: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.title {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
}

.loading-container {
  padding: 20px;
}

.empty-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 0;
}

.association-table {
  margin-top: 20px;
}

.search-section {
  background: #fff;
  margin-bottom: 20px;
  padding: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.search-form {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}
</style>