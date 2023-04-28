<template>
  <AuthForm :on-submit="login">
    <h1>Вход</h1>
    <input v-model="email" type="email" placeholder="Email" required />
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

const { cookies } = useCookies()
const router = useRouter()

const email = ref("")
const password = ref("")
const loading = ref(false)

const login = async () => {
  loading.value = true

  const res = await useFetch("users/login", {
    method: "POST",
    body: {
      email: email.value,
      password: password.value,
    },
  })

  loading.value = false

  if (res.status == 200) {
    const user = useUser()
    user.login(res.data)
    cookies.set("authToken", res.data.token)
    router.push("/")
  } else {
    notify({
      text: "Something went wrong",
      type: "error",
    })
    console.log(res)
  }
}
</script>
