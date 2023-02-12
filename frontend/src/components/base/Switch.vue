<template>
  <div class="switch">
    <span
      v-for="(value, key) in items"
      ref="itemsRef"
      @click="() => activateItem(key as string)"
      class="switch__item"
      :class="{ active: key === activeKey }"
      :key="key"
      :data-key="key"
    >
      {{ value }}
    </span>
    <span ref="itemBgRef" class="switch__item-background"></span>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from "vue"

const { items, modelValue } = defineProps<{
  items: {
    [key: string]: string
  }
  modelValue?: string
}>()

const emit = defineEmits<{
  (e: "update:modelValue", value: string): void
}>()

const activeKey = ref(modelValue)
const itemsRef = ref<HTMLSpanElement[]>([])
const itemBgRef = ref<HTMLSpanElement | null>(null)

const activateItem = (key: string) => {
  activeKey.value = key
  emit("update:modelValue", key)
  updateView()
}

const updateView = () => {
  if (!itemBgRef.value) return

  for (const item of itemsRef.value) {
    if (activeKey.value === item.getAttribute("data-key")) {
      itemBgRef.value.style.width = `${item.clientWidth}px`
      itemBgRef.value.style.left = `${item.offsetLeft}px`
      break
    }
  }
}

onMounted(() => {
  updateView()
})
</script>

<style lang="scss" scoped>
@import "@/assets/css/config";

.switch {
  display: flex;
  position: relative;
  padding: 0.3em;
  border: 2px solid $accent;
  border-radius: $radius;
  font-size: 1rem;
}

.switch__item {
  padding: 0.7em;
  z-index: 1;
  cursor: pointer;
  transition: $transition;

  &.active {
    color: $white;
  }
}

.switch__item-background {
  position: absolute;
  top: 0.3em;
  bottom: 0.3em;
  border-radius: calc($radius - .3em);
  background: $accent;
  transition: $transition;
}
</style>
