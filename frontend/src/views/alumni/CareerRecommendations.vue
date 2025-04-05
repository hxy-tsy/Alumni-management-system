<template>
  <div class="career-recommendations">
    <div class="page-header">
      <h2>毕业去向推荐</h2>
    </div>

    <el-row :gutter="20">
      <!-- 数据图表区域 -->
      <el-col :span="24">
        <el-card class="chart-card" v-loading="chartLoading">
          <div class="chart-header">
            <div class="title">毕业去向分析</div>
            <div class="chart-filters">
              <span class="filter-label">毕业年份：</span>
              <el-select v-model="selectedYear" placeholder="选择年份"  style="width: 100px" @change="fetchChartData">
                <el-option v-for="year in availableYears" :key="year" :label="year + '年'" :value="year" />
              </el-select>
            </div>
          </div>
          <div class="chart-container">
            <el-row :gutter="20">
              <el-col :span="12">
                <div class="chart-title">相同MBTI校友毕业去向分布</div>
                <div id="mbtiChart" class="chart"></div>
                <div v-if="userInfo.mbti" class="chart-info">
                  您的MBTI类型：{{ userInfo.mbti }}
                </div>
              </el-col>
              <el-col :span="12">
                <div class="chart-title">相同学院校友毕业去向分布</div>
                <div id="departmentChart" class="chart"></div>
                <div class="chart-info">
                  您所在的学院：{{ userInfo.department || '未知' }}
                </div>
              </el-col>
            </el-row>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 推荐生成区域 -->
    <el-row :gutter="20" class="recommendation-section">
      <el-col :span="24">
        <el-card>
          <div class="recommendation-header">
            <h3>毕业去向智能推荐</h3>
            <el-button type="primary" @click="generateRecommendation" :loading="loading">
              一键生成推荐
            </el-button>
          </div>
          
          <div v-if="recommendation" class="recommendation-content">
            <el-alert
              :title="recommendation.title"
              type="success"
              :description="recommendation.description"
              show-icon
              :closable="false"
            >
            </el-alert>
            
            <div class="recommendation-details">
              <h4>详细推荐</h4>
              <p><strong>推荐方向：</strong>{{ recommendation.direction }}</p>
              <p><strong>适合职位：</strong>{{ recommendation.position }}</p>
              <p><strong>匹配原因：</strong>{{ recommendation.reason }}</p>
              <p><strong>推荐企业/机构：</strong>{{ recommendation.companies.join('、') }}</p>
              <p><strong>建议准备：</strong>{{ recommendation.preparation }}</p>
            </div>
          </div>
          
          <div v-else class="recommendation-placeholder">
            <el-empty description="点击上方按钮生成个性化推荐"></el-empty>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 详情对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="推荐详情"
      width="50%"
    >
      <div class="dialog-content" v-if="dialogContent">
        <h3>{{ dialogContent.title }}</h3>
        <p v-for="(item, index) in dialogContent.details" :key="index" class="detail-item">
          <strong>{{ item.label }}：</strong>{{ item.value }}
        </p>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted, reactive, computed, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import request from '@/utils/request'

export default {
  name: 'CareerRecommendations',
  setup() {
    const mbtiChart = ref(null)
    const departmentChart = ref(null)
    const loading = ref(false)
    const chartLoading = ref(false)
    const recommendation = ref(null)
    const dialogVisible = ref(false)
    const dialogContent = ref(null)
    const selectedYear = ref(new Date().getFullYear())

    // 可选年份列表（当前年份及前4年）
    const currentYear = new Date().getFullYear()
    const availableYears = [
      currentYear,
      currentYear - 1,
      currentYear - 2,
      currentYear - 3,
      currentYear - 4
    ]

    // 用户信息
    const userInfo = reactive({
      mbti: '',
      department: ''
    })
    
    // 图表数据
    const mbtiData = ref([])
    const departmentData = ref([])
    
    // 获取图表数据
    const fetchChartData = async () => {
      chartLoading.value = true;
      
      try {
        // 保留/api前缀
        const response = await request({
          url: '/api/alumni/career-recommendation-data/',
          method: 'get',
          params: {
            year: selectedYear.value
          }
        });
        
        console.log('API响应数据(原始):', response);
        
        // 检查response的格式，增加调试代码
        if (response && typeof response === 'object') {
          console.log('API响应格式正确');
          
          // 打印具体字段检查
          console.log('mbti_data存在:', response.data.hasOwnProperty('mbti_data'));
          console.log('department_data存在:', response.data.hasOwnProperty('department_data'));
          console.log('user_mbti存在:', response.data.hasOwnProperty('user_mbti'));
          console.log('user_department存在:', response.data.hasOwnProperty('user_department'));
          
          // 确保从API响应中获取相关数据
          if (Array.isArray(response.data.mbti_data)) {
            mbtiData.value = response.data.mbti_data;
          } else {
            console.warn('mbti_data不是数组或不存在:', response.data.mbti_data);
            mbtiData.value = [];
          }
          
          if (Array.isArray(response.data.department_data)) {
            departmentData.value = response.data.department_data;
          } else {
            console.warn('department_data不是数组或不存在:', response.data.department_data);
            departmentData.value = [];
          }
          
          // 保存用户的MBTI和学院信息
          userInfo.mbti = response.data.user_mbti || '未指定';
          userInfo.department = response.data.user_department || '未指定';
        } else {
          console.error('API响应格式不正确:', response);
          ElMessage.warning('API返回数据格式不正确');
          mbtiData.value = [];
          departmentData.value = [];
        }
        
        console.log('处理后的MBTI数据:', mbtiData.value);
        console.log('处理后的学院数据:', departmentData.value);
        console.log('用户MBTI:', userInfo.mbti);
        console.log('用户学院:', userInfo.department);
        
        // 延迟确保图表已初始化
        setTimeout(() => {
          // 更新图表
          updateCharts();
        }, 100);
      } catch (error) {
        console.error('获取数据出错:', error);
        ElMessage.error('获取数据失败，请稍后重试');
        // 清空数据
        mbtiData.value = [];
        departmentData.value = [];
        updateCharts();
      }
      
      chartLoading.value = false;
    }
    
    // 初始化图表
    const initCharts = () => {
      console.log('开始初始化图表');
      
      // 增加延时确保DOM已完全渲染
      setTimeout(() => {
        // 初始化MBTI图表
        const mbtiChartElement = document.getElementById('mbtiChart');
        if (mbtiChartElement) {
          try {
            // 检查元素尺寸
            console.log('MBTI图表元素尺寸:', mbtiChartElement.offsetWidth, mbtiChartElement.offsetHeight);
            if (mbtiChartElement.offsetWidth > 0 && mbtiChartElement.offsetHeight > 0) {
              // 如果已经有图表实例，先销毁
              if (mbtiChart.value) {
                mbtiChart.value.dispose();
              }
              
              // 初始化图表
              mbtiChart.value = echarts.init(mbtiChartElement);
              console.log('MBTI图表初始化完成');
            } else {
              console.error('MBTI图表DOM元素尺寸为0，无法初始化');
              setTimeout(() => initCharts(), 300); // 再次尝试初始化
              return;
            }
          } catch (error) {
            console.error('初始化MBTI图表时出错:', error);
          }
        } else {
          console.error('未找到MBTI图表DOM元素');
        }
        
        // 初始化学院图表
        const departmentChartElement = document.getElementById('departmentChart');
        if (departmentChartElement) {
          try {
            // 检查元素尺寸
            console.log('学院图表元素尺寸:', departmentChartElement.offsetWidth, departmentChartElement.offsetHeight);
            if (departmentChartElement.offsetWidth > 0 && departmentChartElement.offsetHeight > 0) {
              // 如果已经有图表实例，先销毁
              if (departmentChart.value) {
                departmentChart.value.dispose();
              }
              
              // 初始化图表
              departmentChart.value = echarts.init(departmentChartElement);
              console.log('学院图表初始化完成');
            } else {
              console.error('学院图表DOM元素尺寸为0，无法初始化');
              setTimeout(() => initCharts(), 300); // 再次尝试初始化
              return;
            }
          } catch (error) {
            console.error('初始化学院图表时出错:', error);
          }
        } else {
          console.error('未找到学院图表DOM元素');
        }
        
        // 初始化完成后更新图表
        if (mbtiChart.value && departmentChart.value) {
          console.log('图表已初始化，开始更新数据');
          updateCharts();
        } else {
          console.warn('部分图表初始化失败，将在数据加载后再次尝试');
        }
      }, 500); // 增加延时确保DOM已渲染
    }

    // 更新MBTI图表
    const updateMbtiChart = () => {
      if (!mbtiChart.value) {
        console.warn('MBTI图表未初始化');
        return;
      }

      console.log('更新MBTI图表，数据：', mbtiData.value);
      
      // 检查数据是否为空
      if (!mbtiData.value || mbtiData.value.length === 0) {
        console.log('MBTI数据为空，显示暂无数据');
        // 显示无数据的图表
        mbtiChart.value.setOption({
          title: {
            text: '按MBTI类型的毕业去向分布',
            left: 'center'
          },
          tooltip: {
            trigger: 'item'
          },
          legend: {
            orient: 'vertical',
            left: 'left',
            top: 'middle'
          },
          series: [
            {
              name: '暂无数据',
              type: 'pie',
              radius: '60%',
              data: [{ name: '暂无数据', value: 100 }],
              emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
              },
              label: {
                formatter: '暂无数据'
              }
            }
          ]
        });
        return;
      }

      // 检查数据格式并转换
      try {
        // 确保每个数据项都有name和value字段
        const formattedData = mbtiData.value.map(item => {
          // 检查数据项格式
          if (typeof item !== 'object') {
            console.error('无效的数据项:', item);
            return { name: '错误数据', value: 0 };
          }
          
          // 确保有name字段
          const name = item.name || '未命名';
          
          // 确保value字段为数字
          let value = item.value;
          if (typeof value !== 'number') {
            value = parseFloat(value) || 0;
          }
          
          return { name, value };
        });
        
        console.log('格式化后的MBTI数据:', formattedData);
        
        // 正常显示数据
        mbtiChart.value.setOption({
          title: {
            text: '按MBTI类型的毕业去向分布',
            left: 'center'
          },
          tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b}: {c} ({d}%)'
          },
          legend: {
            orient: 'vertical',
            left: 'left',
            top: 'middle',
            data: formattedData.map(item => item.name)
          },
          series: [
            {
              name: '毕业去向',
              type: 'pie',
              radius: '60%',
              data: formattedData,
              emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
              },
              label: {
                formatter: '{b}: {d}%'
              }
            }
          ]
        });
        console.log('MBTI图表更新完成');
      } catch (error) {
        console.error('更新MBTI图表时出错:', error);
        // 错误时显示错误提示
        mbtiChart.value.setOption({
          title: {
            text: '数据处理错误',
            left: 'center'
          },
          series: [
            {
              type: 'pie',
              data: [{ name: '错误', value: 100 }]
            }
          ]
        });
      }
    }

    // 更新学院图表
    const updateDepartmentChart = () => {
      if (!departmentChart.value) {
        console.warn('学院图表未初始化');
        return;
      }

      console.log('更新学院图表，数据：', departmentData.value);
      
      // 检查数据是否为空
      if (!departmentData.value || departmentData.value.length === 0) {
        console.log('学院数据为空，显示暂无数据');
        // 显示无数据的图表
        departmentChart.value.setOption({
          title: {
            text: '按学院的毕业去向分布',
            left: 'center'
          },
          tooltip: {
            trigger: 'item'
          },
          legend: {
            orient: 'vertical',
            left: 'left',
            top: 'middle'
          },
          series: [
            {
              name: '暂无数据',
              type: 'pie',
              radius: '60%',
              data: [{ name: '暂无数据', value: 100 }],
              emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
              },
              label: {
                formatter: '暂无数据'
              }
            }
          ]
        });
        return;
      }

      // 检查数据格式并转换
      try {
        // 确保每个数据项都有name和value字段
        const formattedData = departmentData.value.map(item => {
          // 检查数据项格式
          if (typeof item !== 'object') {
            console.error('无效的数据项:', item);
            return { name: '错误数据', value: 0 };
          }
          
          // 确保有name字段
          const name = item.name || '未命名';
          
          // 确保value字段为数字
          let value = item.value;
          if (typeof value !== 'number') {
            value = parseFloat(value) || 0;
          }
          
          return { name, value };
        });
        
        console.log('格式化后的学院数据:', formattedData);
        
        // 正常显示数据
        departmentChart.value.setOption({
          title: {
            text: '按学院的毕业去向分布',
            left: 'center'
          },
          tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b}: {c} ({d}%)'
          },
          legend: {
            orient: 'vertical',
            left: 'left',
            top: 'middle',
            data: formattedData.map(item => item.name)
          },
          series: [
            {
              name: '毕业去向',
              type: 'pie',
              radius: '60%',
              data: formattedData,
              emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
              },
              label: {
                formatter: '{b}: {d}%'
              }
            }
          ]
        });
        console.log('学院图表更新完成');
      } catch (error) {
        console.error('更新学院图表时出错:', error);
        // 错误时显示错误提示
        departmentChart.value.setOption({
          title: {
            text: '数据处理错误',
            left: 'center'
          },
          series: [
            {
              type: 'pie',
              data: [{ name: '错误', value: 100 }]
            }
          ]
        });
      }
    }

    // 更新图表
    const updateCharts = () => {
      console.log('开始更新图表');
      
      try {
        updateMbtiChart();
      } catch (error) {
        console.error('更新MBTI图表失败:', error);
      }
      
      try {
        updateDepartmentChart();
      } catch (error) {
        console.error('更新学院图表失败:', error);
      }
      
      console.log('图表更新完成');
    }
    
    // 窗口大小改变时重置图表
    const resizeCharts = () => {
      window.addEventListener('resize', () => {
        mbtiChart.value?.resize()
        departmentChart.value?.resize()
      })
    }
    
    // 生成推荐
    const generateRecommendation = () => {
      loading.value = true;
      
      // 模拟API请求延迟
      setTimeout(() => {
        // 随机生成推荐数据，不依赖数据库
        
        // 随机选择的去向列表
        const destinations = [
          '互联网企业', '国有企业', '事业单位', '高校教师', '公务员', 
          '研究所', '银行', '保险公司', '外企', '医疗机构', 
          '创业', '读研深造', '出国留学', '自由职业', '咨询公司'
        ];
        
        // 随机选择的职位列表
        const positions = [
          '软件工程师', '数据分析师', '产品经理', '运营专员', '行政管理',
          '研究员', '讲师', '客户经理', '市场专员', '财务分析师',
          '投资顾问', '咨询顾问', '人力资源专员', '销售经理', '技术支持'
        ];
        
        // 随机选择企业
        const companies = [
          ['腾讯', '阿里巴巴', '百度', '字节跳动', '华为'],
          ['中国银行', '工商银行', '建设银行', '农业银行', '招商银行'],
          ['中国移动', '中国电信', '中国联通', '国家电网', '中国石油'],
          ['清华大学', '北京大学', '浙江大学', '复旦大学', '南京大学'],
          ['中央部委', '省级机关', '市级机关', '区县级机关']
        ];
        
        // 随机选择一个去向和相关数据
        const destinationIndex = Math.floor(Math.random() * destinations.length);
        const destination = destinations[destinationIndex];
        const position = positions[Math.floor(Math.random() * positions.length)];
        const companyGroup = companies[Math.min(Math.floor(destinationIndex / 3), companies.length - 1)];
        
        // 随机生成推荐理由
        const mbtiReasons = [
          `您的MBTI类型(${userInfo.mbti || '未知'})具有很强的分析能力和逻辑思维`,
          `您的MBTI类型(${userInfo.mbti || '未知'})显示您善于沟通和团队协作`,
          `您的MBTI类型(${userInfo.mbti || '未知'})表明您有很强的创新思维`,
          `您的MBTI类型(${userInfo.mbti || '未知'})适合需要细致和耐心的工作`,
          `您的MBTI类型(${userInfo.mbti || '未知'})显示您有较强的领导能力`
        ];
        
        const deptReasons = [
          `您所在的${userInfo.department || '未知'}学院培养了扎实的专业基础`,
          `您所在的${userInfo.department || '未知'}学院的毕业生在该领域有很好的发展前景`,
          `您所在的${userInfo.department || '未知'}学院的课程设置与该职业方向高度相关`,
          `${userInfo.department || '未知'}学院的学生在这个领域有很强的竞争力`,
          `${userInfo.department || '未知'}学院与该行业有紧密的合作关系`
        ];
        
        // 构建推荐
        const recommendationData = {
          title: `推荐去向：${destination}`,
          description: `基于您的个人特点和专业背景，我们推荐您考虑${destination}作为毕业去向。`,
          direction: destination,
          position: position,
          reason: `${mbtiReasons[Math.floor(Math.random() * mbtiReasons.length)]}。${deptReasons[Math.floor(Math.random() * deptReasons.length)]}。综合分析，${destination}可能是您不错的选择。`,
          companies: companyGroup.sort(() => Math.random() - 0.5).slice(0, 3),
          preparation: `建议您积极参加校园招聘，提前了解${destination}的招聘要求，准备相关面试材料，并加强专业技能的学习和实践经验的积累。`
        };
        
        recommendation.value = recommendationData;
        loading.value = false;
      }, 1500);
    }
    
    // 查看详情
    const showDetails = (item) => {
      dialogContent.value = item
      dialogVisible.value = true
    }
    
    onMounted(() => {
      console.log('组件挂载完成');
      
      // 使用nextTick确保DOM已经渲染
      nextTick(() => {
        console.log('DOM已渲染，开始初始化图表');
        initCharts();
        
        // 设置窗口大小改变事件
        resizeCharts();
        
        // 初始化图表后再获取数据
        console.log('开始获取图表数据');
        fetchChartData();
      });
    })
    
    return {
      loading,
      chartLoading,
      recommendation,
      dialogVisible,
      dialogContent,
      selectedYear,
      availableYears,
      userInfo,
      mbtiData,
      departmentData,
      generateRecommendation,
      fetchChartData,
      updateCharts,
      showDetails
    }
  }
}
</script>

<style scoped>
.career-recommendations {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  color: #303133;
}

.chart-card {
  margin-bottom: 20px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px 10px;
  border-bottom: 1px solid #ebeef5;
}

.chart-header .title {
  font-size: 16px;
  font-weight: bold;
  color: #303133;
}

.chart-filters {
  display: flex;
  align-items: center;
}

.filter-label {
  margin-right: 10px;
  color: #606266;
}

.chart-container {
  width: 100%;
  padding: 20px 10px 10px;
}

.chart {
  height: 400px;
  width: 100%;
}

.chart-title {
  text-align: center;
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 10px;
  color: #303133;
}

.chart-info {
  text-align: center;
  color: #606266;
  font-size: 14px;
  margin-top: 10px;
}

.chart-info.warning {
  color: #E6A23C;
}

.recommendation-section {
  margin-top: 20px;
}

.recommendation-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.recommendation-header h3 {
  margin: 0;
  color: #303133;
}

.recommendation-content {
  margin-top: 20px;
}

.recommendation-details {
  margin-top: 20px;
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.recommendation-details h4 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #303133;
}

.recommendation-details p {
  margin: 10px 0;
  line-height: 1.6;
}

.recommendation-placeholder {
  margin: 40px 0;
  text-align: center;
}

.dialog-content {
  padding: 20px;
}

.dialog-content h3 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #303133;
}

.detail-item {
  margin: 12px 0;
  line-height: 1.6;
}

.detail-item strong {
  color: #606266;
}
</style> 