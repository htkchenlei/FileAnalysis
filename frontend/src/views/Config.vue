<template>
  <div class="min-h-screen">
    <NavBar />
    <div class="container mx-auto px-6 py-12">
      <h1 class="text-3xl font-bold mb-8">系统配置</h1>
      
      <div class="card">
        <h2 class="text-xl font-semibold mb-6">硅基流动大模型配置</h2>
        
        <div class="space-y-6">
          <div>
            <label class="block text-sm font-medium mb-2">API URL</label>
            <input 
              type="text" 
              v-model="config.ai_api_url" 
              class="w-full px-4 py-2 border border-gray-300 rounded-button focus:outline-none focus:ring-2 focus:ring-primary"
              placeholder="https://api.siliconflow.cn/v1/chat/completions"
            >
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-2">API Key</label>
            <input 
              type="password" 
              v-model="config.ai_api_key" 
              class="w-full px-4 py-2 border border-gray-300 rounded-button focus:outline-none focus:ring-2 focus:ring-primary"
              placeholder="请输入API Key"
            >
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-2">模型名称</label>
            <input 
              type="text" 
              v-model="config.ai_model" 
              class="w-full px-4 py-2 border border-gray-300 rounded-button focus:outline-none focus:ring-2 focus:ring-primary"
              placeholder="deepseek-ai/deepseek-v3.1-terminus"
            >
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-2">提示词</label>
            <textarea 
              v-model="config.ai_prompt" 
              class="w-full px-4 py-2 border border-gray-300 rounded-button focus:outline-none focus:ring-2 focus:ring-primary h-48"
              placeholder="请输入提示词"
            ></textarea>
          </div>
          
          <div class="flex space-x-4">
            <button 
              class="px-6 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors duration-200"
              @click="saveConfig"
              :disabled="loading"
            >
              {{ loading ? '保存中...' : '保存配置' }}
            </button>
            <button 
              class="px-6 py-2 bg-gray-200 text-text-primary rounded-lg hover:bg-gray-300 transition-colors duration-200"
              @click="testAI"
              :disabled="loading"
            >
              {{ loading ? '测试中...' : '测试连接' }}
            </button>
          </div>
        </div>
        
        <div v-if="message" class="mt-6 p-4 rounded-button" :class="message.type === 'success' ? 'bg-success/10 text-success' : 'bg-error/10 text-error'">
          {{ message.text }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import NavBar from '../components/NavBar.vue'
import axios from 'axios'

const config = ref({
  ai_api_url: '',
  ai_api_key: '',
  ai_model: '',
  ai_prompt: ''
})

const loading = ref(false)
const message = ref(null)

onMounted(() => {
  fetchConfig()
})

const fetchConfig = async () => {
  try {
    const response = await axios.get('/api/config')
    config.value = response.data
  } catch (error) {
    showMessage('获取配置失败', 'error')
  }
}

const saveConfig = async () => {
  loading.value = true
  message.value = null
  
  try {
    await axios.post('/api/config', config.value)
    showMessage('配置保存成功', 'success')
  } catch (error) {
    showMessage('保存配置失败', 'error')
  } finally {
    loading.value = false
  }
}

const testAI = async () => {
  loading.value = true
  message.value = null
  
  try {
    const response = await axios.get('/api/test-ai')
    if (response.data.status === 'success') {
      showMessage('连接成功！' + response.data.response, 'success')
    } else {
      showMessage('连接失败：' + response.data.message, 'error')
    }
  } catch (error) {
    showMessage('测试连接失败', 'error')
  } finally {
    loading.value = false
  }
}

const showMessage = (text, type) => {
  message.value = { text, type }
  setTimeout(() => {
    message.value = null
  }, 3000)
}
</script>

<style scoped>
</style>
