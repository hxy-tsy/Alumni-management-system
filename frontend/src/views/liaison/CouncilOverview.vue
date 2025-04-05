<template>
  <div class="council-overview">
    <!-- 搜索区域 -->
<!--    <div class="search-section">-->
<!--      <el-form :inline="true" :model="searchForm" class="search-form">-->
<!--        <el-form-item label="理事会名称">-->
<!--          <el-input v-model="searchForm.name" placeholder="请输入理事会名称" />-->
<!--        </el-form-item>-->
<!--        <el-form-item label="发送状态">-->
<!--          <el-select v-model="searchForm.invitation_sent" placeholder="请选择发送状态" clearable style="width: 120px;">-->
<!--            <el-option label="已发送邀请" :value="true" />-->
<!--            <el-option label="未发送邀请" :value="false" />-->
<!--          </el-select>-->
<!--        </el-form-item>-->
<!--        <el-form-item>-->
<!--          <el-button type="primary" @click="handleSearch">查询</el-button>-->
<!--          <el-button @click="handleReset">重置</el-button>-->
<!--        </el-form-item>-->
<!--      </el-form>-->
<!--    </div>-->

    <!-- 理事会列表展示区域 -->
    <div class="council-list">
      <el-row :gutter="20">
        <el-col v-for="meeting in meetingList" :key="meeting.id" :span="8">
          <el-card class="council-card" :body-style="{ padding: '0px' }">
            <div class="council-header">
              <h3>{{ meeting.name }}</h3>
              <el-tag v-if="meeting.invitation_sent" type="success">已发送邀请</el-tag>
              <el-tag v-else type="info">未发送邀请</el-tag>
            </div>
            <div class="council-info">
              <p><strong>召开地点：</strong>{{ meeting.location }}</p>
              <p><strong>召开时间：</strong>{{ formatDateTime(meeting.meeting_time) }}</p>
              <p class="council-content"><strong>内容：</strong>{{ meeting.content }}</p>
              <p><strong>邀请人员：</strong>{{ getInvitees(meeting) }}</p>
              <p><strong>召开人：</strong>{{ meeting.user_info?.name || meeting.user_info?.username || '未知' }}</p>
            </div>
            <div class="card-footer">
              <div class="button-group">
                <el-button type="primary" size="small" @click="handleViewDetails(meeting)">查看详情</el-button>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 分页 -->
    <div class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[9, 18, 36, 72]"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <!-- 详情对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="理事会详情"
      width="80%"
    >
      <div v-if="currentMeeting" class="meeting-details">
        <h2>{{ currentMeeting.name }}</h2>
        <el-descriptions :column="1" border>
          <el-descriptions-item label="理事会名称">{{ currentMeeting.name }}</el-descriptions-item>
          <el-descriptions-item label="召开地点">{{ currentMeeting.location }}</el-descriptions-item>
          <el-descriptions-item label="召开时间">{{ formatDateTime(currentMeeting.meeting_time) }}</el-descriptions-item>
          <el-descriptions-item label="内容">{{ currentMeeting.content }}</el-descriptions-item>
          <el-descriptions-item label="邀请状态">
            <el-tag v-if="currentMeeting.invitation_sent" type="success">已发送邀请</el-tag>
            <el-tag v-else type="info">未发送邀请</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="召开人">{{ currentMeeting.user_info?.name || currentMeeting.user_info?.username || '未知' }}</el-descriptions-item>
        </el-descriptions>

        <h3 class="members-title">成员信息表</h3>
        <el-table :data="membersList" style="width: 100%" border stripe height="400">
          <el-table-column label="职位" min-width="100" prop="position" />
          <el-table-column label="姓名" min-width="100" prop="name" />
          <el-table-column label="工号" min-width="100" prop="workId" />
          <el-table-column label="毕业学院" min-width="150" prop="department" />
          <el-table-column label="毕业时间" min-width="120" prop="graduationDate" />
          <el-table-column label="工作单位" min-width="180" prop="company" />
          <el-table-column label="电话" min-width="120" prop="phone" />
          <el-table-column label="备注" min-width="150" prop="remark" />
        </el-table>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import request from '@/utils/request'

export default {
  name: 'CouncilOverview',
  setup() {
    // 搜索表单
    const searchForm = ref({
      name: '',
      invitation_sent: ''
    })

    // 列表数据
    const meetingList = ref([])
    const loading = ref(false)
    const currentPage = ref(1)
    const pageSize = ref(9) // 默认一页显示9个卡片
    const total = ref(0)

    // 详情弹窗
    const dialogVisible = ref(false)
    const currentMeeting = ref(null)
    
    // 成员信息表示例数据
    const membersList = ref([
      {
        position: '理事长',
        name: '张三',
        workId: '20010001',
        department: '计算机科学与技术学院',
        graduationDate: '2005-07-01',
        company: '北京科技有限公司',
        phone: '13800138000',
        remark: '创始人'
      },
      {
        position: '副理事长',
        name: '李四',
        workId: '20020002',
        department: '电子信息工程学院',
        graduationDate: '2006-07-01',
        company: '上海电子科技有限公司',
        phone: '13900139000',
        remark: '技术总监'
      },
      {
        position: '秘书长',
        name: '王五',
        workId: '20030003',
        department: '管理学院',
        graduationDate: '2007-07-01',
        company: '广州企业管理有限公司',
        phone: '13700137000',
        remark: '企业高管'
      },
      {
        position: '理事',
        name: '赵六',
        workId: '20040004',
        department: '机械工程学院',
        graduationDate: '2008-07-01',
        company: '深圳机械制造有限公司',
        phone: '13600136000',
        remark: '工程师'
      },
      {
        position: '理事',
        name: '钱七',
        workId: '20050005',
        department: '经济学院',
        graduationDate: '2009-07-01',
        company: '杭州金融服务有限公司',
        phone: '13500135000',
        remark: '首席经济师'
      },
      {
        position: '理事',
        name: '孙八',
        workId: '20060006',
        department: '外国语学院',
        graduationDate: '2010-07-01',
        company: '南京国际贸易有限公司',
        phone: '13400134000',
        remark: '对外合作部主管'
      },
      {
        position: '理事',
        name: '周九',
        workId: '20070007',
        department: '艺术设计学院',
        graduationDate: '2011-07-01',
        company: '武汉创意设计工作室',
        phone: '13300133000',
        remark: '创意总监'
      },
      {
        position: '理事',
        name: '吴十',
        workId: '20080008',
        department: '材料科学与工程学院',
        graduationDate: '2012-07-01',
        company: '重庆新材料研发中心',
        phone: '13200132000',
        remark: '研发主管'
      }
    ])

    // 获取理事会列表
    const getMeetingList = async () => {
      loading.value = true
      try {
        const params = {
          page: currentPage.value,
          page_size: pageSize.value,
          name: searchForm.value.name
        }

        if (searchForm.value.invitation_sent !== '') {
          params.invitation_sent = searchForm.value.invitation_sent
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

    // 获取邀请人员名单
    const getInvitees = (meeting) => {
      if (!meeting.invitees_info || !meeting.invitees_info.length) return '无'
      return meeting.invitees_info.map(user => user.name || user.username).join(', ')
    }

    // 搜索和重置
    const handleSearch = () => {
      currentPage.value = 1
      getMeetingList()
    }

    const handleReset = () => {
      searchForm.value = {
        name: '',
        invitation_sent: ''
      }
      handleSearch()
    }

    // 查看详情
    const handleViewDetails = (meeting) => {
      currentMeeting.value = meeting
      dialogVisible.value = true
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
      dialogVisible,
      currentMeeting,
      membersList,
      handleSearch,
      handleReset,
      handleViewDetails,
      handleSizeChange,
      handleCurrentChange,
      formatDateTime,
      getInvitees
    }
  }
}
</script>

<style scoped>
.council-overview {
  padding: 20px;
}

.search-section {
  background: #fff;
  padding: 20px;
  border-radius: 4px;
  margin-bottom: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.council-list {
  margin-top: 20px;
}

.council-card {
  margin-bottom: 20px;
  transition: all 0.3s;
  background-color: #fff;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.council-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.council-header {
  padding: 15px;
  background-color: #f5f7fa;
  border-bottom: 1px solid #ebeef5;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.council-header h3 {
  margin: 0;
  font-size: 16px;
  color: #333;
  flex: 1;
}

.council-info {
  padding: 15px;
  flex: 1;
}

.council-info p {
  margin: 8px 0;
  font-size: 14px;
  color: #606266;
}

.council-content {
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.card-footer {
  display: flex;
  justify-content: flex-end;
  padding: 10px 15px;
  border-top: 1px solid #ebeef5;
  background-color: #f5f7fa;
}

.button-group {
  display: flex;
}

.button-group .el-button {
  margin-left: 8px;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}

.meeting-details {
  padding: 10px;
}

.meeting-details h2 {
  text-align: center;
  margin-bottom: 20px;
  color: #409EFF;
}

.members-title {
  margin: 20px 0 10px;
  font-size: 18px;
  font-weight: bold;
  color: #409EFF;
}

.invitees-title {
  margin: 20px 0 10px;
}
</style>