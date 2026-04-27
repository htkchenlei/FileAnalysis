<template>
  <div 
    class="upload-area"
    @dragover.prevent
    @dragenter.prevent
    @dragleave.prevent
    @drop.prevent="handleDrop"
  >
    <!-- 网址输入 -->
    <div class="mb-8">
      <h3 class="text-lg font-medium mb-2">输入网址</h3>
      <input 
        type="url" 
        v-model="url"
        class="w-full px-4 py-2 border border-gray-300 rounded-button focus:outline-none focus:ring-2 focus:ring-primary"
        placeholder="请输入网址，例如：https://example.com"
      >
      <div v-if="url" class="mt-2 p-3 bg-gray-100 rounded flex justify-between items-center">
        <span class="truncate max-w-xs">{{ url }}</span>
        <button 
          class="text-error hover:underline"
          @click="url = ''"
        >
          清除
        </button>
      </div>
    </div>
    
    <!-- 文件上传 -->
    <div v-if="!file" class="space-y-6">
      <div class="text-5xl text-primary transition-transform duration-200 hover:scale-110">📁</div>
      <h3 class="text-xl font-semibold">拖拽文件到这里，或点击选择文件</h3>
      <p class="text-text-secondary">支持 PDF、DOCX、DOC、TXT、RTF 格式，最大 50MB</p>
      <input 
        type="file" 
        ref="fileInput" 
        class="hidden" 
        @change="handleFileSelect"
        accept=".pdf,.docx,.doc,.txt,.rtf"
      >
      <button 
        class="px-6 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors duration-200 w-48 transition-transform duration-200 hover:scale-105"
        @click="$refs.fileInput.click()"
      >
        选择文件
      </button>
    </div>
    <div v-else class="space-y-6">
      <div class="flex items-center justify-between p-4 bg-white rounded-card shadow-sm">
        <div class="flex items-center space-x-4">
          <div class="text-2xl">📄</div>
          <div>
            <div class="font-medium truncate max-w-xs">{{ file.name }}</div>
            <div class="text-sm text-text-secondary">{{ formatFileSize(file.size) }}</div>
          </div>
        </div>
        <button 
          class="text-error hover:underline transition-colors"
          @click="file = null"
        >
          移除
        </button>
      </div>
    </div>
    
    <!-- 开始分析按钮 -->
    <button 
      class="mt-6 px-6 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors duration-200 w-full transition-transform duration-200 hover:scale-105"
      @click="handleAnalysis"
      :disabled="loading || (!file && !url)"
    >
      {{ loading ? '分析中...' : '开始分析' }}
    </button>
    
    <div v-if="loading" class="mt-6">
      <div class="w-full bg-gray-200 rounded-full h-2.5">
        <div 
          class="bg-primary h-2.5 rounded-full transition-all duration-300 ease-out"
          style="width: 70%"
        ></div>
      </div>
      <p class="text-sm text-text-secondary mt-2 text-center">正在处理，请稍候...</p>
    </div>
    
    <div v-if="error" class="mt-6 p-4 bg-error/10 border border-error rounded-card">
      <div class="flex items-center space-x-2">
        <div class="text-error">❌</div>
        <div class="text-error font-medium">{{ error }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps } from 'vue'
import { useFilesStore } from '../stores/files'
import { useRouter } from 'vue-router'
import axios from 'axios'

const props = defineProps({
  projectName: {
    type: String,
    default: ''
  }
})

const filesStore = useFilesStore()
const router = useRouter()

const file = ref(null)
const url = ref('')
const loading = ref(false)
const error = ref(null)

const handleFileSelect = (event) => {
  const selectedFile = event.target.files[0]
  if (selectedFile) {
    validateFile(selectedFile)
  }
}

const handleDrop = (event) => {
  const droppedFile = event.dataTransfer.files[0]
  if (droppedFile) {
    validateFile(droppedFile)
  }
}

const validateFile = (selectedFile) => {
  const allowedTypes = ['.pdf', '.docx', '.doc', '.txt', '.rtf']
  const fileExtension = '.' + selectedFile.name.split('.').pop().toLowerCase()
  
  if (!allowedTypes.includes(fileExtension)) {
    error.value = '不支持的文件格式，请选择 PDF、DOCX、DOC、TXT 或 RTF 格式'
    return
  }
  
  if (selectedFile.size > 50 * 1024 * 1024) {
    error.value = '文件大小超过限制，最大支持 50MB'
    return
  }
  
  error.value = null
  file.value = selectedFile
}

const handleAnalysis = async () => {
  if (!file.value && !url.value) return
  
  loading.value = true
  error.value = null
  
  try {
    if (file.value) {
      // 处理文件上传
      const result = await filesStore.uploadFile(file.value, props.projectName)
      if (result.id) {
        router.push(`/result/${result.id}`)
      } else if (result.status === 'failed') {
        error.value = result.error_message || '转换失败'
      }
    } else if (url.value) {
      // 处理网址
      const response = await axios.post('/api/url', { 
        url: url.value,
        project_name: props.projectName || `url_${Math.abs(url.value.split('').reduce((a, b) => {
          a = ((a << 5) - a) + b.charCodeAt(0);
          return a & a;
        }, 0))}.md`
      })
      if (response.data.id) {
        router.push(`/result/${response.data.id}`)
      } else if (response.data.status === 'failed') {
        error.value = response.data.error_message || '转换失败'
      }
    }
  } catch (err) {
    error.value = '提交失败，请重试'
  } finally {
    loading.value = false
  }
}

const formatFileSize = (bytes) => {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(2) + ' MB'
}
</script>

<style scoped>
.upload-area {
  border: 2px dashed #e2e8f0;
  border-radius: 0.5rem;
  padding: 2rem;
  text-align: center;
  transition: all 0.3s ease;
}

.upload-area:hover {
  border-color: #8b5cf6;
  background-color: #f9fafb;
}
</style>
