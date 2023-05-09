<template>
  <AuthForm :on-submit="register">
    <h1>Регистрация</h1>
    <p style="line-height: 1.6em; margin: -0.5em 0 -0.2em">
      Внимание! Если вы - студент или научный руководитель, обратитесь в свой вуз для регистрации на
      платформе. Эта форма только для посетителей сайта
    </p>
    <input v-model="username" type="text" placeholder="Логин" required />
    <input v-model="email" type="email" placeholder="Email" required />
    <input v-model="password" type="password" placeholder="Пароль" required />
    <div class="labeled-block">
      <p>Как вас зовут?</p>
      <div class="h-block">
        <input v-model="firstName" type="text" placeholder="Имя" required />
        <input v-model="lastName" type="text" placeholder="Фамилия" required />
      </div>
      <div class="h-block" style="margin-top: 0.4em">
        <input v-model="patronymic" type="text" placeholder="Отчество" required />
      </div>
    </div>
    <div v-if="false" class="labeled-block">
      <p>Кем {{ role === "student" ? "ты являешься" : "вы являтесь" }}?</p>
      <Switch
        v-model="role"
        class="short-field"
        :items="{ student: 'Студент', teacher: 'Преподаватель' }"
      />
    </div>
    <Transition v-if="false" name="nonable">
      <div v-if="role === 'student'" class="labeled-block">
        <p>Немного информации о твоем обучении:</p>
        <div class="v-block">
          <input
            v-model="studentProfile.number"
            type="number"
            placeholder="Номер студенческого билета"
            required
          />
          <div class="h-block">
            <input v-model="studentProfile.course" type="number" placeholder="Курс" required />
            <input v-model="studentProfile.group" type="text" placeholder="Группа" required />
          </div>
        </div>
      </div>
    </Transition>
    <BaseButton :loading="loading">Создать аккаунт</BaseButton>
    <BaseButton class="auth-form__link" type="text" link="/login">Уже есть аккаунт</BaseButton>
  </AuthForm>
</template>

<script lang="ts" setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { notify } from "@kyvg/vue3-notification"
import { useFetch } from "@/composables/fetch"
import Switch from "@/components/base/Switch.vue"
import AuthForm from "@/components/base/AuthForm.vue"
import BaseButton from "@/components/base/BaseButton.vue"

const router = useRouter()

const username = ref("")
const email = ref("")
const password = ref("")
const role = ref("student")
const firstName = ref("")
const lastName = ref("")
const patronymic = ref("")
const loading = ref(false)

const studentProfile = ref({
  number: null,
  course: null,
  group: "",
})

const register = async () => {
  loading.value = true

  const res = await useFetch("users", {
    method: "POST",
    body: {
      username: username.value,
      email: email.value,
      password: password.value,
      /*role: role.value,*/
      first_name: firstName.value,
      last_name: lastName.value,
      patronymic: patronymic.value,
      /*student_profile: studentProfile.value,*/
      /*teacher_profile: {},*/
    },
  })

  loading.value = false

  if (res.status == 201) {
    notify({
      type: "success",
      text: `Супер! Теперь вы можете войти в свой аккаунт`,
    })
    router.push("/login")
  } else {
    console.log(res)
    notify({
      text: "Что-то пошло не так",
      type: "error",
    })
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/css/config";

.labeled-block {
  display: flex;
  flex-direction: column;
  gap: 0.4em;
}

.short-field {
  align-self: flex-start;
}

.h-block {
  display: flex;
  gap: 1em;

  > * {
    width: 100%;
  }
}

.v-block {
  display: flex;
  flex-direction: column;
  gap: 1em;
}

.nonable-enter-from,
.nonable-leave-to {
  max-height: 0;
  overflow: hidden;
  margin: -1em 0;
}

.nonable-enter-to,
.nonable-leave-from {
  max-height: 10em;
  overflow: hidden;
}

.nonable-enter-active,
.nonable-leave-active {
  transition: $transition-long;
}
</style>
