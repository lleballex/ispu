<template>
  <WorkForm :work="work" @submit="saveData" />
</template>

<script lang="ts" setup>
import { reactive } from "vue"
import { useRouter } from "vue-router"
import { notify } from "@kyvg/vue3-notification"
import WorkForm from "@/components/WorkForm.vue"
import { useFetch } from "@/composables/fetch"
import { UpdateWork } from "@/models/work"

const work = reactive<UpdateWork>({
  name: "",
  author: "",
  issue: "",
  teacher: null,
  novelty: "",
  field: "",
  tasks: "",
  significance: "",
  tools: "",
  aprobation: "",
  keywords: [] as string[],
  tasks_category: null,
  field_category: null,
})

const router = useRouter()

const saveData = async (work: UpdateWork) => {
  const res = await useFetch("works", {
    method: "POST",
    body: work,
  })

  if (res.status == 201) {
    notify({
      text: "Теперь нужно немного подождать - твоя работа на модерации",
      type: "success",
    })
    router.push("/student/works")
  } else {
    notify({
      text: "Что-то пошло не так",
      type: "error",
    })
  }
}
</script>
