<template>
  <div class="alumni-statistics">
    <!-- 基本信息统计卡片组 -->
    <div class="stat-cards">
      <el-row :gutter="20">
        <el-col :span="8">
          <el-card class="stat-card" shadow="hover">
            <div class="stat-info">
              <div class="stat-number">{{ statistics.total_count }}</div>
              <div class="stat-label">总校友数</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card class="stat-card" shadow="hover">
            <div class="stat-info">
              <div class="stat-number">{{ statistics.male_count }}</div>
              <div class="stat-label">男生人数</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card class="stat-card" shadow="hover">
            <div class="stat-info">
              <div class="stat-number">{{ statistics.female_count }}</div>
              <div class="stat-label">女生人数</div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 图表展示区域 -->
    <div class="charts-container">
      <el-row :gutter="20">
        <!-- 左侧图表 -->
        <el-col :span="12">
          <!-- 院系分布 -->
          <el-card class="chart-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <span>院系分布</span>
              </div>
            </template>
            <div class="chart" ref="departmentChart"></div>
          </el-card>

          <!-- 就业去向分布 -->
          <el-card class="chart-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <span>就业去向分布</span>
              </div>
            </template>
            <div class="chart" ref="industryChart"></div>
          </el-card>
        </el-col>

        <!-- 右侧图表 -->
        <el-col :span="12">
          <!-- 毕业年份分布 -->
          <el-card class="chart-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <span>毕业年份分布</span>
              </div>
            </template>
            <div class="chart" ref="graduationYearChart"></div>
          </el-card>

          <!-- 分会分布情况 -->
          <el-card class="chart-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <span>分会分布情况</span>
              </div>
            </template>
            <div class="chart" ref="regionChart"></div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import request from '@/utils/request'
// 导入中国地图数据
import chinaJson from '@/assets/china.json'

export default {
  name: 'AlumniStatistics',
  setup() {
    const statistics = ref({
      total_count: 0,
      male_count: 0,
      female_count: 0
    })
    
    // 图表引用
    const departmentChart = ref(null)
    const graduationYearChart = ref(null)
    const regionChart = ref(null)
    const industryChart = ref(null)

    let charts = {}  // 存储图表实例

    // 初始化图表
    const initCharts = () => {
      // 统一的柱状图配置
      const barChartOption = {
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
          data: [],
          axisLabel: {
            interval: 0,
            rotate: 45
          }
        },
        yAxis: {
          type: 'value'
        },
        series: [{
          type: 'bar',
          data: [],
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#83bff6' },
              { offset: 0.5, color: '#188df0' },
              { offset: 1, color: '#188df0' }
            ])
          },
          emphasis: {
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: '#2378f7' },
                { offset: 0.7, color: '#2378f7' },
                { offset: 1, color: '#83bff6' }
              ])
            }
          }
        }]
      }

      // 院系分布柱状图
      const deptChart = echarts.init(departmentChart.value)
      deptChart.setOption({
        ...barChartOption,
        title: {
          text: '院系分布',
          left: 'center'
        }
      })

      // 毕业年份柱状图
      const yearChart = echarts.init(graduationYearChart.value)
      yearChart.setOption({
        ...barChartOption,
        title: {
          text: '毕业年份分布',
          left: 'center'
        }
      })

      // 分会分布饼图
      const regChart = echarts.init(regionChart.value)
      regChart.setOption({
        title: {
          text: '分会分布情况',
          left: 'center'
        },
        tooltip: {
          trigger: 'item',
          formatter: '{b}: {c} ({d}%)'
        },
        legend: {
          orient: 'vertical',
          left: 'left',
          top: 'middle'
        },
        series: [{
          name: '分会类型',
          type: 'pie',
          radius: ['40%', '70%'],
          avoidLabelOverlap: false,
          itemStyle: {
            borderRadius: 10,
            borderColor: '#fff',
            borderWidth: 2
          },
          label: {
            show: false
          },
          emphasis: {
            label: {
              show: true,
              fontSize: '16',
              fontWeight: 'bold'
            }
          },
          labelLine: {
            show: false
          },
          data: []
        }]
      })

      // 就业去向柱状图
      const indChart = echarts.init(industryChart.value)
      indChart.setOption({
        ...barChartOption,
        title: {
          text: '就业去向分布',
          left: 'center'
        }
      })

      charts = {
        deptChart,
        yearChart,
        regChart,
        indChart
      }

      return charts
    }

    // 获取统计数据
    const getStatistics = async () => {
      try {
        const response = await request.get('/api/alumni/statistics/')
        statistics.value = response.data

        // 院系分布
        charts.deptChart.setOption({
          xAxis: {
            data: response.data.department_stats.map(item => item.department)
          },
          series: [{
            data: response.data.department_stats.map(item => item.count)
          }]
        })

        // 毕业年份分布
        charts.yearChart.setOption({
          xAxis: {
            data: response.data.graduation_year_stats.map(item => item.year)
          },
          series: [{
            data: response.data.graduation_year_stats.map(item => item.count)
          }]
        })

        // 分会分布
        charts.regChart.setOption({
          series: [{
            data: response.data.association_stats.map(item => ({
              name: item.name,
              value: item.value
            }))
          }]
        })

        // 就业去向分布
        charts.indChart.setOption({
          xAxis: {
            data: response.data.industry_stats.map(item => item.name)
          },
          series: [{
            data: response.data.industry_stats.map(item => item.value)
          }]
        })
      } catch (error) {
        console.error('获取统计数据失败:', error)
      }
    }

    // 窗口大小变化时重绘图表
    const handleResize = () => {
      Object.values(charts).forEach(chart => chart.resize())
    }

    onMounted(() => {
      charts = initCharts()
      getStatistics()
      window.addEventListener('resize', handleResize)
    })

    onUnmounted(() => {
      window.removeEventListener('resize', handleResize)
      Object.values(charts).forEach(chart => chart.dispose())
    })

    return {
      statistics,
      departmentChart,
      graduationYearChart,
      regionChart,
      industryChart
    }
  }
}
</script>

<style scoped>
.alumni-statistics {
  padding: 20px;
}

.stat-cards {
  margin-bottom: 20px;
}

.stat-card {
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  transition: all 0.3s;
  background-color: #fff;
  border-radius: 8px;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-info {
  text-align: center;
  width: 100%;
}

.stat-number {
  font-size: 28px;
  font-weight: bold;
  color: #409EFF;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 16px;
  color: #606266;
}

.charts-container {
  margin-top: 20px;
}

.chart-card {
  margin-bottom: 20px;
  transition: all 0.3s;
  background-color: #fff;
  border-radius: 8px;
}

.chart-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #ebeef5;
}

.card-header span {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.chart {
  height: 400px;
  padding: 20px;
}
</style> 