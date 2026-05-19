<template>
  <section class="page-card">
    <div class="card-header">
      <h2>成绩查询</h2>
      <el-button type="primary" :icon="Refresh" @click="load">刷新</el-button>
    </div>
    <el-form inline class="filter-form">
      <el-form-item label="学生">
        <el-select v-model="filters.student_id" clearable placeholder="全部" filterable style="width: 180px">
          <el-option v-for="s in studentOptions" :key="s.id" :label="`${s.name} (${s.student_no})`" :value="s.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="课程">
        <el-select v-model="filters.course_id" clearable placeholder="全部" filterable style="width: 160px">
          <el-option v-for="c in courseOptions" :key="c.id" :label="c.name" :value="c.id" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="load">查询</el-button>
      </el-form-item>
    </el-form>
    <div v-loading="loading" class="table-wrap">
      <el-table :data="list" stripe border style="width: 100%" :empty-text="'暂无数据'">
        <el-table-column prop="student_name" label="学生姓名" min-width="100" />
        <el-table-column prop="student_no" label="学号" min-width="110" />
        <el-table-column prop="course_name" label="课程" min-width="120" />
        <el-table-column prop="course_credit" label="学分" min-width="80" align="center" />
        <el-table-column prop="score" label="成绩" min-width="90" align="center">
          <template #default="{ row }">
            <el-tag :type="scoreType(row.score)">{{ row.score }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="exam_date" label="考试时间" min-width="160">
          <template #default="{ row }">{{ formatDate(row.exam_date) }}</template>
        </el-table-column>
      </el-table>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Refresh } from '@element-plus/icons-vue'
import { getGrades } from '../api/grades'
import { getStudents } from '../api/students'
import { getCourses } from '../api/courses'

const loading = ref(false)
const list = ref([])
const studentOptions = ref([])
const courseOptions = ref([])
const filters = ref({ student_id: null, course_id: null })

function scoreType(score) {
  const n = Number(score)
  if (n >= 90) return 'success'
  if (n >= 60) return ''
  return 'danger'
}

function formatDate(v) {
  if (!v) return '-'
  const d = new Date(v)
  return isNaN(d.getTime()) ? v : d.toLocaleString('zh-CN')
}

async function load() {
  loading.value = true
  try {
    const [gradesRes, studentsRes, coursesRes] = await Promise.all([
      getGrades({ limit: 200, ...filters.value }),
      getStudents({ limit: 500 }),
      getCourses({ limit: 100 }),
    ])
    list.value = gradesRes || []
    studentOptions.value = studentsRes || []
    courseOptions.value = coursesRes || []
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<style scoped>
.page-card {
  width: 100%;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  padding: 24px;
}
.table-wrap {
  width: 100%;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.card-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #303133;
}
.filter-form {
  margin-bottom: 20px;
}
.table-wrap {
  min-height: 200px;
  overflow: auto;
}
</style>
