<template>
  <div class="min-h-screen">
    <NavBar />
    <div class="container mx-auto px-6 py-12">
      <div class="max-w-3xl mx-auto">
        <h1 class="text-3xl font-bold mb-8 text-center">上传招标文件</h1>
        <FileUpload />
        <div class="mt-12 card">
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
import NavBar from '../components/NavBar.vue'
import FileUpload from '../components/FileUpload.vue'
</script>

<style scoped>
</style>
