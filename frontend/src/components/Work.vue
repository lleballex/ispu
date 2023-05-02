<template>
  <div class="work">
    <div class="work__header">
      <h1 class="work__name">{{ work.name }}</h1>
      <slot></slot>
    </div>
    <p>{{ getWorkAuthor(work) }}</p>
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
import { Work } from "@/models/work"

defineProps<{
  work: Work
}>()

const getWorkAuthor = (work: Work) => {
  if (work.author) return work.author
  return `${work.student.last_name} ${work.student.first_name[0]}. ${work.student.patronymic[0]}.`
}
</script>

<style lang="scss" scoped>
.work {
  display: flex;
  flex-direction: column;
  align-self: center;
  gap: 1.5em;
  max-width: 60em;
}

.work__header {
  display: flex;
  align-items: flex-start;
  gap: 2em;
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
