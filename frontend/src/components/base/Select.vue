<template>
  <div class="select" :class="{ active: isActive }" @click="() => (isActive = !isActive)">
    <Button class="select__header" type="secondary" tag-type="button">
      <span v-if="items[value] !== undefined">{{ items[value] }}</span>
      <span v-else class="select__header-placeholder">{{ placeholder }}</span>
      <icon class="select__header-icon" icon="fa-solid fa-chevron-down" />
    </Button>
    <div class="select__items">
      <span
        v-for="(value, key) in items"
        class="select__item"
        @click="() => onChange(key)"
        :key="key"
      >
        {{ value }}
      </span>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue"
import Button from "@/components/base/BaseButton.vue"

const { items = [], modelValue } = defineProps<{
  items?: {
    [key: string | number]: any
  }
  modelValue?: any
  placeholder?: string
}>()

const value = ref(modelValue)

const emit = defineEmits<{
  (e: "update:modelValue", value: any): void
}>()

const onChange = (key: any) => {
  emit("update:modelValue", key)
  value.value = key
}

const isActive = ref(false)
</script>

<style lang="scss" scoped>
@import "@/assets/css/config";

.select {
  position: relative;
  font-size: 1rem;
  width: 100%;
}

.select__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;

  /*border-color: $text !important;*/
  /*color: $text !important;*/

  .select.active &,
  &:hover {
    background: $secondary !important;
    color: $background !important;

    border-color: $secondary !important;
  }

  .select.active & {
    border-bottom-right-radius: 0;
    border-bottom-left-radius: 0;
  }
}

.select__header-placeholder {
  font-weight: 400;
  color: #9999a9;
  transition: $transition;

  .select:hover &,
  .select.active & {
    color: $background;
  }
}

.select__header-icon {
  transition: transform $transition;

  .select.active & {
    transform: rotate(180deg);
  }
}

.select__items {
  display: flex;
  flex-direction: column;
  position: absolute;
  padding: 0;
  top: 100%;
  left: 0;
  right: 0;
  max-height: 0;
  background: $background;
  border: 1px solid $secondary;
  border-top: none;
  z-index: 2;
  overflow: auto;
  opacity: 0;
  border-radius: 0 0 1em 1em;
  transition: $transition;

  .select.active & {
    max-height: 15em;
    padding: 0.4em 0;
    opacity: 1;
  }
}

.select__item {
  padding: 0.8em 1em;
  transition: $transition;
  cursor: default;

  &:hover {
    background: $background-hover;
  }
}
</style>
