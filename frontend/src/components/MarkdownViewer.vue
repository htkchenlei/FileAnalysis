<template>
  <div class="markdown-content">
    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="text-primary text-2xl">处理中...</div>
    </div>
    <div v-else-if="error" class="text-error py-12">
      {{ error }}
    </div>
    <div v-else v-html="renderedContent" class="prose max-w-none"></div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import MarkdownIt from 'markdown-it'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'

const props = defineProps({
  content: {
    type: String,
    default: ''
  },
  loading: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: ''
  }
})

const md = new MarkdownIt({
  highlight: function (str, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(str, { language: lang }).value
      } catch (__) {}
    }
    return ''
  }
})

const renderedContent = computed(() => {
  return md.render(props.content)
})
</script>

<style scoped>
.markdown-content {
  line-height: 1.6;
  padding: 1rem;
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.markdown-content h1 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  color: var(--text-primary);
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--border);
}

.markdown-content h2 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-top: 2rem;
  margin-bottom: 1rem;
  color: var(--text-primary);
  padding-bottom: 0.375rem;
  border-bottom: 1px solid var(--border);
}

.markdown-content h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
  color: var(--text-primary);
}

.markdown-content p {
  margin-bottom: 1.25rem;
  color: var(--text-primary);
}

.markdown-content ul,
.markdown-content ol {
  margin-bottom: 1.25rem;
  padding-left: 1.75rem;
}

.markdown-content li {
  margin-bottom: 0.5rem;
}

.markdown-content code {
  background-color: #f3f4f6;
  padding: 0.2em 0.4em;
  border-radius: 0.375rem;
  font-family: 'Courier New', Courier, monospace;
  font-size: 0.875rem;
  color: #e11d48;
}

.markdown-content pre {
  background-color: #1e293b;
  padding: 1.25rem;
  border-radius: 0.5rem;
  overflow-x: auto;
  margin-bottom: 1.25rem;
  transition: all 0.2s ease-out;
}

.markdown-content pre:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.markdown-content pre code {
  background-color: transparent;
  padding: 0;
  color: #f8fafc;
}

.markdown-content table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1.25rem;
  overflow: hidden;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.markdown-content th,
.markdown-content td {
  border: 1px solid var(--border);
  padding: 0.75rem;
  text-align: left;
}

.markdown-content th {
  background-color: var(--background);
  font-weight: 600;
  color: var(--text-primary);
}

.markdown-content tr:nth-child(even) {
  background-color: #f9fafb;
}

.markdown-content img {
  max-width: 100%;
  height: auto;
  border-radius: 0.5rem;
  margin-bottom: 1.25rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease-out;
}

.markdown-content img:hover {
  transform: scale(1.02);
}

.markdown-content a {
  color: var(--primary);
  text-decoration: none;
  transition: color 0.2s ease-out;
}

.markdown-content a:hover {
  color: #9a8aa9;
  text-decoration: underline;
}

.markdown-content blockquote {
  border-left: 4px solid var(--primary);
  padding-left: 1rem;
  margin-bottom: 1.25rem;
  color: var(--text-secondary);
  font-style: italic;
}
</style>
