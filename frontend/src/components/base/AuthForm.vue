<template>
  <div class="auth-form">
    <form class="auth-form__form" @submit.prevent="onSubmit">
      <slot />
    </form>
  </div>
</template>

<script lang="ts" setup>
const { onSubmit } = defineProps<{
  onSubmit?: () => void
}>()
</script>

<style lang="scss" scoped>
@import "@/assets/css/config";

.auth-form {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  font-size: 1rem;
}

.auth-form__form {
  display: flex;
  flex-direction: column;
  gap: 2em;
  padding: 3em;
  max-width: 30em;
  width: 100%;
  border-radius: $radius;
  box-shadow: $shadow;
}

:slotted(.auth-form__link) {
  align-self: center;
}
</style>
