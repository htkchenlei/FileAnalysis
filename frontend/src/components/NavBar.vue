<template>
  <nav class="bg-white shadow-sm h-16 flex items-center px-6">
    <div class="container mx-auto flex justify-between items-center">
      <div class="text-2xl font-bold text-primary">
        招标文件智能分析系统
      </div>
      <div class="flex space-x-6">
        <router-link to="/" class="text-text-primary hover:text-primary transition-colors">
          项目列表
        </router-link>
        <router-link to="/create" class="text-text-primary hover:text-primary transition-colors">
          新建项目
        </router-link>
        <router-link to="/history" class="text-text-primary hover:text-primary transition-colors">
          历史记录
        </router-link>
        <router-link to="/config" class="text-text-primary hover:text-primary transition-colors">
          系统配置
        </router-link>
      </div>
    </div>
  </nav>
</template>

<script setup>
</script>

<style scoped>
</style>
