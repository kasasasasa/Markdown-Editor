<template>
  <div :class="['app', { dark: isDarkMode }]">
    <header class="header">
      <h1>Markdown 编辑器</h1>
      <div class="toolbar">
        <button @click="toggleDarkMode" class="btn btn-theme">
          {{ isDarkMode ? '☀' : '🌙' }}
        </button>
        <button @click="exportMarkdown" class="btn btn-export-md">导出 .md</button>
        <button @click="importMarkdown" class="btn btn-import-md">导入 .md</button>
        <input
          v-model="filename"
          placeholder="文件名（可选）"
          class="filename-input"
        />
      </div>
    </header>

    <div class="container">
      <Editor v-model="markdownContent" @update="handleUpdate" />
      <Preview :html="htmlContent" />
    </div>

    <input
      type="file"
      ref="fileInput"
      accept=".md,.markdown"
      style="display: none"
      @change="handleFileImport"
    />
  </div>
</template>

<script>
import { ref } from 'vue'
import Editor from './components/Editor.vue'
import Preview from './components/Preview.vue'
import { marked } from 'marked'
import 'highlight.js/styles/monokai-sublime.css'  // 可选代码高亮主题

// 配置 marked
marked.setOptions({
  gfm: true,           // 启用 GitHub 风格的 Markdown（表格、自动链接等）
  breaks: true,        // 支持换行符转换为 <br>
  highlight: function(code, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(code, { language: lang }).value
      } catch (err) {}
    }
    return hljs.highlightAuto(code).value
  }
})

// 自定义扩展：支持 ==高亮==
const highlightExtension = {
  name: 'highlight',
  level: 'inline',
  start(src) {
    return src.match(/==/)?.index
  },
  tokenizer(src, tokens) {
    const match = src.match(/^==([^==]+)==/)
    if (match) {
      return {
        type: 'highlight',
        raw: match[0],
        text: match[1].trim()
      }
    }
  },
  renderer(token) {
    return `<mark>${token.text}</mark>`
  }
}

marked.use({ extensions: [highlightExtension] })

export default {
  name: 'App',
  components: { Editor, Preview },
  setup() {
    const markdownContent = ref('# 欢迎使用 Markdown 编辑器\n\n开始编写你的文档吧...')
    const htmlContent = ref('')
    const filename = ref('')
    const fileInput = ref(null)
    const isDarkMode = ref(false)

    htmlContent.value = marked(markdownContent.value)

    const handleUpdate = (content) => {
      htmlContent.value = marked(content)
    }

    const exportMarkdown = () => {
      const content = markdownContent.value
      const blob = new Blob([content], { type: 'text/markdown' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = (filename.value ? filename.value.replace(/\.md$/, '') : 'document') + '.md'
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    }

    const importMarkdown = () => {
      fileInput.value.click()
    }

    const handleFileImport = (event) => {
      const file = event.target.files[0]
      if (!file) return
      const reader = new FileReader()
      reader.onload = (e) => {
        const content = e.target.result
        markdownContent.value = content
        htmlContent.value = marked(content)
        filename.value = file.name.replace(/\.md$/, '')
      }
      reader.readAsText(file, 'UTF-8')
      event.target.value = ''
    }

    const toggleDarkMode = () => {
      isDarkMode.value = !isDarkMode.value
      localStorage.setItem('darkMode', isDarkMode.value)
    }

    const savedDarkMode = localStorage.getItem('darkMode')
    if (savedDarkMode !== null) {
      isDarkMode.value = savedDarkMode === 'true'
    }

    return {
      markdownContent,
      htmlContent,
      filename,
      fileInput,
      isDarkMode,
      handleUpdate,
      exportMarkdown,
      importMarkdown,
      handleFileImport,
      toggleDarkMode
    }
  }
}
</script>

<style>
/* 基础样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
}

.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f5f5;
  color: #333;
  transition: background-color 0.3s, color 0.3s;
}

.header {
  background: linear-gradient(135deg, #669fea 0%, #4ba267 100%);
  color: white;
  padding: 20px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.header h1 {
  font-size: 24px;
  font-weight: 600;
}

.toolbar {
  display: flex;
  gap: 10px;
  align-items: center;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s;
}

.btn-theme {
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
  font-size: 18px;
  padding: 8px 16px;
}
.btn-theme:hover {
  background-color: rgba(255, 255, 255, 0.3);
}

.btn-export-md {
  background-color: #d47100;
  color: white;
}
.btn-export-md:hover {
  background-color: #0097a7;
}

.btn-import-md {
  background-color: #9c27b0;
  color: white;
}
.btn-import-md:hover {
  background-color: #7b1fa2;
}

.filename-input {
  padding: 10px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  width: 200px;
  background: white;
  color: #333;
}

.container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  flex: 1;
  gap: 0;
  height: calc(100vh - 80px);
}

/* 夜间模式样式 */
.app.dark {
  background-color: #1e1e2f;
  color: #e0e0e0;
}

.app.dark .header {
  background: linear-gradient(135deg, #2c3e66 0%, #1a2639 100%);
}

.app.dark .btn-theme {
  background-color: rgba(0, 0, 0, 0.3);
}
.app.dark .btn-theme:hover {
  background-color: rgba(0, 0, 0, 0.5);
}

.app.dark .btn-export-md {
  background-color: #008b9c;
}
.app.dark .btn-export-md:hover {
  background-color: #006c7a;
}

.app.dark .btn-import-md {
  background-color: #1fa226;
}
.app.dark .btn-import-md:hover {
  background-color: #12801b;
}

.app.dark .filename-input {
  background-color: #2d2d3a;
  color: #e0e0e0;
  border: 1px solid #3f3f4e;
}

/* 编辑器 & 预览区域暗色模式覆盖 */
.app.dark .editor-container,
.app.dark .preview-container {
  background-color: #2a2a36;
  border-color: #3f3f4e;
}

.app.dark .editor-header,
.app.dark .preview-header {
  background-color: #1e1e2f;
  border-bottom-color: #3f3f4e;
}

.app.dark .editor-header h2,
.app.dark .preview-header h2 {
  color: #e0e0e0;
}

.app.dark .editor-textarea {
  color: #e0e0e0;
  background-color: #2a2a36;
}

.app.dark .editor-textarea::placeholder {
  color: #888;
}

.app.dark .preview-content {
  background-color: #2a2a36;
  color: #e0e0e0;
}

/* 可选：预览内容中代码块背景等 */
.app.dark .preview-content pre,
.app.dark .preview-content code {
  background-color: #1e1e2f;
  color: #e0e0e0;
}
</style>
