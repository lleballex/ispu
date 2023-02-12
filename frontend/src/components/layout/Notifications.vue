<template>
  <notifications width="25em">
    <template #body="props">
      <div class="notification" :class="props.item.type">
        <div v-html="props.item.text" />
        <div class="notification__close" @click="props.close">
          <icon icon="fa-solid fa-times" />
        </div>
      </div>
    </template>
  </notifications>
</template>

<style lang="scss" scoped>
@import "@/assets/css/config";

.notification {
  position: relative;
  margin: 1em 1em 0 0;
  padding: 1.5em 1.5em 1.5em calc(1.5em + 0.7em);
  border-radius: $radius;
  overflow: hidden;

  &:after {
    content: "";
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    width: 0.7em;
  }

  &.error {
    background: #f8d7da;
    color: #b02a37;

    &:after {
      background: #f1aeb5;
    }
  }

  &.success {
    background: #d1e7dd;
    color: #146c43;

    &:after {
      background: #a3cfbb;
    }
  }
}

.notification__close {
  display: flex;
  align-items: center;
  justify-content: center;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  opacity: 0;
  z-index: 1;
  background: rgba(0, 0, 0, 0.4);
  font-size: 2.5em;
  transition: $transition;

  &:hover {
    opacity: 1;
    cursor: pointer;
  }
}
</style>
