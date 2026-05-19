import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'Home', component: () => import('../views/GradeList.vue'), meta: { title: '成绩查询' } },
  { path: '/grades-manage', name: 'GradesManage', component: () => import('../views/GradeManage.vue'), meta: { title: '成绩录入' } },
  { path: '/students', name: 'Students', component: () => import('../views/StudentList.vue'), meta: { title: '学生管理' } },
  { path: '/classes', name: 'Classes', component: () => import('../views/ClassList.vue'), meta: { title: '班级管理' } },
  { path: '/courses', name: 'Courses', component: () => import('../views/CourseList.vue'), meta: { title: '课程管理' } },
]

const router = createRouter({
  history: createWebHistory('/'),
  routes,
})

export default router
