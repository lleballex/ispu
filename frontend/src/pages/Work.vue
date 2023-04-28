<template>
  <div v-if="work" class="work">
    <h1 class="work__name">{{ work.name }}</h1>
    <p>Гвоздева Т.В., Лебедева Е.Ю.</p>
    <div class="work__block">
      <p class="work__block-title">Ключевые слова</p>
      <p class="work__block-content">{{ work.keywords.join(", ") }}</p>
    </div>
    <div class="work__block">
      <p class="work__block-title">Область применения</p>
      <p class="work__block-content">{{ work.field }}</p>
    </div>
    <div class="work__block">
      <p class="work__block-title">Задачи</p>
      <p class="work__block-content">{{ work.tasks }}</p>
    </div>
    <div class="work__block">
      <p class="work__block-title">Научная новизна</p>
      <p class="work__block-content">{{ work.novelty }}</p>
    </div>
    <div class="work__block">
      <p class="work__block-title">Практическая значиость</p>
      <p class="work__block-content">{{ work.significance }}</p>
    </div>
    <div class="work__block">
      <p class="work__block-title">Используемые средства разработки</p>
      <p class="work__block-content">{{ work.tools }}</p>
    </div>
    <div class="work__block">
      <p class="work__block-title">Апробация результатов</p>
      <p class="work__block-content">{{ work.aprobation }}</p>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import { notify } from "@kyvg/vue3-notification"
import { Work } from "@/models/work"
import { useFetch } from "@/composables/fetch"

const work = ref<Work | null>(null)

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
    router.push("/")
  }
})
</script>

<style lang="scss" scoped>
.work {
  display: flex;
  flex-direction: column;
  align-self: center;
  gap: 1.5em;
  max-width: 60em;
}

.work__name {
  margin-bottom: -0.1em;
  font-size: 3em;
}

.work__block {
  display: flex;
  flex-direction: column;
  gap: 0.3em;
}

.work__block-title {
  font-weight: 600;
  /*font-size: 1.1em;*/
}

.work__block-content {
  /*font-size: 1.1em;*/
  line-height: 1.5em;
}
</style>
