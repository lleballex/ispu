import { createApp } from "vue"
import { createPinia } from "pinia"
import { createRouter, createWebHistory } from "vue-router"
import Notifications from "@kyvg/vue3-notification"
import velocity from "velocity-animate"
import { useCookies } from "vue3-cookies"
import { library } from "@fortawesome/fontawesome-svg-core"
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome"
import {
  faSpinner,
  faTimes,
  faChevronDown,
  faClock,
  faCircleCheck,
  faCircleXmark,
  faCheck,
} from "@fortawesome/free-solid-svg-icons"
import { useUser } from "@/stores/user"
import { useFetch } from "@/composables/fetch"
import App from "@/App.vue"
import MainPage from "@/pages/Main.vue"
import WorkPage from "@/pages/Work.vue"
import LoginPage from "@/pages/Login.vue"
import StudentPage from "@/pages/student/Student.vue"
import NewWorkPage from "@/pages/student/New.vue"
import RegisterPage from "@/pages/Register.vue"

library.add(faSpinner, faTimes, faChevronDown, faClock, faCircleCheck, faCircleXmark, faCheck)

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", component: MainPage },
    { path: "/login", component: LoginPage },
    { path: "/register", component: RegisterPage },
    { path: "/works/:id", component: WorkPage },
    { path: "/student/works", component: StudentPage },
    { path: "/student/works/new", component: NewWorkPage },
  ],
})

const app = createApp(App)
app.component("icon", FontAwesomeIcon)
app.use(router)
app.use(createPinia())
app.use(Notifications, { velocity })
app.mount("#app")

const auth = async () => {
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
}
auth()
