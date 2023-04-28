<template>
  <div class="app">
    <Navbar />

    <div class="content">
      <RouterView v-slot="{ Component }">
        <!--<Transition name="slide-fade" mode="out-in">-->
        <component :is="Component" />
        <!--</Transition>-->
      </RouterView>
    </div>

    <Footer class="footer" />
    <Notifications />
  </div>
</template>

<script setup lang="ts">
import { RouterView } from "vue-router"
import Navbar from "@/components/layout/Navbar.vue"
import Footer from "@/components/layout/Footer.vue"
import Notifications from "@/components/layout/Notifications.vue"
</script>

<style lang="scss" scoped>
@import "@/assets/css/config";
@import "@/assets/fonts/stylesheet.css";

.app {
  display: flex;
  flex-direction: column;
  gap: 4em;
  min-height: 100vh;
  background: $background;
  font-family: $regular;
  color: $text;
}

.content {
  display: flex;
  flex-direction: column;
  padding: 0 2em;
}

.footer {
  margin-top: auto;
}

.router-view-enter-active,
.router-view-leave-active {
  transition: $transition;
}

.router-view-enter-from,
.router-view-leave-to {
  opacity: 0;
}

.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  /*transition: all 0.8s cubic-bezier(1, 0.5, 0.8, 1);*/
  transition: all 0.3s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(20px);
  opacity: 0;
}
</style>

<style lang="scss">
@import "@/assets/css/config";

html {
  font-size: 16px;
}

body {
  margin: 0;
  /*overflow-x: hidden;*/
}

h1,
h2 {
  margin: 0;
}

p {
  margin: 0;
}

a {
  color: inherit;
  text-decoration: none;
}

img {
  display: block;
}

input {
  padding: 1em 1.2em;
  border-radius: $radius;
  border: 2px solid $secondary;
  background: #fff;
  color: $text;
  font-size: 1rem;
  font-family: $regular;
  outline: none;
}

input::placeholder {
  color: #999;
}
</style>
