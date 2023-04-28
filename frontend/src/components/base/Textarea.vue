<template>
  <div class="textarea" :data-placeholder="placeholder" contenteditable @input="onChange"></div>
</template>

<script lang="ts" setup>
defineProps<{
  placeholder?: string
}>()

const emit = defineEmits<{
  (e: "update:modelValue", value: string)
}>()

const onChange = (e) => {
  emit("update:modelValue", e.target.innerText)
}
</script>

<style lang="scss" scoped>
@import "@/assets/css/config";

.textarea {
  padding: 1em 1.2em;
  height: 8em;
  width: 100%;
  overflow: auto;
  box-sizing: border-box;
  border-radius: $radius;
  border: 2px solid $secondary;
  background: $background;
  font-size: 1rem;
  color: $text;
  outline: none;
  transition: $transition;

  &:focus {
    border-color: $secondary;
  }

  &:empty:after {
    content: attr(data-placeholder);
    color: #9999a9;
  }
}
</style>
