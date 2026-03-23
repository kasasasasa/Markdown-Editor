<template>
  <div class="editor-container">
    <div class="editor-header">
      <h2>编辑器</h2>
    </div>
    <textarea
      ref="textarea"
      :value="modelValue"
      @input="handleInput"
      @keyup="handleKeyup"
      placeholder="在此输入 Markdown 内容..."
      class="editor-textarea"
    ></textarea>
  </div>
</template>

<script>
export default {
  name: 'Editor',
  props: {
    modelValue: {
      type: String,
      default: ''
    }
  },
  emits: ['update:modelValue', 'update'],
  setup(props, { emit }) {
    const handleInput = (event) => {
      emit('update:modelValue', event.target.value)
      emit('update', event.target.value)
    }

    const handleKeyup = (event) => {
      // 可添加快捷键支持
    }

    return {
      handleInput,
      handleKeyup
    }
  }
}
</script>

<style scoped>
.editor-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  border-right: 1px solid #e0e0e0;
  background: #fafafa;
}

.editor-header {
  padding: 15px 20px;
  background: #f5f5f5;
  border-bottom: 1px solid #e0e0e0;
}

.editor-header h2 {
  font-size: 18px;
  color: #333;
  font-weight: 600;
}

.editor-textarea {
  flex: 1;
  width: 100%;
  padding: 20px;
  border: none;
  resize: none;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 14px;
  line-height: 1.6;
  outline: none;
  background: transparent;
}

.editor-textarea::placeholder {
  color: #999;
}
</style>