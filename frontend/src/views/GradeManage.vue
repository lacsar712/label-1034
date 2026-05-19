<template>
  <section class="page-card">
    <div class="card-header">
      <h2>成绩录入</h2>
      <el-button type="primary" :icon="Plus" @click="openDialog()">录入成绩</el-button>
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
      <el-table :data="list" stripe border style="width: 100%">
        <el-table-column prop="student_name" label="学生" min-width="100" />
        <el-table-column prop="student_no" label="学号" min-width="110" />
        <el-table-column prop="course_name" label="课程" min-width="120" />
        <el-table-column prop="score" label="成绩" min-width="90" align="center">
          <template #default="{ row }">
            <el-tag :type="scoreType(row.score)">{{ row.score }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" min-width="140">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="openEdit(row)">修改成绩</el-button>
            <el-button link type="danger" size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <el-dialog v-model="dialogVisible" :title="editId ? '修改成绩' : '录入成绩'" width="420px" destroy-on-close>
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="学生" prop="student_id">
          <el-select v-model="form.student_id" placeholder="选择学生" filterable style="width: 100%" :disabled="!!editId">
            <el-option v-for="s in studentOptions" :key="s.id" :label="`${s.name} (${s.student_no})`" :value="s.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="课程" prop="course_id">
          <el-select v-model="form.course_id" placeholder="选择课程" filterable style="width: 100%" :disabled="!!editId">
            <el-option v-for="c in courseOptions" :key="c.id" :label="c.name" :value="c.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="成绩" prop="score">
          <el-input-number v-model="form.score" :min="0" :max="100" :precision="2" style="width: 100%" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitLoading" @click="submit">确定</el-button>
      </template>
    </el-dialog>
    <el-dialog v-model="deleteVisible" title="确认删除" width="380px">
      <p>确定删除该条成绩记录吗？</p>
      <template #footer>
        <el-button @click="deleteVisible = false">取消</el-button>
        <el-button type="danger" :loading="deleteLoading" @click="confirmDelete">确定</el-button>
      </template>
    </el-dialog>
  </section>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { getGrades, createGrade, updateGrade, deleteGrade } from '../api/grades'
import { getStudents } from '../api/students'
import { getCourses } from '../api/courses'

const loading = ref(false)
const list = ref([])
const studentOptions = ref([])
const courseOptions = ref([])
const filters = ref({ student_id: null, course_id: null })
const dialogVisible = ref(false)
const editId = ref(null)
const formRef = ref(null)
const submitLoading = ref(false)
const form = reactive({ student_id: null, course_id: null, score: 0 })
const rules = {
  student_id: [{ required: true, message: '请选择学生', trigger: 'change' }],
  course_id: [{ required: true, message: '请选择课程', trigger: 'change' }],
  score: [{ required: true, message: '请输入成绩', trigger: 'blur' }],
}
const deleteVisible = ref(false)
const deleteRow = ref(null)
const deleteLoading = ref(false)

function scoreType(score) {
  const n = Number(score)
  if (n >= 90) return 'success'
  if (n >= 60) return ''
  return 'danger'
}

async function loadOptions() {
  const [s, c] = await Promise.all([getStudents({ limit: 500 }), getCourses({ limit: 100 })])
  studentOptions.value = s || []
  courseOptions.value = c || []
}

async function load() {
  loading.value = true
  try {
    list.value = await getGrades({ limit: 200, ...filters.value })
  } finally {
    loading.value = false
  }
}

function openDialog() {
  editId.value = null
  form.student_id = null
  form.course_id = null
  form.score = 0
  dialogVisible.value = true
}

function openEdit(row) {
  editId.value = row.id
  form.student_id = row.student_id
  form.course_id = row.course_id
  form.score = Number(row.score)
  dialogVisible.value = true
}

async function submit() {
  await formRef.value?.validate()
  submitLoading.value = true
  try {
    if (editId.value) {
      await updateGrade(editId.value, { score: form.score })
      ElMessage.success('修改成功')
    } else {
      await createGrade({
        student_id: form.student_id,
        course_id: form.course_id,
        score: form.score,
      })
      ElMessage.success('录入成功')
    }
    dialogVisible.value = false
    load()
  } finally {
    submitLoading.value = false
  }
}

function handleDelete(row) {
  deleteRow.value = row
  deleteVisible.value = true
}

async function confirmDelete() {
  deleteLoading.value = true
  try {
    await deleteGrade(deleteRow.value.id)
    ElMessage.success('已删除')
    deleteVisible.value = false
    load()
  } finally {
    deleteLoading.value = false
  }
}

onMounted(() => {
  loadOptions()
  load()
})
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
