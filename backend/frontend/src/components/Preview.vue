<template>
  <div class="preview-container">
    <div class="preview-header">
      <h2>预览</h2>
    </div>
    <div class="preview-content" v-html="html"></div>
  </div>
</template>

<script>
export default {
  name: 'Preview',
  props: {
    html: {
      type: String,
      default: ''
    }
  }
}
</script>

<style scoped>
.preview-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: #ffffff;
  overflow: hidden;
}

.preview-header {
  padding: 15px 20px;
  background: #f5f5f5;
  border-bottom: 1px solid #e0e0e0;
}

.preview-header h2 {
  font-size: 18px;
  color: #333;
  font-weight: 600;
}

.preview-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  font-size: 16px;
  line-height: 1.6;
  color: #333;
}

/* 基础 Markdown 样式 */
.preview-content h1,
.preview-content h2,
.preview-content h3,
.preview-content h4,
.preview-content h5,
.preview-content h6 {
  margin-top: 24px;
  margin-bottom: 16px;
  font-weight: 600;
  line-height: 1.25;
}
.preview-content h1 { font-size: 2em; border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; }
.preview-content h2 { font-size: 1.5em; border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; }
.preview-content p { margin-bottom: 16px; }
.preview-content a { color: #0366d6; text-decoration: none; }
.preview-content a:hover { text-decoration: underline; }
.preview-content code {
  padding: 0.2em 0.4em;
  background-color: #f6f8fa;
  border-radius: 3px;
  font-family: monospace;
  font-size: 85%;
}
.preview-content pre {
  padding: 16px;
  overflow: auto;
  background-color: #f6f8fa;
  border-radius: 3px;
  margin-bottom: 16px;
}
.preview-content pre code {
  padding: 0;
  background: none;
}
.preview-content blockquote {
  padding: 0 1em;
  color: #6a737d;
  border-left: 0.25em solid #dfe2e5;
  margin: 0 0 16px 0;
}
.preview-content ul, .preview-content ol {
  padding-left: 2em;
  margin-bottom: 16px;
}
.preview-content img {
  max-width: 100%;
}
.preview-content table {
  border-collapse: collapse;
  width: 100%;
  margin-bottom: 16px;
}
.preview-content th, .preview-content td {
  padding: 6px 13px;
  border: 1px solid #dfe2e5;
}
.preview-content th {
  font-weight: 600;
  background-color: #f6f8fa;
}
</style>
