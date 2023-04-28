<template>
  <component
    class="button"
    @click="onClick"
    :class="type"
    :is="link ? RouterLink : 'button'"
    :to="link"
    :type="tagType"
  >
    <transition name="button__loading">
      <span v-if="loading" class="button__loading"><icon icon="fa-solid fa-spinner" spin /></span>
    </transition>
    <slot />
  </component>
</template>

<script lang="ts" setup>
import { toRef } from "vue"
import { RouterLink } from "vue-router"

interface Props {
  type?: "primary" | "secondary" | "text"
  link?: string
  onClick?: () => void
  loading?: boolean
  tagType?: "button"
}

const props = withDefaults(defineProps<Props>(), {
  type: "primary",
  loading: false,
})
const { type, onClick } = props
const loading = toRef(props, "loading")
</script>

<style lang="scss" scoped>
@import "@/assets/css/config";

.button {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1em 1.2em;
  border-radius: $radius;
  border: none;
  background: none;
  font-weight: 600;
  font-size: 1rem;
  color: $text;
  font-family: $regular;
  text-decoration: none;
  cursor: pointer;
  transition: $transition;

  &.primary {
    background: $primary;
    color: $background;

    &:hover {
      box-shadow: $shadow-primary;
    }
  }

  &.secondary {
    background: $background;
    color: $secondary;
    border: 2px solid $secondary;

    &:hover {
      background: $secondary;
      color: $background;
    }
  }

  &.text {
    padding: 0;
    border-radius: 0;
    border: none;
    color: $secondary;
    font-weight: 400;

    &:hover {
      color: $text;
    }

    &:active {
      font-size: 1.1em;
    }
  }
}

.button__loading {
  display: flex;
  width: 1.8em;
  max-width: 1.8em;
  overflow: hidden;
  text-align: left;
}

.button__loading-enter-from,
.button__loading-leave-to {
  max-width: 0;
}

.button__loading-enter-active,
.button__loading-leave-active {
  transition: 0.3s;
}
</style>
