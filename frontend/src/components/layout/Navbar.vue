<template>
  <nav class="navbar">
    <img class="navbar__logo" src="@/assets/images/logo.svg" alt="s" />
    <div class="navbar__block">
      <RouterLink class="navbar__link" to="/">Каталог</RouterLink>
      <a class="navbar__link" href="http://ivt.ispu.ru/index.php/home/kafedra-it" target="_blank"
        >Кафедра ИТ</a
      >
    </div>
    <div v-if="!user.isAuthed" class="navbar__block">
      <BaseButton class="navbar__primary-btn" type="primary" link="/login">Войти</BaseButton>
    </div>
    <div v-else>
      <BurgerMenu
        :items="[
          { content: 'Мои работы', link: '/student/works' },
          { content: 'Добавить работу', link: '/student/works/new' },
          { content: 'Выйти', onClick: logout },
        ]"
      >
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
  padding-bottom: 0;
  /*background: $primary-simple;*/
  /*color: $background;*/
  font-size: 1rem;
}

.navbar__logo {
  width: 5em;
}

.navbar__block {
  display: flex;
  gap: 3em;
}

.navbar__link {
  position: relative;
  color: $secondary;
  font-size: 1.05em;

  &:after {
    content: "";
    position: absolute;
    bottom: -0.6em;
    height: 2.5px;
    left: 0;
    right: 100%;
    border-radius: $radius;
    background: $primary;
    transition: $transition;
  }

  &:hover:after {
    right: 0;
  }
}

.navbar__primary-btn {
  border: none !important;
  color: $primary-simple !important;

  &:hover {
    color: $background !important;
  }
}

.navbar__user-image-container {
  position: relative;
  width: 3em;
  height: 3em;
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
  box-shadow: 0 0 0 0.2em $background;
}
</style>
