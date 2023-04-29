<template>
  <div v-if="work" class="work">
    <CWork :work="work">
      <BurgerMenu
        v-if="work.student.student_id === user.studentProfile?.id"
        :items="[
          { content: 'Изменить', link: `/works/${work.id}/update` },
          { content: 'Удалить', onClick: deleteWork },
        ]"
      >
        <div class="work__settings">
          <icon class="work__settings-icon" icon="fa-solid fa-ellipsis-v" />
        </div>
      </BurgerMenu>
    </CWork>
    <Comments v-if="work.status === 'ACCEPTED'" :work="work" />
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import { notify } from "@kyvg/vue3-notification"
import Comments from "@/components/Comments.vue"
import BurgerMenu from "@/components/base/BurgerMenu.vue"
import CWork from "@/components/Work.vue"
import { Work } from "@/models/work"
import { useFetch } from "@/composables/fetch"
import { useUser } from "@/stores/user"

const work = ref<Work | null>(null)
const user = useUser()

const route = useRoute()
const router = useRouter()

useFetch<Work>(`works/${route.params.id}`).then(({ status, data }) => {
  console.log(data)

  if (status == 200) {
    work.value = data
  } else if (status == 404) {
    notify({
      text: "Такой работы не существует",
      type: "error",
    })
    router.push("/student/works")
  }
})

const editWork = () => {}

const deleteWork = async () => {
  if (confirm("Точно удалить работу? Восстановить ее будет невозможно") && work.value) {
    const { status } = await useFetch(`works/${work.value.id}`, {
      method: "DELETE",
    })

    if (status === 204) {
      notify({
        type: "success",
        text: "Работа успешно удалена",
      })
      router.push("/")
    } else {
      notify({
        type: "error",
        text: "Что-то пошло не так",
      })
    }
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/css/config";

.work {
  display: flex;
  flex-direction: column;
  align-self: center;
  gap: 1.5em;
  max-width: 60em;
}

.work__settings-icon {
  margin-top: 0.4em;
  padding: 0 0.2em;
  font-size: 2em;
  transition: $transition;

  &:hover {
    transform: scale(1.2);
    cursor: pointer;
  }
}
</style>
