<template>
  <div class="burger" :class="{ active: isShowed }">
    <div className="{childrenClassName}" @click="() => (isShowed = !isShowed)">
      <slot />
    </div>
    <div class="burger__backdrop" @click="isShowed = false"></div>
    <div class="burger__items">
      <BaseButton
        v-for="item in items"
        class="burger__item"
        type="text"
        :link="item.link"
        :on-click="() => onItemClick(item.onClick)"
      >
        {{ item.content }}
      </BaseButton>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue"
import BaseButton from "@/components/base/BaseButton.vue"

const { items } = defineProps<{
  items: {
    content: string
    link?: string
    onClick?: () => void
  }[]
}>()

const isShowed = ref(false)

const onItemClick = (itemOnClick?: () => void) => {
  isShowed.value = false
  itemOnClick?.()
}
</script>

<style lang="scss" scoped>
@import "@/assets/css/config";

.burger {
  position: relative;
  font-size: 1rem;
}

.burger__backdrop {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 2;

  .burger.active & {
    display: block;
  }
}

.burger__items {
  display: flex;
  flex-direction: column;
  position: absolute;
  top: calc(100% + 1.2em);
  right: 0;
  max-height: 0;
  opacity: 0;
  z-index: 2;
  overflow: hidden;
  border-radius: $radius;
  box-shadow: $shadow;
  background: $background;
  transition: $transition;

  .burger.active & {
    padding: 0.4em 0;
    opacity: 1;
    max-height: 10em;
  }
}

.burger__item {
  padding: 0.6em 1.2em !important;
  width: max-content;
  text-align: right;
}
</style>
