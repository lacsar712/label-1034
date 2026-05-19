<template>
  <div class="app-wrap">
    <header class="header">
      <div class="logo">
        <span class="logo-icon"><el-icon :size="26"><Reading /></el-icon></span>
        <span class="logo-text">学生成绩管理系统</span>
      </div>
      <nav class="nav-tabs">
        <router-link
          v-for="tab in tabs"
          :key="tab.path"
          :to="tab.path"
          class="tab-item"
          :class="{ active: activeMenu === tab.path }"
        >
          <el-icon class="tab-icon"><component :is="tab.icon" /></el-icon>
          <span class="tab-label">{{ tab.label }}</span>
        </router-link>
      </nav>
    </header>
    <main class="main">
      <router-view v-slot="{ Component }">
        <Suspense>
          <component :is="Component" />
          <template #fallback>
            <div class="loading-wrap">
              <el-icon class="is-loading" :size="48"><Loading /></el-icon>
              <p>加载中...</p>
            </div>
          </template>
        </Suspense>
      </router-view>
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { Reading, Loading, Search, EditPen, User, School, Collection } from '@element-plus/icons-vue'

const route = useRoute()
const activeMenu = computed(() => route.path || '/')

const tabs = [
  { path: '/', label: '成绩查询', icon: Search },
  { path: '/grades-manage', label: '成绩录入', icon: EditPen },
  { path: '/students', label: '学生管理', icon: User },
  { path: '/classes', label: '班级管理', icon: School },
  { path: '/courses', label: '课程管理', icon: Collection },
]
</script>

<style>
* {
  box-sizing: border-box;
}
html, body, #app {
  height: 100%;
  margin: 0;
}
.app-wrap {
  min-height: 100%;
  display: flex;
  flex-direction: column;
  background: linear-gradient(160deg, #f0f4f8 0%, #e2e8f0 50%, #cbd5e1 100%);
}
</style>

<style scoped>
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 28px 0 24px;
  height: 64px;
  background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 50%, #1e4976 100%);
  box-shadow: 0 4px 20px rgba(30, 58, 95, 0.25);
  position: relative;
  overflow: hidden;
}
.header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  pointer-events: none;
}
.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}
.logo-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: rgba(255,255,255,0.12);
  color: #fff;
  backdrop-filter: blur(8px);
}
.logo-text {
  font-size: 19px;
  font-weight: 600;
  color: #fff;
  letter-spacing: 0.02em;
  text-shadow: 0 1px 2px rgba(0,0,0,0.1);
}
.nav-tabs {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 0;
  flex: 1;
  min-width: 0;
  justify-content: flex-end;
}
.tab-item {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  border-radius: 10px;
  color: rgba(255,255,255,0.85);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.22s ease;
  white-space: nowrap;
}
.tab-item:hover {
  color: #fff;
  background: rgba(255,255,255,0.15);
}
.tab-item.active {
  color: #fff;
  background: rgba(255,255,255,0.22);
  box-shadow: 0 2px 12px rgba(0,0,0,0.15);
}
.tab-icon {
  font-size: 17px;
  opacity: 0.95;
}
.tab-item.active .tab-icon {
  opacity: 1;
}
.tab-label {
  letter-spacing: 0.02em;
}
.main {
  flex: 1;
  padding: 24px;
  width: 100%;
  min-width: 0;
  min-height: calc(100vh - 64px);
}
.loading-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px;
  color: #64748b;
}
.loading-wrap p { margin-top: 16px; }
</style>
