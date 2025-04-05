<template>
  <div class="activity-planning">
    <!-- 页面标题 -->
    <div class="page-header">
      <h2>活动策划推荐</h2>
      <p class="subtitle">基于历史数据分析，为您提供最优活动策划建议</p>
    </div>

    <!-- 数据概览卡片 -->
    <el-row :gutter="20" class="stat-cards">
      <el-col :span="8">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-info">
            <div class="stat-number">{{ totalActivities }}</div>
            <div class="stat-label">历史活动总数</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-info">
            <div class="stat-number">{{ avgParticipants }}</div>
            <div class="stat-label">平均参与人数</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-info">
            <div class="stat-number">{{ avgRating.toFixed(1) }}</div>
            <div class="stat-label">平均好评度</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <div class="charts-container">
      <el-row :gutter="20">
        <!-- 活动举办时间分布 -->
        <el-col :span="24">
          <el-card class="chart-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <span>活动举办时间分布</span>
                <el-tooltip content="展示各月份活动举办频率，帮助选择最佳活动时间">
                  <el-icon><QuestionFilled /></el-icon>
                </el-tooltip>
              </div>
            </template>
            <div class="chart" ref="timeChart"></div>
          </el-card>
        </el-col>

        <!-- 活动参与人数分析 -->
        <el-col :span="12">
          <el-card class="chart-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <span>活动参与人数分析</span>
                <el-tooltip content="展示不同类型活动的参与人数分布">
                  <el-icon><QuestionFilled /></el-icon>
                </el-tooltip>
              </div>
            </template>
            <div class="chart" ref="participantsChart"></div>
          </el-card>
        </el-col>

        <!-- 活动好评度分析 -->
        <el-col :span="12">
          <el-card class="chart-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <span>活动好评度分析</span>
                <el-tooltip content="展示不同类型活动的好评度分布">
                  <el-icon><QuestionFilled /></el-icon>
                </el-tooltip>
              </div>
            </template>
            <div class="chart" ref="ratingChart"></div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 推荐建议 -->
    <el-card class="recommendation-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span>活动策划建议</span>
        </div>
      </template>
      <div class="recommendations">
        <div v-for="(item, index) in recommendations" :key="index" class="recommendation-item">
          <el-icon><Star /></el-icon>
          <span>{{ item }}</span>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import { QuestionFilled, Star } from '@element-plus/icons-vue'
import request from '@/utils/request'

export default {
  name: 'ActivityPlanning',
  components: {
    QuestionFilled,
    Star
  },
  setup() {
    // 基础数据
    const totalActivities = ref(0)
    const avgParticipants = ref(0)
    const avgRating = ref(4.5) // 设置一个默认值
    
    // 图表引用
    const timeChart = ref(null)
    const participantsChart = ref(null)
    const ratingChart = ref(null)
    let charts = {}

    // 推荐建议
    const recommendations = ref([])

    // 初始化图表
    const initCharts = () => {
      // 确保DOM元素已经渲染
      if (!timeChart.value || !participantsChart.value || !ratingChart.value) {
        console.error('图表容器未找到')
        return
      }

      // 活动参与人数分析图表
      const participantsChartInstance = echarts.init(participantsChart.value)
      participantsChartInstance.setOption({
        title: {
          text: '活动参与情况',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '10%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: [],
          axisLabel: {
            interval: 0,
            rotate: 30
          }
        },
        yAxis: {
          type: 'value',
          name: '参与人数',
          minInterval: 1
        },
        series: [{
          name: '参与人数',
          type: 'bar',
          data: [],
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#ff9a9e' },
              { offset: 1, color: '#fad0c4' }
            ])
          }
        }]
      })

      // 活动好评度分析图表
      const ratingChartInstance = echarts.init(ratingChart.value)
      ratingChartInstance.setOption({
        title: {
          text: '活动好评度分析',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '10%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: [],
          axisLabel: {
            interval: 0,
            rotate: 30
          }
        },
        yAxis: {
          type: 'value',
          name: '好评度',
          min: 0,
          max: 5,
          interval: 1
        },
        series: [{
          name: '好评度',
          type: 'bar',
          data: [],
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#81FFEF' },
              { offset: 1, color: '#F067B4' }
            ])
          }
        }]
      })

      // 活动举办时间分布图表
      const timeChartInstance = echarts.init(timeChart.value)
      timeChartInstance.setOption({
        title: {
          text: '月度活动分布',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
        },
        yAxis: {
          type: 'value',
          name: '活动数量',
          minInterval: 1
        },
        series: [{
          name: '活动数量',
          type: 'bar',
          data: new Array(12).fill(0),
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#83bff6' },
              { offset: 0.5, color: '#188df0' },
              { offset: 1, color: '#188df0' }
            ])
          }
        }]
      })

      charts = {
        timeChart: timeChartInstance,
        participantsChart: participantsChartInstance,
        ratingChart: ratingChartInstance
      }

      // 添加窗口大小变化监听
      window.addEventListener('resize', handleResize)
    }

    // 获取数据
    const fetchData = async () => {
      try {
        const response = await request.get('/api/activities/planning/stats/')
        const data = response.data
        
        // 更新基础数据
        totalActivities.value = data.total_activities
        avgParticipants.value = data.avg_participants
        
        // 更新推荐建议
        recommendations.value = data.recommendations

        // 提取活动统计数据
        const activityNames = data.activity_stats.map(stat => stat.name)
        const participantCounts = data.activity_stats.map(stat => stat.participants)
        const ratings = data.activity_stats.map(stat => stat.rating)

        // 更新活动参与情况图表
        if (charts.participantsChart) {
          charts.participantsChart.setOption({
            xAxis: {
              data: activityNames
            },
            series: [{
              data: participantCounts
            }]
          })
        }

        // 更新活动好评度图表
        if (charts.ratingChart) {
          charts.ratingChart.setOption({
            xAxis: {
              data: activityNames
            },
            series: [{
              data: ratings
            }]
          })
        }

        // 更新月度活动分布图表
        if (charts.timeChart) {
          charts.timeChart.setOption({
            series: [{
              data: data.monthly_stats
            }]
          })
        }
      } catch (error) {
        console.error('获取活动策划数据失败:', error)
      }
    }

    // 窗口大小变化时重绘图表
    const handleResize = () => {
      Object.values(charts).forEach(chart => {
        if (chart) {
          chart.resize()
        }
      })
    }

    onMounted(() => {
      // 使用nextTick确保DOM已经渲染
      nextTick(() => {
        initCharts()
        fetchData()
      })
    })

    onUnmounted(() => {
      window.removeEventListener('resize', handleResize)
      Object.values(charts).forEach(chart => {
        if (chart) {
          chart.dispose()
        }
      })
    })

    return {
      totalActivities,
      avgParticipants,
      avgRating,
      timeChart,
      participantsChart,
      ratingChart,
      recommendations
    }
  }
}
</script>

<style scoped>
.activity-planning {
  padding: 20px;
}

.page-header {
  margin-bottom: 24px;
  text-align: center;
}

.page-header h2 {
  margin: 0;
  font-size: 24px;
  color: #303133;
}

.subtitle {
  margin: 8px 0 0;
  font-size: 14px;
  color: #909399;
}

.stat-cards {
  margin-bottom: 24px;
}

.stat-card {
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-info {
  text-align: center;
}

.stat-number {
  font-size: 28px;
  font-weight: bold;
  color: #409EFF;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #606266;
}

.charts-container {
  margin-bottom: 24px;
}

.chart-card {
  margin-bottom: 20px;
  transition: all 0.3s;
}

.chart-card:hover {
  transform: translateY(-5px);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.card-header span {
  font-size: 16px;
  font-weight: 500;
}

.chart {
  height: 400px;
  padding: 20px;
}

.recommendation-card {
  margin-bottom: 24px;
}

.recommendations {
  padding: 0 20px;
}

.recommendation-item {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
  font-size: 14px;
  color: #606266;
}

.recommendation-item .el-icon {
  margin-right: 8px;
  color: #E6A23C;
}

.el-tooltip__trigger {
  cursor: help;
}
</style> 