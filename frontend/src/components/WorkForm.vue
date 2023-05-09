<template>
  <form @submit.prevent="saveData" class="new-work">
    <h1 v-if="isUpdate">Измени свою работу</h1>
    <h1 v-else="">Добавь свою работу</h1>
    <div class="new-work__fields">
      <input v-model="work.name" type="text" placeholder="Название" required />
      <input v-model="work.author" type="text" placeholder="Автор" />
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
      <div class="new-work__field-container">
        <Textarea v-model="work.significance" placeholder="Практическая значимость" />
        <p>Расскажи об эффекте, получаемом от использования инновации</p>
      </div>
      <div class="new-work__field-container">
        <Textarea v-model="work.tools" placeholder="Средства разработки" />
        <p>
          Приведи описание методов и методик, математических моделей, используемых для создания
          инновации; спецификации на внедрение (программное обеспечение, языки программирования и
          т.д.), их доступности
        </p>
      </div>
      <div class="new-work__field-container">
        <input v-model="work.aprobation" type="text" placeholder="Апробация результатов" required />
        <p>
          Укажи методы апробации, которые были использованы для проверки и оценки полученных
          результатов. Например, участие в конференции, внедрение инновации на предприятие
        </p>
      </div>
      <KeywordsField v-model="work.keywords" placeholder="Ключевые слова" />
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
    <div class="new-work__submit">
      <Button :loading="loading">Сохранить</Button>
      <p class="new-work__submit-hint">
        Работа сначала будет отправлена на проверку твоему научному руководителю
      </p>
    </div>
  </form>
</template>

<script lang="ts" setup>
import { ref, reactive } from "vue"
import { notify } from "@kyvg/vue3-notification"
import Select from "@/components/base/Select.vue"
import Button from "@/components/base/BaseButton.vue"
import Textarea from "@/components/base/Textarea.vue"
import KeywordsField from "@/components/base/KeywordsField.vue"
import { UpdateWork } from "@/models/work"
import { PublicTeacher } from "@/models/teacher"
import { useFetch } from "@/composables/fetch"

interface Category {
  id: number
  name: string
}

const { work: initWork, isUpdate } = defineProps<{
  work: UpdateWork
  isUpdate?: boolean
}>()

const work = reactive(initWork)

const emit = defineEmits<{
  (e: "submit", value: UpdateWork): Promise<void>
}>()

const loading = ref(false)

const saveData = async () => {
  if (!work.teacher)
    return notify({
      type: "error",
      text: "Выбери научного руководителя",
    })

  if (!work.novelty)
    return notify({
      type: "error",
      text: "Заполни научную новизну",
    })

  if (!work.tasks)
    return notify({
      type: "error",
      text: "Заполни задачи",
    })

  if (!work.significance)
    return notify({
      type: "error",
      text: "Заполни практическую значимость",
    })

  if (!work.tools)
    return notify({
      type: "error",
      text: "Заполни средства разработки",
    })

  if (!work.tasks_category)
    return notify({
      type: "error",
      text: "Выбери категорию задач",
    })

  if (!work.field_category)
    return notify({
      type: "error",
      text: "Выбери категория области применения",
    })

  loading.value = true
  emit("submit", work)
  loading.value = false
}

const teachers = ref({})
const tasksCategories = ref({})
const fieldCategories = ref({})

useFetch<PublicTeacher[]>("users/teachers").then(({ status, data }) => {
  if (status === 200 && data) {
    teachers.value = data.reduce(
      (prev, curr) => ({
        ...prev,
        [curr.teacher_id]: `${curr.last_name} ${curr.first_name} ${curr.patronymic}`,
      }),
      {}
    )
  } else {
    notify({
      type: "error",
      text: "Что-то пошло не так",
    })
  }
})

useFetch<Category[]>("works/tasks-categories").then(({ status, data }) => {
  if (status === 200 && data) {
    tasksCategories.value = data.reduce((prev, curr) => ({ ...prev, [curr.id]: curr.name }), {})
  } else {
    notify({
      type: "error",
      text: "Что-то пошло не так",
    })
  }
})

useFetch<Category[]>("works/field-categories").then(({ status, data }) => {
  if (status === 200 && data) {
    fieldCategories.value = data.reduce((prev, curr) => ({ ...prev, [curr.id]: curr.name }), {})
  } else {
    notify({
      type: "error",
      text: "Что-то пошло не так",
    })
  }
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

.new-work__submit {
  display: flex;
  flex-direction: column;
  gap: 1em;
}

.new-work__submit-hint {
  font-size: 0.85em;
  text-align: center;
  color: lighten($text, 10%);
}
</style>
