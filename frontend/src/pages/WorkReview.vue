<template>
  <div v-if="work" class="review">
    <CWork :work="work" />
    <form class="review__form" @submit.prevent="saveReview">
      <Select
        class="review__form-select"
        :items="{
          PENDING: 'На рассмотрении',
          REJECTED: 'Есть ошибки. Надо доделать',
          ACCEPTED: 'Все хорошо. Можно публиковать',
        }"
        v-model="work.status"
      />
      <input
        v-if="work.status === 'REJECTED'"
        class="review__form-input"
        v-model="work.message"
        type="text"
        placeholder="Сообщение об ошибке"
      />
      <Button>Сохранить</Button>
    </form>
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import { notify } from "@kyvg/vue3-notification"
import CWork from "@/components/Work.vue"
import Select from "@/components/base/Select.vue"
import Button from "@/components/base/BaseButton.vue"
import { Work } from "@/models/work"
import { useFetch } from "@/composables/fetch"

const work = ref<Work | null>(null)

const route = useRoute()
const router = useRouter()

useFetch<Work>(`works/${route.params.id}`).then(({ status, data }) => {
  if (status == 200) {
    work.value = data
  } else if (status == 404) {
    notify({
      text: "Такой работы не существует",
      type: "error",
    })
    router.push("/")
  }
})

const saveReview = async () => {
  const { status } = await useFetch(`works/${work.value.id}/review`, {
    method: "POST",
    body: work.value,
  })

  if (status == 200) {
    notify({
      text: "Данные успешно изменены",
      type: "success",
    })
    router.push("/teacher/works")
  } else {
    notify({
      text: "Что-то пошло не так",
      type: "error",
    })
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/css/config";

.review {
  display: flex;
  flex-direction: column;
  gap: 2em;
  align-self: center;
}

.review__form {
  display: flex;
  align-self: center;
  gap: 1em;
  max-width: 100%;
  position: sticky;
  padding: 1em;
  bottom: 2em;
  border-radius: $radius;
  background: $background;
  box-shadow: $shadow;
}

.review__form-select {
  width: 20em;
  flex-shrink: 0;

  &.active :deep(.select__header) {
    border-radius: 0 0 1em 1em;
  }

  :deep(.select__items) {
    top: auto;
    bottom: 100%;
    border-radius: 1em 1em 0 0;
    border-bottom: none;
    border-top: 1px solid $secondary;
  }
}

.review__form-input {
  width: 20em;
}
</style>
