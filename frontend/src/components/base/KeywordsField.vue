<template>
  <div class="keywords">
    <div v-if="value.length" class="keywords__items">
      <span v-for="word in value" class="keywords__item" @click="removeWord(word)" :key="word">{{
        word
      }}</span>
    </div>
    <form @submit.prevent="addWord">
      <input
        v-model="activeKeyword"
        class="keywords__input"
        type="text"
        :placeholder="placeholder"
      />
    </form>
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue"

const { modelValue = [] } = defineProps<{
  modelValue?: string[]
  placeholder?: string
}>()

const emit = defineEmits<{
  (e: "update:modelValue", value: string[]): void
}>()

const value = ref(modelValue)
const activeKeyword = ref("")

const addWord = () => {
  if (!value.value.includes(activeKeyword.value)) {
    value.value.push(activeKeyword.value)
    activeKeyword.value = ""
  }
}

const removeWord = (word: string) => {
  const idx = value.value.indexOf(word)
  value.value = [...value.value.slice(0, idx), ...value.value.slice(idx + 1)]
}
</script>

<style lang="scss" scoped>
@import "@/assets/css/config";

.keywords {
  display: flex;
  flex-direction: column;
  gap: 1em;
}

.keywords__items {
  display: flex;
  flex-wrap: wrap;
  gap: 0.7em 1em;
}

.keywords__item {
  padding: 0.2em 0.5em;
  border-radius: $radius;
  background: $secondary;
  color: $background;
  transition: $transition;

  &:hover {
    background: darken($secondary, 10%);
    cursor: pointer;
  }
}

.keywords__input {
  width: 100%;
  box-sizing: border-box;
}
</style>
