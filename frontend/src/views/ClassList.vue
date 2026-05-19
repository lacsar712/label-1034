<template>
  <section class="page-card">
    <div class="card-header">
      <h2>班级管理</h2>
      <el-button type="primary" :icon="Plus" @click="openDialog()">新增班级</el-button>
    </div>
    <div v-loading="loading" class="table-wrap">
      <el-table :data="list" stripe border style="width: 100%">
        <el-table-column prop="id" label="ID" min-width="70" />
        <el-table-column prop="name" label="班级名称" min-width="200" />
        <el-table-column label="操作" min-width="140">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="openDialog(row)">编辑</el-button>
            <el-button link type="danger" size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <el-dialog v-model="dialogVisible" :title="editId ? '编辑班级' : '新增班级'" width="420px" destroy-on-close>
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="班级名称" prop="name">
          <el-input v-model="form.name" placeholder="班级名称" maxlength="64" show-word-limit />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitLoading" @click="submit">确定</el-button>
      </template>
    </el-dialog>
    <el-dialog v-model="deleteVisible" title="确认删除" width="380px">
      <p>确定删除班级「{{ deleteRow?.name }}」吗？该班级下若有学生则无法删除。</p>
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
import { getClasses, createClass, updateClass, deleteClass } from '../api/classes'

const loading = ref(false)
const list = ref([])
const dialogVisible = ref(false)
const editId = ref(null)
const formRef = ref(null)
const submitLoading = ref(false)
const form = reactive({ name: '' })
const rules = {
  name: [{ required: true, message: '请输入班级名称', trigger: 'blur' }],
}
const deleteVisible = ref(false)
const deleteRow = ref(null)
const deleteLoading = ref(false)

async function load() {
  loading.value = true
  try {
    list.value = await getClasses({ limit: 500 })
  } finally {
    loading.value = false
  }
}

function openDialog(row) {
  editId.value = row ? row.id : null
  form.name = row ? row.name : ''
  dialogVisible.value = true
}

async function submit() {
  await formRef.value?.validate()
  submitLoading.value = true
  try {
    if (editId.value) {
      await updateClass(editId.value, { name: form.name })
      ElMessage.success('修改成功')
    } else {
      await createClass({ name: form.name })
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
    await deleteClass(deleteRow.value.id)
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
  width: 100%;
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
  width: 100%;
  min-height: 200px;
  overflow: auto;
}
</style>
