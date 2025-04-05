<!--<template>-->
<!--  <div class="alumni-list">-->
<!--    &lt;!&ndash; 搜索栏 &ndash;&gt;-->
<!--    <div class="search-bar">-->
<!--      <el-form :inline="true" :model="searchForm">-->
<!--        <el-form-item label="学号">-->
<!--          <el-input v-model="searchForm.student_id" placeholder="请输入学号"></el-input>-->
<!--        </el-form-item>-->
<!--        <el-form-item label="姓名">-->
<!--          <el-input v-model="searchForm.name" placeholder="请输入姓名"></el-input>-->
<!--        </el-form-item>-->
<!--        <el-form-item label="学院">-->
<!--          <el-input v-model="searchForm.department" placeholder="请输入学院"></el-input>-->
<!--        </el-form-item>-->
<!--        <el-form-item>-->
<!--          <el-button type="primary" @click="handleSearch">查询</el-button>-->
<!--          <el-button @click="resetSearch">重置</el-button>-->
<!--        </el-form-item>-->
<!--      </el-form>-->
<!--    </div>-->

<!--    &lt;!&ndash; 工具栏 &ndash;&gt;-->
<!--    <div class="toolbar">-->
<!--      <el-button type="primary" @click="handleAdd">新增</el-button>-->
<!--      <el-button type="success" @click="handleImport">导入</el-button>-->
<!--      <el-button type="warning" @click="handleExport">导出</el-button>-->
<!--    </div>-->

<!--    &lt;!&ndash; 数据表格 &ndash;&gt;-->
<!--    <el-table :data="alumniList" border style="width: 100%">-->
<!--      <el-table-column prop="student_id" label="学号" width="120"></el-table-column>-->
<!--      <el-table-column prop="user.username" label="姓名" width="120"></el-table-column>-->
<!--      <el-table-column prop="user.phone" label="电话" width="120"></el-table-column>-->
<!--      <el-table-column prop="birth_date" label="出生日期" width="120"></el-table-column>-->
<!--      <el-table-column prop="user.department" label="学院"></el-table-column>-->
<!--      <el-table-column prop="graduation_date" label="毕业日期" width="120"></el-table-column>-->
<!--      <el-table-column prop="current_company" label="就业去向"></el-table-column>-->
<!--      <el-table-column label="操作" width="150">-->
<!--        <template #default="scope">-->
<!--          <el-button type="primary" size="small" @click="handleEdit(scope.row)">编辑</el-button>-->
<!--          <el-button type="danger" size="small" @click="handleDelete(scope.row)">删除</el-button>-->
<!--        </template>-->
<!--      </el-table-column>-->
<!--    </el-table>-->

<!--    &lt;!&ndash; 分页 &ndash;&gt;-->
<!--    <div class="pagination">-->
<!--      <el-pagination-->
<!--        :current-page="currentPage"-->
<!--        :page-size="pageSize"-->
<!--        :total="total"-->
<!--        layout="total, prev, pager, next"-->
<!--        @current-change="handlePageChange"-->
<!--      ></el-pagination>-->
<!--    </div>-->
<!--  </div>-->
<!--</template>-->

<!--<script>-->
<!--import { ref, onMounted } from 'vue'-->
<!--import request from '@/utils/request'-->

<!--export default {-->
<!--  name: 'AlumniList',-->
<!--  setup() {-->
<!--    const alumniList = ref([])-->
<!--    const currentPage = ref(1)-->
<!--    const pageSize = ref(10)-->
<!--    const total = ref(0)-->
<!--    const searchForm = ref({-->
<!--      student_id: '',-->
<!--      name: '',-->
<!--      department: ''-->
<!--    })-->

<!--    // 获取校友列表-->
<!--    const getAlumniList = async () => {-->
<!--      try {-->
<!--        const response = await request.get('/alumni/', {-->
<!--          params: {-->
<!--            page: currentPage.value,-->
<!--            ...searchForm.value-->
<!--          }-->
<!--        })-->
<!--        alumniList.value = response.data.results-->
<!--        total.value = response.data.count-->
<!--      } catch (error) {-->
<!--        console.error('获取校友列表失败:', error)-->
<!--      }-->
<!--    }-->

<!--    // 搜索-->
<!--    const handleSearch = () => {-->
<!--      currentPage.value = 1-->
<!--      getAlumniList()-->
<!--    }-->

<!--    // 重置搜索-->
<!--    const resetSearch = () => {-->
<!--      searchForm.value = {-->
<!--        student_id: '',-->
<!--        name: '',-->
<!--        department: ''-->
<!--      }-->
<!--      handleSearch()-->
<!--    }-->

<!--    // 分页-->
<!--    const handlePageChange = (page) => {-->
<!--      currentPage.value = page-->
<!--      getAlumniList()-->
<!--    }-->

<!--    onMounted(() => {-->
<!--      getAlumniList()-->
<!--    })-->

<!--    return {-->
<!--      alumniList,-->
<!--      currentPage,-->
<!--      pageSize,-->
<!--      total,-->
<!--      searchForm,-->
<!--      handleSearch,-->
<!--      resetSearch,-->
<!--      handlePageChange-->
<!--    }-->
<!--  }-->
<!--}-->
<!--</script>-->

<!--<style scoped>-->
<!--.alumni-list {-->
<!--  padding: 20px;-->
<!--}-->

<!--.search-bar {-->
<!--  margin-bottom: 20px;-->
<!--}-->

<!--.toolbar {-->
<!--  margin-bottom: 20px;-->
<!--}-->

<!--.pagination {-->
<!--  margin-top: 20px;-->
<!--  text-align: right;-->
<!--}-->
<!--</style>-->