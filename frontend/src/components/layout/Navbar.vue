<template>
  <nav class="navbar">
    <RouterLink to="/"><h2 class="navbar__title">Hello world</h2></RouterLink>
    <div v-if="!user.isAuthed" class="navbar__block">
      <BaseButton type="text" link="/register">Регистрация</BaseButton>
      <BaseButton link="/login">Войти</BaseButton>
    </div>
    <div v-else>
      <BurgerMenu :items="[{ content: 'Профиль' }, { content: '👋 Выйти', onClick: logout }]">
        <div class="navbar__user-image-container">
          <img class="navbar__user-image" src="@/assets/images/user.svg" alt="" />
        </div>
      </BurgerMenu>
    </div>
  </nav>
</template>

<script lang="ts" setup>
import { RouterLink } from "vue-router"
import { useCookies } from "vue3-cookies"
import { useUser } from "@/stores/user"
import BaseButton from "@/components/base/BaseButton.vue"
import BurgerMenu from "@/components/base/BurgerMenu.vue"

const user = useUser()
const { cookies } = useCookies()

const logout = () => {
  user.logout()
  cookies.remove("authToken")
}
</script>

<style lang="scss" scoped>
@import "@/assets/css/config";

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.3em 2em;
  font-size: 1rem;
}

.navbar__block {
  display: flex;
  gap: 2em;
}

.navbar__user-image-container {
  position: relative;
  width: 2.8em;
  height: 2.8em;
  z-index: 1;

  &:after {
    content: "";
    position: absolute;
    top: -0.4em;
    right: -0.4em;
    left: -0.4em;
    bottom: -0.4em;
    z-index: -1;
    border-radius: 50%;
    background: $primary;
  }
}

.navbar__user-image {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  box-shadow: 0 0 0 0.2em $white;
}
</style>
