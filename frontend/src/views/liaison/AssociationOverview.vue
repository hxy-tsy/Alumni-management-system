<template>
  <div class="association-overview">
    <div class="content-card">
      <h1 class="title">{{ associationInfo.name }}</h1>

      <div class="association-content">
        <!-- 校友会图片展示区域 -->
        <div class="image-section">
          <el-image 
            :src="getImageUrl(associationInfo.image)"
            fit="contain"
            class="association-image"
          />
        </div>

        <!-- 校友会信息描述区域 -->
        <div class="description-section">
          <p class="description-text">{{ associationInfo.description }}</p>
        </div>

        <!-- 操作按钮区域 -->
        <div class="action-buttons">
          <el-button type="primary" @click="handleEdit">编辑</el-button>
          <el-button @click="handleCancel">确认</el-button>
        </div>
      </div>
    </div>

    <!-- 编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="编辑校友会信息"
      width="50%"
    >
      <el-form :model="editForm" label-width="100px">
        <el-form-item label="校友会名称">
          <el-input v-model="editForm.name" />
        </el-form-item>
        <el-form-item label="成立时间">
          <el-date-picker
            v-model="editForm.founding_date"
            type="date"
            placeholder="选择日期"
          />
        </el-form-item>
        <el-form-item label="校友会简介">
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
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import request from '@/utils/request'
import store from '@/store'

export default {
  name: 'AssociationOverview',
  setup() {
    const associationInfo = ref({
      name: '',
      description: '',
      founding_date: '',
      image: ''
    })

    const dialogVisible = ref(false)
    const editForm = ref({
      name: '',
      description: '',
      founding_date: '',
      image: ''
    })

    // 获取认证头信息
    const getAuthHeaders = () => {
      const token = store.state.token || localStorage.getItem('token') || ''
      return {
        Authorization: token ? `Bearer ${token}` : ''
      }
    }

    // 获取校友联络人管理的校友会信息
    const fetchAssociationInfo = async () => {
      try {
        const response = await request.get('/api/association/my-branch/')
        associationInfo.value = response.data
      } catch (error) {
        console.error('获取校友会信息失败:', error)
        ElMessage.error('获取校友会信息失败: ' + (error.response?.data?.error || error.message || '未知错误'))
      }
    }

    // 编辑按钮点击事件
    const handleEdit = () => {
      editForm.value = { ...associationInfo.value }
      dialogVisible.value = true
    }

    // 取消按钮点击事件
    const handleCancel = () => {
      // 重新加载数据
      fetchAssociationInfo()
    }

    // 保存编辑内容
    const handleSave = async () => {
      try {
        // 准备要发送的数据
        const formData = {
          name: editForm.value.name,
          description: editForm.value.description
        }
        
        // 处理日期格式
        if (editForm.value.founding_date) {
          // 如果是Date对象，转换为YYYY-MM-DD格式
          if (editForm.value.founding_date instanceof Date) {
            const date = editForm.value.founding_date
            const year = date.getFullYear()
            const month = String(date.getMonth() + 1).padStart(2, '0')
            const day = String(date.getDate()).padStart(2, '0')
            formData.founding_date = `${year}-${month}-${day}`
          } else {
            // 如果已经是字符串，直接使用
            formData.founding_date = editForm.value.founding_date
          }
        }
        
        // 处理图片字段
        if (editForm.value.image) {
          // 如果是新上传的图片（base64格式），则使用image字段
          if (typeof editForm.value.image === 'string' && editForm.value.image.startsWith('data:')) {
            formData.image = editForm.value.image
          } 
          // 如果是已有的图片路径，则使用image_path字段
          else if (typeof editForm.value.image === 'string') {
            formData.image = editForm.value.image
          }
        }
        
        await request.put('/api/association/my-branch/', formData)
        ElMessage.success('保存成功')
        dialogVisible.value = false
        fetchAssociationInfo() // 重新加载数据
      } catch (error) {
        console.error('保存失败:', error)
        ElMessage.error('保存失败: ' + (error.response?.data?.error || error.message || '未知错误'))
        
        // 显示详细错误信息
        if (error.response && error.response.data) {
          console.error('错误详情:', error.response.data)
          
          // 如果是字段验证错误，显示具体字段的错误信息
          const errorData = error.response.data
          if (typeof errorData === 'object' && errorData !== null) {
            Object.keys(errorData).forEach(field => {
              ElMessage.error(`${field}: ${errorData[field]}`)
            })
          }
        }
      }
    }
    // 获取图片URL
    const getImageUrl = (image) => {
      if (!image) {
        return new URL('/src/assets/images/default-association.jpg', import.meta.url).href
      }
      return `${import.meta.env.VITE_API_URL}${image}`
    }

    // 上传图片前的验证
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

    // 图片上传成功回调
    const handleImageSuccess = (response) => {
      console.log('图片上传成功:', response)
      if (response && response.url) {
        editForm.value.image = response.url
      } else {
        console.error('图片上传返回格式不正确:', response)
        ElMessage.error('图片上传失败: 返回格式不正确')
      }
    }

    onMounted(() => {
      fetchAssociationInfo()
    })

    return {
      associationInfo,
      dialogVisible,
      editForm,
      handleEdit,
      handleCancel,
      handleSave,
      beforeUpload,
      handleImageSuccess,
      getAuthHeaders,
      getImageUrl
    }
  }
}
</script>

<style scoped>
.association-overview {
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

.association-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.image-section {
  width: 100%;
  max-width: 800px;
  margin-bottom: 30px;
}

.association-image {
  width: 100%;
  height: 300px;
  object-fit: cover;
  border-radius: 4px;
}

.description-section {
  width: 100%;
  max-width: 800px;
  margin-bottom: 30px;
}

.description-text {
  line-height: 1.8;
  color: #666;
  text-align: justify;
  white-space: pre-wrap;
}

.action-buttons {
  margin-top: 20px;
  text-align: center;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

.preview-image {
  width: 200px;
  height: 120px;
  object-fit: cover;
  border-radius: 4px;
  margin-bottom: 10px;
}
</style> 