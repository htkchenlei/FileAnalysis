<template>
  <div class="min-h-screen">
    <NavBar />
    <div class="container mx-auto px-6 py-12">
      <div class="max-w-4xl mx-auto">
        <div class="flex justify-between items-center mb-8">
          <h1 class="text-3xl font-bold">{{ filename }}</h1>
        </div>
        
        <div class="card mb-8">
          <div class="flex justify-between items-center mb-4">
            <div class="text-sm text-text-secondary">
              转换时间：{{ formatDate(createdAt) }}
            </div>
            <span 
              class="px-4 py-2 rounded-lg text-sm font-medium"
              :class="{
                'bg-success text-white': status === 'completed',
                'bg-error text-white': status === 'failed',
                'bg-warning text-white': status === 'processing'
              }"
            >
              {{ status === 'completed' ? '转换成功' : 
                 status === 'failed' ? '转换失败' : '处理中' }}
            </span>
          </div>
          
          <div v-if="status === 'failed'" class="py-8 text-center">
            <div class="text-4xl text-error mb-4">❌</div>
            <h3 class="text-xl font-semibold mb-2">转换失败</h3>
            <p class="text-text-secondary mb-4">{{ error || '文件转换失败，请重试' }}</p>
            <router-link to="/" class="px-6 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors duration-200">
              返回项目列表
            </router-link>
          </div>
          
          <div v-else-if="status === 'processing'" class="py-8">
            <div class="text-center mb-6">
              <div class="text-4xl text-primary mb-4">⏳</div>
              <h3 class="text-xl font-semibold mb-2">处理中...</h3>
              <p class="text-text-secondary">{{ currentStepText }}</p>
            </div>
            
            <!-- 进度条 -->
            <div class="w-full bg-gray-200 rounded-full h-2.5 mb-4">
              <div 
                class="bg-primary h-2.5 rounded-full transition-all duration-500 ease-out"
                :style="{ width: progressPercentage + '%' }"
              ></div>
            </div>
            
            <div class="flex justify-between text-xs text-text-secondary">
              <span>开始转换</span>
              <span>转换完成</span>
              <span>调用AI分析</span>
              <span>分析完成</span>
            </div>
          </div>
          
          <div v-else-if="!analysis && !analyzing" class="py-8 text-center">
            <div class="text-4xl text-primary mb-4">🤖</div>
            <h3 class="text-xl font-semibold mb-2">正在分析文档...</h3>
            <p class="text-text-secondary">系统正在调用大模型分析文档内容，请稍候...</p>
          </div>
          
          <div v-else-if="analyzing" class="py-8 text-center">
            <div class="text-4xl text-primary mb-4">⏳</div>
            <h3 class="text-xl font-semibold mb-2">分析中...</h3>
            <p class="text-text-secondary">正在提取关键信息，请稍候...</p>
          </div>
          
          <div v-else-if="analysis" class="space-y-4">
            <h2 class="text-xl font-semibold mb-4">智能分析结果</h2>
            <div class="space-y-4">
              <div v-for="(item, index) in analysisItems" :key="index" class="p-4 bg-white rounded-card shadow-sm">
                <div class="font-semibold text-primary mb-2">{{ item.label }}</div>
                <div class="text-text-primary">{{ item.content }}</div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="flex flex-wrap justify-end gap-4">
          <button 
            class="px-6 py-2 bg-gray-200 text-text-primary rounded-lg hover:bg-gray-300 transition-colors duration-200"
            @click="handleDownload"
            v-if="status === 'completed' || (status === 'processing' && currentStep >= 2)"
          >
            下载 Markdown
          </button>
          <button 
            class="px-6 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors duration-200"
            @click="analyzeDocument"
            v-if="status === 'completed' && !analysis"
            :disabled="analyzing"
          >
            {{ analyzing ? '分析中...' : '重新分析' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import NavBar from '../components/NavBar.vue'
import MarkdownViewer from '../components/MarkdownViewer.vue'
import { useFilesStore } from '../stores/files'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const filesStore = useFilesStore()

const fileId = computed(() => route.params.id)

const filename = ref('')
const content = ref('')
const status = ref('')
const createdAt = ref('')
const loading = ref(true)
const error = ref('')
const analysis = ref('')
const analyzing = ref(false)

// 进度跟踪
const currentStep = ref(1) // 1: 开始转换, 2: 转换完成, 3: 调用AI分析, 4: 分析完成
const progressPercentage = ref(0)

onMounted(async () => {
  try {
    await loadFileData()
    
    // 如果文件正在处理中，定期刷新状态
    if (status.value === 'processing') {
      startPolling()
    } else if (status.value === 'completed' && !analysis.value) {
      // 如果没有分析结果，自动调用大模型进行分析
      await analyzeDocument()
    }
  } catch (err) {
    error.value = '获取文件详情失败'
  } finally {
    loading.value = false
  }
})

const loadFileData = async () => {
  try {
    // 确保ID是整数类型
    const fileIdInt = parseInt(fileId.value)
    console.log('Loading file data for ID:', fileIdInt)
    const fileData = await filesStore.getFile(fileIdInt)
    console.log('File data received:', fileData)
    filename.value = fileData.filename
    content.value = fileData.content
    analysis.value = fileData.analysis
    status.value = fileData.status
    createdAt.value = fileData.created_at
    error.value = fileData.error_message || ''
    
    // 打印详细信息，方便调试
    console.log('Content length:', fileData.content ? fileData.content.length : 0)
    console.log('Status:', fileData.status)
    console.log('Error message:', fileData.error_message)
    
    // 更新进度
    if (status.value === 'processing') {
      // 检查文件是否已经转换完成（有内容）
      if (fileData.content && fileData.content.length > 0) {
        currentStep.value = 2 // 转换完成
        progressPercentage.value = 50
        console.log('转换完成，显示下载按钮')
      } else {
        currentStep.value = 1 // 开始转换
        progressPercentage.value = 25
        console.log('开始转换，等待中...')
      }
    } else if (status.value === 'completed') {
      if (fileData.analysis) {
        currentStep.value = 4 // 分析完成
        progressPercentage.value = 100
        console.log('分析完成')
      } else {
        currentStep.value = 2 // 转换完成
        progressPercentage.value = 50
        console.log('转换完成，显示下载按钮')
      }
    } else if (status.value === 'failed') {
      console.log('转换失败:', fileData.error_message)
    }
  } catch (err) {
    console.error('Error loading file data:', err)
    error.value = '获取文件详情失败'
  }
}

// 存储定时器ID
const pollingInterval = ref(null)

const startPolling = () => {
  // 清除之前的定时器（如果存在）
  if (pollingInterval.value) {
    clearInterval(pollingInterval.value)
  }
  
  pollingInterval.value = setInterval(async () => {
    console.log('Polling for file status...')
    await loadFileData()
    console.log('Current status:', status.value)
    if (status.value !== 'processing') {
      console.log('Processing completed, clearing interval')
      clearInterval(pollingInterval.value)
      pollingInterval.value = null
      if (status.value === 'completed' && !analysis.value) {
        console.log('Starting AI analysis')
        currentStep.value = 3 // 开始调用AI分析
        progressPercentage.value = 75
        await analyzeDocument()
      }
    }
  }, 3000) // 每3秒刷新一次
}

// 组件卸载时清除定时器
import { onUnmounted } from 'vue'
onUnmounted(() => {
  if (pollingInterval.value) {
    clearInterval(pollingInterval.value)
    pollingInterval.value = null
  }
})

const handleDownload = () => {
  if (!content.value) return
  
  const blob = new Blob([content.value], { type: 'text/markdown' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${filename.value.split('.').slice(0, -1).join('.')}.md`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

const analyzeDocument = async () => {
  analyzing.value = true
  currentStep.value = 3 // 调用AI分析
  progressPercentage.value = 75
  
  try {
    // 确保ID是整数类型
    const fileIdInt = parseInt(fileId.value)
    const response = await axios.post(`/api/analyze/${fileIdInt}`)
    analysis.value = response.data.analysis
    currentStep.value = 4 // 分析完成
    progressPercentage.value = 100
  } catch (err) {
    alert('分析失败：' + (err.response?.data?.error || '未知错误'))
  } finally {
    analyzing.value = false
  }
}

const handleDelete = async () => {
  if (!confirm('确定要删除这个项目吗？')) return
  
  try {
    // 确保ID是整数类型
    const fileIdInt = parseInt(fileId.value)
    await axios.delete(`/api/files/${fileIdInt}`)
    alert('项目删除成功')
    router.push('/')
  } catch (err) {
    alert('删除失败：' + (err.response?.data?.error || '未知错误'))
  }
}

const analysisItems = computed(() => {
  if (!analysis.value) return []
  
  const items = []
  const lines = analysis.value.split('\n')
  let currentLabel = ''
  let currentContent = []
  
  for (const line of lines) {
    if (line.includes('：')) {
      if (currentLabel) {
        items.push({
          label: currentLabel,
          content: currentContent.join('\n').trim()
        })
      }
      const parts = line.split('：')
      currentLabel = parts[0].trim()
      currentContent = [parts.slice(1).join('：').trim()]
    } else if (currentLabel) {
      currentContent.push(line.trim())
    }
  }
  
  if (currentLabel) {
    items.push({
      label: currentLabel,
      content: currentContent.join('\n').trim()
    })
  }
  
  return items
})

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

const currentStepText = computed(() => {
  switch (currentStep.value) {
    case 1:
      return '系统正在开始转换文件，请稍候...'
    case 2:
      return '文件转换完成，准备进行AI分析...'
    case 3:
      return '正在调用AI分析文档内容，请稍候...'
    case 4:
      return '分析完成，正在整理结果...'
    default:
      return '系统正在处理文件，请稍候...'
  }
})
</script>

<style scoped>
</style>
