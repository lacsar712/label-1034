<template>
  <section class="page-card">
    <div class="card-header">
      <h2>课程管理</h2>
      <el-button type="primary" :icon="Plus" @click="openDialog()">新增课程</el-button>
    </div>
    <div v-loading="loading" class="table-wrap">
      <el-table :data="list" stripe border style="width: 100%">
        <el-table-column prop="id" label="ID" min-width="70" />
        <el-table-column prop="name" label="课程名称" min-width="160" />
        <el-table-column prop="credit" label="学分" min-width="100" align="center" />
        <el-table-column label="操作" min-width="140">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="openDialog(row)">编辑</el-button>
            <el-button link type="danger" size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <el-dialog v-model="dialogVisible" :title="editId ? '编辑课程' : '新增课程'" width="420px" destroy-on-close>
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="课程名" prop="name">
          <el-input v-model="form.name" placeholder="课程名称" maxlength="128" show-word-limit />
        </el-form-item>
        <el-form-item label="学分" prop="credit">
          <el-input-number v-model="form.credit" :min="0" :max="100" :precision="1" style="width: 100%" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitLoading" @click="submit">确定</el-button>
      </template>
    </el-dialog>
    <el-dialog v-model="deleteVisible" title="确认删除" width="380px">
      <p>确定删除课程「{{ deleteRow?.name }}」吗？相关成绩记录将一并删除。</p>
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
import { getCourses, createCourse, updateCourse, deleteCourse } from '../api/courses'

const loading = ref(false)
const list = ref([])
const dialogVisible = ref(false)
const editId = ref(null)
const formRef = ref(null)
const submitLoading = ref(false)
const form = reactive({ name: '', credit: 0 })
const rules = {
  name: [{ required: true, message: '请输入课程名称', trigger: 'blur' }],
  credit: [{ required: true, message: '请输入学分', trigger: 'blur' }],
}
const deleteVisible = ref(false)
const deleteRow = ref(null)
const deleteLoading = ref(false)

async function load() {
  loading.value = true
  try {
    list.value = await getCourses({ limit: 200 })
  } finally {
    loading.value = false
  }
}

function openDialog(row) {
  editId.value = row ? row.id : null
  form.name = row ? row.name : ''
  form.credit = row != null ? Number(row.credit) : 0
  dialogVisible.value = true
}

async function submit() {
  await formRef.value?.validate()
  submitLoading.value = true
  try {
    if (editId.value) {
      await updateCourse(editId.value, { name: form.name, credit: form.credit })
      ElMessage.success('修改成功')
    } else {
      await createCourse({ name: form.name, credit: form.credit })
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
    await deleteCourse(deleteRow.value.id)
    ElMessage.success('已删除')
    deleteVisible.value = false
    load()
  } finally {
    deleteLoading.value = false
  }
}

onMounted(load)
</script>

<style scoped>
.page-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  padding: 24px;
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
.table-wrap {
  min-height: 200px;
}
</style>
