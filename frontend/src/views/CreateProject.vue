<template>
  <div class="min-h-screen">
    <NavBar />
    <div class="container mx-auto px-6 py-12">
      <div class="max-w-3xl mx-auto">
        <h1 class="text-3xl font-bold mb-8 text-center">新建项目</h1>
        
        <div class="card mb-8">
          <h2 class="text-xl font-semibold mb-6">项目信息</h2>
          
          <div class="space-y-6">
            <div>
              <label class="block text-sm font-medium mb-2">项目名称</label>
              <input 
                type="text" 
                v-model="project.name" 
                class="w-full px-4 py-2 border border-gray-300 rounded-button focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="请输入项目名称"
              >
            </div>
            
            <div>
              <label class="block text-sm font-medium mb-4">数据源</label>
              <div class="space-y-8">
                <!-- 文件上传 -->
                <div>
                  <h3 class="text-lg font-medium mb-4">上传文件</h3>
                  <FileUpload :project-name="project.name" />
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="card">
          <h2 class="text-xl font-semibold mb-4">系统功能</h2>
          <ul class="space-y-2">
            <li class="flex items-center space-x-2">
              <span class="text-success">✓</span>
              <span>支持多种文件格式：PDF、DOCX、DOC、TXT、RTF</span>
            </li>
            <li class="flex items-center space-x-2">
              <span class="text-success">✓</span>
              <span>文件大小限制：最大 50MB</span>
            </li>
            <li class="flex items-center space-x-2">
              <span class="text-success">✓</span>
              <span>自动转换为 Markdown 格式</span>
            </li>
            <li class="flex items-center space-x-2">
              <span class="text-success">✓</span>
              <span>保存转换历史记录</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import NavBar from '../components/NavBar.vue'
import FileUpload from '../components/FileUpload.vue'
import axios from 'axios'

const router = useRouter()

const project = ref({
  name: ''
})
</script>

<style scoped>
</style>
