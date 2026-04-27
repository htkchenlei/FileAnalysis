<template>
  <div class="min-h-screen">
    <NavBar />
    <div class="container mx-auto px-6 py-12">
      <h1 class="text-3xl font-bold mb-8">历史记录</h1>
      
      <div v-if="loading" class="flex justify-center items-center py-12">
        <div class="text-primary text-2xl">加载中...</div>
      </div>
      
      <div v-else-if="files.length === 0" class="text-center py-12">
        <div class="text-4xl text-text-secondary mb-4">📄</div>
        <h2 class="text-xl font-semibold mb-2">暂无历史记录</h2>
        <p class="text-text-secondary mb-6">上传文件后，转换记录会显示在这里</p>
        <router-link to="/" class="btn-primary">
          上传文件
        </router-link>
      </div>
      
      <div v-else class="space-y-4">
        <div 
          v-for="file in files" 
          :key="file.id"
          class="card flex justify-between items-center transition-all duration-200 hover:shadow-hover"
        >
          <div class="flex items-center space-x-4">
            <div class="text-2xl transition-transform duration-200 hover:scale-110">📄</div>
            <div>
              <div class="font-medium truncate max-w-md">{{ file.filename }}</div>
              <div class="text-sm text-text-secondary">
                {{ formatDate(file.created_at) }}
              </div>
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <span 
              class="px-3 py-1 rounded-full text-sm transition-all duration-200"
              :class="{
                'bg-success text-white': file.status === 'completed',
                'bg-error text-white': file.status === 'failed',
                'bg-warning text-white': file.status === 'processing',
                'bg-gray-200 text-text-secondary': file.status === 'pending'
              }"
            >
              {{ file.status === 'completed' ? '完成' : 
                 file.status === 'failed' ? '失败' : 
                 file.status === 'processing' ? '处理中' : '等待中' }}
            </span>
            <router-link 
              :to="`/result/${file.id}`"
              class="text-primary hover:underline transition-colors duration-200"
              v-if="file.status === 'completed'"
            >
              查看
            </router-link>
            <button 
              class="text-error hover:underline transition-colors duration-200"
              @click="handleDelete(file.id)"
            >
              删除
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import NavBar from '../components/NavBar.vue'
import { useFilesStore } from '../stores/files'

const filesStore = useFilesStore()

onMounted(() => {
  filesStore.getFiles()
})

const files = computed(() => filesStore.files)
const loading = computed(() => filesStore.loading)

const handleDelete = async (id) => {
  if (confirm('确定要删除这条记录吗？')) {
    await filesStore.deleteFile(id)
  }
}

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
</script>

<style scoped>
</style>
