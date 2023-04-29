<template>
  <WorkForm v-if="work" :work="work" @submit="saveData" is-update />
</template>

<script lang="ts" setup>
import { reactive, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import { notify } from "@kyvg/vue3-notification"
import WorkForm from "@/components/WorkForm.vue"
import { useFetch } from "@/composables/fetch"
import { UpdateWork } from "@/models/work"

const route = useRoute()
/*const workExists = ref(false)*/

useFetch<UpdateWork>(`works/${route.params.id}/update`).then(({ data, status }) => {
  if (status === 200 && data) {
    work.value = data
    /*work.name = data.name*/
    /*work.author = data.author*/
    /*work.teacher = data.teacher*/
    /*work.issue = data.issue*/
    /*work.novelty = data.novelty*/
    /*work.field = data.field*/
    /*work.tasks = data.tasks*/
    /*work.significance = data.significance*/
    /*work.tools = data.tools*/
    /*work.aprobation = data.aprobation*/
    /*work.keywords = data.keywords*/
    /*work.tasks_category = data.tasks_category*/
    /*work.field_category = data.field_category*/
    /*workExists.value = true*/
  } else {
    notify({
      type: "error",
      text: "Что-то пошло не так",
    })
  }
})

const work = ref<UpdateWork | null>(null)

/*const work = reactive<UpdateWork>({*/
/*name: "",*/
/*author: "",*/
/*issue: "",*/
/*teacher: null,*/
/*novelty: "",*/
/*field: "",*/
/*tasks: "",*/
/*significance: "",*/
/*tools: "",*/
/*aprobation: "",*/
/*keywords: [] as string[],*/
/*tasks_category: null,*/
/*field_category: null,*/
/*})*/

const router = useRouter()

const saveData = async (work: UpdateWork) => {
  const res = await useFetch(`works/${work.id}/update`, {
    method: "POST",
    body: work,
  })

  if (res.status == 200) {
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
