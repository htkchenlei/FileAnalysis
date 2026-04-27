import { defineStore } from 'pinia'
import axios from 'axios'

export const useFilesStore = defineStore('files', {
  state: () => ({
    files: [],
    loading: false,
    error: null,
    currentFile: null
  }),
  
  actions: {
    async uploadFile(file, projectName) {
      this.loading = true
      this.error = null
      
      try {
        const formData = new FormData()
        formData.append('file', file)
        if (projectName) {
          formData.append('project_name', projectName)
        }
        
        const response = await axios.post('/api/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        
        this.currentFile = response.data
        await this.getFiles()
        return response.data
      } catch (error) {
        this.error = error.response?.data?.error || '上传失败'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async getFiles() {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get('/api/files')
        // 将每个文件的ID转换为整数类型
        this.files = response.data.map(file => ({
          ...file,
          id: parseInt(file.id)
        }))
      } catch (error) {
        this.error = '获取文件列表失败'
      } finally {
        this.loading = false
      }
    },
    
    async getFile(id) {
      this.loading = true
      this.error = null
      
      try {
        // 确保ID是整数类型
        const fileId = parseInt(id)
        const response = await axios.get(`/api/files/${fileId}`)
        this.currentFile = response.data
        return response.data
      } catch (error) {
        this.error = '获取文件详情失败'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async deleteFile(id) {
      this.loading = true
      this.error = null
      
      try {
        // 确保ID是整数类型
        const fileId = parseInt(id)
        await axios.delete(`/api/files/${fileId}`)
        await this.getFiles()
      } catch (error) {
        this.error = '删除文件失败'
        throw error
      } finally {
        this.loading = false
      }
    }
  }
})
