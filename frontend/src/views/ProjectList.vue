<template>
  <div class="min-h-screen">
    <NavBar />
    <div class="container mx-auto px-6 py-12">
      <div class="max-w-4xl mx-auto">
        <div class="flex justify-between items-center mb-8">
          <h1 class="text-3xl font-bold">项目列表</h1>
          <router-link to="/create" class="btn-primary">
            新建项目
          </router-link>
        </div>
        
        <div v-if="loading" class="flex justify-center items-center py-12">
          <div class="text-4xl text-primary">⏳</div>
        </div>
        
        <div v-else-if="projects.length === 0" class="text-center py-12">
          <div class="text-4xl text-primary mb-4">📋</div>
          <h3 class="text-xl font-semibold mb-2">暂无项目</h3>
          <p class="text-text-secondary mb-6">点击上方"新建项目"按钮开始创建第一个项目</p>
          <router-link to="/create" class="btn-primary">
            新建项目
          </router-link>
        </div>
        
        <div v-else class="space-y-4">
          <div 
            v-for="project in projects" 
            :key="project.id"
            class="card flex justify-between items-center transition-all duration-200 hover:shadow-hover"
          >
            <div class="flex items-center space-x-4">
              <div class="text-2xl transition-transform duration-200 hover:scale-110">📄</div>
              <div>
                <div class="font-medium">{{ project.filename }}</div>
                <div class="text-sm text-text-secondary">
                  {{ formatDate(project.created_at) }}
                </div>
              </div>
            </div>
            <div class="flex items-center space-x-2 flex-shrink-0">
              <span 
                class="px-3 py-1 rounded-lg text-sm font-medium whitespace-nowrap"
                :class="{
                  'bg-success text-white': project.status === 'completed',
                  'bg-error text-white': project.status === 'failed',
                  'bg-warning text-white': project.status === 'processing',
                  'bg-gray-200 text-text-secondary': project.status === 'pending'
                }"
              >
                {{ project.status === 'completed' ? '完成' : 
                   project.status === 'failed' ? '失败' : 
                   project.status === 'processing' ? '处理中' : '等待中' }}
              </span>
              <router-link 
                :to="`/result/${project.id}`"
                class="px-3 py-1 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors duration-200 text-sm whitespace-nowrap"
              >
                查看
              </router-link>
              <button 
                class="px-3 py-1 bg-error text-white rounded-lg hover:bg-error/90 transition-colors duration-200 text-sm whitespace-nowrap"
                @click="handleDelete(project.id)"
              >
                删除
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import NavBar from '../components/NavBar.vue'
import { useFilesStore } from '../stores/files'
import axios from 'axios'

const filesStore = useFilesStore()
const projects = ref([])
const loading = ref(true)

onMounted(async () => {
  await filesStore.getFiles()
  projects.value = filesStore.files
  loading.value = false
})

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const handleDelete = async (id) => {
  if (!confirm('确定要删除这个项目吗？')) return
  
  try {
    // 确保ID是整数类型
    const fileId = parseInt(id)
    await axios.delete(`/api/files/${fileId}`)
    alert('项目删除成功')
    // 重新获取项目列表
    await filesStore.getFiles()
    projects.value = filesStore.files
  } catch (err) {
    alert('删除失败：' + (err.response?.data?.error || '未知错误'))
  }
}
</script>

<style scoped>
</style>
