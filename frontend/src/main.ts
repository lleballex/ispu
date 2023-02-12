import { createApp } from "vue"
import { createPinia } from "pinia"
import { createRouter, createWebHistory } from "vue-router"
import Notifications from "@kyvg/vue3-notification"
import { useCookies } from "vue3-cookies"
import { library } from "@fortawesome/fontawesome-svg-core"
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome"
import { faSpinner, faTimes } from "@fortawesome/free-solid-svg-icons"
import { useUser } from "@/stores/user"
import { useFetch } from "@/composables/fetch"
import App from "@/App.vue"
import MainPage from "@/pages/Main.vue"
import LoginPage from "@/pages/Login.vue"
import RegisterPage from "@/pages/Register.vue"

library.add(faSpinner, faTimes)

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", component: MainPage },
    { path: "/login", component: LoginPage },
    { path: "/register", component: RegisterPage },
  ],
})

const app = createApp(App)
app.component("icon", FontAwesomeIcon)
app.use(router)
app.use(createPinia())
app.use(Notifications)
app.mount("#app")

const { cookies } = useCookies()
const authToken = cookies.get("authToken")
if (authToken) {
  const res = await useFetch("users/login")
  if (res.status == 200) {
    useUser().login(res.data)
  } else {
    cookies.remove("authToken")
  }
}
