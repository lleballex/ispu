<template>
  <form @submit.prevent="saveData" class="new-work">
    <h1>Добавь свою работу</h1>
    <div class="new-work__fields">
      <input v-model="work.name" type="text" placeholder="Название" required />
      <input v-model="work.author" type="text" placeholder="Автор" required />
      <Select v-model="work.teacher" :items="teachers" placeholder="Научный руководитель" />
      <div class="new-work__field-container">
        <input v-model="work.issue" type="text" placeholder="Проблемный вопрос" required />
        <p>
          Сформулируй актуальный вопрос, на решение которого направлена данна разработка. Например,
          как продвигать инновации в интернет среде?
        </p>
      </div>
      <Textarea v-model="work.novelty" placeholder="Научная новизна" />
      <input v-model="work.field" type="text" placeholder="Область применения" required />
      <Textarea v-model="work.tasks" placeholder="Задачи" />
      <Textarea v-model="work.significance" placeholder="Практическая значимость" />
      <Textarea v-model="work.tools" placeholder="Средства разработки" />
      <input v-model="work.aprobation" type="text" placeholder="Апробация результатов" required />
      <KeywordsField v-model="work.keywords" placeholder="Ключевые слова" />
      related works
      <Select
        v-model="work.tasks_category"
        :items="tasksCategories"
        placeholder="Категория задач"
      />
      <Select
        v-model="work.field_category"
        :items="fieldCategories"
        placeholder="Категория области применения"
      />
    </div>
    <Button :loading="isLoading">Сохранить</Button>
  </form>
</template>

<script lang="ts" setup>
import { ref, reactive } from "vue"
import { notify } from "@kyvg/vue3-notification"
import Select from "@/components/base/Select.vue"
import Button from "@/components/base/BaseButton.vue"
import Textarea from "@/components/base/Textarea.vue"
import KeywordsField from "@/components/base/KeywordsField.vue"
import { useFetch } from "@/composables/fetch"

interface Teacher {
  id: number
  teacher_id: number
  first_name: string
  last_name: string
}

interface Category {
  id: number
  name: string
}

const work = reactive({
  name: "",
  author: "",
  issue: "",
  teacher: null as number | null,
  novelty: "",
  field: "",
  tasks: "",
  significance: "",
  tools: "",
  aprobation: "",
  keywords: [] as string[],
  // related
  tasks_category: null as number | null,
  field_category: null as number | null,
})

const isLoading = ref(false)

const saveData = async () => {
  if (
    !work.name ||
    !work.author ||
    !work.issue ||
    !work.teacher ||
    !work.novelty ||
    !work.field ||
    !work.tasks ||
    !work.significance ||
    !work.tools ||
    !work.aprobation ||
    !work.tasks_category ||
    !work.field_category
  ) {
    notify({
      text: "Сначала заполни все поля",
      type: "error",
    })
    return
  }

  isLoading.value = true

  const res = await useFetch("works", {
    method: "POST",
    body: work,
  })

  isLoading.value = false

  if (res.status == 201) {
    notify({
      text: "Теперь нужно немного подождать - твоя работа на модерации",
      type: "success",
    })

    console.log(res)
  } else {
    notify({
      text: "Что-то пошло не так",
      type: "error",
    })
    console.log(res)
  }
}

const teachers = ref({})
const tasksCategories = ref({})
const fieldCategories = ref({})

useFetch<Teacher[]>("users/teachers").then((res) => {
  teachers.value = res.data.reduce(
    (prev, curr) => ({ ...prev, [curr.teacher_id]: `${curr.first_name} ${curr.last_name}` }),
    {}
  )
})

useFetch<Category[]>("works/tasks-categories").then((res) => {
  tasksCategories.value = res.data.reduce((prev, curr) => ({ ...prev, [curr.id]: curr.name }), {})
})

useFetch<Category[]>("works/field-categories").then((res) => {
  fieldCategories.value = res.data.reduce((prev, curr) => ({ ...prev, [curr.id]: curr.name }), {})
})
</script>

<style lang="scss" scoped>
@import "@/assets/css/config";

.new-work {
  display: flex;
  flex-direction: column;
  align-self: center;
  gap: 2.5em;
  padding: 3em;
  max-width: 40em;
  border-radius: $radius;
  box-shadow: $shadow;
}

.new-work__fields {
  display: flex;
  flex-direction: column;
  gap: 2em;
}

.new-work__field-container {
  display: flex;
  flex-direction: column;
  gap: 0.4em;
  line-height: 1.4em;
}
</style>
