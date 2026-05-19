<template>
  <section class="page-card">
    <div class="card-header">
      <h2>学生管理</h2>
      <el-button type="primary" :icon="Plus" @click="openDialog()">新增学生</el-button>
    </div>
    <el-form inline class="filter-form">
      <el-form-item label="班级">
        <el-select v-model="classFilter" placeholder="全部班级" clearable filterable style="width: 180px">
          <el-option v-for="c in classOptions" :key="c.id" :label="c.name" :value="c.id" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="load">查询</el-button>
      </el-form-item>
    </el-form>
    <div v-loading="loading" class="table-wrap">
      <el-table :data="list" stripe border style="width: 100%">
        <el-table-column prop="id" label="ID" min-width="70" />
        <el-table-column prop="name" label="姓名" min-width="100" />
        <el-table-column prop="student_no" label="学号" min-width="120" />
        <el-table-column prop="class_name" label="班级" min-width="140" />
        <el-table-column label="操作" min-width="140">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="openDialog(row)">编辑</el-button>
            <el-button link type="danger" size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <el-dialog v-model="dialogVisible" :title="editId ? '编辑学生' : '新增学生'" width="420px" destroy-on-close>
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="姓名" prop="name">
          <el-input v-model="form.name" placeholder="姓名" maxlength="64" show-word-limit />
        </el-form-item>
        <el-form-item label="学号" prop="student_no">
          <el-input v-model="form.student_no" placeholder="学号" maxlength="32" show-word-limit :disabled="!!editId" />
        </el-form-item>
        <el-form-item label="班级" prop="class_id">
          <el-select v-model="form.class_id" placeholder="选择班级" filterable style="width: 100%">
            <el-option v-for="c in classOptions" :key="c.id" :label="c.name" :value="c.id" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitLoading" @click="submit">确定</el-button>
      </template>
    </el-dialog>
    <el-dialog v-model="deleteVisible" title="确认删除" width="380px">
      <p>确定删除学生「{{ deleteRow?.name }}」吗？其成绩记录将一并删除。</p>
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
import { getStudents, createStudent, updateStudent, deleteStudent } from '../api/students'
import { getClasses } from '../api/classes'

const loading = ref(false)
const list = ref([])
const classOptions = ref([])
const classFilter = ref(null)
const dialogVisible = ref(false)
const editId = ref(null)
const formRef = ref(null)
const submitLoading = ref(false)
const form = reactive({ name: '', student_no: '', class_id: null })
const rules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  student_no: [{ required: true, message: '请输入学号', trigger: 'blur' }],
  class_id: [{ required: true, message: '请选择班级', trigger: 'change' }],
}
const deleteVisible = ref(false)
const deleteRow = ref(null)
const deleteLoading = ref(false)

async function loadClasses() {
  classOptions.value = await getClasses({ limit: 500 }) || []
}

async function load() {
  loading.value = true
  try {
    list.value = await getStudents({
      limit: 200,
      class_id: classFilter.value || undefined,
    })
  } finally {
    loading.value = false
  }
}

function openDialog(row) {
  editId.value = row ? row.id : null
  form.name = row ? row.name : ''
  form.student_no = row ? row.student_no : ''
  form.class_id = row ? row.class_id : null
  dialogVisible.value = true
}

async function submit() {
  await formRef.value?.validate()
  submitLoading.value = true
  try {
    if (editId.value) {
      await updateStudent(editId.value, { name: form.name, class_id: form.class_id })
      ElMessage.success('修改成功')
    } else {
      await createStudent({ name: form.name, student_no: form.student_no, class_id: form.class_id })
      ElMessage.success('添加成功')
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
    await deleteStudent(deleteRow.value.id)
    ElMessage.success('已删除')
    deleteVisible.value = false
    load()
  } finally {
    deleteLoading.value = false
  }
}

onMounted(() => {
  loadClasses()
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
