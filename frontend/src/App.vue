<template>
  <div class="app">
    <Navbar />
    <RouterView />
    <Footer />
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
  background: $white;
  font-family: $regular;
  color: $black;
}
</style>

<style lang="scss">
@import "@/assets/css/config";

html {
  font-size: 16px;
}

body {
  margin: 0;
}

h1,
h2 {
  margin: 0;
}

p {
  margin: 0;
}

a {
  color: $black;
  text-decoration: none;
}

img {
  display: block;
}

input {
  padding: 1em 1.2em;
  border-radius: $radius;
  border: 2px solid $accent;
  background: #fff;
  color: $black;
  font-size: 1rem;
  font-family: $regular;
  outline: none;
}

input::placeholder {
  color: #999;
}
</style>
