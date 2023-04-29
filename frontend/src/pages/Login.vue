<template>
  <AuthForm :on-submit="login">
    <h1>Вход</h1>
    <input v-model="username" type="text" placeholder="Логин" required />
    <input v-model="password" type="password" placeholder="Пароль" required />
    <BaseButton :loading="loading">Войти</BaseButton>
    <BaseButton class="auth-form__link" type="text" link="/register"> Еще нет аккаунта </BaseButton>
  </AuthForm>
</template>

<script lang="ts" setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useCookies } from "vue3-cookies"
import { useUser } from "@/stores/user"
import { useFetch } from "@/composables/fetch"
import { notify } from "@kyvg/vue3-notification"
import AuthForm from "@/components/base/AuthForm.vue"
import BaseButton from "@/components/base/BaseButton.vue"
import { basename } from "path"

const { cookies } = useCookies()
const router = useRouter()

const username = ref("")
const password = ref("")
const loading = ref(false)

const login = async () => {
  loading.value = true

  const { status, data } = await useFetch("users/login", {
    method: "POST",
    body: {
      username: username.value,
      password: password.value,
    },
  })

  loading.value = false

  if (status == 200) {
    const user = useUser()
    user.login(data)
    cookies.set("authToken", data.token)
    router.push("/")
  } else if (status == 400) {
    notify({
      text: "Логин или пароль неправильны",
      type: "error",
    })
  } else {
    notify({
      text: "Что-то пошло не так",
      type: "error",
    })
  }
}
</script>
