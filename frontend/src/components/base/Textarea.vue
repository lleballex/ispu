<template>
  <div
    ref="divRef"
    class="textarea"
    :data-placeholder="placeholder"
    contenteditable
    @input="onChange"
  ></div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue"

const { modelValue } = defineProps<{
  placeholder?: string
  modelValue?: string
}>()

const divRef = ref<HTMLDivElement | null>(null)

onMounted(() => {
  if (divRef.value && modelValue) divRef.value.innerText = modelValue
})

const emit = defineEmits<{
  (e: "update:modelValue", value: string): void
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
