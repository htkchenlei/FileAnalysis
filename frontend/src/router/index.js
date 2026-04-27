import { createRouter, createWebHistory } from 'vue-router'
import ProjectList from '../views/ProjectList.vue'
import CreateProject from '../views/CreateProject.vue'
import Upload from '../views/Upload.vue'
import History from '../views/History.vue'
import Result from '../views/Result.vue'
import Config from '../views/Config.vue'

const routes = [
  {
    path: '/',
    name: 'ProjectList',
    component: ProjectList
  },
  {
    path: '/create',
    name: 'CreateProject',
    component: CreateProject
  },
  {
    path: '/upload',
    name: 'Upload',
    component: Upload
  },
  {
    path: '/history',
    name: 'History',
    component: History
  },
  {
    path: '/result/:id',
    name: 'Result',
    component: Result
  },
  {
    path: '/config',
    name: 'Config',
    component: Config
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
